# Copyright 2022 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Note that this module util is **PRIVATE** to the collection. It can have breaking changes at any time.
# Do not use this from other collections or standalone plugins/modules!

from __future__ import annotations

import json
import os
import tarfile


class ImageArchiveManifestSummary:
    """
    Represents data extracted from a manifest.json found in the tar archive output of the
    "docker image save some:tag > some.tar" command.
    """

    def __init__(self, image_id: str, repo_tags: list[str]) -> None:
        """
        :param image_id:  File name portion of Config entry, e.g. abcde12345 from abcde12345.json
        :param repo_tags  Docker image names, e.g. ["hello-world:latest"]
        """

        self.image_id = image_id
        self.repo_tags = repo_tags


class ImageArchiveInvalidException(Exception):
    pass


def api_image_id(archive_image_id: str) -> str:
    """
    Accepts an image hash in the format stored in manifest.json, and returns an equivalent identifier
    that represents the same image hash, but in the format presented by the Docker Engine API.

    :param archive_image_id: plain image hash
    :returns: Prefixed hash used by REST api
    """

    return f"sha256:{archive_image_id}"


def load_archived_image_manifest(
    archive_path: str,
) -> list[ImageArchiveManifestSummary] | None:
    """
    Attempts to get image IDs and image names from metadata stored in the image
    archive tar file.

    The tar should contain a file "manifest.json" with an array with one or more entries,
    and every entry should have a Config field with the image ID in its file name, as
    well as a RepoTags list, which typically has only one entry.

    :raises:
        ImageArchiveInvalidException: A file already exists at archive_path, but could not extract an image ID from it.

    :param archive_path: Tar file to read
    :return: None, if no file at archive_path, or a list of ImageArchiveManifestSummary objects.
    """

    try:
        # FileNotFoundError does not exist in Python 2
        if not os.path.isfile(archive_path):
            return None

        with tarfile.open(archive_path, "r") as tf:
            try:
                try:
                    reader = tf.extractfile("manifest.json")
                    if reader is None:
                        raise ImageArchiveInvalidException(
                            "Failed to read manifest.json"
                        )
                    with reader as ef:
                        manifest = json.load(ef)
                except ImageArchiveInvalidException:
                    raise
                except Exception as exc:
                    raise ImageArchiveInvalidException(
                        f"Failed to decode and deserialize manifest.json: {exc}"
                    ) from exc

                if len(manifest) == 0:
                    raise ImageArchiveInvalidException(
                        "Expected to have at least one entry in manifest.json but found none"
                    )

                result = []
                for index, meta in enumerate(manifest):
                    try:
                        config_file = meta["Config"]
                    except KeyError as exc:
                        raise ImageArchiveInvalidException(
                            f"Failed to get Config entry from {index + 1}th manifest in manifest.json: {exc}"
                        ) from exc

                    # Extracts hash without 'sha256:' prefix
                    try:
                        # Strip off .json filename extension, leaving just the hash.
                        image_id = os.path.splitext(config_file)[0]
                    except Exception as exc:
                        raise ImageArchiveInvalidException(
                            f"Failed to extract image id from config file name {config_file}: {exc}"
                        ) from exc

                    for prefix in ("blobs/sha256/",):  # Moby 25.0.0, Docker API 1.44
                        if image_id.startswith(prefix):
                            image_id = image_id[len(prefix) :]

                    try:
                        repo_tags = meta["RepoTags"]
                    except KeyError as exc:
                        raise ImageArchiveInvalidException(
                            f"Failed to get RepoTags entry from {index + 1}th manifest in manifest.json: {exc}"
                        ) from exc

                    result.append(
                        ImageArchiveManifestSummary(
                            image_id=image_id, repo_tags=repo_tags
                        )
                    )
                return result

            except ImageArchiveInvalidException:
                raise
            except Exception as exc:
                raise ImageArchiveInvalidException(
                    f"Failed to extract manifest.json from tar file {archive_path}: {exc}"
                ) from exc

    except ImageArchiveInvalidException:
        raise
    except Exception as exc:
        raise ImageArchiveInvalidException(
            f"Failed to open tar file {archive_path}: {exc}"
        ) from exc


def archived_image_manifest(archive_path: str) -> ImageArchiveManifestSummary | None:
    """
    Attempts to get Image.Id and image name from metadata stored in the image
    archive tar file.

    The tar should contain a file "manifest.json" with an array with a single entry,
    and the entry should have a Config field with the image ID in its file name, as
    well as a RepoTags list, which typically has only one entry.

    :raises:
        ImageArchiveInvalidException: A file already exists at archive_path, but could not extract an image ID from it.

    :param archive_path: Tar file to read
    :return: None, if no file at archive_path, or the extracted image ID, which will not have a sha256: prefix.
    """

    results = load_archived_image_manifest(archive_path)
    if results is None:
        return None
    if len(results) == 1:
        return results[0]
    raise ImageArchiveInvalidException(
        f"Expected to have one entry in manifest.json but found {len(results)}"
    )
