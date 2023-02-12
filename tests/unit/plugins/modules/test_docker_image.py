# Copyright 2022 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest

from ansible_collections.community.docker.plugins.modules.docker_image import ImageManager

from ansible_collections.community.docker.plugins.module_utils.image_archive import api_image_id

from ..test_support.docker_image_archive_stubbing import (
    write_imitation_archive,
    write_irrelevant_tar,
)


def assert_no_logging(msg):
    raise AssertionError('Should not have logged anything but logged %s' % msg)


def capture_logging(messages):
    def capture(msg):
        messages.append(msg)

    return capture


@pytest.fixture
def tar_file_name(tmpdir):
    """
    Return the name of a non-existing tar file in an existing temporary directory.
    """

    # Cast to str required by Python 2.x
    return str(tmpdir.join('foo.tar'))


def test_archived_image_action_when_missing(tar_file_name):
    fake_name = 'a:latest'
    fake_id = 'a1'

    expected = 'Archived image %s to %s, since none present' % (fake_name, tar_file_name)

    actual = ImageManager.archived_image_action(assert_no_logging, tar_file_name, fake_name, api_image_id(fake_id))

    assert actual == expected


def test_archived_image_action_when_current(tar_file_name):
    fake_name = 'b:latest'
    fake_id = 'b2'

    write_imitation_archive(tar_file_name, fake_id, [fake_name])

    actual = ImageManager.archived_image_action(assert_no_logging, tar_file_name, fake_name, api_image_id(fake_id))

    assert actual is None


def test_archived_image_action_when_invalid(tar_file_name):
    fake_name = 'c:1.2.3'
    fake_id = 'c3'

    write_irrelevant_tar(tar_file_name)

    expected = 'Archived image %s to %s, overwriting an unreadable archive file' % (fake_name, tar_file_name)

    actual_log = []
    actual = ImageManager.archived_image_action(
        capture_logging(actual_log),
        tar_file_name,
        fake_name,
        api_image_id(fake_id)
    )

    assert actual == expected

    assert len(actual_log) == 1
    assert actual_log[0].startswith('Unable to extract manifest summary from archive')


def test_archived_image_action_when_obsolete_by_id(tar_file_name):
    fake_name = 'd:0.0.1'
    old_id = 'e5'
    new_id = 'd4'

    write_imitation_archive(tar_file_name, old_id, [fake_name])

    expected = 'Archived image %s to %s, overwriting archive with image %s named %s' % (
        fake_name, tar_file_name, old_id, fake_name
    )
    actual = ImageManager.archived_image_action(assert_no_logging, tar_file_name, fake_name, api_image_id(new_id))

    assert actual == expected


def test_archived_image_action_when_obsolete_by_name(tar_file_name):
    old_name = 'hi'
    new_name = 'd:0.0.1'
    fake_id = 'd4'

    write_imitation_archive(tar_file_name, fake_id, [old_name])

    expected = 'Archived image %s to %s, overwriting archive with image %s named %s' % (
        new_name, tar_file_name, fake_id, old_name
    )
    actual = ImageManager.archived_image_action(assert_no_logging, tar_file_name, new_name, api_image_id(fake_id))

    print('actual   : %s', actual)
    print('expected : %s', expected)
    assert actual == expected
