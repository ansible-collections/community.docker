# Copyright (c) 2019 Piotr Wojciechowski (@wojciechowskipiotr) <piotr@it-playground.pl>
# Copyright (c) Thierry Bouvet (@tbouvet)
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Note that this module util is **PRIVATE** to the collection. It can have breaking changes at any time.
# Do not use this from other collections or standalone plugins/modules!

from __future__ import annotations

import json
import typing as t
from time import sleep


try:
    from docker.errors import APIError, NotFound
except ImportError:
    # missing Docker SDK for Python handled in ansible.module_utils.docker.common
    pass

from ansible_collections.community.docker.plugins.module_utils._common import (
    AnsibleDockerClient,
)
from ansible_collections.community.docker.plugins.module_utils._version import (
    LooseVersion,
)


class AnsibleDockerSwarmClient(AnsibleDockerClient):
    def get_swarm_node_id(self) -> str | None:
        """
        Get the 'NodeID' of the Swarm node or 'None' if host is not in Swarm. It returns the NodeID
        of Docker host the module is executed on
        :return:
            NodeID of host or 'None' if not part of Swarm
        """

        try:
            info = self.info()
        except APIError as exc:
            self.fail(f"Failed to get node information for {exc}")

        if info:
            json_str = json.dumps(info, ensure_ascii=False)
            swarm_info = json.loads(json_str)
            if swarm_info["Swarm"]["NodeID"]:
                return swarm_info["Swarm"]["NodeID"]
        return None

    def check_if_swarm_node(self, node_id: str | None = None) -> bool | None:
        """
        Checking if host is part of Docker Swarm. If 'node_id' is not provided it reads the Docker host
        system information looking if specific key in output exists. If 'node_id' is provided then it tries to
        read node information assuming it is run on Swarm manager. The get_node_inspect() method handles exception if
        it is not executed on Swarm manager

        :param node_id: Node identifier
        :return:
            bool: True if node is part of Swarm, False otherwise
        """

        if node_id is None:
            try:
                info = self.info()
            except APIError:
                self.fail("Failed to get host information.")

            if info:
                json_str = json.dumps(info, ensure_ascii=False)
                swarm_info = json.loads(json_str)
                if swarm_info["Swarm"]["NodeID"]:
                    return True
                return swarm_info["Swarm"]["LocalNodeState"] in (
                    "active",
                    "pending",
                    "locked",
                )
            return False
        try:
            node_info = self.get_node_inspect(node_id=node_id)
        except APIError:
            return None

        return node_info["ID"] is not None

    def check_if_swarm_manager(self) -> bool:
        """
        Checks if node role is set as Manager in Swarm. The node is the docker host on which module action
        is performed. The inspect_swarm() will fail if node is not a manager

        :return: True if node is Swarm Manager, False otherwise
        """

        try:
            self.inspect_swarm()
            return True
        except APIError:
            return False

    def fail_task_if_not_swarm_manager(self) -> None:
        """
        If host is not a swarm manager then Ansible task on this host should end with 'failed' state
        """
        if not self.check_if_swarm_manager():
            self.fail(
                "Error running docker swarm module: must run on swarm manager node"
            )

    def check_if_swarm_worker(self) -> bool:
        """
        Checks if node role is set as Worker in Swarm. The node is the docker host on which module action
        is performed. Will fail if run on host that is not part of Swarm via check_if_swarm_node()

        :return: True if node is Swarm Worker, False otherwise
        """

        return bool(self.check_if_swarm_node() and not self.check_if_swarm_manager())

    def check_if_swarm_node_is_down(
        self, node_id: str | None = None, repeat_check: int = 1
    ) -> bool:
        """
        Checks if node status on Swarm manager is 'down'. If node_id is provided it query manager about
        node specified in parameter, otherwise it query manager itself. If run on Swarm Worker node or
        host that is not part of Swarm it will fail the playbook

        :param repeat_check: number of check attempts with 5 seconds delay between them, by default check only once
        :param node_id: node ID or name, if None then method will try to get node_id of host module run on
        :return:
            True if node is part of swarm but its state is down, False otherwise
        """

        repeat_check = max(1, repeat_check)

        if node_id is None:
            node_id = self.get_swarm_node_id()

        for retry in range(0, repeat_check):
            if retry > 0:
                sleep(5)
            node_info = self.get_node_inspect(node_id=node_id)
            if node_info["Status"]["State"] == "down":
                return True
        return False

    @t.overload
    def get_node_inspect(
        self, node_id: str | None = None, skip_missing: t.Literal[False] = False
    ) -> dict[str, t.Any]: ...

    @t.overload
    def get_node_inspect(
        self, node_id: str | None = None, skip_missing: bool = False
    ) -> dict[str, t.Any] | None: ...

    def get_node_inspect(
        self, node_id: str | None = None, skip_missing: bool = False
    ) -> dict[str, t.Any] | None:
        """
        Returns Swarm node info as in 'docker node inspect' command about single node

        :param skip_missing: if True then function will return None instead of failing the task
        :param node_id: node ID or name, if None then method will try to get node_id of host module run on
        :return:
            Single node information structure
        """

        if node_id is None:
            node_id = self.get_swarm_node_id()

        if node_id is None:
            self.fail("Failed to get node information.")

        try:
            node_info = self.inspect_node(node_id=node_id)
        except APIError as exc:
            if exc.status_code == 503:
                self.fail(
                    "Cannot inspect node: To inspect node execute module on Swarm Manager"
                )
            if exc.status_code == 404 and skip_missing:
                return None
            self.fail(f"Error while reading from Swarm manager: {exc}")
        except Exception as exc:  # pylint: disable=broad-exception-caught
            self.fail(f"Error inspecting swarm node: {exc}")

        json_str = json.dumps(node_info, ensure_ascii=False)
        node_info = json.loads(json_str)

        if "ManagerStatus" in node_info and node_info["ManagerStatus"].get("Leader"):
            # This is workaround of bug in Docker when in some cases the Leader IP is 0.0.0.0
            # Check moby/moby#35437 for details
            count_colons = node_info["ManagerStatus"]["Addr"].count(":")
            if count_colons == 1:
                swarm_leader_ip = (
                    node_info["ManagerStatus"]["Addr"].split(":", 1)[0]
                    or node_info["Status"]["Addr"]
                )
            else:
                swarm_leader_ip = node_info["Status"]["Addr"]
            node_info["Status"]["Addr"] = swarm_leader_ip
        return node_info

    def get_all_nodes_inspect(self) -> list[dict[str, t.Any]]:
        """
        Returns Swarm node info as in 'docker node inspect' command about all registered nodes

        :return:
            Structure with information about all nodes
        """
        try:
            node_info = self.nodes()
        except APIError as exc:
            if exc.status_code == 503:
                self.fail(
                    "Cannot inspect node: To inspect node execute module on Swarm Manager"
                )
            self.fail(f"Error while reading from Swarm manager: {exc}")
        except Exception as exc:  # pylint: disable=broad-exception-caught
            self.fail(f"Error inspecting swarm node: {exc}")

        json_str = json.dumps(node_info, ensure_ascii=False)
        node_info = json.loads(json_str)
        return node_info

    @t.overload
    def get_all_nodes_list(self, output: t.Literal["short"] = "short") -> list[str]: ...

    @t.overload
    def get_all_nodes_list(
        self, output: t.Literal["long"]
    ) -> list[dict[str, t.Any]]: ...

    def get_all_nodes_list(
        self, output: t.Literal["short", "long"] = "short"
    ) -> list[str] | list[dict[str, t.Any]]:
        """
        Returns list of nodes registered in Swarm

        :param output: Defines format of returned data
        :return:
            If 'output' is 'short' then return data is list of nodes hostnames registered in Swarm,
            if 'output' is 'long' then returns data is list of dict containing the attributes as in
            output of command 'docker node ls'
        """
        nodes_inspect = self.get_all_nodes_inspect()

        if output == "short":
            nodes_list = []
            for node in nodes_inspect:
                nodes_list.append(node["Description"]["Hostname"])
            return nodes_list
        if output == "long":
            nodes_info_list = []
            for node in nodes_inspect:
                node_property: dict[str, t.Any] = {}

                node_property["ID"] = node["ID"]
                node_property["Hostname"] = node["Description"]["Hostname"]
                node_property["Status"] = node["Status"]["State"]
                node_property["Availability"] = node["Spec"]["Availability"]
                if "ManagerStatus" in node:
                    if node["ManagerStatus"]["Leader"] is True:
                        node_property["Leader"] = True
                    node_property["ManagerStatus"] = node["ManagerStatus"][
                        "Reachability"
                    ]
                node_property["EngineVersion"] = node["Description"]["Engine"][
                    "EngineVersion"
                ]

                nodes_info_list.append(node_property)
            return nodes_info_list

    def get_node_name_by_id(self, nodeid: str) -> str:
        return self.get_node_inspect(nodeid)["Description"]["Hostname"]

    def get_unlock_key(self) -> dict[str, t.Any] | None:
        if self.docker_py_version < LooseVersion("2.7.0"):
            return None
        return super().get_unlock_key()

    def get_service_inspect(
        self, service_id: str, skip_missing: bool = False
    ) -> dict[str, t.Any] | None:
        """
        Returns Swarm service info as in 'docker service inspect' command about single service

        :param service_id: service ID or name
        :param skip_missing: if True then function will return None instead of failing the task
        :return:
            Single service information structure
        """
        try:
            service_info = self.inspect_service(service_id)
        except NotFound as exc:
            if skip_missing is False:
                self.fail(f"Error while reading from Swarm manager: {exc}")
            else:
                return None
        except APIError as exc:
            if exc.status_code == 503:
                self.fail(
                    "Cannot inspect service: To inspect service execute module on Swarm Manager"
                )
            self.fail(f"Error inspecting swarm service: {exc}")
        except Exception as exc:  # pylint: disable=broad-exception-caught
            self.fail(f"Error inspecting swarm service: {exc}")

        json_str = json.dumps(service_info, ensure_ascii=False)
        service_info = json.loads(json_str)
        return service_info
