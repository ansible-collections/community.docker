# Copyright 2022 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import tarfile
from tempfile import TemporaryFile


def write_imitation_archive(file_name, image_id, repo_tags):
    '''
    Write a tar file meeting these requirements:

    * Has a file manifest.json
    * manifest.json contains a one-element array
    * The element has a Config property with "[image_id].json" as the value name

    :param file_name: Name of file to create
    :type file_name: str
    :param image_id: Fake sha256 hash (without the sha256: prefix)
    :type image_id: str
    :param repo_tags: list of fake image:tag's
    :type repo_tags: list
    '''

    manifest = [
        {
            'Config': '%s.json' % image_id,
            'RepoTags': repo_tags
        }
    ]

    write_imitation_archive_with_manifest(file_name, manifest)


def write_imitation_archive_with_manifest(file_name, manifest):
    tf = tarfile.open(file_name, 'w')
    try:
        with TemporaryFile() as f:
            f.write(json.dumps(manifest).encode('utf-8'))

            ti = tarfile.TarInfo('manifest.json')
            ti.size = f.tell()

            f.seek(0)
            tf.addfile(ti, f)

    finally:
        # In Python 2.6, this does not have __exit__
        tf.close()


def write_irrelevant_tar(file_name):
    '''
    Create a tar file that does not match the spec for "docker image save" / "docker image load" commands.

    :param file_name: Name of tar file to create
    :type file_name: str
    '''

    tf = tarfile.open(file_name, 'w')
    try:
        with TemporaryFile() as f:
            f.write('Hello, world.'.encode('utf-8'))

            ti = tarfile.TarInfo('hi.txt')
            ti.size = f.tell()

            f.seek(0)
            tf.addfile(ti, f)

    finally:
        tf.close()
