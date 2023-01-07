#!/usr/bin/python
#
# Copyright (c) 2022, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: docker_container_copy_into

short_description: Copy a file into a Docker container

description:
  - Copy a file into a Docker container.
  - Similar to C(docker cp).
  - To copy files in a non-running container, you must provide the I(owner_id) and I(group_id) options.

attributes:
  check_mode:
    support: full
  diff_mode:
    support: none

options:
  container:
    description:
      - The name of the container to copy files to.
    type: str
    required: true
  path:
    description:
      - Path to a file on the managed node.
    type: path
    required: true
  container_path:
    description:
      - Path to a file inside the Docker container.
      - Must be an absolute path.
    type: str
    required: true
  follow:
    description:
      - This flag indicates that filesystem links in the Docker container, if they exist, should be followed.
    type: bool
    default: false
  local_follow:
    description:
      - This flag indicates that filesystem links in the source tree (where the module is executed), if they exist, should be followed.
    type: bool
    default: true
  owner_id:
    description:
      - The owner ID to use when writing the file to disk.
      - If provided, I(group_id) must also be provided.
      - If not provided, the module will try to determine the user and group ID for the current user in the container.
        This will only work if C(/bin/sh) is present in the container and the C(id) binary or shell builtin is available.
        Also the container must be running.
    type: int
  group_id:
    description:
      - The group ID to use when writing the file to disk.
      - If provided, I(owner_id) must also be provided.
      - If not provided, the module will try to determine the user and group ID for the current user in the container.
        This will only work if C(/bin/sh) is present in the container and the C(id) binary or shell builtin is available.
        Also the container must be running.
    type: int
  mode:
    description:
      - The file mode to use when writing the file to disk.
      - Will use the file's mode from the source system if this option is not provided.
    type: int
  force:
    description:
      - Force writing the file (without performing any idempotency checks).
    type: bool
    default: false

extends_documentation_fragment:
  - community.docker.docker.api_documentation
  - community.docker.attributes
  - community.docker.attributes.actiongroup_docker

author:
  - "Felix Fontein (@felixfontein)"

requirements:
  - "Docker API >= 1.25"
'''

EXAMPLES = '''
- name: Copy a file into the container
  community.docker.docker_container_copy_into:
    container: mydata
    path: /home/user/data.txt
    container_path: /data/input.txt

- name: Copy a file into the container with owner, group, and mode set
  community.docker.docker_container_copy_into:
    container: mydata
    path: /home/user/bin/runme.o
    container_path: /bin/runme
    owner: 0  # root
    group: 0  # root
    mode: 0o755  # readable and executable by all users, writable by root
'''

RETURN = '''
container_path:
  description:
    - The actual path in the container.
    - Can only be different from I(container_path) when I(follow=true).
  type: str
  returned: success
'''

import os
import stat
import traceback

from ansible.module_utils._text import to_bytes, to_text, to_native

from ansible_collections.community.docker.plugins.module_utils.common_api import (
    AnsibleDockerClient,
    RequestException,
)

from ansible_collections.community.docker.plugins.module_utils.copy import (
    DockerFileCopyError,
    DockerFileNotFound,
    DockerUnexpectedError,
    call_client,
    determine_user_group,
    fetch_file_ex,
    put_file,
    stat_file,
)


def are_fileobjs_equal(f1, f2):
    '''Given two (buffered) file objects, compare their contents.'''
    blocksize = 65536
    b1buf = b''
    b2buf = b''
    while True:
        if f1 and len(b1buf) < blocksize:
            f1b = f1.read(blocksize)
            if not f1b:
                # f1 is EOF, so stop reading from it
                f1 = None
            b1buf += f1b
        if f2 and len(b2buf) < blocksize:
            f2b = f2.read(blocksize)
            if not f2b:
                # f2 is EOF, so stop reading from it
                f2 = None
            b2buf += f2b
        if not b1buf or not b2buf:
            # At least one of f1 and f2 is EOF and all its data has
            # been processed. If both are EOF and their data has been
            # processed, the files are equal, otherwise not.
            return not b1buf and not b2buf
        # Compare the next chunk of data, and remove it from the buffers
        buflen = min(len(b1buf), len(b2buf))
        if b1buf[:buflen] != b2buf[:buflen]:
            return False
        b1buf = b1buf[buflen:]
        b2buf = b2buf[buflen:]


def is_idempotent(client, container, managed_path, container_path, follow_links, local_follow_links, owner_id, group_id, mode, force=False):
    # Retrieve information of local file
    try:
        file_stat = os.stat(managed_path) if local_follow_links else os.lstat(managed_path)
    except OSError as exc:
        if exc.errno == 2:
            raise DockerFileNotFound('Cannot find local file {managed_path}'.format(managed_path=managed_path))
        raise
    if mode is None:
        mode = stat.S_IMODE(file_stat.st_mode)
    if not stat.S_ISLNK(file_stat.st_mode) and not stat.S_ISREG(file_stat.st_mode):
        raise DockerFileCopyError('Local path {managed_path} is not a symbolic link or file')

    # When forcing and we're not following links in the container, go!
    if force and not follow_links:
        return container_path, mode, False

    # Resolve symlinks in the container (if requested), and get information on container's file
    real_container_path, regular_stat, link_target = stat_file(
        call_client(client, container),
        container,
        in_path=container_path,
        follow_links=follow_links,
    )

    # Follow links in the Docker container?
    if follow_links:
        container_path = real_container_path

    # When forcing, go!
    if force:
        return container_path, mode, False

    # If the file wasn't found, continue
    if regular_stat is None:
        return container_path, mode, False

    # Basic idempotency checks
    if stat.S_ISLNK(file_stat.st_mode):
        if link_target is None:
            return container_path, mode, False
        local_link_target = os.readlink(managed_path)
        return container_path, mode, local_link_target == link_target
    if link_target is not None:
        return container_path, mode, False
    for bit in (
        # https://pkg.go.dev/io/fs#FileMode
        32 - 1,  # ModeDir
        32 - 4,  # ModeTemporary
        32 - 5,  # ModeSymlink
        32 - 6,  # ModeDevice
        32 - 7,  # ModeNamedPipe
        32 - 8,  # ModeSocket
        32 - 11,  # ModeCharDevice
        32 - 13,  # ModeIrregular
    ):
        if regular_stat['mode'] & (1 << bit) != 0:
            return container_path, mode, False
    if file_stat.st_size != regular_stat['size']:
        return container_path, mode, False
    container_file_mode = regular_stat['mode'] & 0xFFF
    if regular_stat['mode'] & (1 << (32 - 9)) != 0:  # ModeSetuid
        container_file_mode |= stat.S_ISUID  # set UID bit
    if regular_stat['mode'] & (1 << (32 - 10)) != 0:  # ModeSetgid
        container_file_mode |= stat.S_ISGID  # set GID bit
    if regular_stat['mode'] & (1 << (32 - 12)) != 0:  # ModeSticky
        container_file_mode |= stat.S_ISVTX  # sticky bit
    if mode != container_file_mode:
        return container_path, mode, False

    # Fetch file from container
    def process_none(in_path):
        return container_path, mode, False

    def process_regular(in_path, tar, member):
        # Check things like user/group ID and mode
        if member.mode & 0xFFF != mode:
            return container_path, mode, False
        if member.uid != owner_id:
            return container_path, mode, False
        if member.gid != group_id:
            return container_path, mode, False

        if not stat.S_ISREG(file_stat.st_mode):
            return container_path, mode, False
        if member.size != file_stat.st_size:
            return container_path, mode, False

        tar_f = tar.extractfile(member)  # in Python 2, this *cannot* be used in `with`...
        with open(managed_path, 'rb') as local_f:
            return container_path, mode, are_fileobjs_equal(tar_f, local_f)

    def process_symlink(in_path, member):
        # Check things like user/group ID and mode
        if member.mode & 0xFFF != mode:
            return container_path, mode, False
        if member.uid != owner_id:
            return container_path, mode, False
        if member.gid != group_id:
            return container_path, mode, False

        if not stat.S_ISLNK(file_stat.st_mode):
            return container_path, mode, False

        local_link_target = os.readlink(managed_path)
        return container_path, mode, member.linkname == local_link_target

    return fetch_file_ex(
        call_client(client, container, use_file_not_found_exception=True),
        container,
        in_path=container_path,
        process_none=process_none,
        process_regular=process_regular,
        process_symlink=process_symlink,
        follow_links=follow_links,
    )


def copy_into_container(client, container, managed_path, container_path, follow_links, local_follow_links, owner_id, group_id, mode, force=False):
    container_path, mode, idempotent = is_idempotent(
        client, container, managed_path, container_path, follow_links, local_follow_links, owner_id, group_id, mode, force=force)
    changed = not idempotent

    if changed and not client.module.check_mode:
        put_file(
            call_client(client, container),
            container,
            in_path=managed_path,
            out_path=container_path,
            user_id=owner_id,
            group_id=group_id,
            mode=mode,
            follow_links=local_follow_links,
        )

    client.module.exit_json(
        container_path=container_path,
        changed=changed,
    )


def main():
    argument_spec = dict(
        container=dict(type='str', required=True),
        path=dict(type='path', required=True),
        container_path=dict(type='str', required=True),
        follow=dict(type='bool', default=False),
        local_follow=dict(type='bool', default=True),
        owner_id=dict(type='int'),
        group_id=dict(type='int'),
        mode=dict(type='int'),
        force=dict(type='bool', default=False),
    )

    client = AnsibleDockerClient(
        argument_spec=argument_spec,
        min_docker_api_version='1.20',
        supports_check_mode=True,
        required_together=[('owner_id', 'group_id')],
    )

    container = client.module.params['container']
    managed_path = client.module.params['path']
    container_path = client.module.params['container_path']
    follow = client.module.params['follow']
    local_follow = client.module.params['local_follow']
    owner_id = client.module.params['owner_id']
    group_id = client.module.params['group_id']
    mode = client.module.params['mode']
    force = client.module.params['force']

    if not container_path.startswith(os.path.sep):
        container_path = os.path.join(os.path.sep, container_path)
    container_path = os.path.normpath(container_path)

    try:
        if owner_id is None or group_id is None:
            owner_id, group_id = call_client(client, container)(lambda c: determine_user_group(c, container))

        copy_into_container(
            client,
            container,
            managed_path,
            container_path,
            follow_links=follow,
            local_follow_links=local_follow,
            owner_id=owner_id,
            group_id=group_id,
            mode=mode,
            force=force,
        )
    except DockerUnexpectedError as exc:
        client.fail('Unexpected error: {exc}'.format(exc=to_native(exc)), exception=traceback.format_exc())
    except DockerFileCopyError as exc:
        client.fail(to_native(exc))
    except OSError as exc:
        client.fail('Unexpected error: {exc}'.format(exc=to_native(exc)), exception=traceback.format_exc())


if __name__ == '__main__':
    main()
