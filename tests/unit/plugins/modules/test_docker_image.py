# Copyright 2022 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import typing as t

import pytest

from ansible_collections.community.docker.plugins.module_utils._image_archive import (
    api_image_id,
)
from ansible_collections.community.docker.plugins.modules.docker_image import (
    ImageManager,
)

from ..test_support.docker_image_archive_stubbing import (
    write_imitation_archive,
    write_irrelevant_tar,
)


if t.TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path


def assert_no_logging(msg: str) -> t.NoReturn:
    raise AssertionError(f"Should not have logged anything but logged {msg}")


def capture_logging(messages: list[str]) -> Callable[[str], None]:
    def capture(msg: str) -> None:
        messages.append(msg)

    return capture


@pytest.fixture(name="tar_file_name")
def tar_file_name_fixture(tmpdir: t.Any) -> str:
    """
    Return the name of a non-existing tar file in an existing temporary directory.
    """

    return tmpdir.join("foo.tar")


def test_archived_image_action_when_missing(tar_file_name: str) -> None:
    fake_name = "a:latest"
    fake_id = "a1"

    expected = f"Archived image {fake_name} to {tar_file_name}, since none present"

    actual = ImageManager.archived_image_action(
        assert_no_logging, tar_file_name, fake_name, api_image_id(fake_id)
    )

    assert actual == expected


def test_archived_image_action_when_current(tar_file_name: str) -> None:
    fake_name = "b:latest"
    fake_id = "b2"

    write_imitation_archive(tar_file_name, fake_id, [fake_name])

    actual = ImageManager.archived_image_action(
        assert_no_logging, tar_file_name, fake_name, api_image_id(fake_id)
    )

    assert actual is None


def test_archived_image_action_when_invalid(tar_file_name: str) -> None:
    fake_name = "c:1.2.3"
    fake_id = "c3"

    write_irrelevant_tar(tar_file_name)

    expected = f"Archived image {fake_name} to {tar_file_name}, overwriting an unreadable archive file"

    actual_log: list[str] = []
    actual = ImageManager.archived_image_action(
        capture_logging(actual_log), tar_file_name, fake_name, api_image_id(fake_id)
    )

    assert actual == expected

    assert len(actual_log) == 1
    assert actual_log[0].startswith("Unable to extract manifest summary from archive")


def test_archived_image_action_when_obsolete_by_id(tar_file_name: str) -> None:
    fake_name = "d:0.0.1"
    old_id = "e5"
    new_id = "d4"

    write_imitation_archive(tar_file_name, old_id, [fake_name])

    expected = f"Archived image {fake_name} to {tar_file_name}, overwriting archive with image {old_id} named {fake_name}"
    actual = ImageManager.archived_image_action(
        assert_no_logging, tar_file_name, fake_name, api_image_id(new_id)
    )

    assert actual == expected


def test_archived_image_action_when_obsolete_by_name(tar_file_name: str) -> None:
    old_name = "hi"
    new_name = "d:0.0.1"
    fake_id = "d4"

    write_imitation_archive(tar_file_name, fake_id, [old_name])

    expected = f"Archived image {new_name} to {tar_file_name}, overwriting archive with image {fake_id} named {old_name}"
    actual = ImageManager.archived_image_action(
        assert_no_logging, tar_file_name, new_name, api_image_id(fake_id)
    )

    print(f"actual   : {actual}")
    print(f"expected : {expected}")
    assert actual == expected
