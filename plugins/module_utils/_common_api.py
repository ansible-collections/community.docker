# Copyright 2016 Red Hat | Ansible
# Copyright (c) 2022 Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Note that this module util is **PRIVATE** to the collection. It can have breaking changes at any time.
# Do not use this from other collections or standalone plugins/modules!

from __future__ import annotations

import abc
import os
import re
import typing as t
from collections.abc import Mapping, Sequence

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible.module_utils.parsing.convert_bool import BOOLEANS_FALSE, BOOLEANS_TRUE

from ansible_collections.community.docker.plugins.module_utils._version import (
    LooseVersion,
)


try:
    from requests.exceptions import (  # noqa: F401, pylint: disable=unused-import
        RequestException,
        SSLError,
    )
except ImportError:
    # Define an exception class RequestException so that our code does not break.
    class RequestException(Exception):  # type: ignore
        pass


from ansible_collections.community.docker.plugins.module_utils._api import auth
from ansible_collections.community.docker.plugins.module_utils._api.api.client import (
    APIClient as Client,
)
from ansible_collections.community.docker.plugins.module_utils._api.errors import (
    APIError,
    MissingRequirementException,
    NotFound,
    TLSParameterError,
)
from ansible_collections.community.docker.plugins.module_utils._api.tls import TLSConfig
from ansible_collections.community.docker.plugins.module_utils._api.utils.utils import (
    convert_filters,
    parse_repository_tag,
)
from ansible_collections.community.docker.plugins.module_utils._util import (
    DEFAULT_DOCKER_HOST,
    DEFAULT_TIMEOUT_SECONDS,
    DEFAULT_TLS,
    DEFAULT_TLS_VERIFY,
    DOCKER_COMMON_ARGS,
    DOCKER_MUTUALLY_EXCLUSIVE,
    DOCKER_REQUIRED_TOGETHER,
    sanitize_result,
    update_tls_hostname,
)


if t.TYPE_CHECKING:
    from collections.abc import Callable


def _get_tls_config(
    fail_function: Callable[[str], t.NoReturn], **kwargs: t.Any
) -> TLSConfig:
    try:
        return TLSConfig(**kwargs)
    except TLSParameterError as exc:
        fail_function(f"TLS config error: {exc}")


def is_using_tls(auth_data: dict[str, t.Any]) -> bool:
    return auth_data["tls_verify"] or auth_data["tls"]


def get_connect_params(
    auth_data: dict[str, t.Any], fail_function: Callable[[str], t.NoReturn]
) -> dict[str, t.Any]:
    if is_using_tls(auth_data):
        auth_data["docker_host"] = auth_data["docker_host"].replace(
            "tcp://", "https://"
        )

    result = {
        "base_url": auth_data["docker_host"],
        "version": auth_data["api_version"],
        "timeout": auth_data["timeout"],
    }

    if auth_data["tls_verify"]:
        # TLS with verification
        tls_config = {
            "verify": True,
            "assert_hostname": auth_data["tls_hostname"],
            "fail_function": fail_function,
        }
        if auth_data["cert_path"] and auth_data["key_path"]:
            tls_config["client_cert"] = (auth_data["cert_path"], auth_data["key_path"])
        if auth_data["cacert_path"]:
            tls_config["ca_cert"] = auth_data["cacert_path"]
        result["tls"] = _get_tls_config(**tls_config)
    elif auth_data["tls"]:
        # TLS without verification
        tls_config = {
            "verify": False,
            "fail_function": fail_function,
        }
        if auth_data["cert_path"] and auth_data["key_path"]:
            tls_config["client_cert"] = (auth_data["cert_path"], auth_data["key_path"])
        result["tls"] = _get_tls_config(**tls_config)

    if auth_data.get("use_ssh_client"):
        result["use_ssh_client"] = True

    # No TLS
    return result


class AnsibleDockerClientBase(Client):
    def __init__(self, min_docker_api_version: str | None = None) -> None:
        self._connect_params = get_connect_params(
            self.auth_params, fail_function=self.fail
        )

        try:
            super().__init__(**self._connect_params)
            self.docker_api_version_str = self.api_version
        except MissingRequirementException as exc:
            self.fail(
                missing_required_lib(exc.requirement), exception=exc.import_exception
            )
        except APIError as exc:
            self.fail(f"Docker API error: {exc}")
        except Exception as exc:  # pylint: disable=broad-exception-caught
            self.fail(f"Error connecting: {exc}")

        self.docker_api_version = LooseVersion(self.docker_api_version_str)
        min_docker_api_version = min_docker_api_version or "1.25"
        if self.docker_api_version < LooseVersion(min_docker_api_version):
            self.fail(
                f"Docker API version is {self.docker_api_version_str}. Minimum version required is {min_docker_api_version}."
            )

    def log(self, msg: t.Any, pretty_print: bool = False) -> None:
        pass
        # if self.debug:
        #     from .util import log_debug
        #     log_debug(msg, pretty_print=pretty_print)

    @abc.abstractmethod
    def fail(self, msg: str, **kwargs: t.Any) -> t.NoReturn:
        pass

    @abc.abstractmethod
    def deprecate(
        self,
        msg: str,
        version: str | None = None,
        date: str | None = None,
        collection_name: str | None = None,
    ) -> None:
        pass

    @staticmethod
    def _get_value(
        param_name: str,
        param_value: t.Any,
        env_variable: str | None,
        default_value: t.Any | None,
        value_type: t.Literal["str", "bool", "int"] = "str",
    ) -> t.Any:
        if param_value is not None:
            # take module parameter value
            if value_type == "bool":
                if param_value in BOOLEANS_TRUE:
                    return True
                if param_value in BOOLEANS_FALSE:
                    return False
                return bool(param_value)
            if value_type == "int":
                return int(param_value)
            return param_value

        if env_variable is not None:
            env_value = os.environ.get(env_variable)
            if env_value is not None:
                # take the env variable value
                if param_name == "cert_path":
                    return os.path.join(env_value, "cert.pem")
                if param_name == "cacert_path":
                    return os.path.join(env_value, "ca.pem")
                if param_name == "key_path":
                    return os.path.join(env_value, "key.pem")
                if value_type == "bool":
                    if env_value in BOOLEANS_TRUE:
                        return True
                    if env_value in BOOLEANS_FALSE:
                        return False
                    return bool(env_value)
                if value_type == "int":
                    return int(env_value)
                return env_value

        # take the default
        return default_value

    @abc.abstractmethod
    def _get_params(self) -> dict[str, t.Any]:
        pass

    @property
    def auth_params(self) -> dict[str, t.Any]:
        # Get authentication credentials.
        # Precedence: module parameters-> environment variables-> defaults.

        self.log("Getting credentials")

        client_params = self._get_params()

        params = {}
        for key in DOCKER_COMMON_ARGS:
            params[key] = client_params.get(key)

        result = {
            "docker_host": self._get_value(
                "docker_host",
                params["docker_host"],
                "DOCKER_HOST",
                DEFAULT_DOCKER_HOST,
                value_type="str",
            ),
            "tls_hostname": self._get_value(
                "tls_hostname",
                params["tls_hostname"],
                "DOCKER_TLS_HOSTNAME",
                None,
                value_type="str",
            ),
            "api_version": self._get_value(
                "api_version",
                params["api_version"],
                "DOCKER_API_VERSION",
                "auto",
                value_type="str",
            ),
            "cacert_path": self._get_value(
                "cacert_path",
                params["ca_path"],
                "DOCKER_CERT_PATH",
                None,
                value_type="str",
            ),
            "cert_path": self._get_value(
                "cert_path",
                params["client_cert"],
                "DOCKER_CERT_PATH",
                None,
                value_type="str",
            ),
            "key_path": self._get_value(
                "key_path",
                params["client_key"],
                "DOCKER_CERT_PATH",
                None,
                value_type="str",
            ),
            "tls": self._get_value(
                "tls", params["tls"], "DOCKER_TLS", DEFAULT_TLS, value_type="bool"
            ),
            "tls_verify": self._get_value(
                "validate_certs",
                params["validate_certs"],
                "DOCKER_TLS_VERIFY",
                DEFAULT_TLS_VERIFY,
                value_type="bool",
            ),
            "timeout": self._get_value(
                "timeout",
                params["timeout"],
                "DOCKER_TIMEOUT",
                DEFAULT_TIMEOUT_SECONDS,
                value_type="int",
            ),
            "use_ssh_client": self._get_value(
                "use_ssh_client",
                params["use_ssh_client"],
                None,
                False,
                value_type="bool",
            ),
        }

        def depr(*args: t.Any, **kwargs: t.Any) -> None:
            self.deprecate(*args, **kwargs)

        update_tls_hostname(
            result,
            old_behavior=True,
            deprecate_function=depr,
            uses_tls=is_using_tls(result),
        )

        return result

    def _handle_ssl_error(self, error: Exception) -> t.NoReturn:
        match = re.match(r"hostname.*doesn\'t match (\'.*\')", str(error))
        if match:
            hostname = self.auth_params["tls_hostname"]
            self.fail(
                f"You asked for verification that Docker daemons certificate's hostname matches {hostname}. "
                f"The actual certificate's hostname is {match.group(1)}. Most likely you need to set DOCKER_TLS_HOSTNAME "
                f"or pass `tls_hostname` with a value of {match.group(1)}. You may also use TLS without verification by "
                "setting the `tls` parameter to true."
            )
        self.fail(f"SSL Exception: {error}")

    def get_container_by_id(self, container_id: str) -> dict[str, t.Any] | None:
        try:
            self.log(f"Inspecting container Id {container_id}")
            result = self.get_json("/containers/{0}/json", container_id)
            self.log("Completed container inspection")
            return result
        except NotFound:
            return None
        except Exception as exc:  # pylint: disable=broad-exception-caught
            self.fail(f"Error inspecting container: {exc}")

    def get_container(self, name: str | None) -> dict[str, t.Any] | None:
        """
        Lookup a container and return the inspection results.
        """
        if name is None:
            return None

        search_name = name
        if not name.startswith("/"):
            search_name = "/" + name

        result = None
        try:
            params = {
                "limit": -1,
                "all": 1,
                "size": 0,
                "trunc_cmd": 0,
            }
            containers = self.get_json("/containers/json", params=params)
            for container in containers:
                self.log(f"testing container: {container['Names']}")
                if (
                    isinstance(container["Names"], list)
                    and search_name in container["Names"]
                ):
                    result = container
                    break
                if container["Id"].startswith(name):
                    result = container
                    break
                if container["Id"] == name:
                    result = container
                    break
        except SSLError as exc:
            self._handle_ssl_error(exc)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            self.fail(f"Error retrieving container list: {exc}")

        if result is None:
            return None

        return self.get_container_by_id(result["Id"])

    def get_network(
        self, name: str | None = None, network_id: str | None = None
    ) -> dict[str, t.Any] | None:
        """
        Lookup a network and return the inspection results.
        """
        if name is None and network_id is None:
            return None

        result = None

        if network_id is None:
            try:
                networks = self.get_json("/networks")
                for network in networks:
                    self.log(f"testing network: {network['Name']}")
                    if name == network["Name"]:
                        result = network
                        break
                    if network["Id"].startswith(name):
                        result = network
                        break
            except SSLError as exc:
                self._handle_ssl_error(exc)
            except Exception as exc:  # pylint: disable=broad-exception-caught
                self.fail(f"Error retrieving network list: {exc}")

        if result is not None:
            network_id = result["Id"]

        if network_id is not None:
            try:
                self.log(f"Inspecting network Id {network_id}")
                result = self.get_json("/networks/{0}", network_id)
                self.log("Completed network inspection")
            except NotFound:
                return None
            except Exception as exc:  # pylint: disable=broad-exception-caught
                self.fail(f"Error inspecting network: {exc}")

        return result

    def _image_lookup(self, name: str, tag: str | None) -> list[dict[str, t.Any]]:
        """
        Including a tag in the name parameter sent to the Docker SDK for Python images method
        does not work consistently. Instead, get the result set for name and manually check
        if the tag exists.
        """
        try:
            params: dict[str, t.Any] = {
                "only_ids": 0,
                "all": 0,
            }
            if LooseVersion(self.api_version) < LooseVersion("1.25"):
                # only use "filter" on API 1.24 and under, as it is deprecated
                params["filter"] = name
            else:
                params["filters"] = convert_filters({"reference": name})
            images = self.get_json("/images/json", params=params)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            self.fail(f"Error searching for image {name} - {exc}")
        if tag:
            lookup = f"{name}:{tag}"
            lookup_digest = f"{name}@{tag}"
            response = images
            images = []
            for image in response:
                tags = image.get("RepoTags")
                digests = image.get("RepoDigests")
                if (tags and lookup in tags) or (digests and lookup_digest in digests):
                    images = [image]
                    break
        return images

    def find_image(self, name: str, tag: str | None) -> dict[str, t.Any] | None:
        """
        Lookup an image (by name and tag) and return the inspection results.
        """
        if not name:
            return None

        self.log(f"Find image {name}:{tag}")
        images = self._image_lookup(name, tag)
        if not images:
            # In API <= 1.20 seeing 'docker.io/<name>' as the name of images pulled from docker hub
            registry, repo_name = auth.resolve_repository_name(name)
            if registry == "docker.io":
                # If docker.io is explicitly there in name, the image
                # is not found in some cases (#41509)
                self.log(f"Check for docker.io image: {repo_name}")
                images = self._image_lookup(repo_name, tag)
                if not images and repo_name.startswith("library/"):
                    # Sometimes library/xxx images are not found
                    lookup = repo_name[len("library/") :]
                    self.log(f"Check for docker.io image: {lookup}")
                    images = self._image_lookup(lookup, tag)
                if not images:
                    # Last case for some Docker versions: if docker.io was not there,
                    # it can be that the image was not found either
                    # (https://github.com/ansible/ansible/pull/15586)
                    lookup = f"{registry}/{repo_name}"
                    self.log(f"Check for docker.io image: {lookup}")
                    images = self._image_lookup(lookup, tag)
                if not images and "/" not in repo_name:
                    # This seems to be happening with podman-docker
                    # (https://github.com/ansible-collections/community.docker/issues/291)
                    lookup = f"{registry}/library/{repo_name}"
                    self.log(f"Check for docker.io image: {lookup}")
                    images = self._image_lookup(lookup, tag)

        if len(images) > 1:
            self.fail(f"Daemon returned more than one result for {name}:{tag}")

        if len(images) == 1:
            try:
                return self.get_json("/images/{0}/json", images[0]["Id"])
            except NotFound:
                self.log(f"Image {name}:{tag} not found.")
                return None
            except Exception as exc:  # pylint: disable=broad-exception-caught
                self.fail(f"Error inspecting image {name}:{tag} - {exc}")

        self.log(f"Image {name}:{tag} not found.")
        return None

    def find_image_by_id(
        self, image_id: str, accept_missing_image: bool = False
    ) -> dict[str, t.Any] | None:
        """
        Lookup an image (by ID) and return the inspection results.
        """
        if not image_id:
            return None

        self.log(f"Find image {image_id} (by ID)")
        try:
            return self.get_json("/images/{0}/json", image_id)
        except NotFound as exc:
            if not accept_missing_image:
                self.fail(f"Error inspecting image ID {image_id} - {exc}")
            self.log(f"Image {image_id} not found.")
            return None
        except Exception as exc:  # pylint: disable=broad-exception-caught
            self.fail(f"Error inspecting image ID {image_id} - {exc}")

    def pull_image(
        self, name: str, tag: str = "latest", image_platform: str | None = None
    ) -> tuple[dict[str, t.Any] | None, bool]:
        """
        Pull an image
        """
        self.log(f"Pulling image {name}:{tag}")
        old_tag = self.find_image(name, tag)
        try:
            repository, image_tag = parse_repository_tag(name)
            registry, dummy_repo_name = auth.resolve_repository_name(repository)
            params = {
                "tag": tag or image_tag or "latest",
                "fromImage": repository,
            }
            if image_platform is not None:
                params["platform"] = image_platform

            headers = {}
            header = auth.get_config_header(self, registry)
            if header:
                headers["X-Registry-Auth"] = header

            response = self._post(
                self._url("/images/create"),
                params=params,
                headers=headers,
                stream=True,
                timeout=None,
            )
            self._raise_for_status(response)
            for line in self._stream_helper(response, decode=True):
                self.log(line, pretty_print=True)
                if line.get("error"):
                    if line.get("errorDetail"):
                        error_detail = line.get("errorDetail")
                        self.fail(
                            f"Error pulling {name} - code: {error_detail.get('code')} message: {error_detail.get('message')}"
                        )
                    else:
                        self.fail(f"Error pulling {name} - {line.get('error')}")
        except Exception as exc:  # pylint: disable=broad-exception-caught
            self.fail(f"Error pulling image {name}:{tag} - {exc}")

        new_tag = self.find_image(name, tag)

        return new_tag, old_tag == new_tag


class AnsibleDockerClient(AnsibleDockerClientBase):
    def __init__(
        self,
        argument_spec: dict[str, t.Any] | None = None,
        supports_check_mode: bool = False,
        mutually_exclusive: Sequence[Sequence[str]] | None = None,
        required_together: Sequence[Sequence[str]] | None = None,
        required_if: (
            Sequence[
                tuple[str, t.Any, Sequence[str]]
                | tuple[str, t.Any, Sequence[str], bool]
            ]
            | None
        ) = None,
        required_one_of: Sequence[Sequence[str]] | None = None,
        required_by: dict[str, Sequence[str]] | None = None,
        min_docker_api_version: str | None = None,
        option_minimal_versions: dict[str, t.Any] | None = None,
        option_minimal_versions_ignore_params: Sequence[str] | None = None,
        fail_results: dict[str, t.Any] | None = None,
    ):
        # Modules can put information in here which will always be returned
        # in case client.fail() is called.
        self.fail_results = fail_results or {}

        merged_arg_spec = {}
        merged_arg_spec.update(DOCKER_COMMON_ARGS)
        if argument_spec:
            merged_arg_spec.update(argument_spec)
            self.arg_spec = merged_arg_spec

        mutually_exclusive_params: list[Sequence[str]] = []
        mutually_exclusive_params += DOCKER_MUTUALLY_EXCLUSIVE
        if mutually_exclusive:
            mutually_exclusive_params += mutually_exclusive

        required_together_params: list[Sequence[str]] = []
        required_together_params += DOCKER_REQUIRED_TOGETHER
        if required_together:
            required_together_params += required_together

        self.module = AnsibleModule(
            argument_spec=merged_arg_spec,
            supports_check_mode=supports_check_mode,
            mutually_exclusive=mutually_exclusive_params,
            required_together=required_together_params,
            required_if=required_if,
            required_one_of=required_one_of,
            required_by=required_by or {},
        )

        self.debug = self.module.params.get("debug")
        self.check_mode = self.module.check_mode

        super().__init__(min_docker_api_version=min_docker_api_version)

        if option_minimal_versions is not None:
            self._get_minimal_versions(
                option_minimal_versions, option_minimal_versions_ignore_params
            )

    def fail(self, msg: str, **kwargs: t.Any) -> t.NoReturn:
        self.fail_results.update(kwargs)
        self.module.fail_json(msg=msg, **sanitize_result(self.fail_results))

    def deprecate(
        self,
        msg: str,
        version: str | None = None,
        date: str | None = None,
        collection_name: str | None = None,
    ) -> None:
        self.module.deprecate(
            msg, version=version, date=date, collection_name=collection_name
        )

    def _get_params(self) -> dict[str, t.Any]:
        return self.module.params

    def _get_minimal_versions(
        self,
        option_minimal_versions: dict[str, t.Any],
        ignore_params: Sequence[str] | None = None,
    ) -> None:
        self.option_minimal_versions: dict[str, dict[str, t.Any]] = {}
        for option in self.module.argument_spec:
            if ignore_params is not None and option in ignore_params:
                continue
            self.option_minimal_versions[option] = {}
        self.option_minimal_versions.update(option_minimal_versions)

        for option, data in self.option_minimal_versions.items():
            # Test whether option is supported, and store result
            support_docker_api = True
            if "docker_api_version" in data:
                support_docker_api = self.docker_api_version >= LooseVersion(
                    data["docker_api_version"]
                )
            data["supported"] = support_docker_api
            # Fail if option is not supported but used
            if not data["supported"]:
                # Test whether option is specified
                if "detect_usage" in data:
                    used = data["detect_usage"](self)
                else:
                    used = self.module.params.get(option) is not None
                    if used and "default" in self.module.argument_spec[option]:
                        used = (
                            self.module.params[option]
                            != self.module.argument_spec[option]["default"]
                        )
                if used:
                    # If the option is used, compose error message.
                    if "usage_msg" in data:
                        usg = data["usage_msg"]
                    else:
                        usg = f"set {option} option"
                    if not support_docker_api:
                        msg = f"Docker API version is {self.docker_api_version_str}. Minimum version required is {data['docker_api_version']} to {usg}."
                    else:
                        # should not happen
                        msg = f"Cannot {usg} with your configuration."
                    self.fail(msg)

    def report_warnings(
        self, result: t.Any, warnings_key: Sequence[str] | None = None
    ) -> None:
        """
        Checks result of client operation for warnings, and if present, outputs them.

        warnings_key should be a list of keys used to crawl the result dictionary.
        For example, if warnings_key == ['a', 'b'], the function will consider
        result['a']['b'] if these keys exist. If the result is a non-empty string, it
        will be reported as a warning. If the result is a list, every entry will be
        reported as a warning.

        In most cases (if warnings are returned at all), warnings_key should be
        ['Warnings'] or ['Warning']. The default value (if not specified) is ['Warnings'].
        """
        if warnings_key is None:
            warnings_key = ["Warnings"]
        for key in warnings_key:
            if not isinstance(result, Mapping):
                return
            result = result.get(key)
        if isinstance(result, Sequence):
            for warning in result:
                self.module.warn(f"Docker warning: {warning}")
        elif isinstance(result, str) and result:
            self.module.warn(f"Docker warning: {result}")
