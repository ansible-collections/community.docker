# Copyright (c) 2019-2020, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations


DOCUMENTATION = r"""
author:
  - Felix Fontein (@felixfontein)
name: docker_api
short_description: Run tasks in docker containers
version_added: 1.1.0
description:
  - Run commands or put/fetch files to an existing docker container.
  - Uses the L(requests library,https://pypi.org/project/requests/) to interact directly with the Docker daemon instead of
    using the Docker CLI. Use the P(community.docker.docker#connection) connection plugin if you want to use the Docker CLI.
notes:
  - Does B(not work with TCP TLS sockets)! This is caused by the inability to send C(close_notify) without closing the connection
    with Python's C(SSLSocket)s. See U(https://github.com/ansible-collections/community.docker/issues/605) for more information.
extends_documentation_fragment:
  - community.docker._docker.api_documentation
  - community.docker._docker.var_names
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
      - Requires Docker API version 1.35 or later.
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

import os
import os.path
import typing as t

from ansible.errors import AnsibleConnectionFailure, AnsibleFileNotFound
from ansible.module_utils.common.text.converters import to_bytes, to_text
from ansible.plugins.connection import ConnectionBase
from ansible.utils.display import Display

from ansible_collections.community.docker.plugins.module_utils._api.errors import (
    APIError,
    DockerException,
    NotFound,
)
from ansible_collections.community.docker.plugins.module_utils._common_api import (
    RequestException,
)
from ansible_collections.community.docker.plugins.module_utils._copy import (
    DockerFileCopyError,
    DockerFileNotFound,
    fetch_file,
    put_file,
)
from ansible_collections.community.docker.plugins.module_utils._version import (
    LooseVersion,
)
from ansible_collections.community.docker.plugins.plugin_utils._common_api import (
    AnsibleDockerClient,
)
from ansible_collections.community.docker.plugins.plugin_utils._socket_handler import (
    DockerSocketHandler,
)


if t.TYPE_CHECKING:
    from collections.abc import Callable

    _T = t.TypeVar("_T")


MIN_DOCKER_API = None


display = Display()


class Connection(ConnectionBase):
    """Local docker based connections"""

    transport = "community.docker.docker_api"
    has_pipelining = True

    def _call_client(
        self,
        f: Callable[[AnsibleDockerClient], _T],
        not_found_can_be_resource: bool = False,
    ) -> _T:
        if self.client is None:
            raise AssertionError("Client must be present")
        remote_addr = self.get_option("remote_addr")
        try:
            return f(self.client)
        except NotFound as e:
            if not_found_can_be_resource:
                raise AnsibleConnectionFailure(
                    f'Could not find container "{remote_addr}" or resource in it ({e})'
                ) from e
            raise AnsibleConnectionFailure(
                f'Could not find container "{remote_addr}" ({e})'
            ) from e
        except APIError as e:
            if e.response is not None and e.response.status_code == 409:
                raise AnsibleConnectionFailure(
                    f'The container "{remote_addr}" has been paused ({e})'
                ) from e
            self.client.fail(
                f'An unexpected Docker error occurred for container "{remote_addr}": {e}'
            )
        except DockerException as e:
            self.client.fail(
                f'An unexpected Docker error occurred for container "{remote_addr}": {e}'
            )
        except RequestException as e:
            self.client.fail(
                f'An unexpected requests error occurred for container "{remote_addr}" when trying to talk to the Docker daemon: {e}'
            )

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        super().__init__(*args, **kwargs)

        self.client: AnsibleDockerClient | None = None
        self.ids: dict[str | None, tuple[int, int]] = {}

        # Windows uses Powershell modules
        if getattr(self._shell, "_IS_WINDOWS", False):
            self.module_implementation_preferences = (".ps1", ".exe", "")

        self.actual_user: str | None = None

    def _connect(self) -> Connection:
        """Connect to the container. Nothing to do"""
        super()._connect()  # type: ignore[safe-super]
        if not self._connected:
            self.actual_user = self.get_option("remote_user")
            display.vvv(
                f"ESTABLISH DOCKER CONNECTION FOR USER: {self.actual_user or '?'}",
                host=self.get_option("remote_addr"),
            )
            if self.client is None:
                self.client = AnsibleDockerClient(
                    self, min_docker_api_version=MIN_DOCKER_API
                )
            self._connected = True

            if self.actual_user is None and display.verbosity > 2:
                # Since we are not setting the actual_user, look it up so we have it for logging later
                # Only do this if display verbosity is high enough that we'll need the value
                # This saves overhead from calling into docker when we do not need to
                display.vvv("Trying to determine actual user")
                result = self._call_client(
                    lambda client: client.get_json(
                        "/containers/{0}/json", self.get_option("remote_addr")
                    )
                )
                if result.get("Config"):
                    self.actual_user = result["Config"].get("User")
                    if self.actual_user is not None:
                        display.vvv(f"Actual user is '{self.actual_user}'")

        return self

    def exec_command(
        self, cmd: str, in_data: bytes | None = None, sudoable: bool = False
    ) -> tuple[int, bytes, bytes]:
        """Run a command on the docker host"""

        super().exec_command(cmd, in_data=in_data, sudoable=sudoable)  # type: ignore[safe-super]

        if self.client is None:
            raise AssertionError("Client must be present")

        command = [self._play_context.executable, "-c", cmd]

        do_become = self.become and self.become.expect_prompt() and sudoable

        stdin_part = (
            f", with stdin ({len(in_data)} bytes)" if in_data is not None else ""
        )
        become_part = ", with become prompt" if do_become else ""
        display.vvv(
            f"EXEC {to_text(command)}{stdin_part}{become_part}",
            host=self.get_option("remote_addr"),
        )

        need_stdin = bool((in_data is not None) or do_become)

        data = {
            "Container": self.get_option("remote_addr"),
            "User": self.get_option("remote_user") or "",
            "Privileged": self.get_option("privileged"),
            "Tty": False,
            "AttachStdin": need_stdin,
            "AttachStdout": True,
            "AttachStderr": True,
            "Cmd": command,
        }

        if "detachKeys" in self.client._general_configs:
            data["detachKeys"] = self.client._general_configs["detachKeys"]

        if self.get_option("extra_env"):
            data["Env"] = []
            for k, v in self.get_option("extra_env").items():
                for val, what in ((k, "Key"), (v, "Value")):
                    if not isinstance(val, str):
                        raise AnsibleConnectionFailure(
                            f"Non-string {what.lower()} found for extra_env option. Ambiguous env options must be "
                            f"wrapped in quotes to avoid them being interpreted. {what}: {val!r}"
                        )
                kk = to_text(k, errors="surrogate_or_strict")
                vv = to_text(v, errors="surrogate_or_strict")
                data["Env"].append(f"{kk}={vv}")

        if self.get_option("working_dir") is not None:
            data["WorkingDir"] = self.get_option("working_dir")
            if self.client.docker_api_version < LooseVersion("1.35"):
                raise AnsibleConnectionFailure(
                    "Providing the working directory requires Docker API version 1.35 or newer."
                    f" The Docker daemon the connection is using has API version {self.client.docker_api_version_str}."
                )

        exec_data = self._call_client(
            lambda client: client.post_json_to_json(
                "/containers/{0}/exec", self.get_option("remote_addr"), data=data
            )
        )
        exec_id = exec_data["Id"]

        data = {"Tty": False, "Detach": False}
        if need_stdin:
            exec_socket = self._call_client(
                lambda client: client.post_json_to_stream_socket(
                    "/exec/{0}/start", exec_id, data=data
                )
            )
            try:
                with DockerSocketHandler(
                    display, exec_socket, container=self.get_option("remote_addr")
                ) as exec_socket_handler:
                    if do_become:
                        assert self.become is not None

                        become_output = [b""]

                        def append_become_output(stream_id: int, data: bytes) -> None:
                            become_output[0] += data

                        exec_socket_handler.set_block_done_callback(
                            append_become_output
                        )

                        while not self.become.check_success(
                            become_output[0]
                        ) and not self.become.check_password_prompt(become_output[0]):
                            if not exec_socket_handler.select(
                                self.get_option("container_timeout")
                            ):
                                stdout, stderr = exec_socket_handler.consume()
                                raise AnsibleConnectionFailure(
                                    "timeout waiting for privilege escalation password prompt:\n"
                                    + to_text(become_output[0])
                                )

                            if exec_socket_handler.is_eof():
                                raise AnsibleConnectionFailure(
                                    "privilege output closed while waiting for password prompt:\n"
                                    + to_text(become_output[0])
                                )

                        if not self.become.check_success(become_output[0]):
                            become_pass = self.become.get_option(
                                "become_pass", playcontext=self._play_context
                            )
                            exec_socket_handler.write(
                                to_bytes(become_pass, errors="surrogate_or_strict")
                                + b"\n"
                            )

                    if in_data is not None:
                        exec_socket_handler.write(in_data)

                    stdout, stderr = exec_socket_handler.consume()
            finally:
                exec_socket.close()
        else:
            stdout, stderr = self._call_client(
                lambda client: client.post_json_to_stream(
                    "/exec/{0}/start",
                    exec_id,
                    stream=False,
                    demux=True,
                    tty=False,
                    data=data,
                )
            )

        result = self._call_client(
            lambda client: client.get_json("/exec/{0}/json", exec_id)
        )

        return result.get("ExitCode") or 0, stdout or b"", stderr or b""

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
        super().put_file(in_path, out_path)  # type: ignore[safe-super]
        display.vvv(f"PUT {in_path} TO {out_path}", host=self.get_option("remote_addr"))

        if self.client is None:
            raise AssertionError("Client must be present")

        out_path = self._prefix_login_path(out_path)

        if self.actual_user not in self.ids:
            dummy, ids, dummy2 = self.exec_command("id -u && id -g")
            remote_addr = self.get_option("remote_addr")
            try:
                b_user_id, b_group_id = ids.splitlines()
                user_id, group_id = int(b_user_id), int(b_group_id)
                self.ids[self.actual_user] = user_id, group_id
                display.vvvv(
                    f'PUT: Determined uid={user_id} and gid={group_id} for user "{self.actual_user}"',
                    host=remote_addr,
                )
            except Exception as e:
                raise AnsibleConnectionFailure(
                    f'Error while determining user and group ID of current user in container "{remote_addr}": {e}\nGot value: {ids!r}'
                ) from e

        user_id, group_id = self.ids[self.actual_user]
        try:
            self._call_client(
                lambda client: put_file(
                    client,
                    container=self.get_option("remote_addr"),
                    in_path=in_path,
                    out_path=out_path,
                    user_id=user_id,
                    group_id=group_id,
                    user_name=self.actual_user,
                    follow_links=True,
                ),
                not_found_can_be_resource=True,
            )
        except DockerFileNotFound as exc:
            raise AnsibleFileNotFound(to_text(exc)) from exc
        except DockerFileCopyError as exc:
            raise AnsibleConnectionFailure(to_text(exc)) from exc

    def fetch_file(self, in_path: str, out_path: str) -> None:
        """Fetch a file from container to local."""
        super().fetch_file(in_path, out_path)  # type: ignore[safe-super]
        display.vvv(
            f"FETCH {in_path} TO {out_path}", host=self.get_option("remote_addr")
        )

        if self.client is None:
            raise AssertionError("Client must be present")

        in_path = self._prefix_login_path(in_path)

        try:
            self._call_client(
                lambda client: fetch_file(
                    client,
                    container=self.get_option("remote_addr"),
                    in_path=in_path,
                    out_path=out_path,
                    follow_links=True,
                    log=lambda msg: display.vvvv(
                        msg, host=self.get_option("remote_addr")
                    ),
                ),
                not_found_can_be_resource=True,
            )
        except DockerFileNotFound as exc:
            raise AnsibleFileNotFound(to_text(exc)) from exc
        except DockerFileCopyError as exc:
            raise AnsibleConnectionFailure(to_text(exc)) from exc

    def close(self) -> None:
        """Terminate the connection. Nothing to do for Docker"""
        super().close()  # type: ignore[safe-super]
        self._connected = False

    def reset(self) -> None:
        self.ids.clear()
