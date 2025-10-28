# Copyright 2022 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import json
import tarfile
import typing as t
from tempfile import TemporaryFile


def write_imitation_archive(
    file_name: str, image_id: str, repo_tags: list[str]
) -> None:
    """
    Write a tar file meeting these requirements:

    * Has a file manifest.json
    * manifest.json contains a one-element array
    * The element has a Config property with "[image_id].json" as the value name

    :param file_name: Name of file to create
    :type file_name: str
    :param image_id: Fake sha256 hash (without the sha256: prefix)
    :type image_id: str
    :param repo_tags: list of fake image tags
    :type repo_tags: list
    """

    manifest = [{"Config": f"{image_id}.json", "RepoTags": repo_tags}]

    write_imitation_archive_with_manifest(file_name, manifest)


def write_imitation_archive_with_manifest(
    file_name: str, manifest: list[dict[str, t.Any]]
) -> None:
    with tarfile.open(file_name, "w") as tf, TemporaryFile() as f:
        f.write(json.dumps(manifest).encode("utf-8"))

        ti = tarfile.TarInfo("manifest.json")
        ti.size = f.tell()

        f.seek(0)
        tf.addfile(ti, f)


def write_irrelevant_tar(file_name: str) -> None:
    """
    Create a tar file that does not match the spec for "docker image save" / "docker image load" commands.

    :param file_name: Name of tar file to create
    :type file_name: str
    """

    with tarfile.open(file_name, "w") as tf, TemporaryFile() as f:
        f.write("Hello, world.".encode("utf-8"))

        ti = tarfile.TarInfo("hi.txt")
        ti.size = f.tell()

        f.seek(0)
        tf.addfile(ti, f)
