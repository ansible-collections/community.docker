#!/usr/bin/python
#
# Copyright (c) 2023, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations


DOCUMENTATION = r"""
module: docker_compose_v2_exec

short_description: Run command in a container of a Compose service

version_added: 3.13.0

description:
  - Uses Docker Compose to run a command in a service's container.
  - This can be used to run one-off commands in an existing service's container, and encapsulates C(docker compose exec).
extends_documentation_fragment:
  - community.docker._compose_v2
  - community.docker._compose_v2.minimum_version
  - community.docker._docker.cli_documentation
  - community.docker._attributes
  - community.docker._attributes.actiongroup_docker

attributes:
  check_mode:
    support: none
  diff_mode:
    support: none
  idempotent:
    support: N/A
    details:
      - Whether the executed command is idempotent depends on the command.

options:
  service:
    description:
      - The service to run the command in.
    type: str
    required: true
  index:
    description:
      - The index of the container to run the command in if the service has multiple replicas.
    type: int
  argv:
    type: list
    elements: str
    description:
      - The command to execute.
      - Since this is a list of arguments, no quoting is needed.
      - Exactly one of O(argv) or O(command) must be specified.
  command:
    type: str
    description:
      - The command to execute.
      - Exactly one of O(argv) or O(command) must be specified.
  chdir:
    type: str
    description:
      - The directory to run the command in.
  detach:
    description:
      - Whether to run the command synchronously (O(detach=false), default) or asynchronously (O(detach=true)).
      - If set to V(true), O(stdin) cannot be provided, and the return values RV(stdout), RV(stderr), and RV(rc) are not returned.
    type: bool
    default: false
  user:
    type: str
    description:
      - If specified, the user to execute this command with.
  stdin:
    type: str
    description:
      - Set the stdin of the command directly to the specified value.
      - Can only be used if O(detach=false).
  stdin_add_newline:
    type: bool
    default: true
    description:
      - If set to V(true), appends a newline to O(stdin).
  strip_empty_ends:
    type: bool
    default: true
    description:
      - Strip empty lines from the end of stdout/stderr in result.
  privileged:
    type: bool
    default: false
    description:
      - Whether to give extended privileges to the process.
  tty:
    type: bool
    default: true
    description:
      - Whether to allocate a TTY.
  env:
    description:
      - Dictionary of environment variables with their respective values to be passed to the command ran inside the container.
      - Values which might be parsed as numbers, booleans or other types by the YAML parser must be quoted (for example V("true"))
        in order to avoid data loss.
      - Please note that if you are passing values in with Jinja2 templates, like V("{{ value }}"), you need to add V(| string)
        to prevent Ansible to convert strings such as V("true") back to booleans. The correct way is to use V("{{ value |
        string }}").
    type: dict

author:
  - Felix Fontein (@felixfontein)

seealso:
  - module: community.docker.docker_compose_v2

notes:
  - If you need to evaluate environment variables of the container in O(command) or O(argv), you need to pass the command
    through a shell, like O(command=/bin/sh -c "echo $ENV_VARIABLE"). The same needs to be done in case you want to use glob patterns
    or other shell features such as redirects.
"""

EXAMPLES = r"""
---
- name: Run a simple command (command)
  community.docker.docker_compose_v2_exec:
    service: foo
    command: /bin/bash -c "ls -lah"
    chdir: /root
  register: result

- name: Print stdout
  ansible.builtin.debug:
    var: result.stdout

- name: Run a simple command (argv)
  community.docker.docker_compose_v2_exec:
    service: foo
    argv:
      - /bin/bash
      - "-c"
      - "ls -lah > /dev/stderr"
    chdir: /root
  register: result

- name: Print stderr lines
  ansible.builtin.debug:
    var: result.stderr_lines
"""

RETURN = r"""
stdout:
  type: str
  returned: success and O(detach=false)
  description:
    - The standard output of the container command.
stderr:
  type: str
  returned: success and O(detach=false)
  description:
    - The standard error output of the container command.
rc:
  type: int
  returned: success and O(detach=false)
  sample: 0
  description:
    - The exit code of the command.
"""

import shlex
import traceback
import typing as t

from ansible.module_utils.common.text.converters import to_text

from ansible_collections.community.docker.plugins.module_utils._common_cli import (
    AnsibleModuleDockerClient,
    DockerException,
)
from ansible_collections.community.docker.plugins.module_utils._compose_v2 import (
    BaseComposeManager,
    common_compose_argspec_ex,
)


class ExecManager(BaseComposeManager):
    def __init__(self, client: AnsibleModuleDockerClient) -> None:
        super().__init__(client)
        parameters = self.client.module.params

        self.service: str = parameters["service"]
        self.index: int | None = parameters["index"]
        self.chdir: str | None = parameters["chdir"]
        self.detach: bool = parameters["detach"]
        self.user: str | None = parameters["user"]
        self.stdin: str | None = parameters["stdin"]
        self.strip_empty_ends: bool = parameters["strip_empty_ends"]
        self.privileged: bool = parameters["privileged"]
        self.tty: bool = parameters["tty"]
        self.env: dict[str, t.Any] = parameters["env"]

        self.argv: list[str]
        if parameters["command"] is not None:
            self.argv = shlex.split(parameters["command"])
        else:
            self.argv = parameters["argv"]

        if self.detach and self.stdin is not None:
            self.fail("If detach=true, stdin cannot be provided.")

        stdin_add_newline: bool = parameters["stdin_add_newline"]
        if self.stdin is not None and stdin_add_newline:
            self.stdin += "\n"

        if self.env is not None:
            for name, value in list(self.env.items()):
                if not isinstance(value, str):
                    self.fail(
                        "Non-string value found for env option. Ambiguous env options must be "
                        f"wrapped in quotes to avoid them being interpreted. Key: {name}"
                    )
                self.env[name] = to_text(value, errors="surrogate_or_strict")

    def get_exec_cmd(self, dry_run: bool) -> list[str]:
        args = self.get_base_args(plain_progress=True) + ["exec"]
        if self.index is not None:
            args.extend(["--index", str(self.index)])
        if self.chdir is not None:
            args.extend(["--workdir", self.chdir])
        if self.detach:
            args.extend(["--detach"])
        if self.user is not None:
            args.extend(["--user", self.user])
        if self.privileged:
            args.append("--privileged")
        if not self.tty:
            args.append("--no-TTY")
        if self.env:
            for name, value in list(self.env.items()):
                args.append("--env")
                args.append(f"{name}={value}")
        args.append("--")
        args.append(self.service)
        args.extend(self.argv)
        return args

    def run(self) -> dict[str, t.Any]:
        args = self.get_exec_cmd(self.check_mode)
        kwargs: dict[str, t.Any] = {
            "cwd": self.project_src,
        }
        if self.stdin is not None:
            kwargs["data"] = self.stdin.encode("utf-8")
        if self.detach:
            kwargs["check_rc"] = True
        rc, stdout_b, stderr_b = self.client.call_cli(*args, **kwargs)
        if self.detach:
            return {}
        stdout = to_text(stdout_b)
        stderr = to_text(stderr_b)
        if self.strip_empty_ends:
            stdout = stdout.rstrip("\r\n")
            stderr = stderr.rstrip("\r\n")
        return {
            "changed": True,
            "rc": rc,
            "stdout": stdout,
            "stderr": stderr,
        }


def main() -> None:
    argument_spec = {
        "service": {"type": "str", "required": True},
        "index": {"type": "int"},
        "argv": {"type": "list", "elements": "str"},
        "command": {"type": "str"},
        "chdir": {"type": "str"},
        "detach": {"type": "bool", "default": False},
        "user": {"type": "str"},
        "stdin": {"type": "str"},
        "stdin_add_newline": {"type": "bool", "default": True},
        "strip_empty_ends": {"type": "bool", "default": True},
        "privileged": {"type": "bool", "default": False},
        "tty": {"type": "bool", "default": True},
        "env": {"type": "dict"},
    }
    argspec_ex = common_compose_argspec_ex()
    argument_spec.update(argspec_ex.pop("argspec"))

    client = AnsibleModuleDockerClient(
        argument_spec=argument_spec,
        supports_check_mode=False,
        needs_api_version=False,
        **argspec_ex,
    )

    try:
        manager = ExecManager(client)
        result = manager.run()
        manager.cleanup()
        client.module.exit_json(**result)
    except DockerException as e:
        client.fail(
            f"An unexpected Docker error occurred: {e}",
            exception=traceback.format_exc(),
        )


if __name__ == "__main__":
    main()
