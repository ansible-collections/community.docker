#!/usr/bin/python
#
# Copyright (c) 2023, Felix Fontein <felix@fontein.de>
# Copyright (c) 2023, Léo El Amri (@lel-amri)
# Copyright 2016 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations


DOCUMENTATION = r"""
module: docker_compose_v2

short_description: Manage multi-container Docker applications with Docker Compose CLI plugin

version_added: 3.6.0

description:
  - Uses Docker Compose to start or shutdown services.
extends_documentation_fragment:
  - community.docker._compose_v2
  - community.docker._compose_v2.minimum_version
  - community.docker._docker.cli_documentation
  - community.docker._attributes
  - community.docker._attributes.actiongroup_docker

attributes:
  check_mode:
    support: full
    details:
      - In check mode, pulling the image does not result in a changed result.
  diff_mode:
    support: none
  idempotent:
    support: partial
    details:
      - If O(state=restarted) or O(recreate=always) the module is not idempotent.

options:
  state:
    description:
      - Desired state of the project.
      - V(present) is equivalent to running C(docker compose up).
      - V(stopped) is equivalent to running C(docker compose stop).
      - V(absent) is equivalent to running C(docker compose down).
      - V(restarted) is equivalent to running C(docker compose restart).
    type: str
    default: present
    choices:
      - absent
      - stopped
      - restarted
      - present
  pull:
    description:
      - Whether to pull images before running. This is used when C(docker compose up) is run.
      - V(always) ensures that the images are always pulled, even when already present on the Docker daemon.
      - V(missing) only pulls them when they are not present on the Docker daemon.
      - V(never) never pulls images. If they are not present, the module will fail when trying to create the containers that
        need them.
      - V(policy) use the Compose file's C(pull_policy) defined for the service to figure out what to do.
    type: str
    choices:
      - always
      - missing
      - never
      - policy
    default: policy
  build:
    description:
      - Whether to build images before starting containers. This is used when C(docker compose up) is run.
      - V(always) always builds before starting containers. This is equivalent to the C(--build) option of C(docker compose
        up).
      - V(never) never builds before starting containers. This is equivalent to the C(--no-build) option of C(docker compose
        up).
      - V(policy) uses the policy as defined in the Compose file.
    type: str
    choices:
      - always
      - never
      - policy
    default: policy
  dependencies:
    description:
      - When O(state) is V(present) or V(restarted), specify whether or not to include linked services.
    type: bool
    default: true
  ignore_build_events:
    description:
      - Ignores image building events for change detection.
      - If O(state=present) and O(ignore_build_events=true) and O(build=always), a rebuild that does not trigger a container
        restart no longer results in RV(ignore:changed=true).
      - Note that Docker Compose 2.31.0 is the first Compose 2.x version to emit build events. For older versions, the behavior
        is always as if O(ignore_build_events=true).
    type: bool
    default: true
    version_added: 4.2.0
  recreate:
    description:
      - By default containers will be recreated when their configuration differs from the service definition.
      - Setting to V(never) ignores configuration differences and leaves existing containers unchanged.
      - Setting to V(always) forces recreation of all existing containers.
    type: str
    default: auto
    choices:
      - always
      - never
      - auto
  renew_anon_volumes:
    description:
      - Whether to recreate instead of reuse anonymous volumes from previous containers.
      - V(true) is equivalent to the C(--renew-anon-volumes) option of C(docker compose up).
    type: bool
    default: false
    version_added: 4.0.0
  remove_images:
    description:
      - Use with O(state=absent) to remove all images or only local images.
    type: str
    choices:
      - all
      - local
  remove_volumes:
    description:
      - Use with O(state=absent) to remove data volumes.
    type: bool
    default: false
  remove_orphans:
    description:
      - Remove containers for services not defined in the Compose file.
    type: bool
    default: false
  timeout:
    description:
      - Timeout in seconds for container shutdown when attached or when containers are already running.
    type: int
  services:
    description:
      - Specifies a subset of services to be targeted.
    type: list
    elements: str
  scale:
    description:
      - Define how to scale services when running C(docker compose up).
      - Provide a dictionary of key/value pairs where the key is the name of the service and the value is an integer count
        for the number of containers.
    type: dict
    version_added: 3.7.0
  wait:
    description:
      - When running C(docker compose up), pass C(--wait) to wait for services to be running/healthy.
      - A timeout can be set with the O(wait_timeout) option.
    type: bool
    default: false
    version_added: 3.8.0
  wait_timeout:
    description:
      - When O(wait=true), wait at most this amount of seconds.
    type: int
    version_added: 3.8.0
  assume_yes:
    description:
      - When O(assume_yes=true), pass C(-y)/C(--yes) to assume "yes" as answer to all prompts and run non-interactively.
      - Right now a prompt is asked whenever a non-matching volume should be re-created. O(assume_yes=false)
        results in the question being answered by "no", which will simply re-use the existing volume.
      - This option is only available on Docker Compose 2.32.0 or newer.
    type: bool
    default: false
    version_added: 4.5.0

author:
  - Felix Fontein (@felixfontein)

seealso:
  - module: community.docker.docker_compose_v2_pull
"""

EXAMPLES = r"""
---
# Examples use the django example at https://docs.docker.com/compose/django. Follow it to create the
# flask directory

- name: Run using a project directory
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Tear down existing services
      community.docker.docker_compose_v2:
        project_src: flask
        state: absent

    - name: Create and start services
      community.docker.docker_compose_v2:
        project_src: flask
      register: output

    - name: Show results
      ansible.builtin.debug:
        var: output

    - name: Run `docker compose up` again
      community.docker.docker_compose_v2:
        project_src: flask
      register: output

    - name: Show results
      ansible.builtin.debug:
        var: output

    - ansible.builtin.assert:
        that: not output.changed

    - name: Stop all services
      community.docker.docker_compose_v2:
        project_src: flask
        state: stopped
      register: output

    - name: Show results
      ansible.builtin.debug:
        var: output

    - name: Verify that web and db services are not running
      ansible.builtin.assert:
        that:
          - web_container.State != 'running'
          - db_container.State != 'running'
      vars:
        web_container: >-
          {{ output.containers | selectattr("Service", "equalto", "web") | first }}
        db_container: >-
          {{ output.containers | selectattr("Service", "equalto", "db") | first }}

    - name: Restart services
      community.docker.docker_compose_v2:
        project_src: flask
        state: restarted
      register: output

    - name: Show results
      ansible.builtin.debug:
        var: output

    - name: Verify that web and db services are running
      ansible.builtin.assert:
        that:
          - web_container.State == 'running'
          - db_container.State == 'running'
      vars:
        web_container: >-
          {{ output.containers | selectattr("Service", "equalto", "web") | first }}
        db_container: >-
          {{ output.containers | selectattr("Service", "equalto", "db") | first }}
"""

RETURN = r"""
containers:
  description:
    - A list of containers associated to the service.
  returned: success
  type: list
  elements: dict
  contains:
    Command:
      description:
        - The container's command.
      type: raw
    CreatedAt:
      description:
        - The timestamp when the container was created.
      type: str
      sample: "2024-01-02 12:20:41 +0100 CET"
    ExitCode:
      description:
        - The container's exit code.
      type: int
    Health:
      description:
        - The container's health check.
      type: raw
    ID:
      description:
        - The container's ID.
      type: str
      sample: "44a7d607219a60b7db0a4817fb3205dce46e91df2cb4b78a6100b6e27b0d3135"
    Image:
      description:
        - The container's image.
      type: str
    Labels:
      description:
        - Labels for this container.
      type: dict
    LocalVolumes:
      description:
        - The local volumes count.
      type: str
    Mounts:
      description:
        - Mounts.
      type: str
    Name:
      description:
        - The container's primary name.
      type: str
    Names:
      description:
        - List of names of the container.
      type: list
      elements: str
    Networks:
      description:
        - List of networks attached to this container.
      type: list
      elements: str
    Ports:
      description:
        - List of port assignments as a string.
      type: str
    Publishers:
      description:
        - List of port assigments.
      type: list
      elements: dict
      contains:
        URL:
          description:
            - Interface the port is bound to.
          type: str
        TargetPort:
          description:
            - The container's port the published port maps to.
          type: int
        PublishedPort:
          description:
            - The port that is published.
          type: int
        Protocol:
          description:
            - The protocol.
          type: str
          choices:
            - tcp
            - udp
    RunningFor:
      description:
        - Amount of time the container runs.
      type: str
    Service:
      description:
        - The name of the service.
      type: str
    Size:
      description:
        - The container's size.
      type: str
      sample: "0B"
    State:
      description:
        - The container's state.
      type: str
      sample: running
    Status:
      description:
        - The container's status.
      type: str
      sample: Up About a minute
images:
  description:
    - A list of images associated to the service.
  returned: success
  type: list
  elements: dict
  contains:
    ID:
      description:
        - The image's ID.
      type: str
      sample: sha256:c8bccc0af9571ec0d006a43acb5a8d08c4ce42b6cc7194dd6eb167976f501ef1
    ContainerName:
      description:
        - Name of the conainer this image is used by.
      type: str
    Repository:
      description:
        - The repository where this image belongs to.
      type: str
    Tag:
      description:
        - The tag of the image.
      type: str
    Size:
      description:
        - The image's size in bytes.
      type: int
actions:
  description:
    - A list of actions that have been applied.
  returned: success
  type: list
  elements: dict
  contains:
    what:
      description:
        - What kind of resource was changed.
      type: str
      sample: container
      choices:
        - container
        - image
        - network
        - service
        - unknown
        - volume
    id:
      description:
        - The ID of the resource that was changed.
      type: str
      sample: container
    status:
      description:
        - The status change that happened.
      type: str
      sample: Creating
      choices:
        - Starting
        - Exiting
        - Restarting
        - Creating
        - Stopping
        - Killing
        - Removing
        - Recreating
        - Pulling
        - Building
"""

import traceback
import typing as t

from ansible.module_utils.common.validation import check_type_int

from ansible_collections.community.docker.plugins.module_utils._common_cli import (
    AnsibleModuleDockerClient,
    DockerException,
)
from ansible_collections.community.docker.plugins.module_utils._compose_v2 import (
    BaseComposeManager,
    common_compose_argspec_ex,
    is_failed,
)
from ansible_collections.community.docker.plugins.module_utils._version import (
    LooseVersion,
)


class ServicesManager(BaseComposeManager):
    def __init__(self, client: AnsibleModuleDockerClient) -> None:
        super().__init__(client)
        parameters = self.client.module.params

        self.state: t.Literal["absent", "present", "stopped", "restarted"] = parameters[
            "state"
        ]
        self.dependencies: bool = parameters["dependencies"]
        self.pull: t.Literal["always", "missing", "never", "policy"] = parameters[
            "pull"
        ]
        self.build: t.Literal["always", "never", "policy"] = parameters["build"]
        self.ignore_build_events: bool = parameters["ignore_build_events"]
        self.recreate: t.Literal["always", "never", "auto"] = parameters["recreate"]
        self.remove_images: t.Literal["all", "local"] | None = parameters[
            "remove_images"
        ]
        self.remove_volumes: bool = parameters["remove_volumes"]
        self.remove_orphans: bool = parameters["remove_orphans"]
        self.renew_anon_volumes: bool = parameters["renew_anon_volumes"]
        self.timeout: int | None = parameters["timeout"]
        self.services: list[str] = parameters["services"] or []
        self.scale: dict[str, t.Any] = parameters["scale"] or {}
        self.wait: bool = parameters["wait"]
        self.wait_timeout: int | None = parameters["wait_timeout"]
        self.yes: bool = parameters["assume_yes"]
        if self.compose_version < LooseVersion("2.32.0") and self.yes:
            self.fail(
                f"assume_yes=true needs Docker Compose 2.32.0 or newer, not version {self.compose_version}"
            )

        for key, value in self.scale.items():
            if not isinstance(key, str):
                self.fail(f"The key {key!r} for `scale` is not a string")
            try:
                value = check_type_int(value)
            except TypeError:
                self.fail(f"The value {value!r} for `scale[{key!r}]` is not an integer")
            if value < 0:
                self.fail(f"The value {value!r} for `scale[{key!r}]` is negative")
            self.scale[key] = value

    def run(self) -> dict[str, t.Any]:
        if self.state == "present":
            result = self.cmd_up()
        elif self.state == "stopped":
            result = self.cmd_stop()
        elif self.state == "restarted":
            result = self.cmd_restart()
        elif self.state == "absent":
            result = self.cmd_down()
        else:
            raise AssertionError("Unexpected state")

        result["containers"] = self.list_containers()
        result["images"] = self.list_images()
        self.cleanup_result(result)
        return result

    def get_up_cmd(self, dry_run: bool, no_start: bool = False) -> list[str]:
        args = self.get_base_args() + ["up", "--detach", "--no-color", "--quiet-pull"]
        if self.pull != "policy":
            args.extend(["--pull", self.pull])
        if self.remove_orphans:
            args.append("--remove-orphans")
        if self.recreate == "always":
            args.append("--force-recreate")
        if self.recreate == "never":
            args.append("--no-recreate")
        if self.renew_anon_volumes:
            args.append("--renew-anon-volumes")
        if not self.dependencies:
            args.append("--no-deps")
        if self.timeout is not None:
            args.extend(["--timeout", f"{self.timeout}"])
        if self.build == "always":
            args.append("--build")
        elif self.build == "never":
            args.append("--no-build")
        for key, value in sorted(self.scale.items()):
            args.extend(["--scale", f"{key}={value}"])
        if self.wait:
            args.append("--wait")
            if self.wait_timeout is not None:
                args.extend(["--wait-timeout", str(self.wait_timeout)])
        if no_start:
            args.append("--no-start")
        if dry_run:
            args.append("--dry-run")
        if self.yes:
            # Note that for Docker Compose 2.32.x and 2.33.x, the long form is '--y' and not '--yes'.
            # This was fixed in Docker Compose 2.34.0 (https://github.com/docker/compose/releases/tag/v2.34.0).
            args.append(
                "-y" if self.compose_version < LooseVersion("2.34.0") else "--yes"
            )
        args.append("--")
        for service in self.services:
            args.append(service)
        return args

    def cmd_up(self) -> dict[str, t.Any]:
        result: dict[str, t.Any] = {}
        args = self.get_up_cmd(self.check_mode)
        rc, stdout, stderr = self.client.call_cli(*args, cwd=self.project_src)
        events = self.parse_events(stderr, dry_run=self.check_mode, nonzero_rc=rc != 0)
        self.emit_warnings(events)
        self.update_result(
            result,
            events,
            stdout,
            stderr,
            ignore_service_pull_events=True,
            ignore_build_events=self.ignore_build_events,
        )
        self.update_failed(result, events, args, stdout, stderr, rc)
        return result

    def get_stop_cmd(self, dry_run: bool) -> list[str]:
        args = self.get_base_args() + ["stop"]
        if self.timeout is not None:
            args.extend(["--timeout", f"{self.timeout}"])
        if dry_run:
            args.append("--dry-run")
        args.append("--")
        for service in self.services:
            args.append(service)
        return args

    def _are_containers_stopped(self) -> bool:
        return all(
            container["State"] in ("created", "exited", "stopped", "killed")
            for container in self.list_containers_raw()
        )

    def cmd_stop(self) -> dict[str, t.Any]:
        # Since 'docker compose stop' **always** claims it is stopping containers, even if they are already
        # stopped, we have to do this a bit more complicated.

        result: dict[str, t.Any] = {}
        # Make sure all containers are created
        args_1 = self.get_up_cmd(self.check_mode, no_start=True)
        rc_1, stdout_1, stderr_1 = self.client.call_cli(*args_1, cwd=self.project_src)
        events_1 = self.parse_events(
            stderr_1, dry_run=self.check_mode, nonzero_rc=rc_1 != 0
        )
        self.emit_warnings(events_1)
        self.update_result(
            result,
            events_1,
            stdout_1,
            stderr_1,
            ignore_service_pull_events=True,
            ignore_build_events=self.ignore_build_events,
        )
        is_failed_1 = is_failed(events_1, rc_1)
        if not is_failed_1 and not self._are_containers_stopped():
            # Make sure all containers are stopped
            args_2 = self.get_stop_cmd(self.check_mode)
            rc_2, stdout_2, stderr_2 = self.client.call_cli(
                *args_2, cwd=self.project_src
            )
            events_2 = self.parse_events(
                stderr_2, dry_run=self.check_mode, nonzero_rc=rc_2 != 0
            )
            self.emit_warnings(events_2)
            self.update_result(result, events_2, stdout_2, stderr_2)
        else:
            args_2 = []
            rc_2, stdout_2, stderr_2 = 0, b"", b""
            events_2 = []
        # Compose result
        self.update_failed(
            result,
            events_1 + events_2,
            args_1 if is_failed_1 else args_2,
            stdout_1 if is_failed_1 else stdout_2,
            stderr_1 if is_failed_1 else stderr_2,
            rc_1 if is_failed_1 else rc_2,
        )
        return result

    def get_restart_cmd(self, dry_run: bool) -> list[str]:
        args = self.get_base_args() + ["restart"]
        if not self.dependencies:
            args.append("--no-deps")
        if self.timeout is not None:
            args.extend(["--timeout", f"{self.timeout}"])
        if dry_run:
            args.append("--dry-run")
        args.append("--")
        for service in self.services:
            args.append(service)
        return args

    def cmd_restart(self) -> dict[str, t.Any]:
        result: dict[str, t.Any] = {}
        args = self.get_restart_cmd(self.check_mode)
        rc, stdout, stderr = self.client.call_cli(*args, cwd=self.project_src)
        events = self.parse_events(stderr, dry_run=self.check_mode, nonzero_rc=rc != 0)
        self.emit_warnings(events)
        self.update_result(result, events, stdout, stderr)
        self.update_failed(result, events, args, stdout, stderr, rc)
        return result

    def get_down_cmd(self, dry_run: bool) -> list[str]:
        args = self.get_base_args() + ["down"]
        if self.remove_orphans:
            args.append("--remove-orphans")
        if self.remove_images:
            args.extend(["--rmi", self.remove_images])
        if self.remove_volumes:
            args.append("--volumes")
        if self.timeout is not None:
            args.extend(["--timeout", f"{self.timeout}"])
        if dry_run:
            args.append("--dry-run")
        args.append("--")
        for service in self.services:
            args.append(service)
        return args

    def cmd_down(self) -> dict[str, t.Any]:
        result: dict[str, t.Any] = {}
        args = self.get_down_cmd(self.check_mode)
        rc, stdout, stderr = self.client.call_cli(*args, cwd=self.project_src)
        events = self.parse_events(stderr, dry_run=self.check_mode, nonzero_rc=rc != 0)
        self.emit_warnings(events)
        self.update_result(result, events, stdout, stderr)
        self.update_failed(result, events, args, stdout, stderr, rc)
        return result


def main() -> None:
    argument_spec = {
        "state": {
            "type": "str",
            "default": "present",
            "choices": ["absent", "present", "stopped", "restarted"],
        },
        "dependencies": {"type": "bool", "default": True},
        "pull": {
            "type": "str",
            "choices": ["always", "missing", "never", "policy"],
            "default": "policy",
        },
        "build": {
            "type": "str",
            "choices": ["always", "never", "policy"],
            "default": "policy",
        },
        "recreate": {
            "type": "str",
            "default": "auto",
            "choices": ["always", "never", "auto"],
        },
        "renew_anon_volumes": {"type": "bool", "default": False},
        "remove_images": {"type": "str", "choices": ["all", "local"]},
        "remove_volumes": {"type": "bool", "default": False},
        "remove_orphans": {"type": "bool", "default": False},
        "timeout": {"type": "int"},
        "services": {"type": "list", "elements": "str"},
        "scale": {"type": "dict"},
        "wait": {"type": "bool", "default": False},
        "wait_timeout": {"type": "int"},
        "ignore_build_events": {"type": "bool", "default": True},
        "assume_yes": {"type": "bool", "default": False},
    }
    argspec_ex = common_compose_argspec_ex()
    argument_spec.update(argspec_ex.pop("argspec"))

    client = AnsibleModuleDockerClient(
        argument_spec=argument_spec,
        supports_check_mode=True,
        needs_api_version=False,
        **argspec_ex,
    )

    try:
        manager = ServicesManager(client)
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
