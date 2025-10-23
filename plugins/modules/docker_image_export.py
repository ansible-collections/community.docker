#!/usr/bin/python
#
# Copyright (c) 2023, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations


DOCUMENTATION = r"""
module: docker_image_export

short_description: Export (archive) Docker images

version_added: 3.7.0

description:
  - Creates an archive (tarball) from one or more Docker images.
  - This can be copied to another machine and loaded with M(community.docker.docker_image_load).
extends_documentation_fragment:
  - community.docker._docker.api_documentation
  - community.docker._attributes
  - community.docker._attributes.actiongroup_docker

attributes:
  check_mode:
    support: full
  diff_mode:
    support: none
  idempotent:
    support: full

options:
  names:
    description:
      - 'One or more image names. Name format will be one of: C(name), C(repository/name), C(registry_server:port/name). When
        pushing or pulling an image the name can optionally include the tag by appending C(:tag_name).'
      - Note that image IDs (hashes) can also be used.
    type: list
    elements: str
    required: true
    aliases:
      - name
  tag:
    description:
      - Tag for the image name O(name) that is to be tagged.
      - If O(name)'s format is C(name:tag), then the tag value from O(name) will take precedence.
    type: str
    default: latest
  path:
    description:
      - The C(.tar) file the image should be exported to.
    type: path
  force:
    description:
      - Export the image even if the C(.tar) file already exists and seems to contain the right image.
    type: bool
    default: false

requirements:
  - "Docker API >= 1.25"

author:
  - Felix Fontein (@felixfontein)

seealso:
  - module: community.docker.docker_image
  - module: community.docker.docker_image_info
  - module: community.docker.docker_image_load
"""

EXAMPLES = r"""
---
- name: Export an image
  community.docker.docker_image_export:
    name: pacur/centos-7
    path: /tmp/centos-7.tar

- name: Export multiple images
  community.docker.docker_image_export:
    names:
      - hello-world:latest
      - pacur/centos-7:latest
    path: /tmp/various.tar
"""

RETURN = r"""
images:
  description: Image inspection results for the affected images.
  returned: success
  type: list
  elements: dict
  sample: []
"""

import traceback
import typing as t

from ansible_collections.community.docker.plugins.module_utils._api.constants import (
    DEFAULT_DATA_CHUNK_SIZE,
)
from ansible_collections.community.docker.plugins.module_utils._api.errors import (
    DockerException,
)
from ansible_collections.community.docker.plugins.module_utils._api.utils.utils import (
    parse_repository_tag,
)
from ansible_collections.community.docker.plugins.module_utils._common_api import (
    AnsibleDockerClient,
    RequestException,
)
from ansible_collections.community.docker.plugins.module_utils._image_archive import (
    ImageArchiveInvalidException,
    api_image_id,
    load_archived_image_manifest,
)
from ansible_collections.community.docker.plugins.module_utils._util import (
    DockerBaseClass,
    is_image_name_id,
    is_valid_tag,
)


class ImageExportManager(DockerBaseClass):
    def __init__(self, client: AnsibleDockerClient) -> None:
        super().__init__()

        self.client = client
        parameters = self.client.module.params
        self.check_mode = self.client.check_mode

        self.path = parameters["path"]
        self.force = parameters["force"]
        self.tag = parameters["tag"]

        if not is_valid_tag(self.tag, allow_empty=True):
            self.fail(f'"{self.tag}" is not a valid docker tag')

        # If name contains a tag, it takes precedence over tag parameter.
        self.names = []
        for name in parameters["names"]:
            if is_image_name_id(name):
                self.names.append({"id": name, "joined": name})
            else:
                repo, repo_tag = parse_repository_tag(name)
                if not repo_tag:
                    repo_tag = self.tag
                self.names.append(
                    {"name": repo, "tag": repo_tag, "joined": f"{repo}:{repo_tag}"}
                )

        if not self.names:
            self.fail("At least one image name must be specified")

    def fail(self, msg: str) -> t.NoReturn:
        self.client.fail(msg)

    def get_export_reason(self) -> str | None:
        if self.force:
            return "Exporting since force=true"

        try:
            archived_images = load_archived_image_manifest(self.path)
            if archived_images is None:
                return "Overwriting since no image is present in archive"
        except ImageArchiveInvalidException as exc:
            self.log(f"Unable to extract manifest summary from archive: {exc}")
            return "Overwriting an unreadable archive file"

        left_names = list(self.names)
        for archived_image in archived_images:
            found = False
            for i, name in enumerate(left_names):
                if (
                    name["id"] == api_image_id(archived_image.image_id)
                    and [name["joined"]] == archived_image.repo_tags
                ):
                    del left_names[i]
                    found = True
                    break
            if not found:
                return f"Overwriting archive since it contains unexpected image {archived_image.image_id} named {', '.join(archived_image.repo_tags)}"
        if left_names:
            return f"Overwriting archive since it is missing image(s) {', '.join([name['joined'] for name in left_names])}"

        return None

    def write_chunks(self, chunks: t.Generator[bytes]) -> None:
        try:
            with open(self.path, "wb") as fd:
                for chunk in chunks:
                    fd.write(chunk)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            self.fail(f"Error writing image archive {self.path} - {exc}")

    def export_images(self) -> None:
        image_names = [name["joined"] for name in self.names]
        image_names_str = ", ".join(image_names)
        if len(image_names) == 1:
            self.log(f"Getting archive of image {image_names[0]}")
            try:
                chunks = self.client._stream_raw_result(
                    self.client._get(
                        self.client._url("/images/{0}/get", image_names[0]), stream=True
                    ),
                    chunk_size=DEFAULT_DATA_CHUNK_SIZE,
                    decode=False,
                )
            except Exception as exc:  # pylint: disable=broad-exception-caught
                self.fail(f"Error getting image {image_names[0]} - {exc}")
        else:
            self.log(f"Getting archive of images {image_names_str}")
            try:
                chunks = self.client._stream_raw_result(
                    self.client._get(
                        self.client._url("/images/get"),
                        stream=True,
                        params={"names": image_names},
                    ),
                    chunk_size=DEFAULT_DATA_CHUNK_SIZE,
                    decode=False,
                )
            except Exception as exc:  # pylint: disable=broad-exception-caught
                self.fail(f"Error getting images {image_names_str} - {exc}")

        self.write_chunks(chunks)

    def run(self) -> dict[str, t.Any]:
        tag = self.tag
        if not tag:
            tag = "latest"

        images = []
        for name in self.names:
            if "id" in name:
                image = self.client.find_image_by_id(
                    name["id"], accept_missing_image=True
                )
            else:
                image = self.client.find_image(name=name["name"], tag=name["tag"])
            if not image:
                self.fail(f"Image {name['joined']} not found")
            images.append(image)

            # Will have a 'sha256:' prefix
            name["id"] = image["Id"]

        results = {
            "changed": False,
            "images": images,
        }

        reason = self.get_export_reason()
        if reason is not None:
            results["msg"] = reason
            results["changed"] = True

            if not self.check_mode:
                self.export_images()

        return results


def main() -> None:
    argument_spec = {
        "path": {"type": "path"},
        "force": {"type": "bool", "default": False},
        "names": {
            "type": "list",
            "elements": "str",
            "required": True,
            "aliases": ["name"],
        },
        "tag": {"type": "str", "default": "latest"},
    }

    client = AnsibleDockerClient(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    try:
        results = ImageExportManager(client).run()
        client.module.exit_json(**results)
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
