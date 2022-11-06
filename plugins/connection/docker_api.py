# Copyright (c) 2019-2020, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
author:
    - Felix Fontein (@felixfontein)
name: docker_api
short_description: Run tasks in docker containers
version_added: 1.1.0
description:
    - Run commands or put/fetch files to an existing docker container.
    - Uses the L(requests library,https://pypi.org/project/requests/) to interact
      directly with the Docker daemon instead of using the Docker CLI. Use the
      R(community.docker.docker,ansible_collections.community.docker.docker_connection)
      connection plugin if you want to use the Docker CLI.
extends_documentation_fragment:
    - community.docker.docker.api_documentation
    - community.docker.docker.var_names
options:
    remote_user:
        type: str
        description:
            - The user to execute as inside the container.
        vars:
            - name: ansible_user
            - name: ansible_docker_user
        ini:
            - section: defaults
              key: remote_user
        env:
            - name: ANSIBLE_REMOTE_USER
        cli:
            - name: user
        keyword:
            - name: remote_user
    remote_addr:
        type: str
        description:
            - The name of the container you want to access.
        default: inventory_hostname
        vars:
            - name: inventory_hostname
            - name: ansible_host
            - name: ansible_docker_host
    container_timeout:
        default: 10
        description:
            - Controls how long we can wait to access reading output from the container once execution started.
        env:
            - name: ANSIBLE_TIMEOUT
            - name: ANSIBLE_DOCKER_TIMEOUT
              version_added: 2.2.0
        ini:
            - key: timeout
              section: defaults
            - key: timeout
              section: docker_connection
              version_added: 2.2.0
        vars:
            - name: ansible_docker_timeout
              version_added: 2.2.0
        cli:
            - name: timeout
        type: integer
'''

import io
import os
import os.path
import shutil
import tarfile

from ansible.errors import AnsibleFileNotFound, AnsibleConnectionFailure
from ansible.module_utils.common.text.converters import to_bytes, to_native, to_text
from ansible.plugins.connection import ConnectionBase
from ansible.utils.display import Display

from ansible_collections.community.docker.plugins.module_utils.common_api import (
    RequestException,
)
from ansible_collections.community.docker.plugins.plugin_utils.socket_handler import (
    DockerSocketHandler,
)
from ansible_collections.community.docker.plugins.plugin_utils.common_api import (
    AnsibleDockerClient,
)

from ansible_collections.community.docker.plugins.module_utils._api.constants import DEFAULT_DATA_CHUNK_SIZE
from ansible_collections.community.docker.plugins.module_utils._api.errors import APIError, DockerException, NotFound

MIN_DOCKER_API = None


display = Display()


class Connection(ConnectionBase):
    ''' Local docker based connections '''

    transport = 'community.docker.docker_api'
    has_pipelining = True

    def _call_client(self, callable, not_found_can_be_resource=False):
        try:
            return callable()
        except NotFound as e:
            if not_found_can_be_resource:
                raise AnsibleConnectionFailure('Could not find container "{1}" or resource in it ({0})'.format(e, self.get_option('remote_addr')))
            else:
                raise AnsibleConnectionFailure('Could not find container "{1}" ({0})'.format(e, self.get_option('remote_addr')))
        except APIError as e:
            if e.response and e.response.status_code == 409:
                raise AnsibleConnectionFailure('The container "{1}" has been paused ({0})'.format(e, self.get_option('remote_addr')))
            self.client.fail(
                'An unexpected Docker error occurred for container "{1}": {0}'.format(e, self.get_option('remote_addr'))
            )
        except DockerException as e:
            self.client.fail(
                'An unexpected Docker error occurred for container "{1}": {0}'.format(e, self.get_option('remote_addr'))
            )
        except RequestException as e:
            self.client.fail(
                'An unexpected requests error occurred for container "{1}" when trying to talk to the Docker daemon: {0}'
                .format(e, self.get_option('remote_addr'))
            )

    def __init__(self, play_context, new_stdin, *args, **kwargs):
        super(Connection, self).__init__(play_context, new_stdin, *args, **kwargs)

        self.client = None
        self.ids = dict()

        # Windows uses Powershell modules
        if getattr(self._shell, "_IS_WINDOWS", False):
            self.module_implementation_preferences = ('.ps1', '.exe', '')

        self.actual_user = None

    def _connect(self, port=None):
        """ Connect to the container. Nothing to do """
        super(Connection, self)._connect()
        if not self._connected:
            self.actual_user = self.get_option('remote_user')
            display.vvv(u"ESTABLISH DOCKER CONNECTION FOR USER: {0}".format(
                self.actual_user or u'?'), host=self.get_option('remote_addr')
            )
            if self.client is None:
                self.client = AnsibleDockerClient(self, min_docker_api_version=MIN_DOCKER_API)
            self._connected = True

            if self.actual_user is None and display.verbosity > 2:
                # Since we're not setting the actual_user, look it up so we have it for logging later
                # Only do this if display verbosity is high enough that we'll need the value
                # This saves overhead from calling into docker when we don't need to
                display.vvv(u"Trying to determine actual user")
                result = self._call_client(lambda: self.client.get_json('/containers/{0}/json', self.get_option('remote_addr')))
                if result.get('Config'):
                    self.actual_user = result['Config'].get('User')
                    if self.actual_user is not None:
                        display.vvv(u"Actual user is '{0}'".format(self.actual_user))

    def exec_command(self, cmd, in_data=None, sudoable=False):
        """ Run a command on the docker host """

        super(Connection, self).exec_command(cmd, in_data=in_data, sudoable=sudoable)

        command = [self._play_context.executable, '-c', to_text(cmd)]

        do_become = self.become and self.become.expect_prompt() and sudoable

        display.vvv(
            u"EXEC {0}{1}{2}".format(
                to_text(command),
                ', with stdin ({0} bytes)'.format(len(in_data)) if in_data is not None else '',
                ', with become prompt' if do_become else '',
            ),
            host=self.get_option('remote_addr')
        )

        need_stdin = True if (in_data is not None) or do_become else False

        data = {
            'Container': self.get_option('remote_addr'),
            'User': self.get_option('remote_user') or '',
            'Privileged': False,
            'Tty': False,
            'AttachStdin': need_stdin,
            'AttachStdout': True,
            'AttachStderr': True,
            'Cmd': command,
        }

        if 'detachKeys' in self.client._general_configs:
            data['detachKeys'] = self.client._general_configs['detachKeys']

        exec_data = self._call_client(lambda: self.client.post_json_to_json('/containers/{0}/exec', self.get_option('remote_addr'), data=data))
        exec_id = exec_data['Id']

        data = {
            'Tty': False,
            'Detach': False
        }
        if need_stdin:
            exec_socket = self._call_client(lambda: self.client.post_json_to_stream_socket('/exec/{0}/start', exec_id, data=data))
            try:
                with DockerSocketHandler(display, exec_socket, container=self.get_option('remote_addr')) as exec_socket_handler:
                    if do_become:
                        become_output = [b'']

                        def append_become_output(stream_id, data):
                            become_output[0] += data

                        exec_socket_handler.set_block_done_callback(append_become_output)

                        while not self.become.check_success(become_output[0]) and not self.become.check_password_prompt(become_output[0]):
                            if not exec_socket_handler.select(self.get_option('container_timeout')):
                                stdout, stderr = exec_socket_handler.consume()
                                raise AnsibleConnectionFailure('timeout waiting for privilege escalation password prompt:\n' + to_native(become_output[0]))

                            if exec_socket_handler.is_eof():
                                raise AnsibleConnectionFailure('privilege output closed while waiting for password prompt:\n' + to_native(become_output[0]))

                        if not self.become.check_success(become_output[0]):
                            become_pass = self.become.get_option('become_pass', playcontext=self._play_context)
                            exec_socket_handler.write(to_bytes(become_pass, errors='surrogate_or_strict') + b'\n')

                    if in_data is not None:
                        exec_socket_handler.write(in_data)

                    stdout, stderr = exec_socket_handler.consume()
            finally:
                exec_socket.close()
        else:
            stdout, stderr = self._call_client(lambda: self.client.post_json_to_stream(
                '/exec/{0}/start', exec_id, stream=False, demux=True, tty=False, data=data))

        result = self._call_client(lambda: self.client.get_json('/exec/{0}/json', exec_id))

        return result.get('ExitCode') or 0, stdout or b'', stderr or b''

    def _prefix_login_path(self, remote_path):
        ''' Make sure that we put files into a standard path

            If a path is relative, then we need to choose where to put it.
            ssh chooses $HOME but we aren't guaranteed that a home dir will
            exist in any given chroot.  So for now we're choosing "/" instead.
            This also happens to be the former default.

            Can revisit using $HOME instead if it's a problem
        '''
        if getattr(self._shell, "_IS_WINDOWS", False):
            import ntpath
            return ntpath.normpath(remote_path)
        else:
            if not remote_path.startswith(os.path.sep):
                remote_path = os.path.join(os.path.sep, remote_path)
            return os.path.normpath(remote_path)

    def _put_archive(self, container, path, data):
        # data can also be file object for streaming. This is because _put uses requests's put().
        # See https://2.python-requests.org/en/master/user/advanced/#streaming-uploads
        # WARNING: might not work with all transports!
        url = self.client._url('/containers/{0}/archive', container)
        res = self.client._put(url, params={'path': path}, data=data)
        self.client._raise_for_status(res)
        return res.status_code == 200

    def put_file(self, in_path, out_path):
        """ Transfer a file from local to docker container """
        super(Connection, self).put_file(in_path, out_path)
        display.vvv("PUT %s TO %s" % (in_path, out_path), host=self.get_option('remote_addr'))

        out_path = self._prefix_login_path(out_path)
        if not os.path.exists(to_bytes(in_path, errors='surrogate_or_strict')):
            raise AnsibleFileNotFound(
                "file or module does not exist: %s" % to_native(in_path))

        if self.actual_user not in self.ids:
            dummy, ids, dummy = self.exec_command(b'id -u && id -g')
            try:
                user_id, group_id = ids.splitlines()
                self.ids[self.actual_user] = int(user_id), int(group_id)
                display.vvvv(
                    'PUT: Determined uid={0} and gid={1} for user "{2}"'.format(user_id, group_id, self.actual_user),
                    host=self.get_option('remote_addr')
                )
            except Exception as e:
                raise AnsibleConnectionFailure(
                    'Error while determining user and group ID of current user in container "{1}": {0}\nGot value: {2!r}'
                    .format(e, self.get_option('remote_addr'), ids)
                )

        b_in_path = to_bytes(in_path, errors='surrogate_or_strict')

        out_dir, out_file = os.path.split(out_path)

        # TODO: stream tar file, instead of creating it in-memory into a BytesIO

        bio = io.BytesIO()
        with tarfile.open(fileobj=bio, mode='w|', dereference=True, encoding='utf-8') as tar:
            # Note that without both name (bytes) and arcname (unicode), this either fails for
            # Python 2.7, Python 3.5/3.6, or Python 3.7+. Only when passing both (in this
            # form) it works with Python 2.7, 3.5, 3.6, and 3.7 up to 3.11
            tarinfo = tar.gettarinfo(b_in_path, arcname=to_text(out_file))
            user_id, group_id = self.ids[self.actual_user]
            tarinfo.uid = user_id
            tarinfo.uname = ''
            if self.actual_user:
                tarinfo.uname = self.actual_user
            tarinfo.gid = group_id
            tarinfo.gname = ''
            tarinfo.mode &= 0o700
            with open(b_in_path, 'rb') as f:
                tar.addfile(tarinfo, fileobj=f)
        data = bio.getvalue()

        ok = self._call_client(
            lambda: self._put_archive(
                self.get_option('remote_addr'),
                out_dir,
                data,
            ),
            not_found_can_be_resource=True,
        )
        if not ok:
            raise AnsibleConnectionFailure(
                'Unknown error while creating file "{0}" in container "{1}".'
                .format(out_path, self.get_option('remote_addr'))
            )

    def fetch_file(self, in_path, out_path):
        """ Fetch a file from container to local. """
        super(Connection, self).fetch_file(in_path, out_path)
        display.vvv("FETCH %s TO %s" % (in_path, out_path), host=self.get_option('remote_addr'))

        in_path = self._prefix_login_path(in_path)
        b_out_path = to_bytes(out_path, errors='surrogate_or_strict')

        considered_in_paths = set()

        while True:
            if in_path in considered_in_paths:
                raise AnsibleConnectionFailure('Found infinite symbolic link loop when trying to fetch "{0}"'.format(in_path))
            considered_in_paths.add(in_path)

            display.vvvv('FETCH: Fetching "%s"' % in_path, host=self.get_option('remote_addr'))
            stream = self._call_client(
                lambda: self.client.get_raw_stream(
                    '/containers/{0}/archive', self.get_option('remote_addr'),
                    params={'path': in_path},
                    headers={'Accept-Encoding': 'identity'},
                ),
                not_found_can_be_resource=True,
            )

            # TODO: stream tar file instead of downloading it into a BytesIO

            bio = io.BytesIO()
            for chunk in stream:
                bio.write(chunk)
            bio.seek(0)

            with tarfile.open(fileobj=bio, mode='r|') as tar:
                symlink_member = None
                first = True
                for member in tar:
                    if not first:
                        raise AnsibleConnectionFailure('Received tarfile contains more than one file!')
                    first = False
                    if member.issym():
                        symlink_member = member
                        continue
                    if not member.isfile():
                        raise AnsibleConnectionFailure('Remote file "%s" is not a regular file or a symbolic link' % in_path)
                    in_f = tar.extractfile(member)  # in Python 2, this *cannot* be used in `with`...
                    with open(b_out_path, 'wb') as out_f:
                        shutil.copyfileobj(in_f, out_f, member.size)
                if first:
                    raise AnsibleConnectionFailure('Received tarfile is empty!')
                # If the only member was a file, it's already extracted. If it is a symlink, process it now.
                if symlink_member is not None:
                    in_path = os.path.join(os.path.split(in_path)[0], symlink_member.linkname)
                    display.vvvv('FETCH: Following symbolic link to "%s"' % in_path, host=self.get_option('remote_addr'))
                    continue
                return

    def close(self):
        """ Terminate the connection. Nothing to do for Docker"""
        super(Connection, self).close()
        self._connected = False

    def reset(self):
        self.ids.clear()
