# (c) 2021 Jeff Goldschrafe <jeff@holyhandgrenade.org>
# Based on Ansible local connection plugin by:
# (c) 2012 Michael DeHaan <michael.dehaan@gmail.com>
# (c) 2015, 2017 Toshio Kuratomi <tkuratomi@ansible.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    name: nsenter
    short_description: execute on host running controller container
    version_added: 1.9.0
    description:
        - This connection plugin allows Ansible, running in a privileged container, to execute tasks on the container
          host instead of in the container itself.
        - This is useful for running Ansible in a pull model, while still keeping the Ansible control node
          containerized.
        - It relies on having privileged access to run nsenter in the host's PID namespace, allowing it to enter the
          namespaces of the provided PID (default PID 1, or init/systemd).
    author: Jeff Goldschrafe (@jgoldschrafe)
    options:
        host_volume_mount:
            description:
                - Host volume mount to read and write host files through
            type: string
            default: /host
            vars:
                - name: ansible_host_volume_mount
            env:
                - name: ANSIBLE_HOST_VOLUME_MOUNT
            ini:
                - section: nsenter_connection
                  key: host_volume_mount
        nsenter_pid:
            description:
                - PID to attach with using nsenter.
                - The default should be fine unless you're attaching as a non-root user.
            type: int
            default: 1
            vars:
                - name: ansible_nsenter_pid
            env:
                - name: ANSIBLE_NSENTER_PID
            ini:
                - section: nsenter_connection
                  key: nsenter_pid
    #     pipelining:
    #         default: ANSIBLE_PIPELINING
    #         description:
    #             - Pipelining reduces the number of connection operations required to execute a module on the remote
    #               server, by executing many Ansible modules without actual file transfers.
    #             - This can result in a very significant performance improvement when enabled.
    #             - However this can conflict with privilege escalation (become).
    #               For example, when using sudo operations you must first disable 'requiretty' in the sudoers file for
    #               the target hosts, which is why this feature is disabled by default.
    #         env:
    #             - name: ANSIBLE_PIPELINING
    #         ini:
    #             - section: defaults
    #               key: pipelining
    #         type: boolean
    #         vars:
    #             - name: ansible_pipelining
    notes:
        - The remote user is ignored; this plugin always runs as root.
        - "This plugin requires the Ansible controller container to be launched in the following way:"
        - (1) The container image contains the nsenter program;
        - (2) C(/) on the host is mounted read-write to I(host_volume_mount) in the container;
        - (3) The container is launched in privileged mode;
        - (4) The container is launched in the host's PID namespace (i.e. C(--pid host)).
'''

import os
import pty
import shutil
import subprocess
import fcntl

import ansible.constants as C
from ansible.errors import AnsibleError, AnsibleFileNotFound
from ansible.module_utils.compat import selectors
from ansible.module_utils.six import text_type, binary_type
from ansible.module_utils._text import to_bytes, to_native, to_text
from ansible.plugins.connection import ConnectionBase
from ansible.utils.display import Display
from ansible.utils.path import unfrackpath

display = Display()


class Connection(ConnectionBase):
    '''Connections to a container host using nsenter
    '''

    transport = 'nsenter'
    has_pipelining = True

    def __init__(self, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)
        self.cwd = None
        self._host_volume_mount = self.get_option("host_volume_mount")
        self._nsenter_pid = self.get_option("nsenter_pid")

        if not os.path.exists(self._host_volume_mount):
            raise AnsibleError("nsenter: host volume mount does not exist: " + self._host_volume_mount)

    def _connect(self):
        # Because nsenter requires very high privileges, our remote user
        # is always assumed to be root.
        self._play_context.remote_user = "root"

        if not self._connected:
            display.vvv(
                u"ESTABLISH NSENTER CONNECTION FOR USER: {0}".format(
                    self._play_context.remote_user
                ),
                host=self._play_context.remote_addr,
            )
            self._connected = True
        return self

    def exec_command(self, cmd, in_data=None, sudoable=True):
        super(Connection, self).exec_command(cmd, in_data=in_data, sudoable=sudoable)

        display.debug("in nsenter.exec_command()")

        executable = C.DEFAULT_EXECUTABLE.split()[0] if C.DEFAULT_EXECUTABLE else None

        if not os.path.exists(to_bytes(executable, errors='surrogate_or_strict')):
            raise AnsibleError("failed to find the executable specified %s."
                               " Please verify if the executable exists and re-try." % executable)

        # Rewrite the provided command to prefix it with nsenter
        if isinstance(cmd, (text_type, binary_type)):
            nsenter_cmd = "nsenter --all --preserve-credentials --target={0} -- ".format(self._nsenter_pid)
            cmd = to_bytes(nsenter_cmd + cmd)
        else:
            nsenter_cmd = [
                "nsenter",
                "--all",
                "--preserve-credentials",
                "--target=" + str(self._nsenter_pid),
                "--",
            ]
            cmd = map(to_bytes, nsenter_cmd + cmd)

        display.vvv(u"EXEC {0}".format(to_text(cmd)), host=self._play_context.remote_addr)
        display.debug("opening command with Popen()")

        master = None
        stdin = subprocess.PIPE
        if sudoable and self.become and self.become.expect_prompt() and not self.get_option('pipelining'):
            # Create a pty if sudoable for privlege escalation that needs it.
            # Falls back to using a standard pipe if this fails, which may
            # cause the command to fail in certain situations where we are escalating
            # privileges or the command otherwise needs a pty.
            try:
                master, stdin = pty.openpty()
            except (IOError, OSError) as e:
                display.debug("Unable to open pty: %s" % to_native(e))

        p = subprocess.Popen(
            cmd,
            shell=isinstance(cmd, (text_type, binary_type)),
            executable=executable,
            cwd=self.cwd,
            stdin=stdin,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # if we created a master, we can close the other half of the pty now, otherwise master is stdin
        if master is not None:
            os.close(stdin)

        display.debug("done running command with Popen()")

        if self.become and self.become.expect_prompt() and sudoable:
            fcntl.fcntl(p.stdout, fcntl.F_SETFL, fcntl.fcntl(p.stdout, fcntl.F_GETFL) | os.O_NONBLOCK)
            fcntl.fcntl(p.stderr, fcntl.F_SETFL, fcntl.fcntl(p.stderr, fcntl.F_GETFL) | os.O_NONBLOCK)
            selector = selectors.DefaultSelector()
            selector.register(p.stdout, selectors.EVENT_READ)
            selector.register(p.stderr, selectors.EVENT_READ)

            become_output = b''
            try:
                while not self.become.check_success(become_output) and not self.become.check_password_prompt(become_output):
                    events = selector.select(self._play_context.timeout)
                    if not events:
                        stdout, stderr = p.communicate()
                        raise AnsibleError('timeout waiting for privilege escalation password prompt:\n' + to_native(become_output))

                    for key, event in events:
                        if key.fileobj == p.stdout:
                            chunk = p.stdout.read()
                        elif key.fileobj == p.stderr:
                            chunk = p.stderr.read()

                    if not chunk:
                        stdout, stderr = p.communicate()
                        raise AnsibleError('privilege output closed while waiting for password prompt:\n' + to_native(become_output))
                    become_output += chunk
            finally:
                selector.close()

            if not self.become.check_success(become_output):
                become_pass = self.become.get_option('become_pass', playcontext=self._play_context)
                if master is None:
                    p.stdin.write(to_bytes(become_pass, errors='surrogate_or_strict') + b'\n')
                else:
                    os.write(master, to_bytes(become_pass, errors='surrogate_or_strict') + b'\n')

            fcntl.fcntl(p.stdout, fcntl.F_SETFL, fcntl.fcntl(p.stdout, fcntl.F_GETFL) & ~os.O_NONBLOCK)
            fcntl.fcntl(p.stderr, fcntl.F_SETFL, fcntl.fcntl(p.stderr, fcntl.F_GETFL) & ~os.O_NONBLOCK)

        display.debug("getting output with communicate()")
        stdout, stderr = p.communicate(in_data)
        display.debug("done communicating")

        # finally, close the other half of the pty, if it was created
        if master:
            os.close(master)

        display.debug("done with nsenter.exec_command()")
        return (p.returncode, stdout, stderr)

    def put_file(self, in_path, out_path):
        super(Connection, self).put_file(in_path, out_path)

        # Rewrite out_path into host volume mount
        in_path = unfrackpath(in_path, basedir=self.cwd)
        out_path = self._host_volume_mount + unfrackpath(out_path, basedir=self.cwd)

        return self._transfer_file("fetch", in_path, out_path)

    def fetch_file(self, in_path, out_path):
        super(Connection, self).fetch_file(in_path, out_path)

        # Rewrite in_path into host volume mount
        in_path = self._host_volume_mount + unfrackpath(in_path, basedir=self.cwd)
        out_path = unfrackpath(out_path, basedir=self.cwd)

        return self._transfer_file("fetch", in_path, out_path)

    def close(self):
        ''' terminate the connection; nothing to do here '''
        self._connected = False

    def _transfer_file(self, action, in_path, out_path):
        display.vvv(u"{0} {1} TO {2}".format(action.upper(), in_path, out_path), host=self._play_context.remote_addr)
        if not os.path.exists(to_bytes(in_path, errors='surrogate_or_strict')):
            raise AnsibleFileNotFound("file or module does not exist: {0}".format(to_native(in_path)))
        try:
            shutil.copyfile(to_bytes(in_path, errors='surrogate_or_strict'), to_bytes(out_path, errors='surrogate_or_strict'))
        except shutil.Error:
            raise AnsibleError("failed to copy: {0} and {1} are the same".format(to_native(in_path), to_native(out_path)))
        except IOError as e:
            raise AnsibleError("failed to transfer file to {0}: {1}".format(to_native(out_path), to_native(e)))
