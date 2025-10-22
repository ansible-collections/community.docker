#!/usr/bin/python
#
# Copyright 2016 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations


DOCUMENTATION = r"""
module: docker_image_remove

short_description: Remove Docker images

version_added: 3.6.0

description:
  - Remove Docker images from the Docker daemon.
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
    support: full

options:
  name:
    description:
      - 'Image name. Name format will be one of: C(name), C(repository/name), C(registry_server:port/name). When pushing or
        pulling an image the name can optionally include the tag by appending C(:tag_name).'
      - Note that image IDs (hashes) can also be used.
    type: str
    required: true
  tag:
    description:
      - Tag for the image name O(name) that is to be tagged.
      - If O(name)'s format is C(name:tag), then the tag value from O(name) will take precedence.
    type: str
    default: latest
  force:
    description:
      - Un-tag and remove all images matching the specified name.
    type: bool
    default: false
  prune:
    description:
      - Delete untagged parent images.
    type: bool
    default: true

requirements:
  - "Docker API >= 1.25"

author:
  - Felix Fontein (@felixfontein)

seealso:
  - module: community.docker.docker_image_load
  - module: community.docker.docker_image_pull
  - module: community.docker.docker_image_tag
"""

EXAMPLES = r"""
---
- name: Remove an image
  community.docker.docker_image_remove:
    name: pacur/centos-7
"""

RETURN = r"""
image:
  description:
    - Image inspection results for the affected image before removal.
    - Empty if the image was not found.
  returned: success
  type: dict
  sample: {}
deleted:
  description:
    - The digests of the images that were deleted.
  returned: success
  type: list
  elements: str
  sample: []
untagged:
  description:
    - The digests of the images that were untagged.
  returned: success
  type: list
  elements: str
  sample: []
"""

import traceback
import typing as t

from ansible_collections.community.docker.plugins.module_utils._api.errors import (
    DockerException,
    NotFound,
)
from ansible_collections.community.docker.plugins.module_utils._api.utils.utils import (
    parse_repository_tag,
)
from ansible_collections.community.docker.plugins.module_utils._common_api import (
    AnsibleDockerClient,
    RequestException,
)
from ansible_collections.community.docker.plugins.module_utils._util import (
    DockerBaseClass,
    is_image_name_id,
    is_valid_tag,
)


class ImageRemover(DockerBaseClass):
    def __init__(self, client: AnsibleDockerClient) -> None:
        super().__init__()

        self.client = client
        self.check_mode = self.client.check_mode
        self.diff = self.client.module._diff

        parameters = self.client.module.params
        self.name = parameters["name"]
        self.tag = parameters["tag"]
        self.force = parameters["force"]
        self.prune = parameters["prune"]

        if not is_valid_tag(self.tag, allow_empty=True):
            self.fail(f'"{self.tag}" is not a valid docker tag')

        # If name contains a tag, it takes precedence over tag parameter.
        if not is_image_name_id(self.name):
            repo, repo_tag = parse_repository_tag(self.name)
            if repo_tag:
                self.name = repo
                self.tag = repo_tag

    def fail(self, msg: str) -> t.NoReturn:
        self.client.fail(msg)

    def get_diff_state(self, image: dict[str, t.Any] | None) -> dict[str, t.Any]:
        if not image:
            return {"exists": False}
        return {
            "exists": True,
            "id": image["Id"],
            "tags": sorted(image.get("RepoTags") or []),
            "digests": sorted(image.get("RepoDigests") or []),
        }

    def absent(self) -> dict[str, t.Any]:
        actions: list[str] = []
        deleted: list[str] = []
        untagged: list[str] = []
        results: dict[str, t.Any] = {
            "changed": False,
            "actions": actions,
            "image": {},
            "deleted": deleted,
            "untagged": untagged,
        }

        name = self.name
        if is_image_name_id(name):
            image = self.client.find_image_by_id(name, accept_missing_image=True)
        else:
            image = self.client.find_image(name, self.tag)
            if self.tag:
                name = f"{self.name}:{self.tag}"

        diff: dict[str, t.Any] = {}
        if self.diff:
            results["diff"] = diff
            diff["before"] = self.get_diff_state(image)

        if not image:
            if self.diff:
                diff["after"] = self.get_diff_state(image)
            return results

        results["changed"] = True
        actions.append(f"Removed image {name}")
        results["image"] = image

        if not self.check_mode:
            try:
                res = self.client.delete_json(
                    "/images/{0}",
                    name,
                    params={"force": self.force, "noprune": not self.prune},
                )
            except NotFound:
                # If the image vanished while we were trying to remove it, do not fail
                res = []
            except Exception as exc:  # pylint: disable=broad-exception-caught
                self.fail(f"Error removing image {name} - {exc}")

            for entry in res:
                if entry.get("Untagged"):
                    untagged.append(entry["Untagged"])
                if entry.get("Deleted"):
                    deleted.append(entry["Deleted"])

            untagged[:] = sorted(untagged)
            deleted[:] = sorted(deleted)

            if self.diff:
                image_after = self.client.find_image_by_id(
                    image["Id"], accept_missing_image=True
                )
                diff["after"] = self.get_diff_state(image_after)

        elif is_image_name_id(name):
            deleted.append(image["Id"])
            untagged[:] = sorted(
                (image.get("RepoTags") or []) + (image.get("RepoDigests") or [])
            )
            if not self.force and results["untagged"]:
                self.fail(
                    "Cannot delete image by ID that is still in use - use force=true"
                )
            if self.diff:
                diff["after"] = self.get_diff_state({})

        elif is_image_name_id(self.tag):
            untagged.append(name)
            if (
                len(image.get("RepoTags") or []) < 1
                and len(image.get("RepoDigests") or []) < 2
            ):
                deleted.append(image["Id"])
            if self.diff:
                diff["after"] = self.get_diff_state(image)
                try:
                    diff["after"]["digests"].remove(name)
                except ValueError:
                    pass

        else:
            untagged.append(name)
            if (
                len(image.get("RepoTags") or []) < 2
                and len(image.get("RepoDigests") or []) < 1
            ):
                deleted.append(image["Id"])
            if self.diff:
                diff["after"] = self.get_diff_state(image)
                try:
                    diff["after"]["tags"].remove(name)
                except ValueError:
                    pass

        return results


def main() -> None:
    argument_spec = {
        "name": {"type": "str", "required": True},
        "tag": {"type": "str", "default": "latest"},
        "force": {"type": "bool", "default": False},
        "prune": {"type": "bool", "default": True},
    }

    client = AnsibleDockerClient(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    try:
        results = ImageRemover(client).absent()
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
