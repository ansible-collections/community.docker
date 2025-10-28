#!/usr/bin/python
#
# Copyright 2016 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations


DOCUMENTATION = r"""
module: docker_network
short_description: Manage Docker networks
description:
  - Create/remove Docker networks and connect containers to them.
  - Performs largely the same function as the C(docker network) CLI subcommand.
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
      - If O(force=true) the module is not idempotent.

options:
  name:
    description:
      - Name of the network to operate on.
    type: str
    required: true
    aliases:
      - network_name

  config_from:
    description:
      - Specifies the config only network to use the config from.
    type: str
    version_added: 3.10.0

  config_only:
    description:
      - Sets that this is a config only network.
    type: bool
    version_added: 3.10.0

  connected:
    description:
      - List of container names or container IDs to connect to a network.
      - Please note that the module only makes sure that these containers are connected to the network, but does not care
        about connection options. If you rely on specific IP addresses and so on, use the M(community.docker.docker_container)
        module to ensure your containers are correctly connected to this network.
    type: list
    elements: str
    default: []
    aliases:
      - containers

  driver:
    description:
      - Specify the type of network. Docker provides bridge and overlay drivers, but 3rd party drivers can also be used.
    type: str
    default: bridge

  driver_options:
    description:
      - Dictionary of network settings. Consult docker docs for valid options and values.
    type: dict
    default: {}

  force:
    description:
      - With state V(present) will disconnect all containers for existing networks, delete the network and re-create the network.
      - This option is required if you have changed the IPAM or driver options and want an existing network to be updated
        to use the new options.
    type: bool
    default: false

  appends:
    description:
      - By default the connected list is canonical, meaning containers not on the list are removed from the network.
      - Use O(appends) to leave existing containers connected.
    type: bool
    default: false
    aliases:
      - incremental

  enable_ipv4:
    description:
      - Enable IPv4 networking.
      - This is enabled by default, but can be explicitly disabled.
      - Requires Docker API 1.47 or newer.
    type: bool
    version_added: 4.5.0

  enable_ipv6:
    description:
      - Enable IPv6 networking.
    type: bool

  ingress:
    description:
      - Enable Swarm routing-mesh.
    type: bool
    version_added: 4.2.0

  ipam_driver:
    description:
      - Specify an IPAM driver.
    type: str

  ipam_driver_options:
    description:
      - Dictionary of IPAM driver options.
    type: dict

  ipam_config:
    description:
      - List of IPAM config blocks. Consult L(Docker docs,https://docs.docker.com/compose/compose-file/compose-file-v2/#ipam)
        for valid options and values. Note that O(ipam_config[].iprange) is spelled differently here (we use the notation
        from the Docker SDK for Python).
    type: list
    elements: dict
    suboptions:
      subnet:
        description:
          - IP subset in CIDR notation.
        type: str
      iprange:
        description:
          - IP address range in CIDR notation.
        type: str
      gateway:
        description:
          - IP gateway address.
        type: str
      aux_addresses:
        description:
          - Auxiliary IP addresses used by Network driver, as a mapping from hostname to IP.
        type: dict

  state:
    description:
      - V(absent) deletes the network. If a network has connected containers, these will be detached from the network.
      - V(present) creates the network, if it does not already exist with the specified parameters, and connects the list
        of containers provided by the O(connected) parameter. Containers not on the list will be disconnected. An empty list
        will leave no containers connected to the network. Use the O(appends) option to leave existing containers connected.
        Use the O(force) options to force re-creation of the network.
    type: str
    default: present
    choices:
      - absent
      - present

  internal:
    description:
      - Restrict external access to the network.
    type: bool

  labels:
    description:
      - Dictionary of labels.
    type: dict
    default: {}

  scope:
    description:
      - Specify the network's scope.
    type: str
    choices:
      - local
      - global
      - swarm

  attachable:
    description:
      - If enabled, and the network is in the global scope, non-service containers on worker nodes will be able to connect
        to the network.
    type: bool

notes:
  - When network options are changed, the module disconnects all containers from the network, deletes the network, and re-creates
    the network. It does not try to reconnect containers, except the ones listed in (O(connected), and even for these, it
    does not consider specific connection options like fixed IP addresses or MAC addresses. If you need more control over
    how the containers are connected to the network, loop the M(community.docker.docker_container) module to loop over your
    containers to make sure they are connected properly.
  - The module does not support Docker Swarm. This means that it will not try to disconnect or reconnect services. If services
    are connected to the network, deleting the network will fail. When network options are changed, the network has to be
    deleted and recreated, so this will fail as well.
author:
  - "Ben Keith (@keitwb)"
  - "Chris Houseknecht (@chouseknecht)"
  - "Dave Bendit (@DBendit)"

requirements:
  - "Docker API >= 1.25"
"""

EXAMPLES = r"""
---
- name: Create a network
  community.docker.docker_network:
    name: network_one

- name: Remove all but selected list of containers
  community.docker.docker_network:
    name: network_one
    connected:
      - container_a
      - container_b
      - container_c

- name: Remove a single container
  community.docker.docker_network:
    name: network_one
    connected: "{{ fulllist|difference(['container_a']) }}"

- name: Add a container to a network, leaving existing containers connected
  community.docker.docker_network:
    name: network_one
    connected:
      - container_a
    appends: true

- name: Create a network with driver options
  community.docker.docker_network:
    name: network_two
    driver_options:
      com.docker.network.bridge.name: net2

- name: Create a network with custom IPAM config
  community.docker.docker_network:
    name: network_three
    ipam_config:
      - subnet: 172.23.27.0/24
        gateway: 172.23.27.2
        iprange: 172.23.27.0/26
        aux_addresses:
          host1: 172.23.27.3
          host2: 172.23.27.4

- name: Create a network with labels
  community.docker.docker_network:
    name: network_four
    labels:
      key1: value1
      key2: value2

- name: Create a network with IPv6 IPAM config
  community.docker.docker_network:
    name: network_ipv6_one
    enable_ipv6: true
    ipam_config:
      - subnet: fdd1:ac8c:0557:7ce1::/64

- name: Create a network with IPv6 and custom IPv4 IPAM config
  community.docker.docker_network:
    name: network_ipv6_two
    enable_ipv6: true
    ipam_config:
      - subnet: 172.24.27.0/24
      - subnet: fdd1:ac8c:0557:7ce2::/64

- name: Delete a network, disconnecting all containers
  community.docker.docker_network:
    name: network_one
    state: absent
"""

RETURN = r"""
network:
  description:
    - Network inspection results for the affected network.
  returned: success
  type: dict
  sample: {}
"""

import re
import time
import traceback
import typing as t

from ansible.module_utils.common.text.converters import to_text

from ansible_collections.community.docker.plugins.module_utils._api.errors import (
    DockerException,
)
from ansible_collections.community.docker.plugins.module_utils._common_api import (
    AnsibleDockerClient,
    RequestException,
)
from ansible_collections.community.docker.plugins.module_utils._util import (
    DifferenceTracker,
    DockerBaseClass,
    clean_dict_booleans_for_docker_api,
    sanitize_labels,
)


class TaskParameters(DockerBaseClass):
    name: str

    def __init__(self, client: AnsibleDockerClient) -> None:
        super().__init__()
        self.client = client

        self.connected: list[str] = []
        self.config_from: str | None = None
        self.config_only: bool | None = None
        self.driver: str = "bridge"
        self.driver_options: dict[str, t.Any] = {}
        self.ipam_driver: str | None = None
        self.ipam_driver_options: dict[str, t.Any] | None = None
        self.ipam_config: list[dict[str, t.Any]] | None = None
        self.appends: bool = False
        self.force: bool = False
        self.internal: bool | None = None
        self.labels: dict[str, t.Any] = {}
        self.debug: bool = False
        self.enable_ipv4: bool | None = None
        self.enable_ipv6: bool | None = None
        self.scope: t.Literal["local", "global", "swarm"] | None = None
        self.attachable: bool | None = None
        self.ingress: bool | None = None
        self.state: t.Literal["present", "absent"] = "present"

        for key, value in client.module.params.items():
            setattr(self, key, value)

        # config_only sets driver to 'null' (and scope to 'local') so force that here. Otherwise we get
        # diffs of 'null' --> 'bridge' given that the driver option defaults to 'bridge'.
        if self.config_only:
            self.driver = "null"  # type: ignore[unreachable]


def container_names_in_network(network: dict[str, t.Any]) -> list[str]:
    return (
        [c["Name"] for c in network["Containers"].values()]
        if network["Containers"]
        else []
    )


CIDR_IPV4 = re.compile(r"^([0-9]{1,3}\.){3}[0-9]{1,3}/([0-9]|[1-2][0-9]|3[0-2])$")
CIDR_IPV6 = re.compile(r"^[0-9a-fA-F:]+/([0-9]|[1-9][0-9]|1[0-2][0-9])$")


def validate_cidr(cidr: str) -> t.Literal["ipv4", "ipv6"]:
    """Validate CIDR. Return IP version of a CIDR string on success.

    :param cidr: Valid CIDR
    :type cidr: str
    :return: ``ipv4`` or ``ipv6``
    :rtype: str
    :raises ValueError: If ``cidr`` is not a valid CIDR
    """
    if CIDR_IPV4.match(cidr):
        return "ipv4"
    if CIDR_IPV6.match(cidr):
        return "ipv6"
    raise ValueError(f'"{cidr}" is not a valid CIDR')


def normalize_ipam_config_key(key: str) -> str:
    """Normalizes IPAM config keys returned by Docker API to match Ansible keys.

    :param key: Docker API key
    :type key: str
    :return Ansible module key
    :rtype str
    """
    special_cases = {"AuxiliaryAddresses": "aux_addresses"}
    return special_cases.get(key, key.lower())


def dicts_are_essentially_equal(a: dict[str, t.Any], b: dict[str, t.Any]) -> bool:
    """Make sure that a is a subset of b, where None entries of a are ignored."""
    for k, v in a.items():
        if v is None:
            continue
        if b.get(k) != v:
            return False
    return True


class DockerNetworkManager:
    def __init__(self, client: AnsibleDockerClient) -> None:
        self.client = client
        self.parameters = TaskParameters(client)
        self.check_mode = self.client.check_mode
        self.actions: list[str] = []
        self.results: dict[str, t.Any] = {"changed": False, "actions": self.actions}
        self.diff = self.client.module._diff
        self.diff_tracker = DifferenceTracker()
        self.diff_result: dict[str, t.Any] = {}

        self.existing_network = self.get_existing_network()

        if not self.parameters.connected and self.existing_network:
            self.parameters.connected = container_names_in_network(
                self.existing_network
            )

        if self.parameters.ipam_config:
            try:
                for ipam_config in self.parameters.ipam_config:
                    validate_cidr(ipam_config["subnet"])
            except ValueError as e:
                self.client.fail(to_text(e))

        if self.parameters.driver_options:
            self.parameters.driver_options = clean_dict_booleans_for_docker_api(
                self.parameters.driver_options
            )

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

    def get_existing_network(self) -> dict[str, t.Any] | None:
        return self.client.get_network(name=self.parameters.name)

    def has_different_config(
        self, net: dict[str, t.Any]
    ) -> tuple[bool, DifferenceTracker]:
        """
        Evaluates an existing network and returns a tuple containing a boolean
        indicating if the configuration is different and a list of differences.

        :param net: the inspection output for an existing network
        :return: (bool, list)
        """
        differences = DifferenceTracker()
        if (
            self.parameters.config_only is not None
            and self.parameters.config_only != net.get("ConfigOnly", False)
        ):
            differences.add(
                "config_only",
                parameter=self.parameters.config_only,
                active=net.get("ConfigOnly", False),
            )
        if (
            self.parameters.config_from is not None
            and self.parameters.config_from
            != net.get("ConfigFrom", {}).get("Network", "")
        ):
            differences.add(
                "config_from",
                parameter=self.parameters.config_from,
                active=net.get("ConfigFrom", {}).get("Network", ""),
            )
        if self.parameters.driver and self.parameters.driver != net["Driver"]:
            differences.add(
                "driver", parameter=self.parameters.driver, active=net["Driver"]
            )
        if self.parameters.driver_options:
            if not net.get("Options"):
                differences.add(
                    "driver_options",
                    parameter=self.parameters.driver_options,
                    active=net.get("Options"),
                )
            else:
                for key, value in self.parameters.driver_options.items():
                    if key not in net["Options"] or value != net["Options"][key]:
                        differences.add(
                            f"driver_options.{key}",
                            parameter=value,
                            active=net["Options"].get(key),
                        )

        if self.parameters.ipam_driver and (
            not net.get("IPAM") or net["IPAM"]["Driver"] != self.parameters.ipam_driver
        ):
            differences.add(
                "ipam_driver",
                parameter=self.parameters.ipam_driver,
                active=net.get("IPAM"),
            )

        if self.parameters.ipam_driver_options is not None:
            ipam_driver_options = net["IPAM"].get("Options") or {}
            if ipam_driver_options != self.parameters.ipam_driver_options:
                differences.add(
                    "ipam_driver_options",
                    parameter=self.parameters.ipam_driver_options,
                    active=ipam_driver_options,
                )

        if self.parameters.ipam_config is not None and self.parameters.ipam_config:
            if not net.get("IPAM") or not net["IPAM"]["Config"]:
                differences.add(
                    "ipam_config",
                    parameter=self.parameters.ipam_config,
                    active=net.get("IPAM", {}).get("Config"),
                )
            else:
                # Put network's IPAM config into the same format as module's IPAM config
                net_ipam_configs = []
                for net_ipam_config in net["IPAM"]["Config"]:
                    config = {}
                    for k, v in net_ipam_config.items():
                        config[normalize_ipam_config_key(k)] = v
                    net_ipam_configs.append(config)
                # Compare lists of dicts as sets of dicts
                for idx, ipam_config in enumerate(self.parameters.ipam_config):
                    net_config = {}
                    for net_ipam_config in net_ipam_configs:
                        if dicts_are_essentially_equal(ipam_config, net_ipam_config):
                            net_config = net_ipam_config
                            break
                    for key, value in ipam_config.items():
                        if value is None:
                            # due to recursive argument_spec, all keys are always present
                            # (but have default value None if not specified)
                            continue
                        if value != net_config.get(key):
                            differences.add(
                                f"ipam_config[{idx}].{key}",
                                parameter=value,
                                active=net_config.get(key),
                            )

        if (
            self.parameters.enable_ipv4 is not None
            and self.parameters.enable_ipv4 != net.get("EnableIPv4", False)
        ):
            differences.add(
                "enable_ipv4",
                parameter=self.parameters.enable_ipv4,
                active=net.get("EnableIPv4", False),
            )
        if (
            self.parameters.enable_ipv6 is not None
            and self.parameters.enable_ipv6 != net.get("EnableIPv6", False)
        ):
            differences.add(
                "enable_ipv6",
                parameter=self.parameters.enable_ipv6,
                active=net.get("EnableIPv6", False),
            )

        if (
            self.parameters.internal is not None
            and self.parameters.internal != net.get("Internal", False)
        ):
            differences.add(
                "internal",
                parameter=self.parameters.internal,
                active=net.get("Internal"),
            )

        if self.parameters.scope is not None and self.parameters.scope != net.get(
            "Scope"
        ):
            differences.add(
                "scope", parameter=self.parameters.scope, active=net.get("Scope")
            )

        if (
            self.parameters.attachable is not None
            and self.parameters.attachable != net.get("Attachable", False)
        ):
            differences.add(
                "attachable",
                parameter=self.parameters.attachable,
                active=net.get("Attachable"),
            )
        if self.parameters.ingress is not None and self.parameters.ingress != net.get(
            "Ingress", False
        ):
            differences.add(
                "ingress", parameter=self.parameters.ingress, active=net.get("Ingress")
            )
        if self.parameters.labels:
            if not net.get("Labels"):
                differences.add(
                    "labels", parameter=self.parameters.labels, active=net.get("Labels")
                )
            else:
                for key, value in self.parameters.labels.items():
                    if key not in net["Labels"] or value != net["Labels"][key]:
                        differences.add(
                            f"labels.{key}",
                            parameter=value,
                            active=net["Labels"].get(key),
                        )

        return not differences.empty, differences

    def create_network(self) -> None:
        if not self.existing_network:
            data: dict[str, t.Any] = {
                "Name": self.parameters.name,
                "Driver": self.parameters.driver,
                "Options": self.parameters.driver_options,
                "IPAM": None,
                "CheckDuplicate": None,
            }

            if self.parameters.config_only is not None:
                data["ConfigOnly"] = self.parameters.config_only
            if self.parameters.config_from:
                data["ConfigFrom"] = {"Network": self.parameters.config_from}
            if self.parameters.enable_ipv6 is not None:
                data["EnableIPv6"] = self.parameters.enable_ipv6
            if self.parameters.enable_ipv4 is not None:
                data["EnableIPv4"] = self.parameters.enable_ipv4
            if self.parameters.internal:
                data["Internal"] = True
            if self.parameters.scope is not None:
                data["Scope"] = self.parameters.scope
            if self.parameters.attachable is not None:
                data["Attachable"] = self.parameters.attachable
            if self.parameters.ingress is not None:
                data["Ingress"] = self.parameters.ingress
            if self.parameters.labels is not None:
                data["Labels"] = self.parameters.labels

            ipam_pools = []
            if self.parameters.ipam_config:
                for ipam_pool in self.parameters.ipam_config:
                    ipam_pools.append(
                        {
                            "Subnet": ipam_pool["subnet"],
                            "IPRange": ipam_pool["iprange"],
                            "Gateway": ipam_pool["gateway"],
                            "AuxiliaryAddresses": ipam_pool["aux_addresses"],
                        }
                    )

            if (
                self.parameters.ipam_driver
                or self.parameters.ipam_driver_options
                or ipam_pools
            ):
                # Only add IPAM if a driver was specified or if IPAM parameters were
                # specified. Leaving this parameter out can significantly speed up
                # creation; on my machine creation with this option needs ~15 seconds,
                # and without just a few seconds.
                data["IPAM"] = {
                    "Driver": self.parameters.ipam_driver,
                    "Config": ipam_pools or [],
                    "Options": self.parameters.ipam_driver_options,
                }

            if not self.check_mode:
                resp = self.client.post_json_to_json("/networks/create", data=data)
                self.client.report_warnings(resp, ["Warning"])
                self.existing_network = self.client.get_network(network_id=resp["Id"])
            self.actions.append(
                f"Created network {self.parameters.name} with driver {self.parameters.driver}"
            )
            self.results["changed"] = True

    def remove_network(self) -> None:
        if self.existing_network:
            self.disconnect_all_containers()
            if not self.check_mode:
                self.client.delete_call("/networks/{0}", self.parameters.name)
                if self.existing_network.get("Scope", "local") == "swarm":
                    while self.get_existing_network():
                        time.sleep(0.1)
            self.actions.append(f"Removed network {self.parameters.name}")
            self.results["changed"] = True

    def is_container_connected(self, container_name: str) -> bool:
        if not self.existing_network:
            return False
        return container_name in container_names_in_network(self.existing_network)

    def is_container_exist(self, container_name: str) -> bool:
        try:
            container = self.client.get_container(container_name)
            return bool(container)

        except DockerException as e:
            self.client.fail(
                f"An unexpected Docker error occurred: {e}",
                exception=traceback.format_exc(),
            )
        except RequestException as e:
            self.client.fail(
                f"An unexpected requests error occurred when trying to talk to the Docker daemon: {e}",
                exception=traceback.format_exc(),
            )

    def connect_containers(self) -> None:
        for name in self.parameters.connected:
            if not self.is_container_connected(name) and self.is_container_exist(name):
                if not self.check_mode:
                    data = {
                        "Container": name,
                        "EndpointConfig": None,
                    }
                    self.client.post_json(
                        "/networks/{0}/connect", self.parameters.name, data=data
                    )
                self.actions.append(f"Connected container {name}")
                self.results["changed"] = True
                self.diff_tracker.add(f"connected.{name}", parameter=True, active=False)

    def disconnect_missing(self) -> None:
        if not self.existing_network:
            return
        containers = self.existing_network["Containers"]
        if not containers:
            return
        for c in containers.values():
            name = c["Name"]
            if name not in self.parameters.connected:
                self.disconnect_container(name)

    def disconnect_all_containers(self) -> None:
        network = self.client.get_network(name=self.parameters.name)
        if not network:
            return
        containers = network["Containers"]
        if not containers:
            return
        for cont in containers.values():
            self.disconnect_container(cont["Name"])

    def disconnect_container(self, container_name: str) -> None:
        if not self.check_mode:
            data = {"Container": container_name, "Force": True}
            self.client.post_json(
                "/networks/{0}/disconnect", self.parameters.name, data=data
            )
        self.actions.append(f"Disconnected container {container_name}")
        self.results["changed"] = True
        self.diff_tracker.add(
            f"connected.{container_name}", parameter=False, active=True
        )

    def present(self) -> None:
        different = False
        differences = DifferenceTracker()
        if self.existing_network:
            different, differences = self.has_different_config(self.existing_network)

        self.diff_tracker.add(
            "exists", parameter=True, active=self.existing_network is not None
        )
        if self.parameters.force or different:
            self.remove_network()
            self.existing_network = None

        self.create_network()
        self.connect_containers()
        if not self.parameters.appends:
            self.disconnect_missing()

        if self.diff or self.check_mode or self.parameters.debug:
            self.diff_result["differences"] = differences.get_legacy_docker_diffs()
            self.diff_tracker.merge(differences)

        if not self.check_mode and not self.parameters.debug:
            self.results.pop("actions")

        network_facts = self.get_existing_network()
        self.results["network"] = network_facts

    def absent(self) -> None:
        self.diff_tracker.add(
            "exists", parameter=False, active=self.existing_network is not None
        )
        self.remove_network()


def main() -> None:
    argument_spec = {
        "name": {"type": "str", "required": True, "aliases": ["network_name"]},
        "config_from": {"type": "str"},
        "config_only": {"type": "bool"},
        "connected": {
            "type": "list",
            "default": [],
            "elements": "str",
            "aliases": ["containers"],
        },
        "state": {
            "type": "str",
            "default": "present",
            "choices": ["present", "absent"],
        },
        "driver": {"type": "str", "default": "bridge"},
        "driver_options": {"type": "dict", "default": {}},
        "force": {"type": "bool", "default": False},
        "appends": {"type": "bool", "default": False, "aliases": ["incremental"]},
        "ipam_driver": {"type": "str"},
        "ipam_driver_options": {"type": "dict"},
        "ipam_config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "subnet": {"type": "str"},
                "iprange": {"type": "str"},
                "gateway": {"type": "str"},
                "aux_addresses": {"type": "dict"},
            },
        },
        "enable_ipv4": {"type": "bool"},
        "enable_ipv6": {"type": "bool"},
        "internal": {"type": "bool"},
        "labels": {"type": "dict", "default": {}},
        "debug": {"type": "bool", "default": False},
        "scope": {"type": "str", "choices": ["local", "global", "swarm"]},
        "attachable": {"type": "bool"},
        "ingress": {"type": "bool"},
    }

    option_minimal_versions = {
        "config_from": {"docker_api_version": "1.30"},
        "config_only": {"docker_api_version": "1.30"},
        "scope": {"docker_api_version": "1.30"},
        "attachable": {"docker_api_version": "1.26"},
        "enable_ipv4": {"docker_api_version": "1.47"},
    }

    client = AnsibleDockerClient(
        argument_spec=argument_spec,
        supports_check_mode=True,
        # "The docker server >= 1.10.0"
        option_minimal_versions=option_minimal_versions,
    )
    sanitize_labels(client.module.params["labels"], "labels", client)
    try:
        cm = DockerNetworkManager(client)
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
