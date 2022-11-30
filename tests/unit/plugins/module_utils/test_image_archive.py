# Copyright 2022 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import tarfile

from ansible_collections.community.docker.plugins.module_utils.image_archive import (
    api_image_id,
    archived_image_manifest,
    ImageArchiveInvalidException
)

from ..test_support.docker_image_archive_stubbing import (
    write_imitation_archive,
    write_imitation_archive_with_manifest,
    write_irrelevant_tar,
)


@pytest.fixture
def tar_file_name(tmpdir):
    '''
    Return the name of a non-existing tar file in an existing temporary directory.
    '''

    # Cast to str required by Python 2.x
    return str(tmpdir.join('foo.tar'))


@pytest.mark.parametrize('expected, value', [
    ('sha256:foo', 'foo'),
    ('sha256:bar', 'bar')
])
def test_api_image_id_from_archive_id(expected, value):
    assert api_image_id(value) == expected


def test_archived_image_manifest_extracts(tar_file_name):
    expected_id = "abcde12345"
    expected_tags = ["foo:latest", "bar:v1"]

    write_imitation_archive(tar_file_name, expected_id, expected_tags)

    actual = archived_image_manifest(tar_file_name)

    assert actual.image_id == expected_id
    assert actual.repo_tags == expected_tags


def test_archived_image_manifest_extracts_nothing_when_file_not_present(tar_file_name):
    image_id = archived_image_manifest(tar_file_name)

    assert image_id is None


def test_archived_image_manifest_raises_when_file_not_a_tar():
    try:
        archived_image_manifest(__file__)
        raise AssertionError()
    except ImageArchiveInvalidException as e:
        assert isinstance(e.cause, tarfile.ReadError)
        assert str(__file__) in str(e)


def test_archived_image_manifest_raises_when_tar_missing_manifest(tar_file_name):
    write_irrelevant_tar(tar_file_name)

    try:
        archived_image_manifest(tar_file_name)
        raise AssertionError()
    except ImageArchiveInvalidException as e:
        assert isinstance(e.cause, KeyError)
        assert 'manifest.json' in str(e.cause)


def test_archived_image_manifest_raises_when_manifest_missing_id(tar_file_name):
    manifest = [
        {
            'foo': 'bar'
        }
    ]

    write_imitation_archive_with_manifest(tar_file_name, manifest)

    try:
        archived_image_manifest(tar_file_name)
        raise AssertionError()
    except ImageArchiveInvalidException as e:
        assert isinstance(e.cause, KeyError)
        assert 'Config' in str(e.cause)
