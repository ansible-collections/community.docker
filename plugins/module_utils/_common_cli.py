# Copyright (c) 2023, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Note that this module util is **PRIVATE** to the collection. It can have breaking changes at any time.
# Do not use this from other collections or standalone plugins/modules!

from __future__ import annotations

import abc
import json
import shlex
import typing as t

from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.common.process import get_bin_path
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.community.docker.plugins.module_utils._api.auth import (
    resolve_repository_name,
)
from ansible_collections.community.docker.plugins.module_utils._util import (
    DEFAULT_DOCKER_HOST,
    DEFAULT_TLS,
    DEFAULT_TLS_VERIFY,
    DOCKER_MUTUALLY_EXCLUSIVE,
    DOCKER_REQUIRED_TOGETHER,
    sanitize_result,
)
from ansible_collections.community.docker.plugins.module_utils._version import (
    LooseVersion,
)


if t.TYPE_CHECKING:
    from collections.abc import Mapping, Sequence


DOCKER_COMMON_ARGS = {
    "docker_cli": {"type": "path"},
    "docker_host": {
        "type": "str",
        "fallback": (env_fallback, ["DOCKER_HOST"]),
        "aliases": ["docker_url"],
    },
    "tls_hostname": {
        "type": "str",
        "fallback": (env_fallback, ["DOCKER_TLS_HOSTNAME"]),
    },
    "api_version": {
        "type": "str",
        "default": "auto",
        "fallback": (env_fallback, ["DOCKER_API_VERSION"]),
        "aliases": ["docker_api_version"],
    },
    "ca_path": {"type": "path", "aliases": ["ca_cert", "tls_ca_cert", "cacert_path"]},
    "client_cert": {"type": "path", "aliases": ["tls_client_cert", "cert_path"]},
    "client_key": {"type": "path", "aliases": ["tls_client_key", "key_path"]},
    "tls": {
        "type": "bool",
        "default": DEFAULT_TLS,
        "fallback": (env_fallback, ["DOCKER_TLS"]),
    },
    "validate_certs": {
        "type": "bool",
        "default": DEFAULT_TLS_VERIFY,
        "fallback": (env_fallback, ["DOCKER_TLS_VERIFY"]),
        "aliases": ["tls_verify"],
    },
    # "debug": {"type": "bool", "default: False},
    "cli_context": {"type": "str"},
}


class DockerException(Exception):
    pass


class AnsibleDockerClientBase:
    docker_api_version_str: str | None
    docker_api_version: LooseVersion | None

    def __init__(
        self,
        common_args: dict[str, t.Any],
        min_docker_api_version: str | None = None,
        needs_api_version: bool = True,
    ) -> None:
        self._environment: dict[str, str] = {}
        if common_args["tls_hostname"]:
            self._environment["DOCKER_TLS_HOSTNAME"] = common_args["tls_hostname"]
        if common_args["api_version"] and common_args["api_version"] != "auto":
            self._environment["DOCKER_API_VERSION"] = common_args["api_version"]
        cli = common_args.get("docker_cli")
        if cli is None:
            try:
                cli = get_bin_path("docker")
            except ValueError:
                self.fail(
                    "Cannot find docker CLI in path. Please provide it explicitly with the docker_cli parameter"
                )
        self._cli = cli
        self._cli_base = [self._cli]
        docker_host = common_args["docker_host"]
        if not docker_host and not common_args["cli_context"]:
            docker_host = DEFAULT_DOCKER_HOST
        if docker_host:
            self._cli_base.extend(["--host", docker_host])
        if common_args["validate_certs"]:
            self._cli_base.append("--tlsverify")
        elif common_args["tls"]:
            self._cli_base.append("--tls")
        if common_args["ca_path"]:
            self._cli_base.extend(["--tlscacert", common_args["ca_path"]])
        if common_args["client_cert"]:
            self._cli_base.extend(["--tlscert", common_args["client_cert"]])
        if common_args["client_key"]:
            self._cli_base.extend(["--tlskey", common_args["client_key"]])
        if common_args["cli_context"]:
            self._cli_base.extend(["--context", common_args["cli_context"]])

        # `--format json` was only added as a shorthand for `--format {{ json . }}` in Docker 23.0
        dummy, self._version, dummy2 = self.call_cli_json(
            "version", "--format", "{{ json . }}", check_rc=True
        )
        self._info: dict[str, t.Any] | None = None

        if needs_api_version:
            if not isinstance(self._version.get("Server"), dict) or not isinstance(
                self._version["Server"].get("ApiVersion"), str
            ):
                self.fail(
                    "Cannot determine Docker Daemon information. Are you maybe using podman instead of docker?"
                )
            self.docker_api_version_str = to_text(self._version["Server"]["ApiVersion"])
            self.docker_api_version = LooseVersion(self.docker_api_version_str)
            min_docker_api_version = min_docker_api_version or "1.25"
            if self.docker_api_version < LooseVersion(min_docker_api_version):
                self.fail(
                    f"Docker API version is {self.docker_api_version_str}. Minimum version required is {min_docker_api_version}."
                )
        else:
            self.docker_api_version_str = None
            self.docker_api_version = None
            if min_docker_api_version is not None:
                self.fail(
                    "Internal error: cannot have needs_api_version=False with min_docker_api_version not None"
                )

    def log(self, msg: str, pretty_print: bool = False) -> None:
        pass
        # if self.debug:
        #     from .util import log_debug
        #     log_debug(msg, pretty_print=pretty_print)

    def get_cli(self) -> str:
        return self._cli

    def get_version_info(self) -> str:
        return self._version

    def _compose_cmd(self, args: t.Sequence[str]) -> list[str]:
        return self._cli_base + list(args)

    def _compose_cmd_str(self, args: t.Sequence[str]) -> str:
        return " ".join(shlex.quote(a) for a in self._compose_cmd(args))

    @abc.abstractmethod
    def call_cli(
        self,
        *args: str,
        check_rc: bool = False,
        data: bytes | None = None,
        cwd: str | None = None,
        environ_update: dict[str, str] | None = None,
    ) -> tuple[int, bytes, bytes]:
        pass

    def call_cli_json(
        self,
        *args: str,
        check_rc: bool = False,
        data: bytes | None = None,
        cwd: str | None = None,
        environ_update: dict[str, str] | None = None,
        warn_on_stderr: bool = False,
    ) -> tuple[int, t.Any, bytes]:
        rc, stdout, stderr = self.call_cli(
            *args, check_rc=check_rc, data=data, cwd=cwd, environ_update=environ_update
        )
        if warn_on_stderr and stderr:
            self.warn(to_text(stderr))
        try:
            data = json.loads(stdout)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            self.fail(
                f"Error while parsing JSON output of {self._compose_cmd_str(args)}: {exc}\nJSON output: {to_text(stdout)}"
            )
        return rc, data, stderr

    def call_cli_json_stream(
        self,
        *args: str,
        check_rc: bool = False,
        data: bytes | None = None,
        cwd: str | None = None,
        environ_update: dict[str, str] | None = None,
        warn_on_stderr: bool = False,
    ) -> tuple[int, list[t.Any], bytes]:
        rc, stdout, stderr = self.call_cli(
            *args, check_rc=check_rc, data=data, cwd=cwd, environ_update=environ_update
        )
        if warn_on_stderr and stderr:
            self.warn(to_text(stderr))
        result = []
        try:
            for line in stdout.splitlines():
                line = line.strip()
                if line.startswith(b"{"):
                    result.append(json.loads(line))
        except Exception as exc:  # pylint: disable=broad-exception-caught
            self.fail(
                f"Error while parsing JSON output of {self._compose_cmd_str(args)}: {exc}\nJSON output: {to_text(stdout)}"
            )
        return rc, result, stderr

    @abc.abstractmethod
    def fail(self, msg: str, **kwargs: t.Any) -> t.NoReturn:
        pass

    @abc.abstractmethod
    def warn(self, msg: str) -> None:
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

    def get_cli_info(self) -> dict[str, t.Any]:
        if self._info is None:
            dummy, self._info, dummy2 = self.call_cli_json(
                "info", "--format", "{{ json . }}", check_rc=True
            )
        return self._info

    def get_client_plugin_info(self, component: str) -> dict[str, t.Any] | None:
        cli_info = self.get_cli_info()
        if not isinstance(cli_info.get("ClientInfo"), dict):
            self.fail(
                "Cannot determine Docker client information. Are you maybe using podman instead of docker?"
            )
        for plugin in cli_info["ClientInfo"].get("Plugins") or []:
            if plugin.get("Name") == component:
                return plugin
        return None

    def _image_lookup(self, name: str, tag: str) -> list[dict[str, t.Any]]:
        """
        Including a tag in the name parameter sent to the Docker SDK for Python images method
        does not work consistently. Instead, get the result set for name and manually check
        if the tag exists.
        """
        dummy, images, dummy2 = self.call_cli_json_stream(
            "image",
            "ls",
            "--format",
            "{{ json . }}",
            "--no-trunc",
            "--filter",
            f"reference={name}",
            check_rc=True,
        )
        if tag:
            response = images
            images = []
            for image in response:
                if image.get("Tag") == tag or image.get("Digest") == tag:
                    images = [image]
                    break
        return images

    @t.overload
    def find_image(self, name: None, tag: str) -> None: ...

    @t.overload
    def find_image(self, name: str, tag: str) -> dict[str, t.Any] | None: ...

    def find_image(self, name: str | None, tag: str) -> dict[str, t.Any] | None:
        """
        Lookup an image (by name and tag) and return the inspection results.
        """
        if not name:
            return None

        self.log(f"Find image {name}:{tag}")
        images = self._image_lookup(name, tag)
        if not images:
            # In API <= 1.20 seeing 'docker.io/<name>' as the name of images pulled from docker hub
            registry, repo_name = resolve_repository_name(name)
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
            rc, image, stderr = self.call_cli_json("image", "inspect", images[0]["ID"])
            if not image:
                self.log(f"Image {name}:{tag} not found.")
                return None
            if rc != 0:
                self.fail(f"Error inspecting image {name}:{tag} - {to_text(stderr)}")
            return image[0]

        self.log(f"Image {name}:{tag} not found.")
        return None

    @t.overload
    def find_image_by_id(
        self, image_id: None, accept_missing_image: bool = False
    ) -> None: ...

    @t.overload
    def find_image_by_id(
        self, image_id: str | None, accept_missing_image: bool = False
    ) -> dict[str, t.Any] | None: ...

    def find_image_by_id(
        self, image_id: str | None, accept_missing_image: bool = False
    ) -> dict[str, t.Any] | None:
        """
        Lookup an image (by ID) and return the inspection results.
        """
        if not image_id:
            return None

        self.log(f"Find image {image_id} (by ID)")
        rc, image, stderr = self.call_cli_json("image", "inspect", image_id)
        if not image:
            if not accept_missing_image:
                self.fail(f"Error inspecting image ID {image_id} - {to_text(stderr)}")
            self.log(f"Image {image_id} not found.")
            return None
        if rc != 0:
            self.fail(f"Error inspecting image ID {image_id} - {to_text(stderr)}")
        return image[0]


class AnsibleModuleDockerClient(AnsibleDockerClientBase):
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
        required_by: Mapping[str, Sequence[str]] | None = None,
        min_docker_api_version: str | None = None,
        fail_results: dict[str, t.Any] | None = None,
        needs_api_version: bool = True,
    ) -> None:
        # Modules can put information in here which will always be returned
        # in case client.fail() is called.
        self.fail_results = fail_results or {}

        merged_arg_spec = {}
        merged_arg_spec.update(DOCKER_COMMON_ARGS)
        if argument_spec:
            merged_arg_spec.update(argument_spec)
            self.arg_spec = merged_arg_spec

        mutually_exclusive_params: list[Sequence[str]] = [
            ("docker_host", "cli_context")
        ]
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

        self.debug = False  # self.module.params['debug']
        self.check_mode = self.module.check_mode
        self.diff = self.module._diff

        common_args = dict((k, self.module.params[k]) for k in DOCKER_COMMON_ARGS)
        super().__init__(
            common_args,
            min_docker_api_version=min_docker_api_version,
            needs_api_version=needs_api_version,
        )

    def call_cli(
        self,
        *args: str,
        check_rc: bool = False,
        data: bytes | None = None,
        cwd: str | None = None,
        environ_update: dict[str, str] | None = None,
    ) -> tuple[int, bytes, bytes]:
        environment = self._environment.copy()
        if environ_update:
            environment.update(environ_update)
        rc, stdout, stderr = self.module.run_command(
            self._compose_cmd(args),
            binary_data=True,
            check_rc=check_rc,
            cwd=cwd,
            data=data,
            encoding=None,
            environ_update=environment,
            expand_user_and_vars=False,
            ignore_invalid_cwd=False,
        )
        return rc, stdout, stderr

    def fail(self, msg: str, **kwargs: t.Any) -> t.NoReturn:
        self.fail_results.update(kwargs)
        self.module.fail_json(msg=msg, **sanitize_result(self.fail_results))

    def warn(self, msg: str) -> None:
        self.module.warn(msg)

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
