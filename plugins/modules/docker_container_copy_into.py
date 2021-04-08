#!/usr/bin/python
#
# Copyright 2016 Red Hat | Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: docker_container_copy_into

short_description: Copy a file into a Docker container

description:
  - Copy a file into a Docker container.
  - Similar to C(docker cp).
  - The file is processed in-memory. Do not use for large files!

options:
  container:
    description:
      - The name of the container to copy files to/from.
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
    type: int
  group_id:
    description:
      - The group ID to use when writing the file to disk.
      - If provided, I(owner_id) must also be provided.
      - If not provided, the module will try to determine the user and group ID for the current user in the container.
        This will only work if C(/bin/sh) is present in the container and the C(id) binary or shell builtin is available.
    type: int
  mode:
    description:
      - The file mode to use when writing the file to disk.
      - Will use the file's mode from the source system if this option is not provided.
    type: int

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


def is_idempotent(client, container, managed_path, container_path, follow_links, local_follow_links, owner_id, group_id, mode):
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

    real_container_path, regular_stat, link_target = stat_file(
        call_client(client, container),
        container,
        in_path=container_path,
        follow_links=follow_links,
    )

    # Follow links in the Docker container?
    if follow_links:
        container_path = real_container_path

    # If the file wasn't found, continue
    if regular_stat is None and link_target is None:
        return container_path, mode, False

    # Basic idempotency checks
    if stat.S_ISLNK(file_stat.st_mode):
        if link_target is None:
            return container_path, mode, False
        local_link_target = os.readlink(managed_path)
        return container_path, mode, local_link_target == link_target
    if not stat.S_ISREG(file_stat.st_mode):
        raise DockerFileCopyError('Local path {managed_path} is not a symbolic link or file')
    if regular_stat is None:
        return container_path, mode, False
    if file_stat.st_size != regular_stat['size']:
        return container_path, mode, False
    if mode != regular_stat['mode'] & 0xFFF:
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
            return container_path, mode, tar_f.read() == local_f.read()

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


def copy_into_container(client, container, managed_path, container_path, follow_links, local_follow_links, owner_id, group_id, mode):
    container_path, mode, idempotent = is_idempotent(
        client, container, managed_path, container_path, follow_links, local_follow_links, owner_id, group_id, mode)
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
        )
    except DockerUnexpectedError as exc:
        client.fail('Unexpected error: {exc}'.format(exc=to_native(exc)), exception=traceback.format_exc())
    except DockerFileCopyError as exc:
        client.fail(to_native(exc))
    except OSError as exc:
        client.fail('Unexpected error: {exc}'.format(exc=to_native(exc)), exception=traceback.format_exc())


if __name__ == '__main__':
    main()