# Copyright 2016 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Note that this module util is **PRIVATE** to the collection. It can have breaking changes at any time.
# Do not use this from other collections or standalone plugins/modules!

from __future__ import annotations

import abc
import os
import platform
import re
import sys
import traceback
import typing as t
from collections.abc import Mapping, Sequence

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible.module_utils.parsing.convert_bool import BOOLEANS_FALSE, BOOLEANS_TRUE

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
from ansible_collections.community.docker.plugins.module_utils._version import (
    LooseVersion,
)

HAS_DOCKER_PY_2 = False  # pylint: disable=invalid-name
HAS_DOCKER_PY_3 = False  # pylint: disable=invalid-name
HAS_DOCKER_ERROR: None | str  # pylint: disable=invalid-name
HAS_DOCKER_TRACEBACK: None | str  # pylint: disable=invalid-name
docker_version: str | None  # pylint: disable=invalid-name

try:
    from docker import __version__ as docker_version
    from docker.errors import APIError, TLSParameterError
    from docker.tls import TLSConfig

    if LooseVersion(docker_version) >= LooseVersion("3.0.0"):
        HAS_DOCKER_PY_3 = True  # pylint: disable=invalid-name
        from docker import APIClient as Client
    elif LooseVersion(docker_version) >= LooseVersion("2.0.0"):
        HAS_DOCKER_PY_2 = True  # pylint: disable=invalid-name
        from docker import APIClient as Client
    else:
        from docker import Client  # type: ignore

except ImportError as exc:
    HAS_DOCKER_ERROR = str(exc)  # pylint: disable=invalid-name
    HAS_DOCKER_TRACEBACK = traceback.format_exc()  # pylint: disable=invalid-name
    HAS_DOCKER_PY = False  # pylint: disable=invalid-name
    docker_version = None  # pylint: disable=invalid-name
else:
    HAS_DOCKER_PY = True  # pylint: disable=invalid-name
    HAS_DOCKER_ERROR = None  # pylint: disable=invalid-name
    HAS_DOCKER_TRACEBACK = None  # pylint: disable=invalid-name


try:
    from requests.exceptions import (  # noqa: F401, pylint: disable=unused-import
        RequestException,
    )
except ImportError:
    # Either Docker SDK for Python is no longer using requests, or Docker SDK for Python is not around either,
    # or Docker SDK for Python's dependency requests is missing. In any case, define an exception
    # class RequestException so that our code does not break.
    class RequestException(Exception):  # type: ignore
        pass


if t.TYPE_CHECKING:
    from collections.abc import Callable


MIN_DOCKER_VERSION = "2.0.0"


if not HAS_DOCKER_PY:
    # No Docker SDK for Python. Create a place holder client to allow
    # instantiation of AnsibleModule and proper error handing
    class Client:  # type: ignore # noqa: F811, pylint: disable=function-redefined
        def __init__(self, **kwargs: t.Any) -> None:
            pass

    class APIError(Exception):  # type: ignore # noqa: F811, pylint: disable=function-redefined
        pass

    class NotFound(Exception):  # type: ignore # noqa: F811, pylint: disable=function-redefined
        pass


def _get_tls_config(
    fail_function: Callable[[str], t.NoReturn], **kwargs: t.Any
) -> TLSConfig:
    if "assert_hostname" in kwargs and LooseVersion(docker_version) >= LooseVersion(
        "7.0.0b1"
    ):
        assert_hostname = kwargs.pop("assert_hostname")
        if assert_hostname is not None:
            fail_function(
                "tls_hostname is not compatible with Docker SDK for Python 7.0.0+. You are using"
                f" Docker SDK for Python {docker_version}. The tls_hostname option (value: {assert_hostname})"
                " has either been set directly or with the environment variable DOCKER_TLS_HOSTNAME."
                " Make sure it is not set, or switch to an older version of Docker SDK for Python."
            )
    # Filter out all None parameters
    kwargs = dict((k, v) for k, v in kwargs.items() if v is not None)
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
        if LooseVersion(docker_version) < LooseVersion("4.4.0"):
            fail_function(
                "use_ssh_client=True requires Docker SDK for Python 4.4.0 or newer"
            )
        result["use_ssh_client"] = True

    # No TLS
    return result


DOCKERPYUPGRADE_SWITCH_TO_DOCKER = (
    "Try `pip uninstall docker-py` followed by `pip install docker`."
)
DOCKERPYUPGRADE_UPGRADE_DOCKER = "Use `pip install --upgrade docker` to upgrade."


class AnsibleDockerClientBase(Client):
    def __init__(
        self,
        min_docker_version: str | None = None,
        min_docker_api_version: str | None = None,
    ) -> None:
        if min_docker_version is None:
            min_docker_version = MIN_DOCKER_VERSION

        self.docker_py_version = LooseVersion(docker_version)

        if not HAS_DOCKER_PY:
            msg = missing_required_lib("Docker SDK for Python: docker>=5.0.0")
            msg = f"{msg}, for example via `pip install docker`. The error was: {HAS_DOCKER_ERROR}"
            self.fail(msg, exception=HAS_DOCKER_TRACEBACK)

        if self.docker_py_version < LooseVersion(min_docker_version):
            msg = (
                f"Error: Docker SDK for Python version is {docker_version} ({platform.node()}'s Python {sys.executable})."
                f" Minimum version required is {min_docker_version}."
            )
            if docker_version < LooseVersion("2.0"):
                msg += DOCKERPYUPGRADE_SWITCH_TO_DOCKER
            else:
                msg += DOCKERPYUPGRADE_UPGRADE_DOCKER
            self.fail(msg)

        self._connect_params = get_connect_params(
            self.auth_params, fail_function=self.fail
        )

        try:
            super().__init__(**self._connect_params)
            self.docker_api_version_str = self.api_version
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

        update_tls_hostname(result)

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
        min_docker_version: str | None = None,
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

        super().__init__(
            min_docker_version=min_docker_version,
            min_docker_api_version=min_docker_api_version,
        )

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
            support_docker_py = True
            support_docker_api = True
            if "docker_py_version" in data:
                support_docker_py = self.docker_py_version >= LooseVersion(
                    data["docker_py_version"]
                )
            if "docker_api_version" in data:
                support_docker_api = self.docker_api_version >= LooseVersion(
                    data["docker_api_version"]
                )
            data["supported"] = support_docker_py and support_docker_api
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
                    elif not support_docker_py:
                        msg = (
                            f"Docker SDK for Python version is {docker_version} ({platform.node()}'s Python {sys.executable})."
                            f" Minimum version required is {data['docker_py_version']} to {usg}. {DOCKERPYUPGRADE_UPGRADE_DOCKER}"
                        )
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
