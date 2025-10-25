# Copyright (c) 2019, Ximon Eighteen <ximon.eighteen@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations


DOCUMENTATION = r"""
name: docker_machine
author: Ximon Eighteen (@ximon18)
short_description: Docker Machine inventory source
requirements:
  - L(Docker Machine,https://docs.docker.com/machine/)
extends_documentation_fragment:
  - ansible.builtin.constructed
  - community.library_inventory_filtering_v1.inventory_filter
description:
  - Get inventory hosts from Docker Machine.
  - Uses a YAML configuration file that ends with V(docker_machine.(yml|yaml\)).
  - The plugin sets standard host variables C(ansible_host), C(ansible_port), C(ansible_user) and C(ansible_ssh_private_key).
  - The plugin stores the Docker Machine 'env' output variables in C(dm_) prefixed host variables.
notes:
  - The configuration file must be a YAML file whose filename ends with V(docker_machine.yml) or V(docker_machine.yaml). Other
    filenames will not be accepted.
options:
  plugin:
    description: Token that ensures this is a source file for the C(docker_machine) plugin.
    required: true
    choices: ['docker_machine', 'community.docker.docker_machine']
  daemon_env:
    description:
      - Whether docker daemon connection environment variables should be fetched, and how to behave if they cannot be fetched.
      - With V(require) and V(require-silently), fetch them and skip any host for which they cannot be fetched. A warning
        will be issued for any skipped host if the choice is V(require).
      - With V(optional) and V(optional-silently), fetch them and not skip hosts for which they cannot be fetched. A warning
        will be issued for hosts where they cannot be fetched if the choice is V(optional).
      - With V(skip), do not attempt to fetch the docker daemon connection environment variables.
      - If fetched successfully, the variables will be prefixed with C(dm_) and stored as host variables.
    type: str
    choices:
      - require
      - require-silently
      - optional
      - optional-silently
      - skip
    default: require
  running_required:
    description:
      - When V(true), hosts which Docker Machine indicates are in a state other than C(running) will be skipped.
    type: bool
    default: true
  verbose_output:
    description:
      - When V(true), include all available nodes metadata (for example C(Image), C(Region), C(Size)) as a JSON object named
        C(docker_machine_node_attributes).
    type: bool
    default: true
  filters:
    version_added: 3.5.0
"""

EXAMPLES = """
---
# Minimal example
plugin: community.docker.docker_machine

---
# Example using constructed features to create a group per Docker Machine driver
# (https://docs.docker.com/machine/drivers/), for example:
#   $ docker-machine create --driver digitalocean ... mymachine
#   $ ansible-inventory -i ./path/to/docker-machine.yml --host=mymachine
#   {
#     ...
#     "digitalocean": {
#       "hosts": [
#           "mymachine"
#       ]
#     ...
#   }
plugin: community.docker.docker_machine
strict: false
keyed_groups:
  - separator: ''
    key: docker_machine_node_attributes.DriverName

---
# Example grouping hosts by Digital Machine tag
plugin: community.docker.docker_machine
strict: false
keyed_groups:
  - prefix: tag
    key: 'dm_tags'

---
# Example using compose to override the default SSH behaviour of asking the user to accept the remote host key
plugin: community.docker.docker_machine
compose:
  ansible_ssh_common_args: '"-o StrictHostKeyChecking=accept-new"'
"""

import json
import re
import subprocess
import typing as t

from ansible.errors import AnsibleError
from ansible.module_utils.common.process import get_bin_path
from ansible.module_utils.common.text.converters import to_text
from ansible.plugins.inventory import BaseInventoryPlugin, Cacheable, Constructable
from ansible.utils.display import Display
from ansible_collections.community.library_inventory_filtering_v1.plugins.plugin_utils.inventory_filter import (
    filter_host,
    parse_filters,
)

from ansible_collections.community.docker.plugins.plugin_utils._unsafe import (
    make_unsafe,
)


if t.TYPE_CHECKING:
    from ansible.inventory.data import InventoryData
    from ansible.parsing.dataloader import DataLoader

    DaemonEnv = t.Literal[
        "require", "require-silently", "optional", "optional-silently", "skip"
    ]


display = Display()


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):
    """Host inventory parser for ansible using Docker machine as source."""

    NAME = "community.docker.docker_machine"

    docker_machine_path: str | None = None

    def _run_command(self, args: list[str]) -> str:
        if not self.docker_machine_path:
            try:
                self.docker_machine_path = get_bin_path("docker-machine")
            except ValueError as e:
                raise AnsibleError(to_text(e)) from e

        command = [self.docker_machine_path]
        command.extend(args)
        display.debug(f"Executing command {command}")
        try:
            result = subprocess.check_output(command)
        except subprocess.CalledProcessError as e:
            display.warning(
                f"Exception {type(e).__name__} caught while executing command {command}, this was the original exception: {e}"
            )
            raise e

        return to_text(result).strip()

    def _get_docker_daemon_variables(self, machine_name: str) -> list[tuple[str, str]]:
        """
        Capture settings from Docker Machine that would be needed to connect to the remote Docker daemon installed on
        the Docker Machine remote host. Note: passing '--shell=sh' is a workaround for 'Error: Unknown shell'.
        """
        try:
            env_lines = self._run_command(
                ["env", "--shell=sh", machine_name]
            ).splitlines()
        except subprocess.CalledProcessError:
            # This can happen when the machine is created but provisioning is incomplete
            return []

        # example output of docker-machine env --shell=sh:
        #   export DOCKER_TLS_VERIFY="1"
        #   export DOCKER_HOST="tcp://134.209.204.160:2376"
        #   export DOCKER_CERT_PATH="/root/.docker/machine/machines/routinator"
        #   export DOCKER_MACHINE_NAME="routinator"
        #   # Run this command to configure your shell:
        #   # eval $(docker-machine env --shell=bash routinator)

        # capture any of the DOCKER_xxx variables that were output and create Ansible host vars
        # with the same name and value but with a dm_ name prefix.
        env_vars = []
        for line in env_lines:
            match = re.search('(DOCKER_[^=]+)="([^"]+)"', line)
            if match:
                env_var_name = match.group(1)
                env_var_value = match.group(2)
                env_vars.append((env_var_name, env_var_value))

        return env_vars

    def _get_machine_names(self) -> list[str]:
        # Filter out machines that are not in the Running state as we probably cannot do anything useful actions
        # with them.
        ls_command = ["ls", "-q"]
        if self.get_option("running_required"):
            ls_command.extend(["--filter", "state=Running"])

        try:
            ls_lines = self._run_command(ls_command)
        except subprocess.CalledProcessError:
            return []

        return ls_lines.splitlines()

    def _inspect_docker_machine_host(self, node: str) -> t.Any | None:
        try:
            inspect_lines = self._run_command(["inspect", node])
        except subprocess.CalledProcessError:
            return None

        return json.loads(inspect_lines)

    def _ip_addr_docker_machine_host(self, node: str) -> t.Any | None:
        try:
            ip_addr = self._run_command(["ip", node])
        except subprocess.CalledProcessError:
            return None

        return ip_addr

    def _should_skip_host(
        self,
        machine_name: str,
        env_var_tuples: list[tuple[str, str]],
        daemon_env: DaemonEnv,
    ) -> bool:
        if not env_var_tuples:
            warning_prefix = f"Unable to fetch Docker daemon env vars from Docker Machine for host {machine_name}"
            if daemon_env in ("require", "require-silently"):
                if daemon_env == "require":
                    display.warning(f"{warning_prefix}: host will be skipped")
                return True
            if daemon_env == "optional":
                display.warning(
                    f"{warning_prefix}: host will lack dm_DOCKER_xxx variables"
                )
            # daemon_env is 'optional-silently'
        return False

    def _populate(self) -> None:
        if self.inventory is None:
            raise AssertionError("Inventory must be there")

        daemon_env: DaemonEnv = self.get_option("daemon_env")
        filters = parse_filters(self.get_option("filters"))
        try:
            for node in self._get_machine_names():
                node_attrs = self._inspect_docker_machine_host(node)
                if not node_attrs:
                    continue

                unsafe_node_attrs = make_unsafe(node_attrs)

                machine_name = unsafe_node_attrs["Driver"]["MachineName"]
                if not filter_host(self, machine_name, unsafe_node_attrs, filters):
                    continue

                # query `docker-machine env` to obtain remote Docker daemon connection settings in the form of commands
                # that could be used to set environment variables to influence a local Docker client:
                if daemon_env == "skip":
                    env_var_tuples = []
                else:
                    env_var_tuples = self._get_docker_daemon_variables(machine_name)
                    if self._should_skip_host(machine_name, env_var_tuples, daemon_env):
                        continue

                # add an entry in the inventory for this host
                self.inventory.add_host(machine_name)

                # check for valid ip address from inspect output, else explicitly use ip command to find host ip address
                # this works around an issue seen with Google Compute Platform where the IP address was not available
                # via the 'inspect' subcommand but was via the 'ip' subcomannd.
                if unsafe_node_attrs["Driver"]["IPAddress"]:
                    ip_addr = unsafe_node_attrs["Driver"]["IPAddress"]
                else:
                    ip_addr = self._ip_addr_docker_machine_host(node)

                # set standard Ansible remote host connection settings to details captured from `docker-machine`
                # see: https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html
                self.inventory.set_variable(
                    machine_name, "ansible_host", make_unsafe(ip_addr)
                )
                self.inventory.set_variable(
                    machine_name, "ansible_port", unsafe_node_attrs["Driver"]["SSHPort"]
                )
                self.inventory.set_variable(
                    machine_name, "ansible_user", unsafe_node_attrs["Driver"]["SSHUser"]
                )
                self.inventory.set_variable(
                    machine_name,
                    "ansible_ssh_private_key_file",
                    unsafe_node_attrs["Driver"]["SSHKeyPath"],
                )

                # set variables based on Docker Machine tags
                tags = unsafe_node_attrs["Driver"].get("Tags") or ""
                self.inventory.set_variable(machine_name, "dm_tags", make_unsafe(tags))

                # set variables based on Docker Machine env variables
                for kv in env_var_tuples:
                    self.inventory.set_variable(
                        machine_name, f"dm_{kv[0]}", make_unsafe(kv[1])
                    )

                if self.get_option("verbose_output"):
                    self.inventory.set_variable(
                        machine_name,
                        "docker_machine_node_attributes",
                        unsafe_node_attrs,
                    )

                # Use constructed if applicable
                strict = self.get_option("strict")

                # Composed variables
                self._set_composite_vars(
                    self.get_option("compose"),
                    unsafe_node_attrs,
                    machine_name,
                    strict=strict,
                )

                # Complex groups based on jinja2 conditionals, hosts that meet the conditional are added to group
                self._add_host_to_composed_groups(
                    self.get_option("groups"),
                    unsafe_node_attrs,
                    machine_name,
                    strict=strict,
                )

                # Create groups based on variable values and add the corresponding hosts to it
                self._add_host_to_keyed_groups(
                    self.get_option("keyed_groups"),
                    unsafe_node_attrs,
                    machine_name,
                    strict=strict,
                )

        except Exception as e:
            raise AnsibleError(
                f"Unable to fetch hosts from Docker Machine, this was the original exception: {e}"
            ) from e

    def verify_file(self, path: str) -> bool:
        """Return the possibility of a file being consumable by this plugin."""
        return super().verify_file(path) and path.endswith(
            ("docker_machine.yaml", "docker_machine.yml")
        )

    def parse(
        self,
        inventory: InventoryData,
        loader: DataLoader,
        path: str,
        cache: bool = True,
    ) -> None:
        super().parse(inventory, loader, path, cache)
        self._read_config_data(path)
        self._populate()
