# Copyright (c) 2022 Felix Fontein <felix@fontein.de>
# Copyright 2016 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Note that this module util is **PRIVATE** to the collection. It can have breaking changes at any time.
# Do not use this from other collections or standalone plugins/modules!

from __future__ import annotations

import json
import traceback
import typing as t

from ansible.module_utils.common.text.converters import to_text
from ansible.module_utils.common.text.formatters import human_to_bytes

from ansible_collections.community.docker.plugins.module_utils._api.errors import (
    APIError,
    DockerException,
    NotFound,
)
from ansible_collections.community.docker.plugins.module_utils._api.utils.utils import (
    convert_port_bindings,
    normalize_links,
)
from ansible_collections.community.docker.plugins.module_utils._common_api import (
    AnsibleDockerClient,
    RequestException,
)
from ansible_collections.community.docker.plugins.module_utils._module_container.base import (
    OPTION_AUTO_REMOVE,
    OPTION_BLKIO_WEIGHT,
    OPTION_CAP_DROP,
    OPTION_CAPABILITIES,
    OPTION_CGROUP_NS_MODE,
    OPTION_CGROUP_PARENT,
    OPTION_COMMAND,
    OPTION_CPU_PERIOD,
    OPTION_CPU_QUOTA,
    OPTION_CPU_SHARES,
    OPTION_CPUS,
    OPTION_CPUSET_CPUS,
    OPTION_CPUSET_MEMS,
    OPTION_DETACH_INTERACTIVE,
    OPTION_DEVICE_CGROUP_RULES,
    OPTION_DEVICE_READ_BPS,
    OPTION_DEVICE_READ_IOPS,
    OPTION_DEVICE_REQUESTS,
    OPTION_DEVICE_WRITE_BPS,
    OPTION_DEVICE_WRITE_IOPS,
    OPTION_DEVICES,
    OPTION_DNS_OPTS,
    OPTION_DNS_SEARCH_DOMAINS,
    OPTION_DNS_SERVERS,
    OPTION_DOMAINNAME,
    OPTION_ENTRYPOINT,
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
    OPTION_MOUNTS_VOLUMES,
    OPTION_NETWORK,
    OPTION_OOM_KILLER,
    OPTION_OOM_SCORE_ADJ,
    OPTION_PID_MODE,
    OPTION_PIDS_LIMIT,
    OPTION_PLATFORM,
    OPTION_PORTS,
    OPTION_PRIVILEGED,
    OPTION_READ_ONLY,
    OPTION_RESTART_POLICY,
    OPTION_RUNTIME,
    OPTION_SECURITY_OPTS,
    OPTION_SHM_SIZE,
    OPTION_STOP_SIGNAL,
    OPTION_STOP_TIMEOUT,
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
    OPTIONS,
    Engine,
    EngineDriver,
    _is_volume_permissions,
)
from ansible_collections.community.docker.plugins.module_utils._platform import (
    compose_platform_string,
    normalize_platform_string,
)
from ansible_collections.community.docker.plugins.module_utils._util import (
    normalize_healthcheck_test,
    omit_none_from_dict,
)
from ansible_collections.community.docker.plugins.module_utils._version import (
    LooseVersion,
)


if t.TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from ansible.module_utils.basic import AnsibleModule

    from .base import Option, OptionGroup

    Sentry = object


_DEFAULT_IP_REPLACEMENT_STRING = (
    "[[DEFAULT_IP:iewahhaeB4Sae6Aen8IeShairoh4zeph7xaekoh8Geingunaesaeweiy3ooleiwi]]"
)


_SENTRY: Sentry = object()


class DockerAPIEngineDriver(EngineDriver[AnsibleDockerClient]):
    name = "docker_api"

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
    ) -> tuple[AnsibleModule, list[OptionGroup], AnsibleDockerClient]:
        argument_spec = dict(argument_spec or {})
        mutually_exclusive = list(mutually_exclusive or [])
        required_together = list(required_together or [])
        required_one_of = list(required_one_of or [])
        required_if = list(required_if or [])
        required_by = dict(required_by or {})

        active_options = []
        option_minimal_versions = {}
        for options in OPTIONS:
            if not options.supports_engine(self.name):
                continue

            mutually_exclusive.extend(options.ansible_mutually_exclusive)
            required_together.extend(options.ansible_required_together)
            required_one_of.extend(options.ansible_required_one_of)
            required_if.extend(options.ansible_required_if)
            required_by.update(options.ansible_required_by)
            argument_spec.update(options.argument_spec)

            engine = options.get_engine(self.name)
            if engine.min_api_version is not None:
                for option in options.options:
                    if not option.not_an_ansible_option:
                        option_minimal_versions[option.name] = {
                            "docker_api_version": engine.min_api_version
                        }
            if engine.extra_option_minimal_versions:
                option_minimal_versions.update(engine.extra_option_minimal_versions)

            active_options.append(options)

        client = AnsibleDockerClient(
            argument_spec=argument_spec,
            mutually_exclusive=mutually_exclusive,
            required_together=required_together,
            required_one_of=required_one_of,
            required_if=required_if,
            required_by=required_by,
            option_minimal_versions=option_minimal_versions,
            supports_check_mode=True,
        )

        return client.module, active_options, client

    def get_host_info(self, client: AnsibleDockerClient) -> dict[str, t.Any]:
        return client.info()

    def get_api_version(self, client: AnsibleDockerClient) -> LooseVersion:
        return client.docker_api_version

    def get_container_id(self, container: dict[str, t.Any]) -> str:
        return container["Id"]

    def get_image_from_container(self, container: dict[str, t.Any]) -> str:
        return container["Image"]

    def get_image_name_from_container(self, container: dict[str, t.Any]) -> str | None:
        return container["Config"].get("Image")

    def is_container_removing(self, container: dict[str, t.Any]) -> bool:
        if container.get("State"):
            return container["State"].get("Status") == "removing"
        return False

    def is_container_running(self, container: dict[str, t.Any]) -> bool:
        return bool(
            container.get("State")
            and container["State"].get("Running")
            and not container["State"].get("Ghost", False)
        )

    def is_container_paused(self, container: dict[str, t.Any]) -> bool:
        if container.get("State"):
            return container["State"].get("Paused", False)
        return False

    def inspect_container_by_name(
        self, client: AnsibleDockerClient, container_name: str
    ) -> dict[str, t.Any] | None:
        return client.get_container(container_name)

    def inspect_container_by_id(
        self, client: AnsibleDockerClient, container_id: str
    ) -> dict[str, t.Any] | None:
        return client.get_container_by_id(container_id)

    def inspect_image_by_id(
        self, client: AnsibleDockerClient, image_id: str
    ) -> dict[str, t.Any] | None:
        return client.find_image_by_id(image_id, accept_missing_image=True)

    def inspect_image_by_name(
        self, client: AnsibleDockerClient, repository: str, tag: str
    ) -> dict[str, t.Any] | None:
        return client.find_image(repository, tag)

    def pull_image(
        self,
        client: AnsibleDockerClient,
        repository: str,
        tag: str,
        image_platform: str | None = None,
    ) -> tuple[dict[str, t.Any] | None, bool]:
        return client.pull_image(repository, tag, image_platform=image_platform)

    def pause_container(self, client: AnsibleDockerClient, container_id: str) -> None:
        client.post_call("/containers/{0}/pause", container_id)

    def unpause_container(self, client: AnsibleDockerClient, container_id: str) -> None:
        client.post_call("/containers/{0}/unpause", container_id)

    def disconnect_container_from_network(
        self, client: AnsibleDockerClient, container_id: str, network_id: str
    ) -> None:
        client.post_json(
            "/networks/{0}/disconnect", network_id, data={"Container": container_id}
        )

    def _create_endpoint_config(self, parameters: dict[str, t.Any]) -> dict[str, t.Any]:
        parameters = parameters.copy()
        params = {}
        for para, dest_para in {
            "ipv4_address": "IPv4Address",
            "ipv6_address": "IPv6Address",
            "links": "Links",
            "aliases": "Aliases",
            "mac_address": "MacAddress",
            "driver_opts": "DriverOpts",
        }.items():
            value = parameters.pop(para, None)
            if value:
                if para == "links":
                    value = normalize_links(value)
                elif para == "driver_opts":
                    # Ensure driver_opts values are strings
                    for key, val in value.items():
                        if not isinstance(val, str):
                            raise ValueError(
                                f"driver_opts values must be strings, got {type(val).__name__} for key '{key}'"
                            )
                params[dest_para] = value
        for para, dest_para in {
            "gw_priority": "GwPriority",
        }.items():
            value = parameters.pop(para, None)
            if value is not None:
                params[dest_para] = value
        if parameters:
            ups = ", ".join([f'"{p}"' for p in sorted(parameters)])
            raise ValueError(
                f"Unknown parameter(s) for connect_container_to_network for Docker API driver: {ups}"
            )
        ipam_config = {}
        for param in ("IPv4Address", "IPv6Address"):
            if param in params:
                ipam_config[param] = params.pop(param)
        if ipam_config:
            params["IPAMConfig"] = ipam_config
        return params

    def connect_container_to_network(
        self,
        client: AnsibleDockerClient,
        container_id: str,
        network_id: str,
        parameters: dict[str, t.Any] | None = None,
    ) -> None:
        parameters = (parameters or {}).copy()
        params = self._create_endpoint_config(parameters or {})
        data = {
            "Container": container_id,
            "EndpointConfig": params,
        }
        client.post_json("/networks/{0}/connect", network_id, data=data)

    def create_container_supports_more_than_one_network(
        self, client: AnsibleDockerClient
    ) -> bool:
        return client.docker_api_version >= LooseVersion("1.44")

    def create_container(
        self,
        client: AnsibleDockerClient,
        container_name: str,
        create_parameters: dict[str, t.Any],
        networks: dict[str, dict[str, t.Any]] | None = None,
    ) -> str:
        params = {"name": container_name}
        if "platform" in create_parameters:
            params["platform"] = create_parameters.pop("platform")
        if networks is not None:
            create_parameters = create_parameters.copy()
            create_parameters["NetworkingConfig"] = {
                "EndpointsConfig": dict(
                    (network, self._create_endpoint_config(network_params))
                    for network, network_params in networks.items()
                )
            }
        new_container = client.post_json_to_json(
            "/containers/create", data=create_parameters, params=params
        )
        client.report_warnings(new_container)
        return new_container["Id"]

    def start_container(self, client: AnsibleDockerClient, container_id: str) -> None:
        client.post_json("/containers/{0}/start", container_id)

    def wait_for_container(
        self,
        client: AnsibleDockerClient,
        container_id: str,
        timeout: int | float | None = None,
    ) -> int | None:
        return client.post_json_to_json(
            "/containers/{0}/wait", container_id, timeout=timeout
        )["StatusCode"]

    def get_container_output(
        self, client: AnsibleDockerClient, container_id: str
    ) -> tuple[bytes, t.Literal[True]] | tuple[str, t.Literal[False]]:
        config = client.get_json("/containers/{0}/json", container_id)
        logging_driver = config["HostConfig"]["LogConfig"]["Type"]
        if logging_driver in ("json-file", "journald", "local"):
            params = {
                "stderr": 1,
                "stdout": 1,
                "timestamps": 0,
                "follow": 0,
                "tail": "all",
            }
            res = client._get(
                client._url("/containers/{0}/logs", container_id), params=params
            )
            output = client._get_result_tty(False, res, config["Config"]["Tty"])
            return output, True
        return f"Result logged using `{logging_driver}` driver", False

    def update_container(
        self,
        client: AnsibleDockerClient,
        container_id: str,
        update_parameters: dict[str, t.Any],
    ) -> None:
        result = client.post_json_to_json(
            "/containers/{0}/update", container_id, data=update_parameters
        )
        client.report_warnings(result)

    def restart_container(
        self,
        client: AnsibleDockerClient,
        container_id: str,
        timeout: int | float | None = None,
    ) -> None:
        client_timeout: int | float | None = client.timeout
        if client_timeout is not None:
            client_timeout += timeout or 10
        client.post_call(
            "/containers/{0}/restart",
            container_id,
            params={"t": timeout},
            timeout=client_timeout,
        )

    def kill_container(
        self,
        client: AnsibleDockerClient,
        container_id: str,
        kill_signal: str | None = None,
    ) -> None:
        params = {}
        if kill_signal is not None:
            params["signal"] = kill_signal
        client.post_call("/containers/{0}/kill", container_id, params=params)

    def stop_container(
        self,
        client: AnsibleDockerClient,
        container_id: str,
        timeout: int | float | None = None,
    ) -> None:
        if timeout:
            params = {"t": timeout}
        else:
            params = {}
            timeout = 10
        client_timeout = client.timeout
        if client_timeout is not None:
            client_timeout += timeout
        count = 0
        while True:
            try:
                client.post_call(
                    "/containers/{0}/stop",
                    container_id,
                    params=params,
                    timeout=client_timeout,
                )
            except APIError as exc:
                if (
                    "Unpause the container before stopping or killing"
                    in exc.explanation
                ):
                    # New docker daemon versions do not allow containers to be removed
                    # if they are paused. Make sure we do not end up in an infinite loop.
                    if count == 3:
                        raise RuntimeError(
                            f"{exc} [tried to unpause three times]"
                        ) from exc
                    count += 1
                    # Unpause
                    try:
                        self.unpause_container(client, container_id)
                    except Exception as exc2:
                        raise RuntimeError(f"{exc2} [while unpausing]") from exc2
                    # Now try again
                    continue
                raise
            # We only loop when explicitly requested by 'continue'
            break

    def remove_container(
        self,
        client: AnsibleDockerClient,
        container_id: str,
        remove_volumes: bool = False,
        link: bool = False,
        force: bool = False,
    ) -> None:
        params = {"v": remove_volumes, "link": link, "force": force}
        count = 0
        while True:
            try:
                client.delete_call("/containers/{0}", container_id, params=params)
            except NotFound:
                pass
            except APIError as exc:
                if (
                    "Unpause the container before stopping or killing"
                    in exc.explanation
                ):
                    # New docker daemon versions do not allow containers to be removed
                    # if they are paused. Make sure we do not end up in an infinite loop.
                    if count == 3:
                        raise RuntimeError(
                            f"{exc} [tried to unpause three times]"
                        ) from exc
                    count += 1
                    # Unpause
                    try:
                        self.unpause_container(client, container_id)
                    except Exception as exc2:
                        raise RuntimeError(f"{exc2} [while unpausing]") from exc2
                    # Now try again
                    continue
                if (
                    "removal of container " in exc.explanation
                    and " is already in progress" in exc.explanation
                ):
                    pass
                else:
                    raise
            # We only loop when explicitly requested by 'continue'
            break

    def run(self, runner: Callable[[], None], client: AnsibleDockerClient) -> None:
        try:
            runner()
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


class DockerAPIEngine(Engine[AnsibleDockerClient]):
    def get_value(
        self,
        module: AnsibleModule,
        container: dict[str, t.Any],
        api_version: LooseVersion,
        options: list[Option],
        image: dict[str, t.Any] | None,
        host_info: dict[str, t.Any] | None,
    ) -> dict[str, t.Any]:
        return self._get_value(
            module, container, api_version, options, image, host_info
        )

    def compare_value(
        self, option: Option, param_value: t.Any, container_value: t.Any
    ) -> bool:
        if self._compare_value is not None:
            return self._compare_value(option, param_value, container_value)
        return super().compare_value(option, param_value, container_value)

    def set_value(
        self,
        module: AnsibleModule,
        data: dict[str, t.Any],
        api_version: LooseVersion,
        options: list[Option],
        values: dict[str, t.Any],
    ) -> None:
        if self._set_value is not None:
            self._set_value(module, data, api_version, options, values)

    def get_expected_values(
        self,
        module: AnsibleModule,
        client: AnsibleDockerClient,
        api_version: LooseVersion,
        options: list[Option],
        image: dict[str, t.Any] | None,
        values: dict[str, t.Any],
        host_info: dict[str, t.Any] | None,
    ) -> dict[str, t.Any]:
        if self._get_expected_values is None:
            return values
        return self._get_expected_values(
            module, client, api_version, options, image, values, host_info
        )

    def ignore_mismatching_result(
        self,
        module: AnsibleModule,
        client: AnsibleDockerClient,
        api_version: LooseVersion,
        option: Option,
        image: dict[str, t.Any] | None,
        container_value: t.Any,
        expected_value: t.Any,
        host_info: dict[str, t.Any] | None,
    ) -> bool:
        if self._ignore_mismatching_result is None:
            return False
        return self._ignore_mismatching_result(
            module,
            client,
            api_version,
            option,
            image,
            container_value,
            expected_value,
            host_info,
        )

    def preprocess_value(
        self,
        module: AnsibleModule,
        client: AnsibleDockerClient,
        api_version: LooseVersion,
        options: list[Option],
        values: dict[str, t.Any],
    ) -> dict[str, t.Any]:
        if self._preprocess_value is None:
            return values
        return self._preprocess_value(module, client, api_version, options, values)

    def update_value(
        self,
        module: AnsibleModule,
        data: dict[str, t.Any],
        api_version: LooseVersion,
        options: list[Option],
        values: dict[str, t.Any],
    ) -> None:
        if self._update_value is not None:
            self._update_value(module, data, api_version, options, values)

    def can_set_value(self, api_version: LooseVersion) -> bool:
        if self._can_set_value is None:
            return self._set_value is not None
        return self._can_set_value(api_version)

    def can_update_value(self, api_version: LooseVersion) -> bool:
        if self._can_update_value is None:
            return self._update_value is not None
        return self._can_update_value(api_version)

    def needs_container_image(self, values: dict[str, t.Any]) -> bool:
        if self._needs_container_image is None:
            return False
        return self._needs_container_image(values)

    def needs_host_info(self, values: dict[str, t.Any]) -> bool:
        if self._needs_host_info is None:
            return False
        return self._needs_host_info(values)

    def __init__(
        self,
        get_value: Callable[
            [
                AnsibleModule,
                dict[str, t.Any],
                LooseVersion,
                list[Option],
                dict[str, t.Any] | None,
                dict[str, t.Any] | None,
            ],
            dict[str, t.Any],
        ],
        preprocess_value: (
            Callable[
                [
                    AnsibleModule,
                    AnsibleDockerClient,
                    LooseVersion,
                    list[Option],
                    dict[str, t.Any],
                ],
                dict[str, t.Any],
            ]
            | None
        ) = None,
        get_expected_values: (
            Callable[
                [
                    AnsibleModule,
                    AnsibleDockerClient,
                    LooseVersion,
                    list[Option],
                    dict[str, t.Any] | None,
                    dict[str, t.Any],
                    dict[str, t.Any] | None,
                ],
                dict[str, t.Any],
            ]
            | None
        ) = None,
        ignore_mismatching_result: (
            Callable[
                [
                    AnsibleModule,
                    AnsibleDockerClient,
                    LooseVersion,
                    Option,
                    dict[str, t.Any] | None,
                    t.Any,
                    t.Any,
                    dict[str, t.Any] | None,
                ],
                bool,
            ]
            | None
        ) = None,
        set_value: (
            Callable[
                [
                    AnsibleModule,
                    dict[str, t.Any],
                    LooseVersion,
                    list[Option],
                    dict[str, t.Any],
                ],
                None,
            ]
            | None
        ) = None,
        update_value: (
            Callable[
                [
                    AnsibleModule,
                    dict[str, t.Any],
                    LooseVersion,
                    list[Option],
                    dict[str, t.Any],
                ],
                None,
            ]
            | None
        ) = None,
        can_set_value: Callable[[LooseVersion], bool] | None = None,
        can_update_value: Callable[[LooseVersion], bool] | None = None,
        min_api_version: str | None = None,
        compare_value: Callable[[Option, t.Any, t.Any], bool] | None = None,
        needs_container_image: Callable[[dict[str, t.Any]], bool] | None = None,
        needs_host_info: Callable[[dict[str, t.Any]], bool] | None = None,
        extra_option_minimal_versions: dict[str, dict[str, t.Any]] | None = None,
    ):
        self.min_api_version = min_api_version
        self.min_api_version_obj = (
            None if min_api_version is None else LooseVersion(min_api_version)
        )
        self.extra_option_minimal_versions = extra_option_minimal_versions
        self._get_value = get_value
        self._compare_value = compare_value
        self._set_value = set_value
        self._get_expected_values = get_expected_values
        self._ignore_mismatching_result = ignore_mismatching_result
        self._preprocess_value = preprocess_value
        self._update_value = update_value
        self._can_set_value = can_set_value
        self._can_update_value = can_update_value
        self._needs_container_image = needs_container_image
        self._needs_host_info = needs_host_info

    @classmethod
    def config_value(
        cls,
        config_name: str,
        postprocess_for_get: (
            Callable[[AnsibleModule, LooseVersion, t.Any, Sentry], t.Any | Sentry]
            | None
        ) = None,
        preprocess_for_set: (
            Callable[[AnsibleModule, LooseVersion, t.Any], t.Any] | None
        ) = None,
        get_expected_value: (
            Callable[
                [
                    AnsibleModule,
                    AnsibleDockerClient,
                    LooseVersion,
                    dict[str, t.Any] | None,
                    t.Any,
                    Sentry,
                ],
                t.Any | Sentry,
            ]
            | None
        ) = None,
        ignore_mismatching_result: (
            Callable[
                [
                    AnsibleModule,
                    AnsibleDockerClient,
                    LooseVersion,
                    Option,
                    dict[str, t.Any] | None,
                    t.Any,
                    t.Any,
                    dict[str, t.Any] | None,
                ],
                bool,
            ]
            | None
        ) = None,
        min_api_version: str | None = None,
        preprocess_value: (
            Callable[[AnsibleModule, AnsibleDockerClient, LooseVersion, t.Any], t.Any]
            | None
        ) = None,
        update_parameter: str | None = None,
        extra_option_minimal_versions: dict[str, dict[str, t.Any]] | None = None,
    ) -> DockerAPIEngine:
        def preprocess_value_(
            module: AnsibleModule,
            client: AnsibleDockerClient,
            api_version: LooseVersion,
            options: list[Option],
            values: dict[str, t.Any],
        ) -> dict[str, t.Any]:
            if len(options) != 1:
                raise AssertionError(
                    "config_value can only be used for a single option"
                )
            if preprocess_value is not None and options[0].name in values:
                value = preprocess_value(
                    module, client, api_version, values[options[0].name]
                )
                if value is None:
                    del values[options[0].name]
                else:
                    values[options[0].name] = value
            return values

        def get_value(
            module: AnsibleModule,
            container: dict[str, t.Any],
            api_version: LooseVersion,
            options: list[Option],
            image: dict[str, t.Any] | None,
            host_info: dict[str, t.Any] | None,
        ) -> dict[str, t.Any]:
            if len(options) != 1:
                raise AssertionError(
                    "config_value can only be used for a single option"
                )
            value = container["Config"].get(config_name, _SENTRY)
            if postprocess_for_get:
                value = postprocess_for_get(module, api_version, value, _SENTRY)
            if value is _SENTRY:
                return {}
            return {options[0].name: value}

        get_expected_values_: (
            Callable[
                [
                    AnsibleModule,
                    AnsibleDockerClient,
                    LooseVersion,
                    list[Option],
                    dict[str, t.Any] | None,
                    dict[str, t.Any],
                    dict[str, t.Any] | None,
                ],
                dict[str, t.Any],
            ]
            | None
        ) = None
        if get_expected_value:

            def get_expected_values_(  # noqa: F811
                module: AnsibleModule,
                client: AnsibleDockerClient,
                api_version: LooseVersion,
                options: list[Option],
                image: dict[str, t.Any] | None,
                values: dict[str, t.Any],
                host_info: dict[str, t.Any] | None,
            ) -> dict[str, t.Any]:
                if len(options) != 1:
                    raise AssertionError(
                        "host_config_value can only be used for a single option"
                    )
                value = values.get(options[0].name, _SENTRY)
                value = get_expected_value(
                    module, client, api_version, image, value, _SENTRY
                )
                if value is _SENTRY:
                    return values
                return {options[0].name: value}

        def set_value(
            module: AnsibleModule,
            data: dict[str, t.Any],
            api_version: LooseVersion,
            options: list[Option],
            values: dict[str, t.Any],
        ) -> None:
            if len(options) != 1:
                raise AssertionError(
                    "config_value can only be used for a single option"
                )
            if options[0].name not in values:
                return
            value = values[options[0].name]
            if preprocess_for_set:
                value = preprocess_for_set(module, api_version, value)
            data[config_name] = value

        update_value: (
            Callable[
                [
                    AnsibleModule,
                    dict[str, t.Any],
                    LooseVersion,
                    list[Option],
                    dict[str, t.Any],
                ],
                None,
            ]
            | None
        ) = None
        if update_parameter:

            def update_value(  # noqa: F811
                module: AnsibleModule,
                data: dict[str, t.Any],
                api_version: LooseVersion,
                options: list[Option],
                values: dict[str, t.Any],
            ) -> None:
                if len(options) != 1:
                    raise AssertionError(
                        "update_parameter can only be used for a single option"
                    )
                if options[0].name not in values:
                    return
                value = values[options[0].name]
                if preprocess_for_set:
                    value = preprocess_for_set(module, api_version, value)
                data[update_parameter] = value

        return cls(
            get_value=get_value,
            preprocess_value=preprocess_value_,
            get_expected_values=get_expected_values_,
            ignore_mismatching_result=ignore_mismatching_result,
            set_value=set_value,
            min_api_version=min_api_version,
            update_value=update_value,
            extra_option_minimal_versions=extra_option_minimal_versions,
        )

    @classmethod
    def host_config_value(
        cls,
        host_config_name: str,
        postprocess_for_get: (
            Callable[[AnsibleModule, LooseVersion, t.Any, Sentry], t.Any | Sentry]
            | None
        ) = None,
        preprocess_for_set: (
            Callable[[AnsibleModule, LooseVersion, t.Any], t.Any] | None
        ) = None,
        get_expected_value: (
            Callable[
                [
                    AnsibleModule,
                    AnsibleDockerClient,
                    LooseVersion,
                    dict[str, t.Any] | None,
                    t.Any,
                    Sentry,
                ],
                t.Any | Sentry,
            ]
            | None
        ) = None,
        ignore_mismatching_result: (
            Callable[
                [
                    AnsibleModule,
                    AnsibleDockerClient,
                    LooseVersion,
                    Option,
                    dict[str, t.Any] | None,
                    t.Any,
                    t.Any,
                    dict[str, t.Any] | None,
                ],
                bool,
            ]
            | None
        ) = None,
        min_api_version: str | None = None,
        preprocess_value: (
            Callable[[AnsibleModule, AnsibleDockerClient, LooseVersion, t.Any], t.Any]
            | None
        ) = None,
        update_parameter: str | None = None,
        extra_option_minimal_versions: dict[str, dict[str, t.Any]] | None = None,
    ) -> DockerAPIEngine:
        def preprocess_value_(
            module: AnsibleModule,
            client: AnsibleDockerClient,
            api_version: LooseVersion,
            options: list[Option],
            values: dict[str, t.Any],
        ) -> dict[str, t.Any]:
            if len(options) != 1:
                raise AssertionError(
                    "host_config_value can only be used for a single option"
                )
            if preprocess_value is not None and options[0].name in values:
                value = preprocess_value(
                    module, client, api_version, values[options[0].name]
                )
                if value is None:
                    del values[options[0].name]
                else:
                    values[options[0].name] = value
            return values

        def get_value(
            module: AnsibleModule,
            container: dict[str, t.Any],
            api_version: LooseVersion,
            options: list[Option],
            image: dict[str, t.Any] | None,
            host_info: dict[str, t.Any] | None,
        ) -> dict[str, t.Any]:
            if len(options) != 1:
                raise AssertionError(
                    "host_config_value can only be used for a single option"
                )
            value = container["HostConfig"].get(host_config_name, _SENTRY)
            if postprocess_for_get:
                value = postprocess_for_get(module, api_version, value, _SENTRY)
            if value is _SENTRY:
                return {}
            return {options[0].name: value}

        get_expected_values_: (
            Callable[
                [
                    AnsibleModule,
                    AnsibleDockerClient,
                    LooseVersion,
                    list[Option],
                    dict[str, t.Any] | None,
                    dict[str, t.Any],
                    dict[str, t.Any] | None,
                ],
                dict[str, t.Any],
            ]
            | None
        ) = None
        if get_expected_value:

            def get_expected_values_(  # noqa: F811
                module: AnsibleModule,
                client: AnsibleDockerClient,
                api_version: LooseVersion,
                options: list[Option],
                image: dict[str, t.Any] | None,
                values: dict[str, t.Any],
                host_info: dict[str, t.Any] | None,
            ) -> dict[str, t.Any]:
                if len(options) != 1:
                    raise AssertionError(
                        "host_config_value can only be used for a single option"
                    )
                value = values.get(options[0].name, _SENTRY)
                value = get_expected_value(
                    module, client, api_version, image, value, _SENTRY
                )
                if value is _SENTRY:
                    return values
                return {options[0].name: value}

        def set_value(
            module: AnsibleModule,
            data: dict[str, t.Any],
            api_version: LooseVersion,
            options: list[Option],
            values: dict[str, t.Any],
        ) -> None:
            if len(options) != 1:
                raise AssertionError(
                    "host_config_value can only be used for a single option"
                )
            if options[0].name not in values:
                return
            if "HostConfig" not in data:
                data["HostConfig"] = {}
            value = values[options[0].name]
            if preprocess_for_set:
                value = preprocess_for_set(module, api_version, value)
            data["HostConfig"][host_config_name] = value

        update_value: (
            Callable[
                [
                    AnsibleModule,
                    dict[str, t.Any],
                    LooseVersion,
                    list[Option],
                    dict[str, t.Any],
                ],
                None,
            ]
            | None
        ) = None
        if update_parameter:

            def update_value(  # noqa: F811
                module: AnsibleModule,
                data: dict[str, t.Any],
                api_version: LooseVersion,
                options: list[Option],
                values: dict[str, t.Any],
            ) -> None:
                if len(options) != 1:
                    raise AssertionError(
                        "update_parameter can only be used for a single option"
                    )
                if options[0].name not in values:
                    return
                value = values[options[0].name]
                if preprocess_for_set:
                    value = preprocess_for_set(module, api_version, value)
                data[update_parameter] = value

        return cls(
            get_value=get_value,
            preprocess_value=preprocess_value_,
            get_expected_values=get_expected_values_,
            ignore_mismatching_result=ignore_mismatching_result,
            set_value=set_value,
            min_api_version=min_api_version,
            update_value=update_value,
            extra_option_minimal_versions=extra_option_minimal_versions,
        )


def _normalize_port(port: str) -> str:
    if "/" not in port:
        return port + "/tcp"
    return port


def _get_default_host_ip(module: AnsibleModule, client: AnsibleDockerClient) -> str:
    if module.params["default_host_ip"] is not None:
        return module.params["default_host_ip"]
    ip = "0.0.0.0"
    for network_data in module.params["networks"] or []:
        if network_data.get("name"):
            network = client.get_network(network_data["name"])
            if network is None:
                client.fail(
                    f"Cannot inspect the network '{network_data['name']}' to determine the default IP",
                )
            if network.get("Driver") == "bridge" and network.get("Options", {}).get(
                "com.docker.network.bridge.host_binding_ipv4"
            ):
                ip = network["Options"]["com.docker.network.bridge.host_binding_ipv4"]
                break
    return ip


def _get_value_detach_interactive(
    module: AnsibleModule,
    container: dict[str, t.Any],
    api_version: LooseVersion,
    options: list[Option],
    image: dict[str, t.Any] | None,
    host_info: dict[str, t.Any] | None,
) -> dict[str, t.Any]:
    attach_stdin = container["Config"].get("OpenStdin")
    attach_stderr = container["Config"].get("AttachStderr")
    attach_stdout = container["Config"].get("AttachStdout")
    return {
        "interactive": bool(attach_stdin),
        "detach": not (attach_stderr and attach_stdout),
    }


def _set_value_detach_interactive(
    module: AnsibleModule,
    data: dict[str, t.Any],
    api_version: LooseVersion,
    options: list[Option],
    values: dict[str, t.Any],
) -> None:
    interactive = values.get("interactive")
    detach = values.get("detach")

    data["AttachStdout"] = False
    data["AttachStderr"] = False
    data["AttachStdin"] = False
    data["StdinOnce"] = False
    data["OpenStdin"] = interactive
    if not detach:
        data["AttachStdout"] = True
        data["AttachStderr"] = True
        if interactive:
            data["AttachStdin"] = True
            data["StdinOnce"] = True


def _get_expected_env_value(
    module: AnsibleModule,
    client: AnsibleDockerClient,
    api_version: LooseVersion,
    image: dict[str, t.Any] | None,
    value: t.Any,
    sentry: Sentry,
) -> t.Any | Sentry:
    expected_env = {}
    if image and image["Config"].get("Env"):
        for env_var in image["Config"]["Env"]:
            parts = env_var.split("=", 1)
            expected_env[parts[0]] = parts[1]
    if value and value is not sentry:
        for env_var in value:
            parts = env_var.split("=", 1)
            expected_env[parts[0]] = parts[1]
    param_env = []
    for key, env_value in expected_env.items():
        param_env.append(f"{key}={env_value}")
    return param_env


def _preprocess_cpus(
    module: AnsibleModule,
    client: AnsibleDockerClient,
    api_version: LooseVersion,
    value: t.Any,
) -> t.Any:
    if value is not None:
        value = int(round(value * 1e9))
    return value


def _preprocess_devices(
    module: AnsibleModule,
    client: AnsibleDockerClient,
    api_version: LooseVersion,
    value: t.Any,
) -> t.Any:
    if not value:
        return value
    expected_devices = []
    for device in value:
        parts = device.split(":")
        if len(parts) == 1:
            expected_devices.append(
                {
                    "CgroupPermissions": "rwm",
                    "PathInContainer": parts[0],
                    "PathOnHost": parts[0],
                }
            )
        elif len(parts) == 2:
            parts = device.split(":")
            expected_devices.append(
                {
                    "CgroupPermissions": "rwm",
                    "PathInContainer": parts[1],
                    "PathOnHost": parts[0],
                }
            )
        else:
            expected_devices.append(
                {
                    "CgroupPermissions": parts[2],
                    "PathInContainer": parts[1],
                    "PathOnHost": parts[0],
                }
            )
    return expected_devices


def _preprocess_rate_bps(
    module: AnsibleModule,
    client: AnsibleDockerClient,
    api_version: LooseVersion,
    value: t.Any,
) -> t.Any:
    if not value:
        return value
    devices = []
    for device in value:
        devices.append(
            {
                "Path": device["path"],
                "Rate": human_to_bytes(device["rate"]),
            }
        )
    return devices


def _preprocess_rate_iops(
    module: AnsibleModule,
    client: AnsibleDockerClient,
    api_version: LooseVersion,
    value: t.Any,
) -> t.Any:
    if not value:
        return value
    devices = []
    for device in value:
        devices.append(
            {
                "Path": device["path"],
                "Rate": device["rate"],
            }
        )
    return devices


def _preprocess_device_requests(
    module: AnsibleModule,
    client: AnsibleDockerClient,
    api_version: LooseVersion,
    value: t.Any,
) -> t.Any:
    if not value:
        return value
    device_requests = []
    for dr in value:
        device_requests.append(
            {
                "Driver": dr["driver"],
                "Count": dr["count"],
                "DeviceIDs": dr["device_ids"],
                "Capabilities": dr["capabilities"],
                "Options": dr["options"],
            }
        )
    return device_requests


def _preprocess_etc_hosts(
    module: AnsibleModule,
    client: AnsibleDockerClient,
    api_version: LooseVersion,
    value: t.Any,
) -> t.Any:
    if value is None:
        return value
    results = []
    for key, val in value.items():
        results.append(f"{key}:{val}")
    return results


def _preprocess_healthcheck(
    module: AnsibleModule,
    client: AnsibleDockerClient,
    api_version: LooseVersion,
    value: t.Any,
) -> t.Any:
    if value is None:
        return value
    if not value or not (
        value.get("test")
        or (value.get("test_cli_compatible") and value.get("test") is None)
    ):
        value = {"test": ["NONE"]}
    elif "test" in value:
        value["test"] = normalize_healthcheck_test(value["test"])
    return omit_none_from_dict(
        {
            "Test": value.get("test"),
            "Interval": value.get("interval"),
            "Timeout": value.get("timeout"),
            "StartPeriod": value.get("start_period"),
            "StartInterval": value.get("start_interval"),
            "Retries": value.get("retries"),
        }
    )


def _postprocess_healthcheck_get_value(
    module: AnsibleModule, api_version: LooseVersion, value: t.Any, sentry: Sentry
) -> t.Any | Sentry:
    if value is None or value is sentry or value.get("Test") == ["NONE"]:
        return {"Test": ["NONE"]}
    return value


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


def _get_image_labels(image: dict[str, t.Any] | None) -> dict[str, str]:
    if not image:
        return {}

    # Cannot use get('Labels', {}) because 'Labels' may be present and be None
    return image["Config"].get("Labels") or {}


def _get_expected_labels_value(
    module: AnsibleModule,
    client: AnsibleDockerClient,
    api_version: LooseVersion,
    image: dict[str, t.Any] | None,
    value: dict[str, t.Any],
    sentry: Sentry,
) -> dict[str, t.Any] | Sentry:
    if value is sentry:
        return sentry
    expected_labels = {}
    if module.params["image_label_mismatch"] == "ignore":
        expected_labels.update(dict(_get_image_labels(image)))
    expected_labels.update(value)
    return expected_labels


def _preprocess_links(
    module: AnsibleModule,
    client: AnsibleDockerClient,
    api_version: LooseVersion,
    value: t.Any,
) -> t.Any:
    if value is None:
        return None

    result = []
    for link in value:
        parsed_link = link.split(":", 1)
        if len(parsed_link) == 2:
            link, alias = parsed_link
        else:
            link, alias = parsed_link[0], parsed_link[0]
        result.append(f"/{link}:/{module.params['name']}/{alias}")

    return result


def _ignore_mismatching_label_result(
    module: AnsibleModule,
    client: AnsibleDockerClient,
    api_version: LooseVersion,
    option: Option,
    image: dict[str, t.Any] | None,
    container_value: t.Any,
    expected_value: t.Any,
    host_info: dict[str, t.Any] | None,
) -> bool:
    if (
        option.comparison == "strict"
        and module.params["image_label_mismatch"] == "fail"
    ):
        # If there are labels from the base image that should be removed and
        # base_image_mismatch is fail we want raise an error.
        image_labels = _get_image_labels(image)
        would_remove_labels = []
        labels_param = module.params["labels"] or {}
        for label in image_labels:
            if label not in labels_param:
                # Format label for error message
                would_remove_labels.append(f'"{label}"')
        if would_remove_labels:
            labels = ", ".join(would_remove_labels)
            msg = (
                "Some labels should be removed but are present in the base image. You can set image_label_mismatch to 'ignore' to ignore"
                f" this error. Labels: {labels}"
            )
            client.fail(msg)
    return False


def _needs_host_info_network(values: dict[str, t.Any]) -> bool:
    return values.get("network_mode") == "default"


def _ignore_mismatching_network_result(
    module: AnsibleModule,
    client: AnsibleDockerClient,
    api_version: LooseVersion,
    option: Option,
    image: dict[str, t.Any] | None,
    container_value: t.Any,
    expected_value: t.Any,
    host_info: dict[str, t.Any] | None,
) -> bool:
    # 'networks' is handled out-of-band
    if option.name == "networks":
        return True
    # The 'default' network_mode value is translated by the Docker daemon to 'bridge' on Linux and 'nat' on Windows.
    # This happens since Docker 26.1.0 due to https://github.com/moby/moby/pull/47431; before, 'default' was returned.
    if option.name == "network_mode" and expected_value == "default":
        os_type = host_info.get("OSType") if host_info else None
        if (container_value, os_type) in (("bridge", "linux"), ("nat", "windows")):
            return True
    return False


def _preprocess_network_values(
    module: AnsibleModule,
    client: AnsibleDockerClient,
    api_version: LooseVersion,
    options: list[Option],
    values: dict[str, t.Any],
) -> dict[str, t.Any]:
    if "networks" in values:
        for network in values["networks"]:
            network["id"] = _get_network_id(module, client, network["name"])
            if not network["id"]:
                client.fail(
                    f"Parameter error: network named {network['name']} could not be found. Does it exist?"
                )

    if "network_mode" in values:
        values["network_mode"] = _preprocess_container_names(
            module, client, api_version, values["network_mode"]
        )

    return values


def _get_network_id(
    module: AnsibleModule, client: AnsibleDockerClient, network_name: str
) -> str | None:
    try:
        params = {"filters": json.dumps({"name": [network_name]})}
        for network in client.get_json("/networks", params=params):
            if network["Name"] == network_name:
                return network["Id"]
        return None
    except Exception as exc:  # pylint: disable=broad-exception-caught
        client.fail(f"Error getting network id for {network_name} - {exc}")


def _get_values_network(
    module: AnsibleModule,
    container: dict[str, t.Any],
    api_version: LooseVersion,
    options: list[Option],
    image: dict[str, t.Any] | None,
    host_info: dict[str, t.Any] | None,
) -> dict[str, t.Any]:
    value = container["HostConfig"].get("NetworkMode", _SENTRY)
    if value is _SENTRY:
        return {}
    return {"network_mode": value}


def _set_values_network(
    module: AnsibleModule,
    data: dict[str, t.Any],
    api_version: LooseVersion,
    options: list[Option],
    values: dict[str, t.Any],
) -> None:
    if "network_mode" not in values:
        return
    if "HostConfig" not in data:
        data["HostConfig"] = {}
    value = values["network_mode"]
    data["HostConfig"]["NetworkMode"] = value


def _get_values_mounts(
    module: AnsibleModule,
    container: dict[str, t.Any],
    api_version: LooseVersion,
    options: list[Option],
    image: dict[str, t.Any] | None,
    host_info: dict[str, t.Any] | None,
) -> dict[str, t.Any]:
    volumes = container["Config"].get("Volumes")
    binds = container["HostConfig"].get("Binds")
    # According to https://github.com/moby/moby/, support for HostConfig.Mounts
    # has been included at least since v17.03.0-ce, which has API version 1.26.
    # The previous tag, v1.9.1, has API version 1.21 and does not have
    # HostConfig.Mounts. I have no idea what about API 1.25...
    mounts = container["HostConfig"].get("Mounts")
    if mounts is not None:
        mounts_list = []
        empty_dict: dict[str, t.Any] = {}
        for mount in mounts:
            mounts_list.append(
                {
                    "type": mount.get("Type"),
                    "source": mount.get("Source"),
                    "target": mount.get("Target"),
                    "read_only": mount.get(
                        "ReadOnly", False
                    ),  # golang's omitempty for bool returns None for False
                    "consistency": mount.get("Consistency"),
                    "propagation": mount.get("BindOptions", empty_dict).get(
                        "Propagation"
                    ),
                    "no_copy": mount.get("VolumeOptions", empty_dict).get(
                        "NoCopy", False
                    ),
                    "labels": mount.get("VolumeOptions", empty_dict).get(
                        "Labels", empty_dict
                    ),
                    "volume_driver": mount.get("VolumeOptions", empty_dict)
                    .get("DriverConfig", empty_dict)
                    .get("Name"),
                    "volume_options": mount.get("VolumeOptions", empty_dict)
                    .get("DriverConfig", empty_dict)
                    .get("Options", empty_dict),
                    "tmpfs_size": mount.get("TmpfsOptions", empty_dict).get(
                        "SizeBytes"
                    ),
                    "tmpfs_mode": mount.get("TmpfsOptions", empty_dict).get("Mode"),
                    "non_recursive": mount.get("BindOptions", empty_dict).get(
                        "NonRecursive"
                    ),
                    "create_mountpoint": mount.get("BindOptions", empty_dict).get(
                        "CreateMountpoint"
                    ),
                    "read_only_non_recursive": mount.get("BindOptions", empty_dict).get(
                        "ReadOnlyNonRecursive"
                    ),
                    "read_only_force_recursive": mount.get(
                        "BindOptions", empty_dict
                    ).get("ReadOnlyForceRecursive"),
                    "subpath": mount.get("VolumeOptions", empty_dict).get("Subpath")
                    or mount.get("ImageOptions", empty_dict).get("Subpath"),
                    "tmpfs_options": mount.get("TmpfsOptions", empty_dict).get(
                        "Options"
                    ),
                }
            )
        mounts = mounts_list
    result = {}
    if volumes is not None:
        result["volumes"] = volumes
    if binds is not None:
        result["volume_binds"] = binds
    if mounts is not None:
        result["mounts"] = mounts
    return result


def _get_bind_from_dict(volume_dict: dict[str, t.Any] | None) -> list[str]:
    results = []
    if volume_dict:
        for host_path, config in volume_dict.items():
            if isinstance(config, dict) and config.get("bind"):
                container_path = config.get("bind")
                mode = config.get("mode", "rw")
                results.append(f"{host_path}:{container_path}:{mode}")
    return results


def _get_image_binds(volumes: dict[str, t.Any] | list[dict[str, t.Any]]) -> list[str]:
    """
    Convert array of binds to array of strings with format host_path:container_path:mode

    :param volumes: array of bind dicts
    :return: array of strings
    """
    results = []
    if isinstance(volumes, dict):
        results += _get_bind_from_dict(volumes)
    elif isinstance(volumes, list):
        for vol in volumes:
            results += _get_bind_from_dict(vol)
    return results


def _get_expected_values_mounts(
    module: AnsibleModule,
    client: AnsibleDockerClient,
    api_version: LooseVersion,
    options: list[Option],
    image: dict[str, t.Any] | None,
    values: dict[str, t.Any],
    host_info: dict[str, t.Any] | None,
) -> dict[str, t.Any]:
    expected_values = {}

    # binds
    if "mounts" in values:
        expected_values["mounts"] = values["mounts"]

    # volumes
    expected_vols = {}
    if image and image["Config"].get("Volumes"):
        expected_vols.update(image["Config"].get("Volumes"))
    if "volumes" in values:
        for vol in values["volumes"]:
            # We only expect anonymous volumes to show up in the list
            if ":" in vol:
                parts = vol.split(":")
                if len(parts) == 3:
                    continue
                if len(parts) == 2 and not _is_volume_permissions(parts[1]):
                    continue
            expected_vols[vol] = {}
    if expected_vols:
        expected_values["volumes"] = expected_vols

    # binds
    image_vols = []
    if image:
        image_vols = _get_image_binds(image["Config"].get("Volumes"))
    param_vols = []
    if "volume_binds" in values:
        param_vols = values["volume_binds"]
    expected_values["volume_binds"] = list(set(image_vols + param_vols))

    return expected_values


def _set_values_mounts(
    module: AnsibleModule,
    data: dict[str, t.Any],
    api_version: LooseVersion,
    options: list[Option],
    values: dict[str, t.Any],
) -> None:
    if "mounts" in values:
        if "HostConfig" not in data:
            data["HostConfig"] = {}
        mounts: list[dict[str, t.Any]] = []
        for mount in values["mounts"]:
            mount_type = mount.get("type")
            mount_res = {
                "Target": mount.get("target"),
                "Source": mount.get("source"),
                "Type": mount_type,
                "ReadOnly": mount.get("read_only"),
            }
            if "consistency" in mount:
                mount_res["Consistency"] = mount["consistency"]
            if mount_type == "bind":
                bind_opts: dict[str, t.Any] = {}
                if "propagation" in mount:
                    bind_opts["Propagation"] = mount["propagation"]
                if "non_recursive" in mount:
                    bind_opts["NonRecursive"] = mount["non_recursive"]
                if "create_mountpoint" in mount:
                    bind_opts["CreateMountpoint"] = mount["create_mountpoint"]
                if "read_only_non_recursive" in mount:
                    bind_opts["ReadOnlyNonRecursive"] = mount["read_only_non_recursive"]
                if "read_only_force_recursive" in mount:
                    bind_opts["ReadOnlyForceRecursive"] = mount[
                        "read_only_force_recursive"
                    ]
                if bind_opts:
                    mount_res["BindOptions"] = bind_opts
            if mount_type == "volume":
                volume_opts: dict[str, t.Any] = {}
                if mount.get("no_copy"):
                    volume_opts["NoCopy"] = True
                if mount.get("labels"):
                    volume_opts["Labels"] = mount.get("labels")
                if mount.get("volume_driver"):
                    driver_config: dict[str, t.Any] = {
                        "Name": mount.get("volume_driver"),
                    }
                    if mount.get("volume_options"):
                        driver_config["Options"] = mount.get("volume_options")
                    volume_opts["DriverConfig"] = driver_config
                if "subpath" in mount:
                    volume_opts["Subpath"] = mount["subpath"]
                if volume_opts:
                    mount_res["VolumeOptions"] = volume_opts
            if mount_type == "tmpfs":
                tmpfs_opts: dict[str, t.Any] = {}
                if mount.get("tmpfs_mode"):
                    tmpfs_opts["Mode"] = mount.get("tmpfs_mode")
                if mount.get("tmpfs_size"):
                    tmpfs_opts["SizeBytes"] = mount.get("tmpfs_size")
                if "tmpfs_options" in mount:
                    tmpfs_opts["Options"] = mount["tmpfs_options"]
                if tmpfs_opts:
                    mount_res["TmpfsOptions"] = tmpfs_opts
            if mount_type == "image":
                image_opts: dict[str, t.Any] = {}
                if "subpath" in mount:
                    image_opts["Subpath"] = mount["subpath"]
                if image_opts:
                    mount_res["ImageOptions"] = image_opts
            mounts.append(mount_res)
        data["HostConfig"]["Mounts"] = mounts
    if "volumes" in values:
        volumes: dict[str, t.Any] = {}
        for volume in values["volumes"]:
            # Only pass anonymous volumes to create container
            if ":" in volume:
                parts = volume.split(":")
                if len(parts) == 3:
                    continue
                if len(parts) == 2 and not _is_volume_permissions(parts[1]):
                    continue
            volumes[volume] = {}
        data["Volumes"] = volumes
    if "volume_binds" in values:
        if "HostConfig" not in data:
            data["HostConfig"] = {}
        data["HostConfig"]["Binds"] = values["volume_binds"]


def _get_values_log(
    module: AnsibleModule,
    container: dict[str, t.Any],
    api_version: LooseVersion,
    options: list[Option],
    image: dict[str, t.Any] | None,
    host_info: dict[str, t.Any] | None,
) -> dict[str, t.Any]:
    log_config = container["HostConfig"].get("LogConfig") or {}
    return {
        "log_driver": log_config.get("Type"),
        "log_options": log_config.get("Config"),
    }


def _set_values_log(
    module: AnsibleModule,
    data: dict[str, t.Any],
    api_version: LooseVersion,
    options: list[Option],
    values: dict[str, t.Any],
) -> None:
    if "log_driver" not in values:
        return
    log_config = {
        "Type": values["log_driver"],
        "Config": values.get("log_options") or {},
    }
    if "HostConfig" not in data:
        data["HostConfig"] = {}
    data["HostConfig"]["LogConfig"] = log_config


def _get_values_platform(
    module: AnsibleModule,
    container: dict[str, t.Any],
    api_version: LooseVersion,
    options: list[Option],
    image: dict[str, t.Any] | None,
    host_info: dict[str, t.Any] | None,
) -> dict[str, t.Any]:
    if image and (image.get("Os") or image.get("Architecture") or image.get("Variant")):
        return {
            "platform": compose_platform_string(
                os=image.get("Os"),
                arch=image.get("Architecture"),
                variant=image.get("Variant"),
                daemon_os=host_info.get("OSType") if host_info else None,
                daemon_arch=host_info.get("Architecture") if host_info else None,
            )
        }
    return {
        "platform": container.get("Platform"),
    }


def _get_expected_values_platform(
    module: AnsibleModule,
    client: AnsibleDockerClient,
    api_version: LooseVersion,
    options: list[Option],
    image: dict[str, t.Any] | None,
    values: dict[str, t.Any],
    host_info: dict[str, t.Any] | None,
) -> dict[str, t.Any]:
    expected_values = {}
    if "platform" in values:
        try:
            expected_values["platform"] = normalize_platform_string(
                values["platform"],
                daemon_os=host_info.get("OSType") if host_info else None,
                daemon_arch=host_info.get("Architecture") if host_info else None,
            )
        except ValueError as exc:
            module.fail_json(msg=f"Error while parsing platform parameer: {exc}")
    return expected_values


def _set_values_platform(
    module: AnsibleModule,
    data: dict[str, t.Any],
    api_version: LooseVersion,
    options: list[Option],
    values: dict[str, t.Any],
) -> None:
    if "platform" in values:
        data["platform"] = values["platform"]


def _needs_container_image_platform(values: dict[str, t.Any]) -> bool:
    return "platform" in values


def _needs_host_info_platform(values: dict[str, t.Any]) -> bool:
    return "platform" in values


def _get_values_restart(
    module: AnsibleModule,
    container: dict[str, t.Any],
    api_version: LooseVersion,
    options: list[Option],
    image: dict[str, t.Any] | None,
    host_info: dict[str, t.Any] | None,
) -> dict[str, t.Any]:
    restart_policy = container["HostConfig"].get("RestartPolicy") or {}
    return {
        "restart_policy": restart_policy.get("Name"),
        "restart_retries": restart_policy.get("MaximumRetryCount"),
    }


def _set_values_restart(
    module: AnsibleModule,
    data: dict[str, t.Any],
    api_version: LooseVersion,
    options: list[Option],
    values: dict[str, t.Any],
) -> None:
    if "restart_policy" not in values:
        return
    restart_policy = {
        "Name": values["restart_policy"],
        "MaximumRetryCount": values.get("restart_retries"),
    }
    if "HostConfig" not in data:
        data["HostConfig"] = {}
    data["HostConfig"]["RestartPolicy"] = restart_policy


def _update_value_restart(
    module: AnsibleModule,
    data: dict[str, t.Any],
    api_version: LooseVersion,
    options: list[Option],
    values: dict[str, t.Any],
) -> None:
    if "restart_policy" not in values:
        return
    data["RestartPolicy"] = {
        "Name": values["restart_policy"],
        "MaximumRetryCount": values.get("restart_retries"),
    }


def _get_values_ports(
    module: AnsibleModule,
    container: dict[str, t.Any],
    api_version: LooseVersion,
    options: list[Option],
    image: dict[str, t.Any] | None,
    host_info: dict[str, t.Any] | None,
) -> dict[str, t.Any]:
    host_config = container["HostConfig"]
    config = container["Config"]

    # "ExposedPorts": null returns None type & causes AttributeError - PR #5517
    if config.get("ExposedPorts") is not None:
        expected_exposed = [_normalize_port(p) for p in config.get("ExposedPorts", {})]
    else:
        expected_exposed = []

    return {
        "published_ports": host_config.get("PortBindings"),
        "exposed_ports": expected_exposed,
        "publish_all_ports": host_config.get("PublishAllPorts"),
    }


def _get_expected_values_ports(
    module: AnsibleModule,
    client: AnsibleDockerClient,
    api_version: LooseVersion,
    options: list[Option],
    image: dict[str, t.Any] | None,
    values: dict[str, t.Any],
    host_info: dict[str, t.Any] | None,
) -> dict[str, t.Any]:
    expected_values: dict[str, t.Any] = {}

    if "published_ports" in values:
        expected_bound_ports = {}
        for container_port, config in values["published_ports"].items():
            if isinstance(container_port, int):
                container_port = f"{container_port}/tcp"
            if len(config) == 1:
                if isinstance(config[0], int):
                    expected_bound_ports[container_port] = [
                        {"HostIp": "0.0.0.0", "HostPort": config[0]}
                    ]
                else:
                    expected_bound_ports[container_port] = [
                        {"HostIp": config[0], "HostPort": ""}
                    ]
            elif isinstance(config[0], tuple):
                expected_bound_ports[container_port] = []
                for host_ip, host_port in config:
                    expected_bound_ports[container_port].append(
                        {
                            "HostIp": host_ip,
                            "HostPort": to_text(
                                host_port, errors="surrogate_or_strict"
                            ),
                        }
                    )
            else:
                expected_bound_ports[container_port] = [
                    {
                        "HostIp": config[0],
                        "HostPort": to_text(config[1], errors="surrogate_or_strict"),
                    }
                ]
        expected_values["published_ports"] = expected_bound_ports

    image_ports = []
    if image:
        image_exposed_ports = image["Config"].get("ExposedPorts") or {}
        image_ports = [_normalize_port(p) for p in image_exposed_ports]
    param_ports = []
    if "ports" in values:
        param_ports = [
            to_text(p[0], errors="surrogate_or_strict") + "/" + p[1]
            for p in values["ports"]
        ]
    result = list(set(image_ports + param_ports))
    expected_values["exposed_ports"] = result

    if "publish_all_ports" in values:
        expected_values["publish_all_ports"] = values["publish_all_ports"]

    return expected_values


def _set_values_ports(
    module: AnsibleModule,
    data: dict[str, t.Any],
    api_version: LooseVersion,
    options: list[Option],
    values: dict[str, t.Any],
) -> None:
    if "ports" in values:
        exposed_ports: dict[str, dict[str, t.Any]] = {}
        for port_definition in values["ports"]:
            port = port_definition
            proto = "tcp"
            if isinstance(port_definition, tuple):
                if len(port_definition) == 2:
                    proto = port_definition[1]
                port = port_definition[0]
            exposed_ports[f"{port}/{proto}"] = {}
        data["ExposedPorts"] = exposed_ports
    if "published_ports" in values:
        if "HostConfig" not in data:
            data["HostConfig"] = {}
        data["HostConfig"]["PortBindings"] = convert_port_bindings(
            values["published_ports"]
        )
    if "publish_all_ports" in values and values["publish_all_ports"]:
        if "HostConfig" not in data:
            data["HostConfig"] = {}
        data["HostConfig"]["PublishAllPorts"] = values["publish_all_ports"]


def _preprocess_value_ports(
    module: AnsibleModule,
    client: AnsibleDockerClient,
    api_version: LooseVersion,
    options: list[Option],
    values: dict[str, t.Any],
) -> dict[str, t.Any]:
    if "published_ports" not in values:
        return values
    found = False
    for port_spec in values["published_ports"].values():
        if port_spec[0] == _DEFAULT_IP_REPLACEMENT_STRING:
            found = True
            break
    if not found:
        return values
    default_ip = _get_default_host_ip(module, client)
    for port, port_spec in values["published_ports"].items():
        if port_spec[0] == _DEFAULT_IP_REPLACEMENT_STRING:
            values["published_ports"][port] = tuple([default_ip] + list(port_spec[1:]))
    return values


def _preprocess_container_names(
    module: AnsibleModule,
    client: AnsibleDockerClient,
    api_version: LooseVersion,
    value: t.Any,
) -> t.Any:
    if value is None or not value.startswith("container:"):
        return value
    container_name = value[len("container:") :]
    # Try to inspect container to see whether this is an ID or a
    # name (and in the latter case, retrieve its ID)
    container = client.get_container(container_name)
    if container is None:
        # If we cannot find the container, issue a warning and continue with
        # what the user specified.
        module.warn(f'Cannot find a container with name or ID "{container_name}"')
        return value
    return f"container:{container['Id']}"


def _get_value_command(
    module: AnsibleModule,
    container: dict[str, t.Any],
    api_version: LooseVersion,
    options: list[Option],
    image: dict[str, t.Any] | None,
    host_info: dict[str, t.Any] | None,
) -> dict[str, t.Any]:
    value = container["Config"].get("Cmd", _SENTRY)
    if value is _SENTRY:
        return {}
    return {"command": value}


def _set_value_command(
    module: AnsibleModule,
    data: dict[str, t.Any],
    api_version: LooseVersion,
    options: list[Option],
    values: dict[str, t.Any],
) -> None:
    if "command" not in values:
        return
    value = values["command"]
    data["Cmd"] = value


def _get_expected_values_command(
    module: AnsibleModule,
    client: AnsibleDockerClient,
    api_version: LooseVersion,
    options: list[Option],
    image: dict[str, t.Any] | None,
    values: dict[str, t.Any],
    host_info: dict[str, t.Any] | None,
) -> dict[str, t.Any]:
    expected_values = {}
    if "command" in values:
        command = values["command"]
        if command == [] and image and image["Config"].get("Cmd"):
            command = image["Config"].get("Cmd")
        expected_values["command"] = command
    return expected_values


def _needs_container_image_command(values: dict[str, t.Any]) -> bool:
    return values.get("command") == []


OPTION_AUTO_REMOVE.add_engine(
    "docker_api", DockerAPIEngine.host_config_value("AutoRemove")
)

OPTION_BLKIO_WEIGHT.add_engine(
    "docker_api",
    DockerAPIEngine.host_config_value("BlkioWeight", update_parameter="BlkioWeight"),
)

OPTION_CAPABILITIES.add_engine(
    "docker_api", DockerAPIEngine.host_config_value("CapAdd")
)

OPTION_CAP_DROP.add_engine("docker_api", DockerAPIEngine.host_config_value("CapDrop"))

OPTION_CGROUP_NS_MODE.add_engine(
    "docker_api",
    DockerAPIEngine.host_config_value("CgroupnsMode", min_api_version="1.41"),
)

OPTION_CGROUP_PARENT.add_engine(
    "docker_api", DockerAPIEngine.host_config_value("CgroupParent")
)

OPTION_COMMAND.add_engine(
    "docker_api",
    DockerAPIEngine(
        get_value=_get_value_command,
        set_value=_set_value_command,
        get_expected_values=_get_expected_values_command,
        needs_container_image=_needs_container_image_command,
    ),
)

OPTION_CPU_PERIOD.add_engine(
    "docker_api",
    DockerAPIEngine.host_config_value("CpuPeriod", update_parameter="CpuPeriod"),
)

OPTION_CPU_QUOTA.add_engine(
    "docker_api",
    DockerAPIEngine.host_config_value("CpuQuota", update_parameter="CpuQuota"),
)

OPTION_CPUSET_CPUS.add_engine(
    "docker_api",
    DockerAPIEngine.host_config_value("CpusetCpus", update_parameter="CpusetCpus"),
)

OPTION_CPUSET_MEMS.add_engine(
    "docker_api",
    DockerAPIEngine.host_config_value("CpusetMems", update_parameter="CpusetMems"),
)

OPTION_CPU_SHARES.add_engine(
    "docker_api",
    DockerAPIEngine.host_config_value("CpuShares", update_parameter="CpuShares"),
)

OPTION_ENTRYPOINT.add_engine("docker_api", DockerAPIEngine.config_value("Entrypoint"))

OPTION_CPUS.add_engine(
    "docker_api",
    DockerAPIEngine.host_config_value("NanoCpus", preprocess_value=_preprocess_cpus),
)

OPTION_DETACH_INTERACTIVE.add_engine(
    "docker_api",
    DockerAPIEngine(
        get_value=_get_value_detach_interactive, set_value=_set_value_detach_interactive
    ),
)

OPTION_DEVICES.add_engine(
    "docker_api",
    DockerAPIEngine.host_config_value("Devices", preprocess_value=_preprocess_devices),
)

OPTION_DEVICE_READ_BPS.add_engine(
    "docker_api",
    DockerAPIEngine.host_config_value(
        "BlkioDeviceReadBps", preprocess_value=_preprocess_rate_bps
    ),
)

OPTION_DEVICE_WRITE_BPS.add_engine(
    "docker_api",
    DockerAPIEngine.host_config_value(
        "BlkioDeviceWriteBps", preprocess_value=_preprocess_rate_bps
    ),
)

OPTION_DEVICE_READ_IOPS.add_engine(
    "docker_api",
    DockerAPIEngine.host_config_value(
        "BlkioDeviceReadIOps", preprocess_value=_preprocess_rate_iops
    ),
)

OPTION_DEVICE_WRITE_IOPS.add_engine(
    "docker_api",
    DockerAPIEngine.host_config_value(
        "BlkioDeviceWriteIOps", preprocess_value=_preprocess_rate_iops
    ),
)

OPTION_DEVICE_REQUESTS.add_engine(
    "docker_api",
    DockerAPIEngine.host_config_value(
        "DeviceRequests",
        min_api_version="1.40",
        preprocess_value=_preprocess_device_requests,
    ),
)

OPTION_DEVICE_CGROUP_RULES.add_engine(
    "docker_api",
    DockerAPIEngine.host_config_value("DeviceCgroupRules", min_api_version="1.28"),
)

OPTION_DNS_SERVERS.add_engine("docker_api", DockerAPIEngine.host_config_value("Dns"))

OPTION_DNS_OPTS.add_engine(
    "docker_api", DockerAPIEngine.host_config_value("DnsOptions")
)

OPTION_DNS_SEARCH_DOMAINS.add_engine(
    "docker_api", DockerAPIEngine.host_config_value("DnsSearch")
)

OPTION_DOMAINNAME.add_engine("docker_api", DockerAPIEngine.config_value("Domainname"))

OPTION_ENVIRONMENT.add_engine(
    "docker_api",
    DockerAPIEngine.config_value("Env", get_expected_value=_get_expected_env_value),
)

OPTION_ETC_HOSTS.add_engine(
    "docker_api",
    DockerAPIEngine.host_config_value(
        "ExtraHosts", preprocess_value=_preprocess_etc_hosts
    ),
)

OPTION_GROUPS.add_engine("docker_api", DockerAPIEngine.host_config_value("GroupAdd"))

OPTION_HEALTHCHECK.add_engine(
    "docker_api",
    DockerAPIEngine.config_value(
        "Healthcheck",
        preprocess_value=_preprocess_healthcheck,
        postprocess_for_get=_postprocess_healthcheck_get_value,
        extra_option_minimal_versions={
            "healthcheck.start_interval": {
                "docker_api_version": "1.44",
                "detect_usage": lambda c: c.module.params["healthcheck"]
                and c.module.params["healthcheck"]["start_interval"] is not None,
            },
        },
    ),
)

OPTION_HOSTNAME.add_engine("docker_api", DockerAPIEngine.config_value("Hostname"))

OPTION_IMAGE.add_engine(
    "docker_api",
    DockerAPIEngine.config_value(
        "Image",
        ignore_mismatching_result=lambda module, client, api_version, option, image, container_value, expected_value, host_info: True,
    ),
)

OPTION_INIT.add_engine("docker_api", DockerAPIEngine.host_config_value("Init"))

OPTION_IPC_MODE.add_engine(
    "docker_api",
    DockerAPIEngine.host_config_value(
        "IpcMode", preprocess_value=_preprocess_container_names
    ),
)

OPTION_KERNEL_MEMORY.add_engine(
    "docker_api",
    DockerAPIEngine.host_config_value("KernelMemory", update_parameter="KernelMemory"),
)

OPTION_LABELS.add_engine(
    "docker_api",
    DockerAPIEngine.config_value(
        "Labels",
        get_expected_value=_get_expected_labels_value,
        ignore_mismatching_result=_ignore_mismatching_label_result,
    ),
)

OPTION_LINKS.add_engine(
    "docker_api",
    DockerAPIEngine.host_config_value("Links", preprocess_value=_preprocess_links),
)

OPTION_LOG_DRIVER_OPTIONS.add_engine(
    "docker_api",
    DockerAPIEngine(
        get_value=_get_values_log,
        set_value=_set_values_log,
    ),
)

OPTION_MAC_ADDRESS.add_engine("docker_api", DockerAPIEngine.config_value("MacAddress"))

OPTION_MEMORY.add_engine(
    "docker_api", DockerAPIEngine.host_config_value("Memory", update_parameter="Memory")
)

OPTION_MEMORY_RESERVATION.add_engine(
    "docker_api",
    DockerAPIEngine.host_config_value(
        "MemoryReservation", update_parameter="MemoryReservation"
    ),
)

OPTION_MEMORY_SWAP.add_engine(
    "docker_api",
    DockerAPIEngine.host_config_value("MemorySwap", update_parameter="MemorySwap"),
)

OPTION_MEMORY_SWAPPINESS.add_engine(
    "docker_api", DockerAPIEngine.host_config_value("MemorySwappiness")
)

OPTION_STOP_TIMEOUT.add_engine(
    "docker_api", DockerAPIEngine.config_value("StopTimeout")
)

OPTION_NETWORK.add_engine(
    "docker_api",
    DockerAPIEngine(
        preprocess_value=_preprocess_network_values,
        get_value=_get_values_network,
        set_value=_set_values_network,
        ignore_mismatching_result=_ignore_mismatching_network_result,
        needs_host_info=_needs_host_info_network,
        extra_option_minimal_versions={
            "networks.mac_address": {
                "docker_api_version": "1.44",
                "detect_usage": lambda c: any(
                    net_info.get("mac_address") is not None
                    for net_info in (c.module.params["networks"] or [])
                ),
            },
            "networks.driver_opts": {
                "docker_api_version": "1.32",
                "detect_usage": lambda c: any(
                    net_info.get("driver_opts") is not None
                    for net_info in (c.module.params["networks"] or [])
                ),
            },
            "networks.gw_priority": {
                "docker_api_version": "1.48",
                "detect_usage": lambda c: any(
                    net_info.get("gw_priority") is not None
                    for net_info in (c.module.params["networks"] or [])
                ),
            },
        },
    ),
)

OPTION_OOM_KILLER.add_engine(
    "docker_api", DockerAPIEngine.host_config_value("OomKillDisable")
)

OPTION_OOM_SCORE_ADJ.add_engine(
    "docker_api", DockerAPIEngine.host_config_value("OomScoreAdj")
)

OPTION_PID_MODE.add_engine(
    "docker_api",
    DockerAPIEngine.host_config_value(
        "PidMode", preprocess_value=_preprocess_container_names
    ),
)

OPTION_PIDS_LIMIT.add_engine(
    "docker_api", DockerAPIEngine.host_config_value("PidsLimit")
)

OPTION_PLATFORM.add_engine(
    "docker_api",
    DockerAPIEngine(
        get_value=_get_values_platform,
        set_value=_set_values_platform,
        get_expected_values=_get_expected_values_platform,
        needs_container_image=_needs_container_image_platform,
        needs_host_info=_needs_host_info_platform,
        min_api_version="1.41",
    ),
)

OPTION_PRIVILEGED.add_engine(
    "docker_api", DockerAPIEngine.host_config_value("Privileged")
)

OPTION_READ_ONLY.add_engine(
    "docker_api", DockerAPIEngine.host_config_value("ReadonlyRootfs")
)

OPTION_RESTART_POLICY.add_engine(
    "docker_api",
    DockerAPIEngine(
        get_value=_get_values_restart,
        set_value=_set_values_restart,
        update_value=_update_value_restart,
    ),
)

OPTION_RUNTIME.add_engine("docker_api", DockerAPIEngine.host_config_value("Runtime"))

OPTION_SECURITY_OPTS.add_engine(
    "docker_api", DockerAPIEngine.host_config_value("SecurityOpt")
)

OPTION_SHM_SIZE.add_engine("docker_api", DockerAPIEngine.host_config_value("ShmSize"))

OPTION_STOP_SIGNAL.add_engine("docker_api", DockerAPIEngine.config_value("StopSignal"))

OPTION_STORAGE_OPTS.add_engine(
    "docker_api", DockerAPIEngine.host_config_value("StorageOpt")
)

OPTION_SYSCTLS.add_engine("docker_api", DockerAPIEngine.host_config_value("Sysctls"))

OPTION_TMPFS.add_engine("docker_api", DockerAPIEngine.host_config_value("Tmpfs"))

OPTION_TTY.add_engine("docker_api", DockerAPIEngine.config_value("Tty"))

OPTION_ULIMITS.add_engine("docker_api", DockerAPIEngine.host_config_value("Ulimits"))

OPTION_USER.add_engine("docker_api", DockerAPIEngine.config_value("User"))

OPTION_USERNS_MODE.add_engine(
    "docker_api", DockerAPIEngine.host_config_value("UsernsMode")
)

OPTION_UTS.add_engine("docker_api", DockerAPIEngine.host_config_value("UTSMode"))

OPTION_VOLUME_DRIVER.add_engine(
    "docker_api", DockerAPIEngine.host_config_value("VolumeDriver")
)

OPTION_VOLUMES_FROM.add_engine(
    "docker_api", DockerAPIEngine.host_config_value("VolumesFrom")
)

OPTION_WORKING_DIR.add_engine("docker_api", DockerAPIEngine.config_value("WorkingDir"))

OPTION_MOUNTS_VOLUMES.add_engine(
    "docker_api",
    DockerAPIEngine(
        get_value=_get_values_mounts,
        get_expected_values=_get_expected_values_mounts,
        set_value=_set_values_mounts,
        extra_option_minimal_versions={
            "mounts.non_recursive": {
                "docker_api_version": "1.40",
                "detect_usage": lambda c: any(
                    mount.get("non_recursive") is not None
                    for mount in (c.module.params["mounts"] or [])
                ),
            },
            "mounts.create_mountpoint": {
                "docker_api_version": "1.42",
                "detect_usage": lambda c: any(
                    mount.get("create_mountpoint") is not None
                    for mount in (c.module.params["mounts"] or [])
                ),
            },
            "mounts.type=cluster": {
                "docker_api_version": "1.42",
                "detect_usage": lambda c: any(
                    mount.get("type") == "cluster"
                    for mount in (c.module.params["mounts"] or [])
                ),
            },
            "mounts.read_only_non_recursive": {
                "docker_api_version": "1.44",
                "detect_usage": lambda c: any(
                    mount.get("read_only_non_recursive") is not None
                    for mount in (c.module.params["mounts"] or [])
                ),
            },
            "mounts.read_only_force_recursive": {
                "docker_api_version": "1.44",
                "detect_usage": lambda c: any(
                    mount.get("read_only_force_recursive") is not None
                    for mount in (c.module.params["mounts"] or [])
                ),
            },
            "mounts.subpath": {
                "docker_api_version": "1.45",
                "detect_usage": lambda c: any(
                    mount.get("subpath") is not None
                    for mount in (c.module.params["mounts"] or [])
                ),
            },
            "mounts.tmpfs_options": {
                "docker_api_version": "1.46",
                "detect_usage": lambda c: any(
                    mount.get("tmpfs_options") is not None
                    for mount in (c.module.params["mounts"] or [])
                ),
            },
            "mounts.type=image": {
                "docker_api_version": "1.47",
                "detect_usage": lambda c: any(
                    mount.get("type") == "image"
                    for mount in (c.module.params["mounts"] or [])
                ),
            },
        },
    ),
)

OPTION_PORTS.add_engine(
    "docker_api",
    DockerAPIEngine(
        get_value=_get_values_ports,
        get_expected_values=_get_expected_values_ports,
        set_value=_set_values_ports,
        preprocess_value=_preprocess_value_ports,
    ),
)
