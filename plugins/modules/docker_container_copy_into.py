#!/usr/bin/python
#
# Copyright (c) 2022, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations


DOCUMENTATION = r"""
module: docker_container_copy_into

short_description: Copy a file into a Docker container

version_added: 3.4.0

description:
  - Copy a file into a Docker container.
  - Similar to C(docker cp).
  - To copy files in a non-running container, you must provide the O(owner_id) and O(group_id) options. This is also necessary
    if the container does not contain a C(/bin/sh) shell with an C(id) tool.
attributes:
  check_mode:
    support: full
  diff_mode:
    support: full
    details:
      - Additional data will need to be transferred to compute diffs.
      - The module uses R(the MAX_FILE_SIZE_FOR_DIFF ansible-core configuration,MAX_FILE_SIZE_FOR_DIFF) to determine for how
        large files diffs should be computed.
  idempotent:
    support: partial
    details:
      - If O(force=true) the module is not idempotent.

options:
  container:
    description:
      - The name of the container to copy files to.
    type: str
    required: true
  path:
    description:
      - Path to a file on the managed node.
      - Mutually exclusive with O(content). One of O(content) and O(path) is required.
    type: path
  content:
    description:
      - The file's content.
      - If you plan to provide binary data, provide it pre-encoded to base64, and set O(content_is_b64=true).
      - Mutually exclusive with O(path). One of O(content) and O(path) is required.
    type: str
  content_is_b64:
    description:
      - If set to V(true), the content in O(content) is assumed to be Base64 encoded and will be decoded before being used.
      - To use binary O(content), it is better to keep it Base64 encoded and let it be decoded by this option. Otherwise you
        risk the data to be interpreted as UTF-8 and corrupted.
    type: bool
    default: false
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
      - This flag indicates that filesystem links in the source tree (where the module is executed), if they exist, should
        be followed.
    type: bool
    default: true
  owner_id:
    description:
      - The owner ID to use when writing the file to disk.
      - If provided, O(group_id) must also be provided.
      - If not provided, the module will try to determine the user and group ID for the current user in the container. This
        will only work if C(/bin/sh) is present in the container and the C(id) binary or shell builtin is available. Also
        the container must be running.
    type: int
  group_id:
    description:
      - The group ID to use when writing the file to disk.
      - If provided, O(owner_id) must also be provided.
      - If not provided, the module will try to determine the user and group ID for the current user in the container. This
        will only work if C(/bin/sh) is present in the container and the C(id) binary or shell builtin is available. Also
        the container must be running.
    type: int
  mode:
    description:
      - The file mode to use when writing the file to disk.
      - Will use the file's mode from the source system if this option is not provided.
      - This option is parsed depending on how O(mode_parse) is set.
    type: raw
  mode_parse:
    description:
      - Determines how to parse the O(mode) parameter.
    type: str
    choices:
      legacy:
        - Parses the value of O(mode) as an integer.
        - Note that if you provide an octal number as a string to O(mode), it will be parsed as a B(decimal) number.
          If you provide an octal integer directly, though, it will work as expected.
        - This has been the default behavior of the module since it was added to community.docker.
      modern:
        - Parses the value of O(mode) as an octal string, or takes the integer value if an integer has been provided.
        - This is how M(ansible.builtin.copy) treats its O(ansible.builtin.copy#module:mode) option.
      octal_string_only:
        - Rejects everything that is not a string that can be parsed as an octal number.
        - Use this value to ensure that no accidental conversion to integers happen.
    default: legacy
    version_added: 4.6.0
  force:
    description:
      - If set to V(true), force writing the file (without performing any idempotency checks).
      - If set to V(false), only write the file if it does not exist on the target. If a filesystem object exists at the destination,
        the module will not do any change.
      - If this option is not specified, the module will be idempotent. To verify idempotency, it will try to get information
        on the filesystem object in the container, and if everything seems to match will download the file from the container
        to compare it to the file to upload.
    type: bool

extends_documentation_fragment:
  - community.docker._docker.api_documentation
  - community.docker._attributes
  - community.docker._attributes.actiongroup_docker

author:
  - "Felix Fontein (@felixfontein)"

requirements:
  - "Docker API >= 1.25"
"""

EXAMPLES = r"""
---
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
    owner_id: 0 # root
    group_id: 0 # root
    mode: "0755" # readable and executable by all users, writable by root
    mode_parse: modern # ensure that strings passed for 'mode' are passed as octal numbers
"""

RETURN = r"""
container_path:
  description:
    - The actual path in the container.
    - Can only be different from O(container_path) when O(follow=true).
  type: str
  returned: success
"""

import base64
import io
import os
import stat
import traceback
import typing as t

from ansible.module_utils.common.text.converters import to_bytes, to_text
from ansible.module_utils.common.validation import check_type_int

from ansible_collections.community.docker.plugins.module_utils._api.errors import (
    APIError,
    DockerException,
    NotFound,
)
from ansible_collections.community.docker.plugins.module_utils._common_api import (
    AnsibleDockerClient,
    RequestException,
)
from ansible_collections.community.docker.plugins.module_utils._copy import (
    DockerFileCopyError,
    DockerFileNotFound,
    DockerUnexpectedError,
    determine_user_group,
    fetch_file_ex,
    put_file,
    put_file_content,
    stat_file,
)
from ansible_collections.community.docker.plugins.module_utils._scramble import (
    generate_insecure_key,
    scramble,
)


if t.TYPE_CHECKING:
    import tarfile


def are_fileobjs_equal(f1: t.IO[bytes], f2: t.IO[bytes]) -> bool:
    """Given two (buffered) file objects, compare their contents."""
    f1on: t.IO[bytes] | None = f1
    f2on: t.IO[bytes] | None = f2
    blocksize = 65536
    b1buf = b""
    b2buf = b""
    while True:
        if f1on and len(b1buf) < blocksize:
            f1b = f1on.read(blocksize)
            if not f1b:
                # f1 is EOF, so stop reading from it
                f1on = None
            b1buf += f1b
        if f2on and len(b2buf) < blocksize:
            f2b = f2on.read(blocksize)
            if not f2b:
                # f2 is EOF, so stop reading from it
                f2on = None
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


def are_fileobjs_equal_read_first(
    f1: t.IO[bytes], f2: t.IO[bytes]
) -> tuple[bool, bytes]:
    """Given two (buffered) file objects, compare their contents.

    Returns a tuple (is_equal, content_of_f1), where the first element indicates
    whether the two file objects have the same content, and the second element is
    the content of the first file object."""
    f1on: t.IO[bytes] | None = f1
    f2on: t.IO[bytes] | None = f2
    blocksize = 65536
    b1buf = b""
    b2buf = b""
    is_equal = True
    content = []
    while True:
        if f1on and len(b1buf) < blocksize:
            f1b = f1on.read(blocksize)
            if not f1b:
                # f1 is EOF, so stop reading from it
                f1on = None
            b1buf += f1b
        if f2on and len(b2buf) < blocksize:
            f2b = f2on.read(blocksize)
            if not f2b:
                # f2 is EOF, so stop reading from it
                f2on = None
            b2buf += f2b
        if not b1buf or not b2buf:
            # At least one of f1 and f2 is EOF and all its data has
            # been processed. If both are EOF and their data has been
            # processed, the files are equal, otherwise not.
            is_equal = not b1buf and not b2buf
            break
        # Compare the next chunk of data, and remove it from the buffers
        buflen = min(len(b1buf), len(b2buf))
        if b1buf[:buflen] != b2buf[:buflen]:
            is_equal = False
            break
        content.append(b1buf[:buflen])
        b1buf = b1buf[buflen:]
        b2buf = b2buf[buflen:]

    content.append(b1buf)
    if f1on:
        content.append(f1on.read())

    return is_equal, b"".join(content)


def is_container_file_not_regular_file(container_stat: dict[str, t.Any]) -> bool:
    return any(
        container_stat["mode"] & 1 << bit != 0
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
        )
    )


def get_container_file_mode(container_stat: dict[str, t.Any]) -> int:
    mode = container_stat["mode"] & 0xFFF
    if container_stat["mode"] & (1 << (32 - 9)) != 0:  # ModeSetuid
        mode |= stat.S_ISUID  # set UID bit
    if container_stat["mode"] & (1 << (32 - 10)) != 0:  # ModeSetgid
        mode |= stat.S_ISGID  # set GID bit
    if container_stat["mode"] & (1 << (32 - 12)) != 0:  # ModeSticky
        mode |= stat.S_ISVTX  # sticky bit
    return mode


def add_other_diff(
    diff: dict[str, t.Any] | None, in_path: str, member: tarfile.TarInfo
) -> None:
    if diff is None:
        return
    diff["before_header"] = in_path
    if member.isdir():
        diff["before"] = "(directory)"
    elif member.issym() or member.islnk():
        diff["before"] = member.linkname
    elif member.ischr():
        diff["before"] = "(character device)"
    elif member.isblk():
        diff["before"] = "(block device)"
    elif member.isfifo():
        diff["before"] = "(fifo)"
    elif member.isdev():
        diff["before"] = "(device)"
    elif member.isfile():
        raise DockerUnexpectedError("should not be a regular file")
    else:
        diff["before"] = "(unknown filesystem object)"


def retrieve_diff(
    client: AnsibleDockerClient,
    container: str,
    container_path: str,
    follow_links: bool,
    diff: dict[str, t.Any] | None,
    max_file_size_for_diff: int,
    regular_stat: dict[str, t.Any] | None = None,
    link_target: str | None = None,
) -> None:
    if diff is None:
        return
    if regular_stat is not None:
        # First handle all filesystem object types that are not regular files
        if regular_stat["mode"] & (1 << (32 - 1)) != 0:
            diff["before_header"] = container_path
            diff["before"] = "(directory)"
            return
        if regular_stat["mode"] & (1 << (32 - 4)) != 0:
            diff["before_header"] = container_path
            diff["before"] = "(temporary file)"
            return
        if regular_stat["mode"] & (1 << (32 - 5)) != 0:
            diff["before_header"] = container_path
            diff["before"] = link_target
            return
        if regular_stat["mode"] & (1 << (32 - 6)) != 0:
            diff["before_header"] = container_path
            diff["before"] = "(device)"
            return
        if regular_stat["mode"] & (1 << (32 - 7)) != 0:
            diff["before_header"] = container_path
            diff["before"] = "(named pipe)"
            return
        if regular_stat["mode"] & (1 << (32 - 8)) != 0:
            diff["before_header"] = container_path
            diff["before"] = "(socket)"
            return
        if regular_stat["mode"] & (1 << (32 - 11)) != 0:
            diff["before_header"] = container_path
            diff["before"] = "(character device)"
            return
        if regular_stat["mode"] & (1 << (32 - 13)) != 0:
            diff["before_header"] = container_path
            diff["before"] = "(unknown filesystem object)"
            return
        # Check whether file is too large
        if regular_stat["size"] > max_file_size_for_diff > 0:
            diff["dst_larger"] = max_file_size_for_diff
            return

    # We need to get hold of the content
    def process_none(in_path: str) -> None:
        diff["before"] = ""

    def process_regular(
        in_path: str, tar: tarfile.TarFile, member: tarfile.TarInfo
    ) -> None:
        add_diff_dst_from_regular_member(
            diff, max_file_size_for_diff, in_path, tar, member
        )

    def process_symlink(in_path: str, member: tarfile.TarInfo) -> None:
        diff["before_header"] = in_path
        diff["before"] = member.linkname

    def process_other(in_path: str, member: tarfile.TarInfo) -> None:
        add_other_diff(diff, in_path, member)

    fetch_file_ex(
        client,
        container,
        in_path=container_path,
        process_none=process_none,
        process_regular=process_regular,
        process_symlink=process_symlink,
        process_other=process_other,
        follow_links=follow_links,
    )


def is_binary(content: bytes) -> bool:
    if b"\x00" in content:  # noqa: SIM103
        return True
    # TODO: better detection
    # (ansible-core also just checks for 0x00, and even just sticks to the first 8k, so this is not too bad...)
    return False


def are_fileobjs_equal_with_diff_of_first(
    f1: t.IO[bytes],
    f2: t.IO[bytes],
    size: int,
    diff: dict[str, t.Any] | None,
    max_file_size_for_diff: int,
    container_path: str,
) -> bool:
    if diff is None:
        return are_fileobjs_equal(f1, f2)
    if size > max_file_size_for_diff > 0:
        diff["dst_larger"] = max_file_size_for_diff
        return are_fileobjs_equal(f1, f2)
    is_equal, content = are_fileobjs_equal_read_first(f1, f2)
    if is_binary(content):
        diff["dst_binary"] = 1
    else:
        diff["before_header"] = container_path
        diff["before"] = to_text(content)
    return is_equal


def add_diff_dst_from_regular_member(
    diff: dict[str, t.Any] | None,
    max_file_size_for_diff: int,
    container_path: str,
    tar: tarfile.TarFile,
    member: tarfile.TarInfo,
) -> None:
    if diff is None:
        return
    if member.size > max_file_size_for_diff > 0:
        diff["dst_larger"] = max_file_size_for_diff
        return

    mf = tar.extractfile(member)
    if not mf:
        raise AssertionError("Member should be present for regular file")
    with mf as tar_f:
        content = tar_f.read()

    if is_binary(content):
        diff["dst_binary"] = 1
    else:
        diff["before_header"] = container_path
        diff["before"] = to_text(content)


def copy_dst_to_src(diff: dict[str, t.Any] | None) -> None:
    if diff is None:
        return
    for frm, to in [
        ("dst_size", "src_size"),
        ("dst_binary", "src_binary"),
        ("before_header", "after_header"),
        ("before", "after"),
    ]:
        if frm in diff:
            diff[to] = diff[frm]
        elif to in diff:
            diff.pop(to)


def is_file_idempotent(
    client: AnsibleDockerClient,
    container: str,
    managed_path: str,
    container_path: str,
    follow_links: bool,
    local_follow_links: bool,
    owner_id: int,
    group_id: int,
    mode: int | None,
    force: bool | None = False,
    diff: dict[str, t.Any] | None = None,
    max_file_size_for_diff: int = 1,
) -> tuple[str, int, bool]:
    # Retrieve information of local file
    try:
        file_stat = (
            os.stat(managed_path) if local_follow_links else os.lstat(managed_path)
        )
    except OSError as exc:
        if exc.errno == 2:
            raise DockerFileNotFound(f"Cannot find local file {managed_path}") from exc
        raise
    if mode is None:
        mode = stat.S_IMODE(file_stat.st_mode)
    if not stat.S_ISLNK(file_stat.st_mode) and not stat.S_ISREG(file_stat.st_mode):
        raise DockerFileCopyError(
            "Local path {managed_path} is not a symbolic link or file"
        )

    if diff is not None:
        if file_stat.st_size > max_file_size_for_diff > 0:
            diff["src_larger"] = max_file_size_for_diff
        elif stat.S_ISLNK(file_stat.st_mode):
            diff["after_header"] = managed_path
            diff["after"] = os.readlink(managed_path)
        else:
            with open(managed_path, "rb") as f:
                content = f.read()
            if is_binary(content):
                diff["src_binary"] = 1
            else:
                diff["after_header"] = managed_path
                diff["after"] = to_text(content)

    # When forcing and we are not following links in the container, go!
    if force and not follow_links:
        retrieve_diff(
            client,
            container,
            container_path,
            follow_links,
            diff,
            max_file_size_for_diff,
        )
        return container_path, mode, False

    # Resolve symlinks in the container (if requested), and get information on container's file
    real_container_path, regular_stat, link_target = stat_file(
        client,
        container,
        in_path=container_path,
        follow_links=follow_links,
    )

    # Follow links in the Docker container?
    if follow_links:
        container_path = real_container_path

    # If the file was not found, continue
    if regular_stat is None:
        if diff is not None:
            diff["before_header"] = container_path
            diff["before"] = ""
        return container_path, mode, False

    # When forcing, go!
    if force:
        retrieve_diff(
            client,
            container,
            container_path,
            follow_links,
            diff,
            max_file_size_for_diff,
            regular_stat,
            link_target,
        )
        return container_path, mode, False

    # If force is set to False, and the destination exists, assume there's nothing to do
    if force is False:
        retrieve_diff(
            client,
            container,
            container_path,
            follow_links,
            diff,
            max_file_size_for_diff,
            regular_stat,
            link_target,
        )
        copy_dst_to_src(diff)
        return container_path, mode, True

    # Basic idempotency checks
    if stat.S_ISLNK(file_stat.st_mode):
        if link_target is None:
            retrieve_diff(
                client,
                container,
                container_path,
                follow_links,
                diff,
                max_file_size_for_diff,
                regular_stat,
                link_target,
            )
            return container_path, mode, False
        local_link_target = os.readlink(managed_path)
        retrieve_diff(
            client,
            container,
            container_path,
            follow_links,
            diff,
            max_file_size_for_diff,
            regular_stat,
            link_target,
        )
        return container_path, mode, local_link_target == link_target
    if link_target is not None:
        retrieve_diff(
            client,
            container,
            container_path,
            follow_links,
            diff,
            max_file_size_for_diff,
            regular_stat,
            link_target,
        )
        return container_path, mode, False
    if is_container_file_not_regular_file(regular_stat):
        retrieve_diff(
            client,
            container,
            container_path,
            follow_links,
            diff,
            max_file_size_for_diff,
            regular_stat,
            link_target,
        )
        return container_path, mode, False
    if file_stat.st_size != regular_stat["size"]:
        retrieve_diff(
            client,
            container,
            container_path,
            follow_links,
            diff,
            max_file_size_for_diff,
            regular_stat,
            link_target,
        )
        return container_path, mode, False
    if mode != get_container_file_mode(regular_stat):
        retrieve_diff(
            client,
            container,
            container_path,
            follow_links,
            diff,
            max_file_size_for_diff,
            regular_stat,
            link_target,
        )
        return container_path, mode, False

    # Fetch file from container
    def process_none(in_path: str) -> tuple[str, int, bool]:
        return container_path, mode, False

    def process_regular(
        in_path: str, tar: tarfile.TarFile, member: tarfile.TarInfo
    ) -> tuple[str, int, bool]:
        # Check things like user/group ID and mode
        if any(
            [
                member.mode & 0xFFF != mode,
                member.uid != owner_id,
                member.gid != group_id,
                not stat.S_ISREG(file_stat.st_mode),
                member.size != file_stat.st_size,
            ]
        ):
            add_diff_dst_from_regular_member(
                diff, max_file_size_for_diff, in_path, tar, member
            )
            return container_path, mode, False

        mf = tar.extractfile(member)
        if mf is None:
            raise AssertionError("Member should be present for regular file")
        with mf as tar_f, open(managed_path, "rb") as local_f:
            is_equal = are_fileobjs_equal_with_diff_of_first(
                tar_f, local_f, member.size, diff, max_file_size_for_diff, in_path
            )
        return container_path, mode, is_equal

    def process_symlink(in_path: str, member: tarfile.TarInfo) -> tuple[str, int, bool]:
        if diff is not None:
            diff["before_header"] = in_path
            diff["before"] = member.linkname

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

    def process_other(in_path: str, member: tarfile.TarInfo) -> tuple[str, int, bool]:
        add_other_diff(diff, in_path, member)
        return container_path, mode, False

    return fetch_file_ex(
        client,
        container,
        in_path=container_path,
        process_none=process_none,
        process_regular=process_regular,
        process_symlink=process_symlink,
        process_other=process_other,
        follow_links=follow_links,
    )


def copy_file_into_container(
    client: AnsibleDockerClient,
    container: str,
    managed_path: str,
    container_path: str,
    follow_links: bool,
    local_follow_links: bool,
    owner_id: int,
    group_id: int,
    mode: int | None,
    force: bool | None = False,
    do_diff: bool = False,
    max_file_size_for_diff: int = 1,
) -> t.NoReturn:
    diff: dict[str, t.Any] | None
    diff = {} if do_diff else None

    container_path, mode, idempotent = is_file_idempotent(
        client,
        container,
        managed_path,
        container_path,
        follow_links,
        local_follow_links,
        owner_id,
        group_id,
        mode,
        force=force,
        diff=diff,
        max_file_size_for_diff=max_file_size_for_diff,
    )
    changed = not idempotent

    if changed and not client.module.check_mode:
        put_file(
            client,
            container,
            in_path=managed_path,
            out_path=container_path,
            user_id=owner_id,
            group_id=group_id,
            mode=mode,
            follow_links=local_follow_links,
        )

    result = {
        "container_path": container_path,
        "changed": changed,
    }
    if diff:
        result["diff"] = diff
    client.module.exit_json(**result)


def is_content_idempotent(
    client: AnsibleDockerClient,
    container: str,
    content: bytes,
    container_path: str,
    follow_links: bool,
    owner_id: int,
    group_id: int,
    mode: int,
    force: bool | None = False,
    diff: dict[str, t.Any] | None = None,
    max_file_size_for_diff: int = 1,
) -> tuple[str, int, bool]:
    if diff is not None:
        if len(content) > max_file_size_for_diff > 0:
            diff["src_larger"] = max_file_size_for_diff
        elif is_binary(content):
            diff["src_binary"] = 1
        else:
            diff["after_header"] = "dynamically generated"
            diff["after"] = to_text(content)

    # When forcing and we are not following links in the container, go!
    if force and not follow_links:
        retrieve_diff(
            client,
            container,
            container_path,
            follow_links,
            diff,
            max_file_size_for_diff,
        )
        return container_path, mode, False

    # Resolve symlinks in the container (if requested), and get information on container's file
    real_container_path, regular_stat, link_target = stat_file(
        client,
        container,
        in_path=container_path,
        follow_links=follow_links,
    )

    # Follow links in the Docker container?
    if follow_links:
        container_path = real_container_path

    # If the file was not found, continue
    if regular_stat is None:
        if diff is not None:
            diff["before_header"] = container_path
            diff["before"] = ""
        return container_path, mode, False

    # When forcing, go!
    if force:
        retrieve_diff(
            client,
            container,
            container_path,
            follow_links,
            diff,
            max_file_size_for_diff,
            regular_stat,
            link_target,
        )
        return container_path, mode, False

    # If force is set to False, and the destination exists, assume there's nothing to do
    if force is False:
        retrieve_diff(
            client,
            container,
            container_path,
            follow_links,
            diff,
            max_file_size_for_diff,
            regular_stat,
            link_target,
        )
        copy_dst_to_src(diff)
        return container_path, mode, True

    # Basic idempotency checks
    if link_target is not None:
        retrieve_diff(
            client,
            container,
            container_path,
            follow_links,
            diff,
            max_file_size_for_diff,
            regular_stat,
            link_target,
        )
        return container_path, mode, False
    if is_container_file_not_regular_file(regular_stat):
        retrieve_diff(
            client,
            container,
            container_path,
            follow_links,
            diff,
            max_file_size_for_diff,
            regular_stat,
            link_target,
        )
        return container_path, mode, False
    if len(content) != regular_stat["size"]:
        retrieve_diff(
            client,
            container,
            container_path,
            follow_links,
            diff,
            max_file_size_for_diff,
            regular_stat,
            link_target,
        )
        return container_path, mode, False
    if mode != get_container_file_mode(regular_stat):
        retrieve_diff(
            client,
            container,
            container_path,
            follow_links,
            diff,
            max_file_size_for_diff,
            regular_stat,
            link_target,
        )
        return container_path, mode, False

    # Fetch file from container
    def process_none(in_path: str) -> tuple[str, int, bool]:
        if diff is not None:
            diff["before"] = ""
        return container_path, mode, False

    def process_regular(
        in_path: str, tar: tarfile.TarFile, member: tarfile.TarInfo
    ) -> tuple[str, int, bool]:
        # Check things like user/group ID and mode
        if any(
            [
                member.mode & 0xFFF != mode,
                member.uid != owner_id,
                member.gid != group_id,
                member.size != len(content),
            ]
        ):
            add_diff_dst_from_regular_member(
                diff, max_file_size_for_diff, in_path, tar, member
            )
            return container_path, mode, False

        mf = tar.extractfile(member)
        if mf is None:
            raise AssertionError("Member should be present for regular file")
        with mf as tar_f:
            is_equal = are_fileobjs_equal_with_diff_of_first(
                tar_f,
                io.BytesIO(content),
                member.size,
                diff,
                max_file_size_for_diff,
                in_path,
            )
        return container_path, mode, is_equal

    def process_symlink(in_path: str, member: tarfile.TarInfo) -> tuple[str, int, bool]:
        if diff is not None:
            diff["before_header"] = in_path
            diff["before"] = member.linkname

        return container_path, mode, False

    def process_other(in_path: str, member: tarfile.TarInfo) -> tuple[str, int, bool]:
        add_other_diff(diff, in_path, member)
        return container_path, mode, False

    return fetch_file_ex(
        client,
        container,
        in_path=container_path,
        process_none=process_none,
        process_regular=process_regular,
        process_symlink=process_symlink,
        process_other=process_other,
        follow_links=follow_links,
    )


def copy_content_into_container(
    client: AnsibleDockerClient,
    container: str,
    content: bytes,
    container_path: str,
    follow_links: bool,
    owner_id: int,
    group_id: int,
    mode: int,
    force: bool | None = False,
    do_diff: bool = False,
    max_file_size_for_diff: int = 1,
) -> t.NoReturn:
    diff: dict[str, t.Any] | None = {} if do_diff else None

    container_path, mode, idempotent = is_content_idempotent(
        client,
        container,
        content,
        container_path,
        follow_links,
        owner_id,
        group_id,
        mode,
        force=force,
        diff=diff,
        max_file_size_for_diff=max_file_size_for_diff,
    )
    changed = not idempotent

    if changed and not client.module.check_mode:
        put_file_content(
            client,
            container,
            content=content,
            out_path=container_path,
            user_id=owner_id,
            group_id=group_id,
            mode=mode,
        )

    result = {
        "container_path": container_path,
        "changed": changed,
    }
    if diff:
        # Since the content is no_log, make sure that the before/after strings look sufficiently different
        key = generate_insecure_key()
        diff["scrambled_diff"] = base64.b64encode(key)
        for k in ("before", "after"):
            if k in diff:
                diff[k] = scramble(diff[k], key)
        result["diff"] = diff
    client.module.exit_json(**result)


def parse_modern(mode: str | int) -> int:
    if isinstance(mode, str):
        return int(to_text(mode), 8)
    if isinstance(mode, int):
        return mode
    raise TypeError(f"must be an octal string or an integer, got {mode!r}")


def parse_octal_string_only(mode: str) -> int:
    if isinstance(mode, str):
        return int(to_text(mode), 8)
    raise TypeError(f"must be an octal string, got {mode!r}")


def main() -> None:
    argument_spec = {
        "container": {"type": "str", "required": True},
        "path": {"type": "path"},
        "container_path": {"type": "str", "required": True},
        "follow": {"type": "bool", "default": False},
        "local_follow": {"type": "bool", "default": True},
        "owner_id": {"type": "int"},
        "group_id": {"type": "int"},
        "mode": {"type": "raw"},
        "mode_parse": {
            "type": "str",
            "choices": ["legacy", "modern", "octal_string_only"],
            "default": "legacy",
        },
        "force": {"type": "bool"},
        "content": {"type": "str", "no_log": True},
        "content_is_b64": {"type": "bool", "default": False},
        # Undocumented parameters for use by the action plugin
        "_max_file_size_for_diff": {"type": "int"},
    }

    client = AnsibleDockerClient(
        argument_spec=argument_spec,
        min_docker_api_version="1.20",
        supports_check_mode=True,
        mutually_exclusive=[("path", "content")],
        required_together=[("owner_id", "group_id")],
        required_by={
            "content": ["mode"],
        },
    )

    container: str = client.module.params["container"]
    managed_path: str | None = client.module.params["path"]
    container_path: str = client.module.params["container_path"]
    follow: bool = client.module.params["follow"]
    local_follow: bool = client.module.params["local_follow"]
    owner_id: int | None = client.module.params["owner_id"]
    group_id: int | None = client.module.params["group_id"]
    mode: t.Any = client.module.params["mode"]
    force: bool | None = client.module.params["force"]
    content_str: str | None = client.module.params["content"]
    max_file_size_for_diff: int = client.module.params["_max_file_size_for_diff"] or 1

    if mode is not None:
        mode_parse: t.Literal["legacy", "modern", "octal_string_only"] = (
            client.module.params["mode_parse"]
        )
        try:
            if mode_parse == "legacy":
                mode = check_type_int(mode)
            elif mode_parse == "modern":
                mode = parse_modern(mode)
            elif mode_parse == "octal_string_only":
                mode = parse_octal_string_only(mode)
        except (TypeError, ValueError) as e:
            client.fail(f"Error while parsing 'mode': {e}")
        if mode < 0:
            client.fail(f"'mode' must not be negative; got {mode}")

    content: bytes | None = None
    if content_str is not None:
        if client.module.params["content_is_b64"]:
            try:
                content = base64.b64decode(content_str)
            except Exception as e:  # pylint: disable=broad-exception-caught
                client.fail(f"Cannot Base64 decode the content option: {e}")
        else:
            content = to_bytes(content_str)

    if not container_path.startswith(os.path.sep):
        container_path = os.path.join(os.path.sep, container_path)
    container_path = os.path.normpath(container_path)

    try:
        if owner_id is None or group_id is None:
            owner_id, group_id = determine_user_group(client, container)

        if content is not None:
            assert mode is not None  # see required_by above
            copy_content_into_container(
                client,
                container,
                content,
                container_path,
                follow_links=follow,
                owner_id=owner_id,
                group_id=group_id,
                mode=mode,
                force=force,
                do_diff=client.module._diff,
                max_file_size_for_diff=max_file_size_for_diff,
            )
        elif managed_path is not None:
            copy_file_into_container(
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
                do_diff=client.module._diff,
                max_file_size_for_diff=max_file_size_for_diff,
            )
        else:
            # Can happen if a user explicitly passes `content: null` or `path: null`...
            client.fail("One of path and content must be supplied")
    except NotFound as exc:
        client.fail(f'Could not find container "{container}" or resource in it ({exc})')
    except APIError as exc:
        client.fail(
            f'An unexpected Docker error occurred for container "{container}": {exc}',
            exception=traceback.format_exc(),
        )
    except DockerException as exc:
        client.fail(
            f'An unexpected Docker error occurred for container "{container}": {exc}',
            exception=traceback.format_exc(),
        )
    except RequestException as exc:
        client.fail(
            f'An unexpected requests error occurred for container "{container}" when trying to talk to the Docker daemon: {exc}',
            exception=traceback.format_exc(),
        )
    except DockerUnexpectedError as exc:
        client.fail(f"Unexpected error: {exc}", exception=traceback.format_exc())
    except DockerFileCopyError as exc:
        client.fail(to_text(exc))
    except OSError as exc:
        client.fail(f"Unexpected error: {exc}", exception=traceback.format_exc())


if __name__ == "__main__":
    main()
