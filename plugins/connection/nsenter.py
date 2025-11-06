# Copyright (c) 2021 Jeff Goldschrafe <jeff@holyhandgrenade.org>
# Based on Ansible local connection plugin by:
# Copyright (c) 2012 Michael DeHaan <michael.dehaan@gmail.com>
# Copyright (c) 2015, 2017 Toshio Kuratomi <tkuratomi@ansible.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations


DOCUMENTATION = r"""
name: nsenter
short_description: execute on host running controller container
version_added: 1.9.0
description:
  - This connection plugin allows Ansible, running in a privileged container, to execute tasks on the container host instead
    of in the container itself.
  - This is useful for running Ansible in a pull model, while still keeping the Ansible control node containerized.
  - It relies on having privileged access to run C(nsenter) in the host's PID namespace, allowing it to enter the namespaces
    of the provided PID (default PID 1, or init/systemd).
author: Jeff Goldschrafe (@jgoldschrafe)
options:
  nsenter_pid:
    description:
      - PID to attach with using nsenter.
      - The default should be fine unless you are attaching as a non-root user.
    type: int
    default: 1
    vars:
      - name: ansible_nsenter_pid
    env:
      - name: ANSIBLE_NSENTER_PID
    ini:
      - section: nsenter_connection
        key: nsenter_pid
notes:
  - The remote user is ignored; this plugin always runs as root.
  - "This plugin requires the Ansible controller container to be launched in the following way: (1) The container image contains
    the C(nsenter) program; (2) The container is launched in privileged mode; (3) The container is launched in the host's
    PID namespace (C(--pid host))."
"""

import fcntl
import os
import pty
import selectors
import shlex
import subprocess
import typing as t

import ansible.constants as C
from ansible.errors import AnsibleError
from ansible.module_utils.common.text.converters import to_bytes, to_text
from ansible.plugins.connection import ConnectionBase
from ansible.utils.display import Display
from ansible.utils.path import unfrackpath


display = Display()


class Connection(ConnectionBase):
    """Connections to a container host using nsenter"""

    transport = "community.docker.nsenter"
    has_pipelining = False

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        super().__init__(*args, **kwargs)
        self.cwd = None
        self._nsenter_pid = None

    def _connect(self) -> t.Self:
        self._nsenter_pid = self.get_option("nsenter_pid")

        # Because nsenter requires very high privileges, our remote user
        # is always assumed to be root.
        self._play_context.remote_user = "root"

        if not self._connected:
            display.vvv(
                f"ESTABLISH NSENTER CONNECTION FOR USER: {self._play_context.remote_user}",
                host=self._play_context.remote_addr,
            )
            self._connected = True
        return self

    def exec_command(
        self, cmd: str, in_data: bytes | None = None, sudoable: bool = True
    ) -> tuple[int, bytes, bytes]:
        super().exec_command(cmd, in_data=in_data, sudoable=sudoable)  # type: ignore[safe-super]

        display.debug("in nsenter.exec_command()")

        # pylint: disable-next=no-member
        def_executable: str | None = C.DEFAULT_EXECUTABLE  # type: ignore[attr-defined]
        executable = def_executable.split()[0] if def_executable else None

        if not os.path.exists(to_bytes(executable, errors="surrogate_or_strict")):
            raise AnsibleError(
                f"failed to find the executable specified {executable}."
                " Please verify if the executable exists and re-try."
            )

        # Rewrite the provided command to prefix it with nsenter
        nsenter_cmd_parts = [
            "nsenter",
            "--ipc",
            "--mount",
            "--net",
            "--pid",
            "--uts",
            "--preserve-credentials",
            f"--target={self._nsenter_pid}",
            "--",
        ]

        cmd_parts = nsenter_cmd_parts + [cmd]
        cmd_b = to_bytes(" ".join(cmd_parts))

        display.vvv(f"EXEC {to_text(cmd_b)}", host=self._play_context.remote_addr)
        display.debug("opening command with Popen()")

        master = None
        stdin = subprocess.PIPE

        # This plugin does not support pipelining. This diverges from the behavior of
        # the core "local" connection plugin that this one derives from.
        if sudoable and self.become and self.become.expect_prompt():
            # Create a pty if sudoable for privilege escalation that needs it.
            # Falls back to using a standard pipe if this fails, which may
            # cause the command to fail in certain situations where we are escalating
            # privileges or the command otherwise needs a pty.
            try:
                master, stdin = pty.openpty()
            except (IOError, OSError) as e:
                display.debug(f"Unable to open pty: {e}")

        with subprocess.Popen(
            cmd_b,
            shell=True,
            executable=executable,
            cwd=self.cwd,
            stdin=stdin,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ) as p:
            assert p.stderr is not None
            assert p.stdin is not None
            assert p.stdout is not None
            # if we created a master, we can close the other half of the pty now, otherwise master is stdin
            if master is not None:
                os.close(stdin)

            display.debug("done running command with Popen()")

            if self.become and self.become.expect_prompt() and sudoable:
                fcntl.fcntl(
                    p.stdout,
                    fcntl.F_SETFL,
                    fcntl.fcntl(p.stdout, fcntl.F_GETFL) | os.O_NONBLOCK,
                )
                fcntl.fcntl(
                    p.stderr,
                    fcntl.F_SETFL,
                    fcntl.fcntl(p.stderr, fcntl.F_GETFL) | os.O_NONBLOCK,
                )
                selector = selectors.DefaultSelector()
                selector.register(p.stdout, selectors.EVENT_READ)
                selector.register(p.stderr, selectors.EVENT_READ)

                become_output = b""
                try:
                    while not self.become.check_success(
                        become_output
                    ) and not self.become.check_password_prompt(become_output):
                        events = selector.select(self._play_context.timeout)
                        if not events:
                            stdout, stderr = p.communicate()
                            raise AnsibleError(
                                "timeout waiting for privilege escalation password prompt:\n"
                                + to_text(become_output)
                            )

                        chunks = b""
                        for key, dummy_event in events:
                            if key.fileobj == p.stdout:
                                chunk = p.stdout.read()
                                if chunk:
                                    chunks += chunk
                            elif key.fileobj == p.stderr:
                                chunk = p.stderr.read()
                                if chunk:
                                    chunks += chunk

                        if not chunks:
                            stdout, stderr = p.communicate()
                            raise AnsibleError(
                                "privilege output closed while waiting for password prompt:\n"
                                + to_text(become_output)
                            )
                        become_output += chunks
                finally:
                    selector.close()

                if not self.become.check_success(become_output):
                    become_pass = self.become.get_option(
                        "become_pass", playcontext=self._play_context
                    )
                    if master is None:
                        p.stdin.write(
                            to_bytes(become_pass, errors="surrogate_or_strict") + b"\n"
                        )
                    else:
                        os.write(
                            master,
                            to_bytes(become_pass, errors="surrogate_or_strict") + b"\n",
                        )

                fcntl.fcntl(
                    p.stdout,
                    fcntl.F_SETFL,
                    fcntl.fcntl(p.stdout, fcntl.F_GETFL) & ~os.O_NONBLOCK,
                )
                fcntl.fcntl(
                    p.stderr,
                    fcntl.F_SETFL,
                    fcntl.fcntl(p.stderr, fcntl.F_GETFL) & ~os.O_NONBLOCK,
                )

            display.debug("getting output with communicate()")
            stdout, stderr = p.communicate(in_data)
            display.debug("done communicating")

            # finally, close the other half of the pty, if it was created
            if master:
                os.close(master)

            display.debug("done with nsenter.exec_command()")
            return (p.returncode, stdout, stderr)

    def put_file(self, in_path: str, out_path: str) -> None:
        super().put_file(in_path, out_path)  # type: ignore[safe-super]

        in_path = unfrackpath(in_path, basedir=self.cwd)
        out_path = unfrackpath(out_path, basedir=self.cwd)

        display.vvv(f"PUT {in_path} to {out_path}", host=self._play_context.remote_addr)
        try:
            with open(to_bytes(in_path, errors="surrogate_or_strict"), "rb") as in_file:
                in_data = in_file.read()
            rc, dummy_out, err = self.exec_command(
                cmd=f"tee {shlex.quote(out_path)}", in_data=in_data
            )
            if rc != 0:
                raise AnsibleError(
                    f"failed to transfer file to {out_path}: {to_text(err)}"
                )
        except IOError as e:
            raise AnsibleError(f"failed to transfer file to {out_path}: {e}") from e

    def fetch_file(self, in_path: str, out_path: str) -> None:
        super().fetch_file(in_path, out_path)  # type: ignore[safe-super]

        in_path = unfrackpath(in_path, basedir=self.cwd)
        out_path = unfrackpath(out_path, basedir=self.cwd)

        try:
            rc, out, err = self.exec_command(cmd=f"cat {shlex.quote(in_path)}")
            display.vvv(
                f"FETCH {in_path} TO {out_path}", host=self._play_context.remote_addr
            )
            if rc != 0:
                raise AnsibleError(
                    f"failed to transfer file to {in_path}: {to_text(err)}"
                )
            with open(
                to_bytes(out_path, errors="surrogate_or_strict"), "wb"
            ) as out_file:
                out_file.write(out)
        except IOError as e:
            raise AnsibleError(
                f"failed to transfer file to {to_text(out_path)}: {e}"
            ) from e

    def close(self) -> None:
        """terminate the connection; nothing to do here"""
        self._connected = False
