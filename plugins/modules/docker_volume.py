#!/usr/bin/python
#
# Copyright 2017 Red Hat | Ansible, Alex Grönholm <alex.gronholm@nextday.fi>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations


DOCUMENTATION = r"""
module: docker_volume
short_description: Manage Docker volumes
description:
  - Create/remove Docker volumes.
  - Performs largely the same function as the C(docker volume) CLI subcommand.
extends_documentation_fragment:
  - community.docker._docker.api_documentation
  - community.docker._attributes
  - community.docker._attributes.actiongroup_docker

attributes:
  check_mode:
    support: full
  diff_mode:
    support: full
  idempotent:
    support: partial
    details:
      - If O(recreate=always) the module is not idempotent.

options:
  volume_name:
    description:
      - Name of the volume to operate on.
    type: str
    required: true
    aliases:
      - name

  driver:
    description:
      - Specify the type of volume. Docker provides the V(local) driver, but 3rd party drivers can also be used.
    type: str
    default: local

  driver_options:
    description:
      - 'Dictionary of volume settings. Consult the Docker documentation for valid options and values:
        U(https://docs.docker.com/engine/reference/commandline/volume_create/#driver-specific-options).'
    type: dict
    default: {}

  labels:
    description:
      - Dictionary of label key/values to set for the volume.
    type: dict

  recreate:
    description:
      - Controls when a volume will be recreated when O(state=present). Please note that recreating an existing volume will
        cause B(any data in the existing volume to be lost!) The volume will be deleted and a new volume with the same name
        will be created.
      - The value V(always) forces the volume to be always recreated.
      - The value V(never) makes sure the volume will not be recreated.
      - The value V(options-changed) makes sure the volume will be recreated if the volume already exist and the driver, driver
        options or labels differ.
    type: str
    default: never
    choices:
      - always
      - never
      - options-changed

  state:
    description:
      - V(absent) deletes the volume.
      - V(present) creates the volume, if it does not already exist.
    type: str
    default: present
    choices:
      - absent
      - present

author:
  - Alex Grönholm (@agronholm)

requirements:
  - "Docker API >= 1.25"
"""

EXAMPLES = r"""
---
- name: Create a volume
  community.docker.docker_volume:
    name: volume_one

- name: Remove a volume
  community.docker.docker_volume:
    name: volume_one
    state: absent

- name: Create a volume with options
  community.docker.docker_volume:
    name: volume_two
    driver_options:
      type: btrfs
      device: /dev/sda2
"""

RETURN = r"""
volume:
  description:
    - Volume inspection results for the affected volume.
  returned: success
  type: dict
  sample: {}
"""

import traceback
import typing as t

from ansible.module_utils.common.text.converters import to_text

from ansible_collections.community.docker.plugins.module_utils._api.errors import (
    APIError,
    DockerException,
)
from ansible_collections.community.docker.plugins.module_utils._common_api import (
    AnsibleDockerClient,
    RequestException,
)
from ansible_collections.community.docker.plugins.module_utils._util import (
    DifferenceTracker,
    DockerBaseClass,
    sanitize_labels,
)


class TaskParameters(DockerBaseClass):
    volume_name: str

    def __init__(self, client: AnsibleDockerClient) -> None:
        super().__init__()
        self.client = client

        self.driver: str = "local"
        self.driver_options: dict[str, t.Any] = {}
        self.labels: dict[str, t.Any] | None = None
        self.recreate: t.Literal["always", "never", "options-changed"] = "never"
        self.debug: bool = False
        self.state: t.Literal["present", "absent"] = "present"

        for key, value in client.module.params.items():
            setattr(self, key, value)


class DockerVolumeManager:
    def __init__(self, client: AnsibleDockerClient) -> None:
        self.client = client
        self.parameters = TaskParameters(client)
        self.check_mode = self.client.check_mode
        self.actions: list[str] = []
        self.results: dict[str, t.Any] = {"changed": False, "actions": self.actions}
        self.diff = self.client.module._diff
        self.diff_tracker = DifferenceTracker()
        self.diff_result: dict[str, t.Any] = {}

        self.existing_volume = self.get_existing_volume()

        state = self.parameters.state
        if state == "present":
            self.present()
        elif state == "absent":
            self.absent()

        if self.diff or self.check_mode or self.parameters.debug:
            if self.diff:
                self.diff_result["before"], self.diff_result["after"] = (
                    self.diff_tracker.get_before_after()
                )
            self.results["diff"] = self.diff_result

    def get_existing_volume(self) -> dict[str, t.Any] | None:
        try:
            volumes = self.client.get_json("/volumes")
        except APIError as e:
            self.client.fail(to_text(e))

        if volumes["Volumes"] is None:
            return None

        for volume in volumes["Volumes"]:
            if volume["Name"] == self.parameters.volume_name:
                return volume

        return None

    def has_different_config(self) -> DifferenceTracker:
        """
        Return the list of differences between the current parameters and the existing volume.

        :return: list of options that differ
        """
        assert self.existing_volume is not None
        differences = DifferenceTracker()
        if (
            self.parameters.driver
            and self.parameters.driver != self.existing_volume["Driver"]
        ):
            differences.add(
                "driver",
                parameter=self.parameters.driver,
                active=self.existing_volume["Driver"],
            )
        if self.parameters.driver_options:
            if not self.existing_volume.get("Options"):
                differences.add(
                    "driver_options",
                    parameter=self.parameters.driver_options,
                    active=self.existing_volume.get("Options"),
                )
            else:
                for key, value in self.parameters.driver_options.items():
                    if (
                        not self.existing_volume["Options"].get(key)
                        or value != self.existing_volume["Options"][key]
                    ):
                        differences.add(
                            f"driver_options.{key}",
                            parameter=value,
                            active=self.existing_volume["Options"].get(key),
                        )
        if self.parameters.labels:
            existing_labels = self.existing_volume.get("Labels") or {}
            for label in self.parameters.labels:
                if existing_labels.get(label) != self.parameters.labels.get(label):
                    differences.add(
                        f"labels.{label}",
                        parameter=self.parameters.labels.get(label),
                        active=existing_labels.get(label),
                    )

        return differences

    def create_volume(self) -> None:
        if not self.existing_volume:
            if not self.check_mode:
                try:
                    data = {
                        "Name": self.parameters.volume_name,
                        "Driver": self.parameters.driver,
                        "DriverOpts": self.parameters.driver_options,
                    }
                    if self.parameters.labels is not None:
                        data["Labels"] = self.parameters.labels
                    resp = self.client.post_json_to_json("/volumes/create", data=data)
                    self.existing_volume = self.client.get_json(
                        "/volumes/{0}", resp["Name"]
                    )
                except APIError as e:
                    self.client.fail(to_text(e))

            self.actions.append(
                f"Created volume {self.parameters.volume_name} with driver {self.parameters.driver}"
            )
            self.results["changed"] = True

    def remove_volume(self) -> None:
        if self.existing_volume:
            if not self.check_mode:
                try:
                    self.client.delete_call("/volumes/{0}", self.parameters.volume_name)
                except APIError as e:
                    self.client.fail(to_text(e))

            self.actions.append(f"Removed volume {self.parameters.volume_name}")
            self.results["changed"] = True

    def present(self) -> None:
        differences = DifferenceTracker()
        if self.existing_volume:
            differences = self.has_different_config()

        self.diff_tracker.add(
            "exists", parameter=True, active=self.existing_volume is not None
        )
        if (
            not differences.empty and self.parameters.recreate == "options-changed"
        ) or self.parameters.recreate == "always":
            self.remove_volume()
            self.existing_volume = None

        self.create_volume()

        if self.diff or self.check_mode or self.parameters.debug:
            self.diff_result["differences"] = differences.get_legacy_docker_diffs()
            self.diff_tracker.merge(differences)

        if not self.check_mode and not self.parameters.debug:
            self.results.pop("actions")

        volume_facts = self.get_existing_volume()
        self.results["volume"] = volume_facts

    def absent(self) -> None:
        self.diff_tracker.add(
            "exists", parameter=False, active=self.existing_volume is not None
        )
        self.remove_volume()


def main() -> None:
    argument_spec = {
        "volume_name": {"type": "str", "required": True, "aliases": ["name"]},
        "state": {
            "type": "str",
            "default": "present",
            "choices": ["present", "absent"],
        },
        "driver": {"type": "str", "default": "local"},
        "driver_options": {"type": "dict", "default": {}},
        "labels": {"type": "dict"},
        "recreate": {
            "type": "str",
            "default": "never",
            "choices": ["always", "never", "options-changed"],
        },
        "debug": {"type": "bool", "default": False},
    }

    client = AnsibleDockerClient(
        argument_spec=argument_spec,
        supports_check_mode=True,
        # "The docker server >= 1.9.0"
    )
    sanitize_labels(client.module.params["labels"], "labels", client)

    try:
        cm = DockerVolumeManager(client)
        client.module.exit_json(**cm.results)
    except DockerException as e:
        client.fail(
            f"An unexpected Docker error occurred: {e}",
            exception=traceback.format_exc(),
        )
    except RequestException as e:
        client.fail(
            f"An unexpected requests error occurred when trying to talk to the Docker daemon: {e}",
            exception=traceback.format_exc(),
        )


if __name__ == "__main__":
    main()
