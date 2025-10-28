# Copyright (c) 2022 Felix Fontein <felix@fontein.de>
# Copyright 2016 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Note that this module util is **PRIVATE** to the collection. It can have breaking changes at any time.
# Do not use this from other collections or standalone plugins/modules!

from __future__ import annotations

import abc
import os
import re
import shlex
import typing as t
from functools import partial

from ansible.module_utils.common.text.converters import to_text
from ansible.module_utils.common.text.formatters import human_to_bytes

from ansible_collections.community.docker.plugins.module_utils._api.utils.utils import (
    parse_env_file,
)
from ansible_collections.community.docker.plugins.module_utils._platform import (
    compare_platform_strings,
)
from ansible_collections.community.docker.plugins.module_utils._util import (
    clean_dict_booleans_for_docker_api,
    compare_generic,
    normalize_healthcheck,
    omit_none_from_dict,
    sanitize_labels,
)


if t.TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from ansible.module_utils.basic import AnsibleModule

    from ansible_collections.community.docker.plugins.module_utils._version import (
        LooseVersion,
    )

    ValueType = t.Literal["set", "list", "dict", "bool", "int", "float", "str"]
    AnsibleType = t.Literal["list", "dict", "bool", "int", "float", "str"]
    ComparisonMode = t.Literal["ignore", "strict", "allow_more_present"]
    ComparisonType = t.Literal["set", "set(dict)", "list", "dict", "value"]

Client = t.TypeVar("Client")


_DEFAULT_IP_REPLACEMENT_STRING = (
    "[[DEFAULT_IP:iewahhaeB4Sae6Aen8IeShairoh4zeph7xaekoh8Geingunaesaeweiy3ooleiwi]]"
)


_MOUNT_OPTION_TYPES = {
    "create_mountpoint": ("bind",),
    "labels": ("volume",),
    "no_copy": ("volume",),
    "non_recursive": ("bind",),
    "propagation": ("bind",),
    "read_only_force_recursive": ("bind",),
    "read_only_non_recursive": ("bind",),
    "subpath": ("volume", "image"),
    "tmpfs_size": ("tmpfs",),
    "tmpfs_mode": ("tmpfs",),
    "tmpfs_options": ("tmpfs",),
    "volume_driver": ("volume",),
    "volume_options": ("volume",),
}


def _get_ansible_type(
    value_type: ValueType,
) -> AnsibleType:
    if value_type == "set":
        return "list"
    if value_type not in ("list", "dict", "bool", "int", "float", "str"):
        raise ValueError(f'Invalid type "{value_type}"')
    return value_type


class Option:
    def __init__(
        self,
        name: str,
        *,
        value_type: ValueType,
        owner: OptionGroup,
        ansible_type: AnsibleType | None = None,
        elements: ValueType | None = None,
        ansible_elements: AnsibleType | None = None,
        ansible_suboptions: dict[str, t.Any] | None = None,
        ansible_aliases: Sequence[str] | None = None,
        ansible_choices: Sequence[str] | None = None,
        needs_no_suboptions: bool = False,
        default_comparison: ComparisonMode | None = None,
        not_a_container_option: bool = False,
        not_an_ansible_option: bool = False,
        copy_comparison_from: str | None = None,
        compare: Callable[[Option, t.Any, t.Any], bool] | None = None,
    ):
        self.name = name
        self.value_type = value_type
        self.ansible_type = ansible_type or _get_ansible_type(value_type)
        needs_elements = self.value_type in ("list", "set")
        needs_ansible_elements = self.ansible_type in ("list",)
        if elements is not None and not needs_elements:
            raise ValueError("elements only allowed for lists/sets")
        if elements is None and needs_elements:
            raise ValueError("elements required for lists/sets")
        if ansible_elements is not None and not needs_ansible_elements:
            raise ValueError("Ansible elements only allowed for Ansible lists")
        if (elements is None and ansible_elements is None) and needs_ansible_elements:
            raise ValueError("Ansible elements required for Ansible lists")
        self.elements = elements if needs_elements else None
        self.ansible_elements: AnsibleType | None = (
            (ansible_elements or _get_ansible_type(elements or "str"))
            if needs_ansible_elements
            else None
        )
        needs_suboptions = (
            self.ansible_type == "list" and self.ansible_elements == "dict"
        ) or (self.ansible_type == "dict")
        if ansible_suboptions is not None and not needs_suboptions:
            raise ValueError(
                "suboptions only allowed for Ansible lists with dicts, or Ansible dicts"
            )
        if (
            ansible_suboptions is None
            and needs_suboptions
            and not needs_no_suboptions
            and not not_an_ansible_option
        ):
            raise ValueError(
                "suboptions required for Ansible lists with dicts, or Ansible dicts"
            )
        self.ansible_suboptions = ansible_suboptions if needs_suboptions else None
        self.ansible_aliases = ansible_aliases or []
        self.ansible_choices = ansible_choices
        comparison_type: ComparisonType
        if self.value_type == "set" and self.elements == "dict":
            comparison_type = "set(dict)"
        elif self.value_type in ("set", "list", "dict"):
            comparison_type = self.value_type  # type: ignore
        else:
            comparison_type = "value"
        self.comparison_type = comparison_type
        if default_comparison is not None:
            self.comparison = default_comparison
        elif comparison_type in ("list", "value"):
            self.comparison = "strict"
        else:
            self.comparison = "allow_more_present"
        self.not_a_container_option = not_a_container_option
        self.not_an_ansible_option = not_an_ansible_option
        self.copy_comparison_from = copy_comparison_from
        self.compare = (
            (
                lambda param_value, container_value: compare(
                    self, param_value, container_value
                )
            )
            if compare
            else (
                lambda param_value, container_value: compare_generic(
                    param_value, container_value, self.comparison, self.comparison_type
                )
            )
        )


class OptionGroup:
    def __init__(
        self,
        *,
        preprocess: (
            Callable[[AnsibleModule, dict[str, t.Any]], dict[str, t.Any]] | None
        ) = None,
        ansible_mutually_exclusive: Sequence[Sequence[str]] | None = None,
        ansible_required_together: Sequence[Sequence[str]] | None = None,
        ansible_required_one_of: Sequence[Sequence[str]] | None = None,
        ansible_required_if: (
            Sequence[
                tuple[str, t.Any, Sequence[str]]
                | tuple[str, t.Any, Sequence[str], bool]
            ]
            | None
        ) = None,
        ansible_required_by: dict[str, Sequence[str]] | None = None,
    ) -> None:
        if preprocess is None:

            def preprocess(
                module: AnsibleModule, values: dict[str, t.Any]
            ) -> dict[str, t.Any]:
                return values

        self.preprocess = preprocess
        self.options: list[Option] = []
        self.all_options: list[Option] = []
        self.engines: dict[str, Engine] = {}
        self.ansible_mutually_exclusive = ansible_mutually_exclusive or []
        self.ansible_required_together = ansible_required_together or []
        self.ansible_required_one_of = ansible_required_one_of or []
        self.ansible_required_if = ansible_required_if or []
        self.ansible_required_by = ansible_required_by or {}
        self.argument_spec: dict[str, t.Any] = {}

    def add_option(self, name: str, **kwargs: t.Any) -> OptionGroup:
        option = Option(name, owner=self, **kwargs)
        if not option.not_a_container_option:
            self.options.append(option)
        self.all_options.append(option)
        if not option.not_an_ansible_option:
            ansible_option: dict[str, t.Any] = {
                "type": option.ansible_type,
            }
            if option.ansible_elements is not None:
                ansible_option["elements"] = option.ansible_elements
            if option.ansible_suboptions is not None:
                ansible_option["options"] = option.ansible_suboptions
            if option.ansible_aliases:
                ansible_option["aliases"] = option.ansible_aliases
            if option.ansible_choices is not None:
                ansible_option["choices"] = option.ansible_choices
            self.argument_spec[option.name] = ansible_option
        return self

    def supports_engine(self, engine_name: str) -> bool:
        return engine_name in self.engines

    def get_engine(self, engine_name: str) -> Engine:
        return self.engines[engine_name]

    def add_engine(self, engine_name: str, engine: Engine) -> OptionGroup:
        self.engines[engine_name] = engine
        return self


class Engine(t.Generic[Client]):
    min_api_version: str | None = None
    min_api_version_obj: LooseVersion | None = None
    extra_option_minimal_versions: dict[str, dict[str, t.Any]] | None = None

    @abc.abstractmethod
    def get_value(
        self,
        module: AnsibleModule,
        container: dict[str, t.Any],
        api_version: LooseVersion,
        options: list[Option],
        image: dict[str, t.Any] | None,
        host_info: dict[str, t.Any] | None,
    ) -> dict[str, t.Any]:
        pass

    def compare_value(
        self, option: Option, param_value: t.Any, container_value: t.Any
    ) -> bool:
        return option.compare(param_value, container_value)

    @abc.abstractmethod
    def set_value(
        self,
        module: AnsibleModule,
        data: dict[str, t.Any],
        api_version: LooseVersion,
        options: list[Option],
        values: dict[str, t.Any],
    ) -> None:
        pass

    @abc.abstractmethod
    def get_expected_values(
        self,
        module: AnsibleModule,
        client: Client,
        api_version: LooseVersion,
        options: list[Option],
        image: dict[str, t.Any] | None,
        values: dict[str, t.Any],
        host_info: dict[str, t.Any] | None,
    ) -> dict[str, t.Any]:
        pass

    @abc.abstractmethod
    def ignore_mismatching_result(
        self,
        module: AnsibleModule,
        client: Client,
        api_version: LooseVersion,
        option: Option,
        image: dict[str, t.Any] | None,
        container_value: t.Any,
        expected_value: t.Any,
        host_info: dict[str, t.Any] | None,
    ) -> bool:
        pass

    @abc.abstractmethod
    def preprocess_value(
        self,
        module: AnsibleModule,
        client: Client,
        api_version: LooseVersion,
        options: list[Option],
        values: dict[str, t.Any],
    ) -> dict[str, t.Any]:
        pass

    @abc.abstractmethod
    def update_value(
        self,
        module: AnsibleModule,
        data: dict[str, t.Any],
        api_version: LooseVersion,
        options: list[Option],
        values: dict[str, t.Any],
    ) -> None:
        pass

    @abc.abstractmethod
    def can_set_value(self, api_version: LooseVersion) -> bool:
        pass

    @abc.abstractmethod
    def can_update_value(self, api_version: LooseVersion) -> bool:
        pass

    @abc.abstractmethod
    def needs_container_image(self, values: dict[str, t.Any]) -> bool:
        pass

    @abc.abstractmethod
    def needs_host_info(self, values: dict[str, t.Any]) -> bool:
        pass


class EngineDriver(t.Generic[Client]):
    name: str

    @abc.abstractmethod
    def setup(
        self,
        argument_spec: dict[str, t.Any],
        mutually_exclusive: Sequence[Sequence[str]] | None = None,
        required_together: Sequence[Sequence[str]] | None = None,
        required_one_of: Sequence[Sequence[str]] | None = None,
        required_if: (
            Sequence[
                tuple[str, t.Any, Sequence[str]]
                | tuple[str, t.Any, Sequence[str], bool]
            ]
            | None
        ) = None,
        required_by: dict[str, Sequence[str]] | None = None,
    ) -> tuple[AnsibleModule, list[OptionGroup], Client]:
        pass

    @abc.abstractmethod
    def get_host_info(self, client: Client) -> dict[str, t.Any]:
        pass

    @abc.abstractmethod
    def get_api_version(self, client: Client) -> LooseVersion:
        pass

    @abc.abstractmethod
    def get_container_id(self, container: dict[str, t.Any]) -> str:
        pass

    @abc.abstractmethod
    def get_image_from_container(self, container: dict[str, t.Any]) -> str:
        pass

    @abc.abstractmethod
    def get_image_name_from_container(self, container: dict[str, t.Any]) -> str | None:
        pass

    @abc.abstractmethod
    def is_container_removing(self, container: dict[str, t.Any]) -> bool:
        pass

    @abc.abstractmethod
    def is_container_running(self, container: dict[str, t.Any]) -> bool:
        pass

    @abc.abstractmethod
    def is_container_paused(self, container: dict[str, t.Any]) -> bool:
        pass

    @abc.abstractmethod
    def inspect_container_by_name(
        self, client: Client, container_name: str
    ) -> dict[str, t.Any] | None:
        pass

    @abc.abstractmethod
    def inspect_container_by_id(
        self, client: Client, container_id: str
    ) -> dict[str, t.Any] | None:
        pass

    @abc.abstractmethod
    def inspect_image_by_id(
        self, client: Client, image_id: str
    ) -> dict[str, t.Any] | None:
        pass

    @abc.abstractmethod
    def inspect_image_by_name(
        self, client: Client, repository: str, tag: str
    ) -> dict[str, t.Any] | None:
        pass

    @abc.abstractmethod
    def pull_image(
        self,
        client: Client,
        repository: str,
        tag: str,
        image_platform: str | None = None,
    ) -> tuple[dict[str, t.Any] | None, bool]:
        pass

    @abc.abstractmethod
    def pause_container(self, client: Client, container_id: str) -> None:
        pass

    @abc.abstractmethod
    def unpause_container(self, client: Client, container_id: str) -> None:
        pass

    @abc.abstractmethod
    def disconnect_container_from_network(
        self, client: Client, container_id: str, network_id: str
    ) -> None:
        pass

    @abc.abstractmethod
    def connect_container_to_network(
        self,
        client: Client,
        container_id: str,
        network_id: str,
        parameters: dict[str, t.Any] | None = None,
    ) -> None:
        pass

    def create_container_supports_more_than_one_network(self, client: Client) -> bool:
        return False

    @abc.abstractmethod
    def create_container(
        self,
        client: Client,
        container_name: str,
        create_parameters: dict[str, t.Any],
        networks: dict[str, dict[str, t.Any]] | None = None,
    ) -> str:
        pass

    @abc.abstractmethod
    def start_container(self, client: Client, container_id: str) -> None:
        pass

    @abc.abstractmethod
    def wait_for_container(
        self, client: Client, container_id: str, timeout: int | float | None = None
    ) -> int | None:
        pass

    @abc.abstractmethod
    def get_container_output(
        self, client: Client, container_id: str
    ) -> tuple[bytes, t.Literal[True]] | tuple[str, t.Literal[False]]:
        pass

    @abc.abstractmethod
    def update_container(
        self, client: Client, container_id: str, update_parameters: dict[str, t.Any]
    ) -> None:
        pass

    @abc.abstractmethod
    def restart_container(
        self, client: Client, container_id: str, timeout: int | float | None = None
    ) -> None:
        pass

    @abc.abstractmethod
    def kill_container(
        self, client: Client, container_id: str, kill_signal: str | None = None
    ) -> None:
        pass

    @abc.abstractmethod
    def stop_container(
        self, client: Client, container_id: str, timeout: int | float | None = None
    ) -> None:
        pass

    @abc.abstractmethod
    def remove_container(
        self,
        client: Client,
        container_id: str,
        remove_volumes: bool = False,
        link: bool = False,
        force: bool = False,
    ) -> None:
        pass

    @abc.abstractmethod
    def run(self, runner: Callable[[], None], client: Client) -> None:
        pass


def _is_volume_permissions(mode: str) -> bool:
    for part in mode.split(","):
        if part not in (
            "rw",
            "ro",
            "z",
            "Z",
            "consistent",
            "delegated",
            "cached",
            "rprivate",
            "private",
            "rshared",
            "shared",
            "rslave",
            "slave",
            "nocopy",
        ):
            return False
    return True


def _parse_port_range(range_or_port: str, module: AnsibleModule) -> list[int]:
    """
    Parses a string containing either a single port or a range of ports.

    Returns a list of integers for each port in the list.
    """
    if "-" in range_or_port:
        try:
            start, end = [int(port) for port in range_or_port.split("-")]
        except ValueError:
            module.fail_json(msg=f'Invalid port range: "{range_or_port}"')
        if end < start:
            module.fail_json(msg=f'Invalid port range: "{range_or_port}"')
        return list(range(start, end + 1))
    try:
        return [int(range_or_port)]
    except ValueError:
        module.fail_json(msg=f'Invalid port: "{range_or_port}"')


def _split_colon_ipv6(text: str, module: AnsibleModule) -> list[str]:
    """
    Split string by ':', while keeping IPv6 addresses in square brackets in one component.
    """
    if "[" not in text:
        return text.split(":")
    start = 0
    result = []
    while start < len(text):
        i = text.find("[", start)
        if i < 0:
            result.extend(text[start:].split(":"))
            break
        j = text.find("]", i)
        if j < 0:
            module.fail_json(
                msg=f'Cannot find closing "]" in input "{text}" for opening "[" at index {i + 1}!'
            )
        result.extend(text[start:i].split(":"))
        k = text.find(":", j)
        if k < 0:
            result[-1] += text[i:]
            start = len(text)
        else:
            result[-1] += text[i:k]
            if k == len(text):
                result.append("")
                break
            start = k + 1
    return result


def _preprocess_command(
    module: AnsibleModule, values: dict[str, t.Any]
) -> dict[str, t.Any]:
    if "command" not in values:
        return values
    value = values["command"]
    if module.params["command_handling"] == "correct":
        if value is not None:
            if not isinstance(value, list):
                # convert from str to list
                value = shlex.split(to_text(value, errors="surrogate_or_strict"))
            value = [to_text(x, errors="surrogate_or_strict") for x in value]
    elif value:
        # convert from list to str
        if isinstance(value, list):
            value = shlex.split(
                " ".join([to_text(x, errors="surrogate_or_strict") for x in value])
            )
            value = [to_text(x, errors="surrogate_or_strict") for x in value]
        else:
            value = shlex.split(to_text(value, errors="surrogate_or_strict"))
            value = [to_text(x, errors="surrogate_or_strict") for x in value]
    else:
        return {}
    return {
        "command": value,
    }


def _preprocess_entrypoint(
    module: AnsibleModule, values: dict[str, t.Any]
) -> dict[str, t.Any]:
    if "entrypoint" not in values:
        return values
    value = values["entrypoint"]
    if module.params["command_handling"] == "correct":
        if value is not None:
            value = [to_text(x, errors="surrogate_or_strict") for x in value]
    elif value:
        # convert from list to str.
        value = shlex.split(
            " ".join([to_text(x, errors="surrogate_or_strict") for x in value])
        )
        value = [to_text(x, errors="surrogate_or_strict") for x in value]
    else:
        return {}
    return {
        "entrypoint": value,
    }


def _preprocess_env(
    module: AnsibleModule, values: dict[str, t.Any]
) -> dict[str, t.Any]:
    if not values:
        return {}
    final_env = {}
    if "env_file" in values:
        parsed_env_file = parse_env_file(values["env_file"])
        for name, value in parsed_env_file.items():
            final_env[name] = to_text(value, errors="surrogate_or_strict")
    if "env" in values:
        for name, value in values["env"].items():
            if not isinstance(value, str):
                module.fail_json(
                    msg="Non-string value found for env option. Ambiguous env options must be "
                    f"wrapped in quotes to avoid them being interpreted. Key: {name}"
                )
            final_env[name] = to_text(value, errors="surrogate_or_strict")
    formatted_env = []
    for key, value in final_env.items():
        formatted_env.append(f"{key}={value}")
    return {
        "env": formatted_env,
    }


def _preprocess_healthcheck(
    module: AnsibleModule, values: dict[str, t.Any]
) -> dict[str, t.Any]:
    if not values:
        return {}
    return {
        "healthcheck": normalize_healthcheck(
            values["healthcheck"], normalize_test=False
        ),
    }


def _preprocess_convert_to_bytes(
    module: AnsibleModule,
    values: dict[str, t.Any],
    name: str,
    unlimited_value: int | None = None,
) -> dict[str, t.Any]:
    if name not in values:
        return values
    try:
        value = values[name]
        if unlimited_value is not None and value in ("unlimited", str(unlimited_value)):
            value = unlimited_value
        else:
            value = human_to_bytes(value)
        values[name] = value
        return values
    except ValueError as exc:
        module.fail_json(msg=f"Failed to convert {name} to bytes: {exc}")


def _preprocess_mac_address(
    module: AnsibleModule, values: dict[str, t.Any]
) -> dict[str, t.Any]:
    if "mac_address" not in values:
        return values
    return {
        "mac_address": values["mac_address"].replace("-", ":"),
    }


def _preprocess_networks(
    module: AnsibleModule, values: dict[str, t.Any]
) -> dict[str, t.Any]:
    if (
        module.params["networks_cli_compatible"] is True
        and values.get("networks")
        and "network_mode" not in values
    ):
        # Same behavior as Docker CLI: if networks are specified, use the name of the first network as the value for network_mode
        # (assuming no explicit value is specified for network_mode)
        values["network_mode"] = values["networks"][0]["name"]

    if "networks" in values:
        for network in values["networks"]:
            if network["links"]:
                parsed_links = []
                for link in network["links"]:
                    parsed_link = link.split(":", 1)
                    if len(parsed_link) == 1:
                        parsed_link = (link, link)
                    parsed_links.append(tuple(parsed_link))
                network["links"] = parsed_links
            if network["mac_address"]:
                network["mac_address"] = network["mac_address"].replace("-", ":")

    return values


def _preprocess_sysctls(
    module: AnsibleModule, values: dict[str, t.Any]
) -> dict[str, t.Any]:
    if "sysctls" in values:
        for key, value in values["sysctls"].items():
            values["sysctls"][key] = to_text(value, errors="surrogate_or_strict")
    return values


def _preprocess_tmpfs(
    module: AnsibleModule, values: dict[str, t.Any]
) -> dict[str, t.Any]:
    if "tmpfs" not in values:
        return values
    result = {}
    for tmpfs_spec in values["tmpfs"]:
        split_spec = tmpfs_spec.split(":", 1)
        if len(split_spec) > 1:
            result[split_spec[0]] = split_spec[1]
        else:
            result[split_spec[0]] = ""
    return {"tmpfs": result}


def _preprocess_ulimits(
    module: AnsibleModule, values: dict[str, t.Any]
) -> dict[str, t.Any]:
    if "ulimits" not in values:
        return values
    result = []
    for limit in values["ulimits"]:
        limits = {}
        pieces = limit.split(":")
        if len(pieces) >= 2:
            limits["Name"] = pieces[0]
            limits["Soft"] = int(pieces[1])
            limits["Hard"] = int(pieces[1])
        if len(pieces) == 3:
            limits["Hard"] = int(pieces[2])
        result.append(limits)
    return {
        "ulimits": result,
    }


def _preprocess_mounts(
    module: AnsibleModule, values: dict[str, t.Any]
) -> dict[str, t.Any]:
    last: dict[str, str] = {}

    def check_collision(target: str, name: str) -> None:
        if target in last:
            if name == last[target]:
                module.fail_json(
                    msg=f'The mount point "{target}" appears twice in the {name} option'
                )
            else:
                module.fail_json(
                    msg=f'The mount point "{target}" appears both in the {name} and {last[target]} option'
                )
        last[target] = name

    if "mounts" in values:
        mounts = []
        for mount in values["mounts"]:
            target = mount["target"]
            mount_type = mount["type"]

            check_collision(target, "mounts")

            mount_dict = dict(mount)

            # Sanity checks
            if mount["source"] is None and mount_type not in (
                "tmpfs",
                "volume",
                "image",
                "cluster",
            ):
                module.fail_json(
                    msg=f'source must be specified for mount "{target}" of type "{mount_type}"'
                )
            for option, req_mount_types in _MOUNT_OPTION_TYPES.items():
                if mount[option] is not None and mount_type not in req_mount_types:
                    type_plural = "" if len(req_mount_types) == 1 else "s"
                    type_list = '", "'.join(req_mount_types)
                    module.fail_json(
                        msg=f'{option} cannot be specified for mount "{target}" of type "{mount_type}" (needs type{type_plural} "{type_list}")'
                    )

            # Streamline options
            volume_options = mount_dict.pop("volume_options")
            if mount_dict["volume_driver"] and volume_options:
                mount_dict["volume_options"] = clean_dict_booleans_for_docker_api(
                    volume_options
                )
            if mount_dict["labels"]:
                mount_dict["labels"] = clean_dict_booleans_for_docker_api(
                    mount_dict["labels"]
                )
            if mount_dict["tmpfs_size"] is not None:
                try:
                    mount_dict["tmpfs_size"] = human_to_bytes(mount_dict["tmpfs_size"])
                except ValueError as exc:
                    module.fail_json(
                        msg=f'Failed to convert tmpfs_size of mount "{target}" to bytes: {exc}'
                    )
            if mount_dict["tmpfs_mode"] is not None:
                try:
                    mount_dict["tmpfs_mode"] = int(mount_dict["tmpfs_mode"], 8)
                except ValueError:
                    module.fail_json(
                        msg=f'tmp_fs mode of mount "{target}" is not an octal string!'
                    )
            if mount_dict["tmpfs_options"]:
                opts = []
                for idx, opt in enumerate(mount_dict["tmpfs_options"]):
                    if len(opt) != 1:
                        module.fail_json(
                            msg=f'tmpfs_options[{idx + 1}] of mount "{target}" must be a one-element dictionary!'
                        )
                    k, v = list(opt.items())[0]
                    if not isinstance(k, str):
                        module.fail_json(
                            msg=f'key {k!r} in tmpfs_options[{idx + 1}] of mount "{target}" must be a string!'
                        )
                    if v is not None and not isinstance(v, str):
                        module.fail_json(
                            msg=f'value {v!r} in tmpfs_options[{idx + 1}] of mount "{target}" must be a string or null/none!'
                        )
                    opts.append([k, v] if v is not None else [k])
                mount_dict["tmpfs_options"] = opts

            # Add result to list
            mounts.append(omit_none_from_dict(mount_dict))
        values["mounts"] = mounts
    if "volumes" in values:
        new_vols = []
        for vol in values["volumes"]:
            parts = vol.split(":")
            if ":" in vol:
                if len(parts) == 3:
                    host, container, mode = parts
                    if not _is_volume_permissions(mode):
                        module.fail_json(msg=f"Found invalid volumes mode: {mode}")
                    if re.match(r"[.~]", host):
                        host = os.path.abspath(os.path.expanduser(host))
                    check_collision(container, "volumes")
                    new_vols.append(f"{host}:{container}:{mode}")
                    continue
                if (
                    len(parts) == 2
                    and not _is_volume_permissions(parts[1])
                    and re.match(r"[.~]", parts[0])
                ):
                    host = os.path.abspath(os.path.expanduser(parts[0]))
                    check_collision(parts[1], "volumes")
                    new_vols.append(f"{host}:{parts[1]}:rw")
                    continue
            check_collision(parts[min(1, len(parts) - 1)], "volumes")
            new_vols.append(vol)
        values["volumes"] = new_vols
        new_binds = []
        for vol in new_vols:
            host = None
            if ":" in vol:
                parts = vol.split(":")
                if len(parts) == 3:
                    host, container, mode = parts
                    if not _is_volume_permissions(mode):
                        module.fail_json(msg=f"Found invalid volumes mode: {mode}")
                elif len(parts) == 2:
                    if not _is_volume_permissions(parts[1]):
                        host, container, mode = parts + ["rw"]
            if host is not None:
                new_binds.append(f"{host}:{container}:{mode}")
        values["volume_binds"] = new_binds
    return values


def _preprocess_labels(
    module: AnsibleModule, values: dict[str, t.Any]
) -> dict[str, t.Any]:
    result = {}
    if "labels" in values:
        labels = values["labels"]
        if labels is not None:
            labels = dict(labels)
            sanitize_labels(labels, "labels", module=module)
        result["labels"] = labels
    return result


def _preprocess_log(
    module: AnsibleModule, values: dict[str, t.Any]
) -> dict[str, t.Any]:
    result: dict[str, t.Any] = {}
    if "log_driver" not in values:
        return result
    result["log_driver"] = values["log_driver"]
    if "log_options" in values:
        options: dict[str, str] = {}
        for k, v in values["log_options"].items():
            if not isinstance(v, str):
                value = to_text(v, errors="surrogate_or_strict")
                module.warn(
                    f"Non-string value found for log_options option '{k}'. The value is automatically converted to {value!r}. "
                    "If this is not correct, or you want to avoid such warnings, please quote the value."
                )
                v = value
            options[k] = v
        result["log_options"] = options
    return result


def _preprocess_ports(
    module: AnsibleModule, values: dict[str, t.Any]
) -> dict[str, t.Any]:
    if "published_ports" in values:
        if "all" in values["published_ports"]:
            module.fail_json(
                msg='Specifying "all" in published_ports is no longer allowed. Set publish_all_ports to "true" instead '
                "to randomly assign port mappings for those not specified by published_ports."
            )

        binds: dict[
            str | int,
            tuple[str]
            | tuple[str, str | int]
            | list[tuple[str] | tuple[str, str | int]],
        ] = {}
        for port in values["published_ports"]:
            parts = _split_colon_ipv6(
                to_text(port, errors="surrogate_or_strict"), module
            )
            container_port = parts[-1]
            protocol = ""
            if "/" in container_port:
                container_port, protocol = parts[-1].split("/")
            container_ports = _parse_port_range(container_port, module)

            p_len = len(parts)
            port_binds: Sequence[tuple[str] | tuple[str, str | int]]
            if p_len == 1:
                port_binds = len(container_ports) * [(_DEFAULT_IP_REPLACEMENT_STRING,)]
            elif p_len == 2:
                if len(container_ports) == 1:
                    port_binds = [(_DEFAULT_IP_REPLACEMENT_STRING, parts[0])]
                else:
                    port_binds = [
                        (_DEFAULT_IP_REPLACEMENT_STRING, port)
                        for port in _parse_port_range(parts[0], module)
                    ]
            elif p_len == 3:
                # We only allow IPv4 and IPv6 addresses for the bind address
                ipaddr = parts[0]
                if not re.match(
                    r"^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$", parts[0]
                ) and not re.match(r"^\[[0-9a-fA-F:]+(?:|%[^\]/]+)\]$", ipaddr):
                    module.fail_json(
                        msg="Bind addresses for published ports must be IPv4 or IPv6 addresses, not hostnames. "
                        f"Use the dig lookup to resolve hostnames. (Found hostname: {ipaddr})"
                    )
                if re.match(r"^\[[0-9a-fA-F:]+\]$", ipaddr):
                    ipaddr = ipaddr[1:-1]
                if parts[1]:
                    if len(container_ports) == 1:
                        port_binds = [(ipaddr, parts[1])]
                    else:
                        port_binds = [
                            (ipaddr, port)
                            for port in _parse_port_range(parts[1], module)
                        ]
                else:
                    port_binds = len(container_ports) * [(ipaddr,)]
            else:
                return module.fail_json(
                    msg=f'Invalid port description "{port}" - expected 1 to 3 colon-separated parts, but got {p_len}. '
                    "Maybe you forgot to use square brackets ([...]) around an IPv6 address?"
                )

            for bind, container_port_val in zip(port_binds, container_ports):
                idx = (
                    f"{container_port_val}/{protocol}"
                    if protocol
                    else container_port_val
                )
                if idx in binds:
                    old_bind = binds[idx]
                    if isinstance(old_bind, list):
                        old_bind.append(bind)
                    else:
                        binds[idx] = [old_bind, bind]
                else:
                    binds[idx] = bind
        values["published_ports"] = binds

    exposed = []
    if "exposed_ports" in values:
        for port in values["exposed_ports"]:
            port = to_text(port, errors="surrogate_or_strict").strip()
            protocol = "tcp"
            matcher = re.search(r"(/.+$)", port)
            if matcher:
                protocol = matcher.group(1).replace("/", "")
                port = re.sub(r"/.+$", "", port)
            exposed.append((port, protocol))
    if "published_ports" in values:
        # Any published port should also be exposed
        for publish_port in values["published_ports"]:
            match = False
            if isinstance(publish_port, str) and "/" in publish_port:
                port, protocol = publish_port.split("/")
                port = int(port)
            else:
                protocol = "tcp"
                port = int(publish_port)
            for exposed_port in exposed:
                if exposed_port[1] != protocol:
                    continue
                if isinstance(exposed_port[0], str) and "-" in exposed_port[0]:
                    start_port, end_port = exposed_port[0].split("-")
                    if int(start_port) <= port <= int(end_port):
                        match = True
                elif exposed_port[0] == port:
                    match = True
            if not match:
                exposed.append((port, protocol))
    values["ports"] = exposed
    return values


def _compare_platform(
    option: Option, param_value: t.Any, container_value: t.Any
) -> bool:
    if option.comparison == "ignore":
        return True
    try:
        return compare_platform_strings(param_value, container_value)
    except ValueError:
        return param_value == container_value


OPTION_AUTO_REMOVE = OptionGroup().add_option("auto_remove", value_type="bool")

OPTION_BLKIO_WEIGHT = OptionGroup().add_option("blkio_weight", value_type="int")

OPTION_CAPABILITIES = OptionGroup().add_option(
    "capabilities", value_type="set", elements="str"
)

OPTION_CAP_DROP = OptionGroup().add_option("cap_drop", value_type="set", elements="str")

OPTION_CGROUP_NS_MODE = OptionGroup().add_option(
    "cgroupns_mode", value_type="str", ansible_choices=["private", "host"]
)

OPTION_CGROUP_PARENT = OptionGroup().add_option("cgroup_parent", value_type="str")

OPTION_COMMAND = OptionGroup(preprocess=_preprocess_command).add_option(
    "command", value_type="list", elements="str", ansible_type="raw"
)

OPTION_CPU_PERIOD = OptionGroup().add_option("cpu_period", value_type="int")

OPTION_CPU_QUOTA = OptionGroup().add_option("cpu_quota", value_type="int")

OPTION_CPUSET_CPUS = OptionGroup().add_option("cpuset_cpus", value_type="str")

OPTION_CPUSET_MEMS = OptionGroup().add_option("cpuset_mems", value_type="str")

OPTION_CPU_SHARES = OptionGroup().add_option("cpu_shares", value_type="int")

OPTION_ENTRYPOINT = OptionGroup(preprocess=_preprocess_entrypoint).add_option(
    "entrypoint", value_type="list", elements="str"
)

OPTION_CPUS = OptionGroup().add_option("cpus", value_type="int", ansible_type="float")

OPTION_DETACH_INTERACTIVE = (
    OptionGroup()
    .add_option("detach", value_type="bool")
    .add_option("interactive", value_type="bool")
)

OPTION_DEVICES = OptionGroup().add_option(
    "devices", value_type="set", elements="dict", ansible_elements="str"
)

OPTION_DEVICE_READ_BPS = OptionGroup().add_option(
    "device_read_bps",
    value_type="set",
    elements="dict",
    ansible_suboptions={
        "path": {"type": "str", "required": True},
        "rate": {"type": "str", "required": True},
    },
)

OPTION_DEVICE_WRITE_BPS = OptionGroup().add_option(
    "device_write_bps",
    value_type="set",
    elements="dict",
    ansible_suboptions={
        "path": {"type": "str", "required": True},
        "rate": {"type": "str", "required": True},
    },
)

OPTION_DEVICE_READ_IOPS = OptionGroup().add_option(
    "device_read_iops",
    value_type="set",
    elements="dict",
    ansible_suboptions={
        "path": {"type": "str", "required": True},
        "rate": {"type": "int", "required": True},
    },
)

OPTION_DEVICE_WRITE_IOPS = OptionGroup().add_option(
    "device_write_iops",
    value_type="set",
    elements="dict",
    ansible_suboptions={
        "path": {"type": "str", "required": True},
        "rate": {"type": "int", "required": True},
    },
)

OPTION_DEVICE_REQUESTS = OptionGroup().add_option(
    "device_requests",
    value_type="set",
    elements="dict",
    ansible_suboptions={
        "capabilities": {"type": "list", "elements": "list"},
        "count": {"type": "int"},
        "device_ids": {"type": "list", "elements": "str"},
        "driver": {"type": "str"},
        "options": {"type": "dict"},
    },
)

OPTION_DEVICE_CGROUP_RULES = OptionGroup().add_option(
    "device_cgroup_rules", value_type="list", elements="str"
)

OPTION_DNS_SERVERS = OptionGroup().add_option(
    "dns_servers", value_type="list", elements="str"
)

OPTION_DNS_OPTS = OptionGroup().add_option("dns_opts", value_type="set", elements="str")

OPTION_DNS_SEARCH_DOMAINS = OptionGroup().add_option(
    "dns_search_domains", value_type="list", elements="str"
)

OPTION_DOMAINNAME = OptionGroup().add_option("domainname", value_type="str")

OPTION_ENVIRONMENT = (
    OptionGroup(preprocess=_preprocess_env)
    .add_option(
        "env",
        value_type="set",
        ansible_type="dict",
        elements="str",
        needs_no_suboptions=True,
    )
    .add_option(
        "env_file",
        value_type="set",
        ansible_type="path",
        elements="str",
        not_a_container_option=True,
    )
)

OPTION_ETC_HOSTS = OptionGroup().add_option(
    "etc_hosts",
    value_type="set",
    ansible_type="dict",
    elements="str",
    needs_no_suboptions=True,
)

OPTION_GROUPS = OptionGroup().add_option("groups", value_type="set", elements="str")

OPTION_HEALTHCHECK = OptionGroup(preprocess=_preprocess_healthcheck).add_option(
    "healthcheck",
    value_type="dict",
    ansible_suboptions={
        "test": {"type": "raw"},
        "test_cli_compatible": {"type": "bool", "default": False},
        "interval": {"type": "str"},
        "timeout": {"type": "str"},
        "start_period": {"type": "str"},
        "start_interval": {"type": "str"},
        "retries": {"type": "int"},
    },
)

OPTION_HOSTNAME = OptionGroup().add_option("hostname", value_type="str")

OPTION_IMAGE = OptionGroup().add_option("image", value_type="str")

OPTION_INIT = OptionGroup().add_option("init", value_type="bool")

OPTION_IPC_MODE = OptionGroup().add_option("ipc_mode", value_type="str")

OPTION_KERNEL_MEMORY = OptionGroup(
    preprocess=partial(_preprocess_convert_to_bytes, name="kernel_memory")
).add_option("kernel_memory", value_type="int", ansible_type="str")

OPTION_LABELS = OptionGroup(preprocess=_preprocess_labels).add_option(
    "labels", value_type="dict", needs_no_suboptions=True
)

OPTION_LINKS = OptionGroup().add_option(
    "links", value_type="set", elements="list", ansible_elements="str"
)

OPTION_LOG_DRIVER_OPTIONS = (
    OptionGroup(
        preprocess=_preprocess_log, ansible_required_by={"log_options": ["log_driver"]}
    )
    .add_option("log_driver", value_type="str")
    .add_option(
        "log_options",
        value_type="dict",
        ansible_aliases=["log_opt"],
        needs_no_suboptions=True,
    )
)

OPTION_MAC_ADDRESS = OptionGroup(preprocess=_preprocess_mac_address).add_option(
    "mac_address", value_type="str"
)

OPTION_MEMORY = OptionGroup(
    preprocess=partial(_preprocess_convert_to_bytes, name="memory")
).add_option("memory", value_type="int", ansible_type="str")

OPTION_MEMORY_RESERVATION = OptionGroup(
    preprocess=partial(_preprocess_convert_to_bytes, name="memory_reservation")
).add_option("memory_reservation", value_type="int", ansible_type="str")

OPTION_MEMORY_SWAP = OptionGroup(
    preprocess=partial(
        _preprocess_convert_to_bytes, name="memory_swap", unlimited_value=-1
    )
).add_option("memory_swap", value_type="int", ansible_type="str")

OPTION_MEMORY_SWAPPINESS = OptionGroup().add_option(
    "memory_swappiness", value_type="int"
)

OPTION_STOP_TIMEOUT = OptionGroup().add_option(
    "stop_timeout", value_type="int", default_comparison="ignore"
)

OPTION_NETWORK = (
    OptionGroup(preprocess=_preprocess_networks)
    .add_option("network_mode", value_type="str")
    .add_option(
        "networks",
        value_type="set",
        elements="dict",
        ansible_suboptions={
            "name": {"type": "str", "required": True},
            "ipv4_address": {"type": "str"},
            "ipv6_address": {"type": "str"},
            "aliases": {"type": "list", "elements": "str"},
            "links": {"type": "list", "elements": "str"},
            "mac_address": {"type": "str"},
            "driver_opts": {"type": "dict"},
            "gw_priority": {"type": "int"},
        },
    )
)

OPTION_OOM_KILLER = OptionGroup().add_option("oom_killer", value_type="bool")

OPTION_OOM_SCORE_ADJ = OptionGroup().add_option("oom_score_adj", value_type="int")

OPTION_PID_MODE = OptionGroup().add_option("pid_mode", value_type="str")

OPTION_PIDS_LIMIT = OptionGroup().add_option("pids_limit", value_type="int")

OPTION_PLATFORM = OptionGroup().add_option(
    "platform", value_type="str", compare=_compare_platform
)

OPTION_PRIVILEGED = OptionGroup().add_option("privileged", value_type="bool")

OPTION_READ_ONLY = OptionGroup().add_option("read_only", value_type="bool")

OPTION_RESTART_POLICY = (
    OptionGroup(ansible_required_by={"restart_retries": ["restart_policy"]})
    .add_option(
        "restart_policy",
        value_type="str",
        ansible_choices=["no", "on-failure", "always", "unless-stopped"],
    )
    .add_option("restart_retries", value_type="int")
)

OPTION_RUNTIME = OptionGroup().add_option("runtime", value_type="str")

OPTION_SECURITY_OPTS = OptionGroup().add_option(
    "security_opts", value_type="set", elements="str"
)

OPTION_SHM_SIZE = OptionGroup(
    preprocess=partial(_preprocess_convert_to_bytes, name="shm_size")
).add_option("shm_size", value_type="int", ansible_type="str")

OPTION_STOP_SIGNAL = OptionGroup().add_option("stop_signal", value_type="str")

OPTION_STORAGE_OPTS = OptionGroup().add_option(
    "storage_opts", value_type="dict", needs_no_suboptions=True
)

OPTION_SYSCTLS = OptionGroup(preprocess=_preprocess_sysctls).add_option(
    "sysctls", value_type="dict", needs_no_suboptions=True
)

OPTION_TMPFS = OptionGroup(preprocess=_preprocess_tmpfs).add_option(
    "tmpfs", value_type="dict", ansible_type="list", ansible_elements="str"
)

OPTION_TTY = OptionGroup().add_option("tty", value_type="bool")

OPTION_ULIMITS = OptionGroup(preprocess=_preprocess_ulimits).add_option(
    "ulimits", value_type="set", elements="dict", ansible_elements="str"
)

OPTION_USER = OptionGroup().add_option("user", value_type="str")

OPTION_USERNS_MODE = OptionGroup().add_option("userns_mode", value_type="str")

OPTION_UTS = OptionGroup().add_option("uts", value_type="str")

OPTION_VOLUME_DRIVER = OptionGroup().add_option("volume_driver", value_type="str")

OPTION_VOLUMES_FROM = OptionGroup().add_option(
    "volumes_from", value_type="set", elements="str"
)

OPTION_WORKING_DIR = OptionGroup().add_option("working_dir", value_type="str")

OPTION_MOUNTS_VOLUMES = (
    OptionGroup(preprocess=_preprocess_mounts)
    .add_option(
        "mounts",
        value_type="set",
        elements="dict",
        ansible_suboptions={
            "target": {"type": "str", "required": True},
            "source": {"type": "str"},
            "type": {
                "type": "str",
                "choices": ["bind", "volume", "tmpfs", "npipe", "cluster", "image"],
                "default": "volume",
            },
            "read_only": {"type": "bool"},
            "consistency": {
                "type": "str",
                "choices": ["default", "consistent", "cached", "delegated"],
            },
            "propagation": {
                "type": "str",
                "choices": [
                    "private",
                    "rprivate",
                    "shared",
                    "rshared",
                    "slave",
                    "rslave",
                ],
            },
            "no_copy": {"type": "bool"},
            "labels": {"type": "dict"},
            "volume_driver": {"type": "str"},
            "volume_options": {"type": "dict"},
            "tmpfs_size": {"type": "str"},
            "tmpfs_mode": {"type": "str"},
            "non_recursive": {"type": "bool"},
            "create_mountpoint": {"type": "bool"},
            "read_only_non_recursive": {"type": "bool"},
            "read_only_force_recursive": {"type": "bool"},
            "subpath": {"type": "str"},
            "tmpfs_options": {"type": "list", "elements": "dict"},
        },
    )
    .add_option("volumes", value_type="set", elements="str")
    .add_option(
        "volume_binds",
        value_type="set",
        elements="str",
        not_an_ansible_option=True,
        copy_comparison_from="volumes",
    )
)

OPTION_PORTS = (
    OptionGroup(preprocess=_preprocess_ports)
    .add_option(
        "exposed_ports",
        value_type="set",
        elements="str",
        ansible_aliases=["exposed", "expose"],
    )
    .add_option("publish_all_ports", value_type="bool")
    .add_option(
        "published_ports",
        value_type="dict",
        ansible_type="list",
        ansible_elements="str",
        ansible_aliases=["ports"],
    )
    .add_option(
        "ports",
        value_type="set",
        elements="str",
        not_an_ansible_option=True,
        default_comparison="ignore",
    )
)

OPTIONS = [
    OPTION_AUTO_REMOVE,
    OPTION_BLKIO_WEIGHT,
    OPTION_CAPABILITIES,
    OPTION_CAP_DROP,
    OPTION_CGROUP_NS_MODE,
    OPTION_CGROUP_PARENT,
    OPTION_COMMAND,
    OPTION_CPU_PERIOD,
    OPTION_CPU_QUOTA,
    OPTION_CPUSET_CPUS,
    OPTION_CPUSET_MEMS,
    OPTION_CPU_SHARES,
    OPTION_ENTRYPOINT,
    OPTION_CPUS,
    OPTION_DETACH_INTERACTIVE,
    OPTION_DEVICES,
    OPTION_DEVICE_READ_BPS,
    OPTION_DEVICE_WRITE_BPS,
    OPTION_DEVICE_READ_IOPS,
    OPTION_DEVICE_WRITE_IOPS,
    OPTION_DEVICE_REQUESTS,
    OPTION_DEVICE_CGROUP_RULES,
    OPTION_DNS_SERVERS,
    OPTION_DNS_OPTS,
    OPTION_DNS_SEARCH_DOMAINS,
    OPTION_DOMAINNAME,
    OPTION_ENVIRONMENT,
    OPTION_ETC_HOSTS,
    OPTION_GROUPS,
    OPTION_HEALTHCHECK,
    OPTION_HOSTNAME,
    OPTION_IMAGE,
    OPTION_INIT,
    OPTION_IPC_MODE,
    OPTION_KERNEL_MEMORY,
    OPTION_LABELS,
    OPTION_LINKS,
    OPTION_LOG_DRIVER_OPTIONS,
    OPTION_MAC_ADDRESS,
    OPTION_MEMORY,
    OPTION_MEMORY_RESERVATION,
    OPTION_MEMORY_SWAP,
    OPTION_MEMORY_SWAPPINESS,
    OPTION_STOP_TIMEOUT,
    OPTION_NETWORK,
    OPTION_OOM_KILLER,
    OPTION_OOM_SCORE_ADJ,
    OPTION_PID_MODE,
    OPTION_PIDS_LIMIT,
    OPTION_PLATFORM,
    OPTION_PRIVILEGED,
    OPTION_READ_ONLY,
    OPTION_RESTART_POLICY,
    OPTION_RUNTIME,
    OPTION_SECURITY_OPTS,
    OPTION_SHM_SIZE,
    OPTION_STOP_SIGNAL,
    OPTION_STORAGE_OPTS,
    OPTION_SYSCTLS,
    OPTION_TMPFS,
    OPTION_TTY,
    OPTION_ULIMITS,
    OPTION_USER,
    OPTION_USERNS_MODE,
    OPTION_UTS,
    OPTION_VOLUME_DRIVER,
    OPTION_VOLUMES_FROM,
    OPTION_WORKING_DIR,
    OPTION_MOUNTS_VOLUMES,
    OPTION_PORTS,
]
