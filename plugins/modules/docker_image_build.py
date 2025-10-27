#!/usr/bin/python
#
# Copyright (c) 2023, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations


DOCUMENTATION = r"""
module: docker_image_build

short_description: Build Docker images using Docker buildx

version_added: 3.6.0

description:
  - This module allows you to build Docker images using Docker's buildx plugin (BuildKit).
  - Note that the module is B(not idempotent) in the sense of classical Ansible modules. The only idempotence check is whether
    the built image already exists. This check can be disabled with the O(rebuild) option.
extends_documentation_fragment:
  - community.docker._docker.cli_documentation
  - community.docker._attributes
  - community.docker._attributes.actiongroup_docker

attributes:
  check_mode:
    support: full
  diff_mode:
    support: none
  idempotent:
    support: partial
    details:
      - If O(rebuild=always) the module is not idempotent.

options:
  name:
    description:
      - 'Image name. Name format will be one of: C(name), C(repository/name), C(registry_server:port/name). When pushing or
        pulling an image the name can optionally include the tag by appending C(:tag_name).'
      - Note that image IDs (hashes) and names with digest cannot be used.
    type: str
    required: true
  tag:
    description:
      - Tag for the image name O(name) that is to be tagged.
      - If O(name)'s format is C(name:tag), then the tag value from O(name) will take precedence.
    type: str
    default: latest
  path:
    description:
      - The path for the build environment.
    type: path
    required: true
  dockerfile:
    description:
      - Provide an alternate name for the Dockerfile to use when building an image.
      - This can also include a relative path (relative to O(path)).
    type: str
  cache_from:
    description:
      - List of image names to consider as cache source.
    type: list
    elements: str
  pull:
    description:
      - When building an image downloads any updates to the FROM image in Dockerfile.
    type: bool
    default: false
  network:
    description:
      - The network to use for C(RUN) build instructions.
    type: str
  nocache:
    description:
      - Do not use cache when building an image.
    type: bool
    default: false
  etc_hosts:
    description:
      - Extra hosts to add to C(/etc/hosts) in building containers, as a mapping of hostname to IP address.
      - Instead of an IP address, the special value V(host-gateway) can also be used, which resolves to the host's gateway
        IP and allows building containers to connect to services running on the host.
    type: dict
  args:
    description:
      - Provide a dictionary of C(key:value) build arguments that map to Dockerfile ARG directive.
      - Docker expects the value to be a string. For convenience any non-string values will be converted to strings.
    type: dict
  target:
    description:
      - When building an image specifies an intermediate build stage by name as a final stage for the resulting image.
    type: str
  platform:
    description:
      - Platforms in the format C(os[/arch[/variant]]).
      - Since community.docker 3.10.0 this can be a list of platforms, instead of just a single platform.
    type: list
    elements: str
  shm_size:
    description:
      - Size of C(/dev/shm) in format C(<number>[<unit>]). Number is positive integer. Unit can be V(B) (byte), V(K) (kibibyte,
        1024B), V(M) (mebibyte), V(G) (gibibyte), V(T) (tebibyte), or V(P) (pebibyte).
      - Omitting the unit defaults to bytes. If you omit the size entirely, Docker daemon uses V(64M).
    type: str
  labels:
    description:
      - Dictionary of key value pairs.
    type: dict
  rebuild:
    description:
      - Defines the behavior of the module if the image to build (as specified in O(name) and O(tag)) already exists.
    type: str
    choices:
      - never
      - always
    default: never
  secrets:
    description:
      - Secrets to expose to the build.
    type: list
    elements: dict
    version_added: 3.10.0
    suboptions:
      id:
        description:
          - The secret identifier.
          - The secret will be made available as a file in the container under C(/run/secrets/<id>).
        type: str
        required: true
      type:
        description:
          - Type of the secret.
        type: str
        choices:
          file:
            - Reads the secret from a file on the target.
            - The file must be specified in O(secrets[].src).
          env:
            - Reads the secret from an environment variable on the target.
            - The environment variable must be named in O(secrets[].env).
            - Note that this requires the Buildkit plugin to have version 0.6.0 or newer.
          value:
            - Provides the secret from a given value O(secrets[].value).
            - B(Note) that the secret will be passed as an environment variable to C(docker compose). Use another mean of
              transport if you consider this not safe enough.
            - Note that this requires the Buildkit plugin to have version 0.6.0 or newer.
        required: true
      src:
        description:
          - Source path of the secret.
          - Only supported and required for O(secrets[].type=file).
        type: path
      env:
        description:
          - Environment value of the secret.
          - Only supported and required for O(secrets[].type=env).
        type: str
      value:
        description:
          - Value of the secret.
          - B(Note) that the secret will be passed as an environment variable to C(docker compose). Use another mean of transport
            if you consider this not safe enough.
          - Only supported and required for O(secrets[].type=value).
        type: str
  outputs:
    description:
      - Output destinations.
      - You can provide a list of exporters to export the built image in various places. Note that not all exporters might
        be supported by the build driver used.
      - Note that depending on how this option is used, no image with name O(name) and tag O(tag) might be created, which
        can cause the basic idempotency this module offers to not work.
      - Providing an empty list to this option is equivalent to not specifying it at all. The default behavior is a single
        entry with O(outputs[].type=image).
      - B(Note) that since community.docker 4.2.0, an entry for O(name)/O(tag) is added if O(outputs) has at least one entry
        and no entry has type O(outputs[].type=image) and includes O(name)/O(tag) in O(outputs[].name). This is because the
        module would otherwise pass C(--tag name:image) to the buildx plugin, which for some reason overwrites all images
        in O(outputs) by the C(name:image) provided in O(name)/O(tag).
    type: list
    elements: dict
    version_added: 3.10.0
    suboptions:
      type:
        description:
          - The type of exporter to use.
        type: str
        choices:
          local:
            - This export type writes all result files to a directory on the client. The new files will be owned by the current
              user. On multi-platform builds, all results will be put in subdirectories by their platform.
            - The destination has to be provided in O(outputs[].dest).
          tar:
            - This export type export type writes all result files as a single tarball on the client. On multi-platform builds,
              all results will be put in subdirectories by their platform.
            - The destination has to be provided in O(outputs[].dest).
          oci:
            - This export type writes the result image or manifest list as an L(OCI image layout,
              https://github.com/opencontainers/image-spec/blob/v1.0.1/image-layout.md)
              tarball on the client.
            - The destination has to be provided in O(outputs[].dest).
          docker:
            - This export type writes the single-platform result image as a Docker image specification tarball on the client.
              Tarballs created by this exporter are also OCI compatible.
            - The destination can be provided in O(outputs[].dest). If not specified, the tar will be loaded automatically
              to the local image store.
            - The Docker context where to import the result can be provided in O(outputs[].context).
          image:
            - This exporter writes the build result as an image or a manifest list. When using this driver, the image will
              appear in C(docker images).
            - The image name can be provided in O(outputs[].name). If it is not provided, O(name) and O(tag) will be used.
            - Optionally, image can be automatically pushed to a registry by setting O(outputs[].push=true).
        required: true
      dest:
        description:
          - The destination path.
          - Required for O(outputs[].type=local), O(outputs[].type=tar), O(outputs[].type=oci).
          - Optional for O(outputs[].type=docker).
        type: path
      context:
        description:
          - Name for the Docker context where to import the result.
          - Optional for O(outputs[].type=docker).
        type: str
      name:
        description:
          - Name(s) under which the image is stored under.
          - If not provided, O(name) and O(tag) will be used.
          - Optional for O(outputs[].type=image).
          - This can be a list of strings since community.docker 4.2.0.
        type: list
        elements: str
      push:
        description:
          - Whether to push the built image to a registry.
          - Only used for O(outputs[].type=image).
        type: bool
        default: false
requirements:
  - "Docker CLI with Docker buildx plugin"

author:
  - Felix Fontein (@felixfontein)

seealso:
  - module: community.docker.docker_image_push
  - module: community.docker.docker_image_tag
"""

EXAMPLES = r"""
---
- name: Build Python 3.12 image
  community.docker.docker_image_build:
    name: localhost/python/3.12:latest
    path: /home/user/images/python
    dockerfile: Dockerfile-3.12

- name: Build multi-platform image
  community.docker.docker_image_build:
    name: multi-platform-image
    tag: "1.5.2"
    path: /home/user/images/multi-platform
    platform:
      - linux/amd64
      - linux/arm64/v8
"""

RETURN = r"""
image:
  description: Image inspection results for the affected image.
  returned: success
  type: dict
  sample: {}

command:
  description: The command executed.
  returned: success and for some failures
  type: list
  elements: str
  version_added: 4.2.0
"""

import base64
import os
import traceback
import typing as t

from ansible.module_utils.common.text.converters import to_text
from ansible.module_utils.common.text.formatters import human_to_bytes

from ansible_collections.community.docker.plugins.module_utils._api.utils.utils import (
    parse_repository_tag,
)
from ansible_collections.community.docker.plugins.module_utils._common_cli import (
    AnsibleModuleDockerClient,
    DockerException,
)
from ansible_collections.community.docker.plugins.module_utils._util import (
    DockerBaseClass,
    clean_dict_booleans_for_docker_api,
    is_image_name_id,
    is_valid_tag,
)
from ansible_collections.community.docker.plugins.module_utils._version import (
    LooseVersion,
)


if t.TYPE_CHECKING:
    from ansible.module_utils.basic import AnsibleModule


def convert_to_bytes(
    value: str | None,
    module: AnsibleModule,
    name: str,
    unlimited_value: int | None = None,
) -> int | None:
    if value is None:
        return value
    try:
        if unlimited_value is not None and value in ("unlimited", str(unlimited_value)):
            return unlimited_value
        return human_to_bytes(value)
    except ValueError as exc:
        module.fail_json(msg=f"Failed to convert {name} to bytes: {exc}")


def dict_to_list(dictionary: dict[str, t.Any], concat: str = "=") -> list[str]:
    return [f"{k}{concat}{v}" for k, v in sorted(dictionary.items())]


def _quote_csv(text: str) -> str:
    if text.strip() == text and all(i not in text for i in '",\r\n'):
        return text
    text = text.replace('"', '""')
    return f'"{text}"'


class ImageBuilder(DockerBaseClass):
    def __init__(self, client: AnsibleModuleDockerClient) -> None:
        super().__init__()
        self.client = client
        self.check_mode = self.client.check_mode
        parameters = self.client.module.params

        self.cache_from = parameters["cache_from"]
        self.pull = parameters["pull"]
        self.network = parameters["network"]
        self.nocache = parameters["nocache"]
        self.etc_hosts = clean_dict_booleans_for_docker_api(parameters["etc_hosts"])
        self.args = clean_dict_booleans_for_docker_api(parameters["args"])
        self.target = parameters["target"]
        self.platform = parameters["platform"]
        self.shm_size = convert_to_bytes(
            parameters["shm_size"], self.client.module, "shm_size"
        )
        self.labels = clean_dict_booleans_for_docker_api(parameters["labels"])
        self.rebuild = parameters["rebuild"]
        self.secrets = parameters["secrets"]
        self.outputs = parameters["outputs"]

        buildx = self.client.get_client_plugin_info("buildx")
        if buildx is None:
            self.fail(
                f"Docker CLI {self.client.get_cli()} does not have the buildx plugin installed"
            )
        buildx_version = buildx["Version"].lstrip("v")

        if self.secrets:
            for secret in self.secrets:
                if secret["type"] in ("env", "value") and LooseVersion(
                    buildx_version
                ) < LooseVersion("0.6.0"):
                    self.fail(
                        f"The Docker buildx plugin has version {buildx_version}, but 0.6.0 is needed for secrets of type=env and type=value"
                    )
        if (
            self.outputs
            and len(self.outputs) > 1
            and LooseVersion(buildx_version) < LooseVersion("0.13.0")
        ):
            self.fail(
                f"The Docker buildx plugin has version {buildx_version}, but 0.13.0 is needed to specify more than one output"
            )

        self.path = parameters["path"]
        if not os.path.isdir(self.path):
            self.fail(f'"{self.path}" is not an existing directory')
        self.dockerfile = parameters["dockerfile"]
        if self.dockerfile and not os.path.isfile(
            os.path.join(self.path, self.dockerfile)
        ):
            self.fail(
                f'"{os.path.join(self.path, self.dockerfile)}" is not an existing file'
            )

        self.name = parameters["name"]
        self.tag = parameters["tag"]
        if not is_valid_tag(self.tag, allow_empty=True):
            self.fail(f'"{self.tag}" is not a valid docker tag')
        if is_image_name_id(self.name):
            self.fail("Image name must not be a digest")

        # If name contains a tag, it takes precedence over tag parameter.
        repo, repo_tag = parse_repository_tag(self.name)
        if repo_tag:
            self.name = repo
            self.tag = repo_tag

        if is_image_name_id(self.tag):
            self.fail("Image name must not contain a digest, but have a tag")

        if self.outputs:
            found = False
            name_tag = f"{self.name}:{self.tag}"
            for output in self.outputs:
                if output["type"] == "image":
                    if not output["name"]:
                        # Since we no longer pass --tag if --output is provided, we need to set this manually
                        output["name"] = [name_tag]
                    if output["name"] and name_tag in output["name"]:
                        found = True
            if not found:
                self.outputs.append(
                    {
                        "type": "image",
                        "name": [name_tag],
                        "push": False,
                    }
                )
                if LooseVersion(buildx_version) < LooseVersion("0.13.0"):
                    self.fail(
                        f"The output does not include an image with name {name_tag}, and the Docker"
                        f" buildx plugin has version {buildx_version} which only supports one output."
                    )

    def fail(self, msg: str, **kwargs: t.Any) -> t.NoReturn:
        self.client.fail(msg, **kwargs)

    def add_list_arg(self, args: list[str], option: str, values: list[str]) -> None:
        for value in values:
            args.extend([option, value])

    def add_args(self, args: list[str]) -> dict[str, t.Any]:
        environ_update = {}
        if not self.outputs:
            args.extend(["--tag", f"{self.name}:{self.tag}"])
        if self.dockerfile:
            args.extend(["--file", os.path.join(self.path, self.dockerfile)])
        if self.cache_from:
            self.add_list_arg(args, "--cache-from", self.cache_from)
        if self.pull:
            args.append("--pull")
        if self.network:
            args.extend(["--network", self.network])
        if self.nocache:
            args.append("--no-cache")
        if self.etc_hosts:
            self.add_list_arg(args, "--add-host", dict_to_list(self.etc_hosts, ":"))
        if self.args:
            self.add_list_arg(args, "--build-arg", dict_to_list(self.args))
        if self.target:
            args.extend(["--target", self.target])
        if self.platform:
            for platform in self.platform:
                args.extend(["--platform", platform])
        if self.shm_size:
            args.extend(["--shm-size", str(self.shm_size)])
        if self.labels:
            self.add_list_arg(args, "--label", dict_to_list(self.labels))
        if self.secrets:
            random_prefix = None
            for index, secret in enumerate(self.secrets):
                sid = secret["id"]
                if secret["type"] == "file":
                    src = secret["src"]
                    args.extend(["--secret", f"id={sid},type=file,src={src}"])
                if secret["type"] == "env":
                    env = secret["src"]
                    args.extend(["--secret", f"id={sid},type=env,env={env}"])
                if secret["type"] == "value":
                    # We pass values on using environment variables. The user has been warned in the documentation
                    # that they should only use this mechanism when being comfortable with it.
                    if random_prefix is None:
                        # Use /dev/urandom to generate some entropy to make the environment variable's name unguessable
                        random_prefix = (
                            base64.b64encode(os.urandom(16))
                            .decode("utf-8")
                            .replace("=", "")
                        )
                    env_name = (
                        f"ANSIBLE_DOCKER_COMPOSE_ENV_SECRET_{random_prefix}_{index}"
                    )
                    environ_update[env_name] = secret["value"]
                    args.extend(["--secret", f"id={sid},type=env,env={env_name}"])
        if self.outputs:
            for output in self.outputs:
                subargs = []
                if output["type"] == "local":
                    dest = output["dest"]
                    subargs.extend(["type=local", f"dest={dest}"])
                if output["type"] == "tar":
                    dest = output["dest"]
                    subargs.extend(["type=tar", f"dest={dest}"])
                if output["type"] == "oci":
                    dest = output["dest"]
                    subargs.extend(["type=oci", f"dest={dest}"])
                if output["type"] == "docker":
                    subargs.append("type=docker")
                    dest = output["dest"]
                    if output["dest"] is not None:
                        subargs.append(f"dest={dest}")
                    if output["context"] is not None:
                        context = output["context"]
                        subargs.append(f"context={context}")
                if output["type"] == "image":
                    subargs.append("type=image")
                    if output["name"] is not None:
                        name = ",".join(output["name"])
                        subargs.append(f"name={name}")
                    if output["push"]:
                        subargs.append("push=true")
                if subargs:
                    args.extend(
                        ["--output", ",".join(_quote_csv(subarg) for subarg in subargs)]
                    )
        return environ_update

    def build_image(self) -> dict[str, t.Any]:
        image = self.client.find_image(self.name, self.tag)
        results: dict[str, t.Any] = {
            "changed": False,
            "actions": [],
            "image": image or {},
        }

        if image and self.rebuild == "never":
            return results

        results["changed"] = True
        if not self.check_mode:
            args = ["buildx", "build", "--progress", "plain"]
            environ_update = self.add_args(args)
            args.extend(["--", self.path])
            rc, stdout, stderr = self.client.call_cli(
                *args, environ_update=environ_update
            )
            if rc != 0:
                self.fail(
                    f"Building {self.name}:{self.tag} failed",
                    stdout=to_text(stdout),
                    stderr=to_text(stderr),
                    command=args,
                )
            results["stdout"] = to_text(stdout)
            results["stderr"] = to_text(stderr)
            results["image"] = self.client.find_image(self.name, self.tag) or {}
            results["command"] = args

        return results


def main() -> None:
    argument_spec = {
        "name": {"type": "str", "required": True},
        "tag": {"type": "str", "default": "latest"},
        "path": {"type": "path", "required": True},
        "dockerfile": {"type": "str"},
        "cache_from": {"type": "list", "elements": "str"},
        "pull": {"type": "bool", "default": False},
        "network": {"type": "str"},
        "nocache": {"type": "bool", "default": False},
        "etc_hosts": {"type": "dict"},
        "args": {"type": "dict"},
        "target": {"type": "str"},
        "platform": {"type": "list", "elements": "str"},
        "shm_size": {"type": "str"},
        "labels": {"type": "dict"},
        "rebuild": {"type": "str", "choices": ["never", "always"], "default": "never"},
        "secrets": {
            "type": "list",
            "elements": "dict",
            "options": {
                "id": {"type": "str", "required": True},
                "type": {
                    "type": "str",
                    "choices": ["file", "env", "value"],
                    "required": True,
                },
                "src": {"type": "path"},
                "env": {"type": "str"},
                "value": {"type": "str", "no_log": True},
            },
            "required_if": [
                ("type", "file", ["src"]),
                ("type", "env", ["env"]),
                ("type", "value", ["value"]),
            ],
            "mutually_exclusive": [
                ("src", "env", "value"),
            ],
            "no_log": False,
        },
        "outputs": {
            "type": "list",
            "elements": "dict",
            "options": {
                "type": {
                    "type": "str",
                    "choices": ["local", "tar", "oci", "docker", "image"],
                    "required": True,
                },
                "dest": {"type": "path"},
                "context": {"type": "str"},
                "name": {"type": "list", "elements": "str"},
                "push": {"type": "bool", "default": False},
            },
            "required_if": [
                ("type", "local", ["dest"]),
                ("type", "tar", ["dest"]),
                ("type", "oci", ["dest"]),
            ],
            "mutually_exclusive": [
                ("dest", "name"),
                ("dest", "push"),
                ("context", "name"),
                ("context", "push"),
            ],
        },
    }

    client = AnsibleModuleDockerClient(
        argument_spec=argument_spec,
        supports_check_mode=True,
        needs_api_version=False,
    )

    try:
        results = ImageBuilder(client).build_image()
        client.module.exit_json(**results)
    except DockerException as e:
        client.fail(
            f"An unexpected Docker error occurred: {e}",
            exception=traceback.format_exc(),
        )


if __name__ == "__main__":
    main()
