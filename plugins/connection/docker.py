# Based on the chroot connection plugin by Maykel Moya
#
# (c) 2014, Lorin Hochstein
# (c) 2015, Leendert Brouwer (https://github.com/objectified)
# (c) 2015, Toshio Kuratomi <tkuratomi@ansible.com>
# Copyright (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations


DOCUMENTATION = r"""
author:
  - Lorin Hochestein (!UNKNOWN)
  - Leendert Brouwer (!UNKNOWN)
name: docker
short_description: Run tasks in docker containers
description:
  - Run commands or put/fetch files to an existing docker container.
  - Uses the Docker CLI to execute commands in the container. If you prefer to directly connect to the Docker daemon, use
    the P(community.docker.docker_api#connection) connection plugin.
options:
  remote_addr:
    description:
      - The name of the container you want to access.
    default: inventory_hostname
    vars:
      - name: inventory_hostname
      - name: ansible_host
      - name: ansible_docker_host
  remote_user:
    description:
      - The user to execute as inside the container.
      - If Docker is too old to allow this (< 1.7), the one set by Docker itself will be used.
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
  docker_extra_args:
    description:
      - Extra arguments to pass to the docker command line.
    default: ''
    vars:
      - name: ansible_docker_extra_args
    ini:
      - section: docker_connection
        key: extra_cli_args
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
  extra_env:
    description:
      - Provide extra environment variables to set when running commands in the Docker container.
      - This option can currently only be provided as Ansible variables due to limitations of ansible-core's configuration
        manager.
    vars:
      - name: ansible_docker_extra_env
    type: dict
    version_added: 3.12.0
  working_dir:
    description:
      - The directory inside the container to run commands in.
      - Requires Docker CLI version 18.06 or later.
    env:
      - name: ANSIBLE_DOCKER_WORKING_DIR
    ini:
      - key: working_dir
        section: docker_connection
    vars:
      - name: ansible_docker_working_dir
    type: string
    version_added: 3.12.0
  privileged:
    description:
      - Whether commands should be run with extended privileges.
      - B(Note) that this allows command to potentially break out of the container. Use with care!
    env:
      - name: ANSIBLE_DOCKER_PRIVILEGED
    ini:
      - key: privileged
        section: docker_connection
    vars:
      - name: ansible_docker_privileged
    type: boolean
    default: false
    version_added: 3.12.0
"""

import fcntl
import os
import os.path
import re
import selectors
import subprocess
import typing as t
from shlex import quote

from ansible.errors import AnsibleConnectionFailure, AnsibleError, AnsibleFileNotFound
from ansible.module_utils.common.process import get_bin_path
from ansible.module_utils.common.text.converters import to_bytes, to_text
from ansible.plugins.connection import BUFSIZE, ConnectionBase
from ansible.utils.display import Display

from ansible_collections.community.docker.plugins.module_utils._version import (
    LooseVersion,
)


display = Display()


class Connection(ConnectionBase):
    """Local docker based connections"""

    transport = "community.docker.docker"
    has_pipelining = True

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        super().__init__(*args, **kwargs)

        # Note: docker supports running as non-root in some configurations.
        # (For instance, setting the UNIX socket file to be readable and
        # writable by a specific UNIX group and then putting users into that
        # group).  Therefore we do not check that the user is root when using
        # this connection.  But if the user is getting a permission denied
        # error it probably means that docker on their system is only
        # configured to be connected to by root and they are not running as
        # root.

        self._docker_args: list[bytes | str] = []
        self._container_user_cache: dict[str, str | None] = {}
        self._version: str | None = None
        self.remote_user: str | None = None
        self.timeout: int | float | None = None

        # Windows uses Powershell modules
        if getattr(self._shell, "_IS_WINDOWS", False):
            self.module_implementation_preferences = (".ps1", ".exe", "")

        if "docker_command" in kwargs:
            self.docker_cmd = kwargs["docker_command"]
        else:
            try:
                self.docker_cmd = get_bin_path("docker")
            except ValueError as exc:
                raise AnsibleError("docker command not found in PATH") from exc

    @staticmethod
    def _sanitize_version(version: str) -> str:
        version = re.sub("[^0-9a-zA-Z.]", "", version)
        version = re.sub("^v", "", version)
        return version

    def _old_docker_version(self) -> tuple[list[str], str, bytes, int]:
        cmd_args = self._docker_args

        old_version_subcommand = ["version"]

        old_docker_cmd = [self.docker_cmd] + cmd_args + old_version_subcommand
        with subprocess.Popen(
            old_docker_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ) as p:
            cmd_output, err = p.communicate()

        return old_docker_cmd, to_text(cmd_output), err, p.returncode

    def _new_docker_version(self) -> tuple[list[str], str, bytes, int]:
        # no result yet, must be newer Docker version
        cmd_args = self._docker_args

        new_version_subcommand = ["version", "--format", "'{{.Server.Version}}'"]

        new_docker_cmd = [self.docker_cmd] + cmd_args + new_version_subcommand
        with subprocess.Popen(
            new_docker_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ) as p:
            cmd_output, err = p.communicate()
            return new_docker_cmd, to_text(cmd_output), err, p.returncode

    def _get_docker_version(self) -> str:
        cmd, cmd_output, err, returncode = self._old_docker_version()
        if returncode == 0:
            for line in to_text(cmd_output, errors="surrogate_or_strict").split("\n"):
                if line.startswith("Server version:"):  # old docker versions
                    return self._sanitize_version(line.split()[2])

        cmd, cmd_output, err, returncode = self._new_docker_version()
        if returncode:
            raise AnsibleError(
                f"Docker version check ({to_text(cmd)}) failed: {to_text(err)}"
            )

        return self._sanitize_version(to_text(cmd_output, errors="surrogate_or_strict"))

    def _get_docker_remote_user(self) -> str | None:
        """Get the default user configured in the docker container"""
        container = self.get_option("remote_addr")
        if container in self._container_user_cache:
            return self._container_user_cache[container]
        with subprocess.Popen(
            [self.docker_cmd, "inspect", "--format", "{{.Config.User}}", container],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ) as p:
            out_b, err_b = p.communicate()
            out = to_text(out_b, errors="surrogate_or_strict")

            if p.returncode != 0:
                display.warning(
                    f"unable to retrieve default user from docker container: {out} {to_text(err_b)}"
                )
                self._container_user_cache[container] = None
                return None

        # The default exec user is root, unless it was changed in the Dockerfile with USER
        user = out.strip() or "root"
        self._container_user_cache[container] = user
        return user

    def _build_exec_cmd(self, cmd: list[bytes | str]) -> list[bytes | str]:
        """Build the local docker exec command to run cmd on remote_host

        If remote_user is available and is supported by the docker
        version we are using, it will be provided to docker exec.
        """

        local_cmd = [self.docker_cmd]

        if self._docker_args:
            local_cmd += self._docker_args

        local_cmd += [b"exec"]

        if self.remote_user is not None:
            local_cmd += [b"-u", self.remote_user]

        if self.get_option("extra_env"):
            for k, v in self.get_option("extra_env").items():
                for val, what in ((k, "Key"), (v, "Value")):
                    if not isinstance(val, str):
                        raise AnsibleConnectionFailure(
                            f"Non-string {what.lower()} found for extra_env option. Ambiguous env options must be "
                            f"wrapped in quotes to avoid them being interpreted. {what}: {val!r}"
                        )
                local_cmd += [
                    b"-e",
                    b"%s=%s"
                    % (
                        to_bytes(k, errors="surrogate_or_strict"),
                        to_bytes(v, errors="surrogate_or_strict"),
                    ),
                ]

        if self.get_option("working_dir") is not None:
            local_cmd += [
                b"-w",
                to_bytes(self.get_option("working_dir"), errors="surrogate_or_strict"),
            ]
            if self.docker_version != "dev" and LooseVersion(
                self.docker_version
            ) < LooseVersion("18.06"):
                # https://github.com/docker/cli/pull/732, first appeared in release 18.06.0
                raise AnsibleConnectionFailure(
                    f"Providing the working directory requires Docker CLI version 18.06 or newer. You have Docker CLI version {self.docker_version}."
                )

        if self.get_option("privileged"):
            local_cmd += [b"--privileged"]

        # -i is needed to keep stdin open which allows pipelining to work
        local_cmd += [b"-i", self.get_option("remote_addr")] + cmd

        return local_cmd

    def _set_docker_args(self) -> None:
        # TODO: this is mostly for backwards compatibility, play_context is used as fallback for older versions
        # docker arguments
        del self._docker_args[:]
        extra_args = self.get_option("docker_extra_args") or getattr(
            self._play_context, "docker_extra_args", ""
        )
        if extra_args:
            self._docker_args += extra_args.split(" ")

    def _set_conn_data(self) -> None:
        """initialize for the connection, cannot do only in init since all data is not ready at that point"""

        self._set_docker_args()

        self.remote_user = self.get_option("remote_user")
        if self.remote_user is None and self._play_context.remote_user is not None:
            self.remote_user = self._play_context.remote_user

        # timeout, use unless default and pc is different, backwards compat
        self.timeout = self.get_option("container_timeout")
        if self.timeout == 10 and self.timeout != self._play_context.timeout:
            self.timeout = self._play_context.timeout

    @property
    def docker_version(self) -> str:
        if not self._version:
            self._set_docker_args()

            self._version = self._get_docker_version()
            if self._version == "dev":
                display.warning(
                    'Docker version number is "dev". Will assume latest version.'
                )
            if self._version != "dev" and LooseVersion(self._version) < LooseVersion(
                "1.3"
            ):
                raise AnsibleError(
                    "docker connection type requires docker 1.3 or higher"
                )
        return self._version

    def _get_actual_user(self) -> str | None:
        if self.remote_user is not None:
            # An explicit user is provided
            if self.docker_version == "dev" or LooseVersion(
                self.docker_version
            ) >= LooseVersion("1.7"):
                # Support for specifying the exec user was added in docker 1.7
                return self.remote_user
            self.remote_user = None
            actual_user = self._get_docker_remote_user()
            if actual_user != self.get_option("remote_user"):
                display.warning(
                    f"docker {self.docker_version} does not support remote_user, using container default: {actual_user or '?'}"
                )
            return actual_user
        if self._display.verbosity > 2:
            # Since we are not setting the actual_user, look it up so we have it for logging later
            # Only do this if display verbosity is high enough that we'll need the value
            # This saves overhead from calling into docker when we do not need to.
            return self._get_docker_remote_user()
        return None

    def _connect(self) -> t.Self:
        """Connect to the container. Nothing to do"""
        super()._connect()  # type: ignore[safe-super]
        if not self._connected:
            self._set_conn_data()
            actual_user = self._get_actual_user()
            display.vvv(
                f"ESTABLISH DOCKER CONNECTION FOR USER: {actual_user or '?'}",
                host=self.get_option("remote_addr"),
            )
            self._connected = True
        return self

    def exec_command(
        self, cmd: str, in_data: bytes | None = None, sudoable: bool = False
    ) -> tuple[int, bytes, bytes]:
        """Run a command on the docker host"""

        self._set_conn_data()

        super().exec_command(cmd, in_data=in_data, sudoable=sudoable)  # type: ignore[safe-super]

        local_cmd = self._build_exec_cmd([self._play_context.executable, "-c", cmd])

        display.vvv(f"EXEC {to_text(local_cmd)}", host=self.get_option("remote_addr"))
        display.debug("opening command with Popen()")

        local_cmd = [to_bytes(i, errors="surrogate_or_strict") for i in local_cmd]

        with subprocess.Popen(
            local_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ) as p:
            assert p.stdin is not None
            assert p.stdout is not None
            assert p.stderr is not None
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
                        events = selector.select(self.timeout)
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
                    p.stdin.write(
                        to_bytes(become_pass, errors="surrogate_or_strict") + b"\n"
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

            display.debug("done with docker.exec_command()")
            return (p.returncode, stdout, stderr)

    def _prefix_login_path(self, remote_path: str) -> str:
        """Make sure that we put files into a standard path

        If a path is relative, then we need to choose where to put it.
        ssh chooses $HOME but we are not guaranteed that a home dir will
        exist in any given chroot.  So for now we are choosing "/" instead.
        This also happens to be the former default.

        Can revisit using $HOME instead if it is a problem
        """
        if getattr(self._shell, "_IS_WINDOWS", False):
            import ntpath

            return ntpath.normpath(remote_path)
        if not remote_path.startswith(os.path.sep):
            remote_path = os.path.join(os.path.sep, remote_path)
        return os.path.normpath(remote_path)

    def put_file(self, in_path: str, out_path: str) -> None:
        """Transfer a file from local to docker container"""
        self._set_conn_data()
        super().put_file(in_path, out_path)  # type: ignore[safe-super]
        display.vvv(f"PUT {in_path} TO {out_path}", host=self.get_option("remote_addr"))

        out_path = self._prefix_login_path(out_path)
        if not os.path.exists(to_bytes(in_path, errors="surrogate_or_strict")):
            raise AnsibleFileNotFound(
                f"file or module does not exist: {to_text(in_path)}"
            )

        out_path = quote(out_path)
        # Older docker does not have native support for copying files into
        # running containers, so we use docker exec to implement this
        # Although docker version 1.8 and later provide support, the
        # owner and group of the files are always set to root
        with open(to_bytes(in_path, errors="surrogate_or_strict"), "rb") as in_file:
            if not os.fstat(in_file.fileno()).st_size:
                count = " count=0"
            else:
                count = ""
            args = self._build_exec_cmd(
                [
                    self._play_context.executable,
                    "-c",
                    f"dd of={out_path} bs={BUFSIZE}{count}",
                ]
            )
            args = [to_bytes(i, errors="surrogate_or_strict") for i in args]
            try:
                # pylint: disable-next=consider-using-with
                p = subprocess.Popen(
                    args, stdin=in_file, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
            except OSError as exc:
                raise AnsibleError(
                    "docker connection requires dd command in the container to put files"
                ) from exc
            stdout, stderr = p.communicate()

            if p.returncode != 0:
                raise AnsibleError(
                    f"failed to transfer file {to_text(in_path)} to {to_text(out_path)}:\n{to_text(stdout)}\n{to_text(stderr)}"
                )

    def fetch_file(self, in_path: str, out_path: str) -> None:
        """Fetch a file from container to local."""
        self._set_conn_data()
        super().fetch_file(in_path, out_path)  # type: ignore[safe-super]
        display.vvv(
            f"FETCH {in_path} TO {out_path}", host=self.get_option("remote_addr")
        )

        in_path = self._prefix_login_path(in_path)
        # out_path is the final file path, but docker takes a directory, not a
        # file path
        out_dir = os.path.dirname(out_path)

        args = [
            self.docker_cmd,
            "cp",
            f"{self.get_option('remote_addr')}:{in_path}",
            out_dir,
        ]
        args = [to_bytes(i, errors="surrogate_or_strict") for i in args]

        with subprocess.Popen(
            args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ) as p:
            p.communicate()

            if getattr(self._shell, "_IS_WINDOWS", False):
                import ntpath

                actual_out_path = ntpath.join(out_dir, ntpath.basename(in_path))
            else:
                actual_out_path = os.path.join(out_dir, os.path.basename(in_path))

            if p.returncode != 0:
                # Older docker does not have native support for fetching files command `cp`
                # If `cp` fails, try to use `dd` instead
                args = self._build_exec_cmd(
                    [
                        self._play_context.executable,
                        "-c",
                        f"dd if={in_path} bs={BUFSIZE}",
                    ]
                )
                args = [to_bytes(i, errors="surrogate_or_strict") for i in args]
                with open(
                    to_bytes(actual_out_path, errors="surrogate_or_strict"), "wb"
                ) as out_file:
                    try:
                        # pylint: disable-next=consider-using-with
                        pp = subprocess.Popen(
                            args,
                            stdin=subprocess.PIPE,
                            stdout=out_file,
                            stderr=subprocess.PIPE,
                        )
                    except OSError as exc:
                        raise AnsibleError(
                            "docker connection requires dd command in the container to put files"
                        ) from exc
                    stdout, stderr = pp.communicate()

                    if pp.returncode != 0:
                        raise AnsibleError(
                            f"failed to fetch file {in_path} to {out_path}:\n{stdout!r}\n{stderr!r}"
                        )

        # Rename if needed
        if actual_out_path != out_path:
            os.rename(
                to_bytes(actual_out_path, errors="strict"),
                to_bytes(out_path, errors="strict"),
            )

    def close(self) -> None:
        """Terminate the connection. Nothing to do for Docker"""
        super().close()  # type: ignore[safe-super]
        self._connected = False

    def reset(self) -> None:
        # Clear container user cache
        self._container_user_cache = {}
