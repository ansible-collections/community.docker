# Copyright 2016 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import base64
import io
import json
import os
import os.path
import shutil
import tarfile

from ansible.module_utils.common.text.converters import to_bytes, to_native, to_text
from ansible.module_utils.six import raise_from

from ansible_collections.community.docker.plugins.module_utils.common_api import (
    RequestException,
)

from ansible_collections.community.docker.plugins.module_utils._api.errors import APIError, DockerException, NotFound


class DockerFileCopyError(Exception):
    pass


class DockerUnexpectedError(DockerFileCopyError):
    pass


class DockerFileNotFound(DockerFileCopyError):
    pass


def _put_archive(client, container, path, data):
    # data can also be file object for streaming. This is because _put uses requests's put().
    # See https://2.python-requests.org/en/master/user/advanced/#streaming-uploads
    # WARNING: might not work with all transports!
    url = client._url('/containers/{0}/archive', container)
    res = client._put(url, params={'path': path}, data=data)
    client._raise_for_status(res)
    return res.status_code == 200


def put_file(call_client, container, in_path, out_path, user_id, group_id, mode=None, user_name=None, follow_links=False, log=None):
    """Transfer a file from local to Docker container."""
    if not os.path.exists(to_bytes(in_path, errors='surrogate_or_strict')):
        raise DockerFileNotFound(
            "file or module does not exist: %s" % to_native(in_path))

    b_in_path = to_bytes(in_path, errors='surrogate_or_strict')

    out_dir, out_file = os.path.split(out_path)

    # TODO: stream tar file, instead of creating it in-memory into a BytesIO

    bio = io.BytesIO()
    with tarfile.open(fileobj=bio, mode='w|', dereference=follow_links, encoding='utf-8') as tar:
        # Note that without both name (bytes) and arcname (unicode), this either fails for
        # Python 2.7, Python 3.5/3.6, or Python 3.7+. Only when passing both (in this
        # form) it works with Python 2.7, 3.5, 3.6, and 3.7 up to 3.11
        tarinfo = tar.gettarinfo(b_in_path, arcname=to_text(out_file))
        tarinfo.uid = user_id
        tarinfo.uname = ''
        if user_name:
            tarinfo.uname = user_name
        tarinfo.gid = group_id
        tarinfo.gname = ''
        tarinfo.mode &= 0o700
        if mode is not None:
            tarinfo.mode = mode
        if os.path.isfile(b_in_path) or follow_links:
            with open(b_in_path, 'rb') as f:
                tar.addfile(tarinfo, fileobj=f)
        else:
            tar.addfile(tarinfo)
    data = bio.getvalue()

    ok = call_client(
        lambda client: _put_archive(
            client,
            container,
            out_dir,
            data,
        )
    )
    if not ok:
        raise DockerFileCopyError('Unknown error while creating file "{0}" in container "{1}".'.format(out_path, container))


def stat_file(call_client, container, in_path, follow_links=False, log=None):
    """Fetch information on a file from a Docker container to local.

    Return a tuple ``(path, stat_data, link_target)`` where:

    :path: is the resolved path in case ``follow_links=True``;
    :stat_data: is ``None`` if the file does not exist, or a dictionary with fields
        ``name`` (string), ``size`` (integer), ``mode`` (integer, see https://pkg.go.dev/io/fs#FileMode),
        ``mtime`` (string), and ``linkTarget`` (string);
    :link_target: is ``None`` if the file is not a symlink or when ``follow_links=False``,
        and a string with the symlink target otherwise.
    """
    considered_in_paths = set()

    while True:
        if in_path in considered_in_paths:
            raise DockerFileCopyError('Found infinite symbolic link loop when trying to stating "{0}"'.format(in_path))
        considered_in_paths.add(in_path)

        if log:
            log('FETCH: Stating "%s"' % in_path)

        def f(client):
            response = client._head(
                client._url('/containers/{0}/archive', container),
                params={'path': in_path},
            )
            if response.status_code == 404:
                return None
            client._raise_for_status(response)
            header = response.headers.get('x-docker-container-path-stat')
            try:
                return json.loads(base64.b64decode(header))
            except Exception as exc:
                raise DockerUnexpectedError(
                    'When retrieving information for {in_path} from {container}, obtained header {header!r} that cannot be loaded as JSON: {exc}'
                    .format(in_path=in_path, container=container, header=header, exc=exc)
                )

        stat_data = call_client(f)
        if stat_data is None:
            return in_path, None, None

        # https://pkg.go.dev/io/fs#FileMode: bit 32 - 5 means ModeSymlink
        if stat_data['mode'] & (1 << (32 - 5)) != 0:
            link_target = stat_data['linkTarget']
            if not follow_links:
                return in_path, stat_data, link_target
            in_path = os.path.join(os.path.split(in_path)[0], link_target)
            continue

        return in_path, stat_data, None


class _RawGeneratorFileobj(io.RawIOBase):
    def __init__(self, stream):
        self._stream = stream
        self._buf = b''

    def readable(self):
        return True

    def _readinto_from_buf(self, b, index, length):
        cpy = min(length - index, len(self._buf))
        if cpy:
            b[index:index + cpy] = self._buf[:cpy]
            self._buf = self._buf[cpy:]
            index += cpy
        return index

    def readinto(self, b):
        index = 0
        length = len(b)

        index = self._readinto_from_buf(b, index, length)
        if index == length:
            return index

        try:
            self._buf += next(self._stream)
        except StopIteration:
            return index

        return self._readinto_from_buf(b, index, length)


def _stream_generator_to_fileobj(stream):
    '''Given a generator that generates chunks of bytes, create a readable buffered stream.'''
    raw = _RawGeneratorFileobj(stream)
    return io.BufferedReader(raw)


def fetch_file_ex(call_client, container, in_path, process_none, process_regular, process_symlink, follow_links=False, log=None):
    """Fetch a file (as a tar file entry) from a Docker container to local."""
    considered_in_paths = set()

    while True:
        if in_path in considered_in_paths:
            raise DockerFileCopyError('Found infinite symbolic link loop when trying to fetch "{0}"'.format(in_path))
        considered_in_paths.add(in_path)

        if log:
            log('FETCH: Fetching "%s"' % in_path)
        try:
            stream = call_client(
                lambda client: client.get_raw_stream(
                    '/containers/{0}/archive', container,
                    params={'path': in_path},
                    headers={'Accept-Encoding': 'identity'},
                )
            )
        except DockerFileNotFound:
            return process_none(in_path)

        with tarfile.open(fileobj=_stream_generator_to_fileobj(stream), mode='r|') as tar:
            file_member = None
            symlink_member = None
            result = None
            found = False
            for member in tar:
                if found:
                    raise DockerFileCopyError('Received tarfile contains more than one file!')
                found = True
                if member.issym():
                    symlink_member = member
                    continue
                if member.isfile():
                    result = process_regular(in_path, tar, member)
                    continue
                raise DockerFileCopyError('Remote file "%s" is not a regular file or a symbolic link' % in_path)
            if symlink_member:
                if not follow_links:
                    return process_symlink(in_path, symlink_member)
                in_path = os.path.join(os.path.split(in_path)[0], symlink_member.linkname)
                if log:
                    log('FETCH: Following symbolic link to "%s"' % in_path)
                continue
            if found:
                return result
            raise DockerUnexpectedError('Received tarfile is empty!')


def fetch_file(call_client, container, in_path, out_path, follow_links=False, log=None):
    b_out_path = to_bytes(out_path, errors='surrogate_or_strict')

    def process_none(in_path):
        raise DockerFileNotFound(
            'File {in_path} does not exist in container {container}'
            .format(in_path=in_path, container=container)
        )

    def process_regular(in_path, tar, member):
        if not follow_links and os.path.exists(b_out_path):
            os.unlink(b_out_path)

        in_f = tar.extractfile(member)  # in Python 2, this *cannot* be used in `with`...
        with open(b_out_path, 'wb') as out_f:
            shutil.copyfileobj(in_f, out_f)
        return in_path

    def process_symlink(in_path, member):
        if os.path.exists(b_out_path):
            os.unlink(b_out_path)

        os.symlink(member.linkname, b_out_path)
        return in_path

    return fetch_file_ex(call_client, container, in_path, process_none, process_regular, process_symlink, follow_links=follow_links, log=log)


def call_client(client, container, use_file_not_found_exception=False):
    def f(callback):
        try:
            return callback(client)
        except NotFound as e:
            if use_file_not_found_exception:
                raise_from(DockerFileNotFound(to_native(e)), e)
            raise_from(
                DockerFileCopyError('Could not find container "{1}" or resource in it ({0})'.format(e, container)),
                e,
            )
        except APIError as e:
            if e.response is not None and e.response.status_code == 409:
                raise_from(
                    DockerFileCopyError('The container "{1}" has been paused ({0})'.format(e, container)),
                    e,
                )
            raise_from(
                DockerUnexpectedError('An unexpected Docker error occurred for container "{1}": {0}'.format(e, container)),
                e,
            )
        except DockerException as e:
            raise_from(
                DockerUnexpectedError('An unexpected Docker error occurred for container "{1}": {0}'.format(e, container)),
                e,
            )
        except RequestException as e:
            raise_from(
                DockerUnexpectedError(
                    'An unexpected requests error occurred for container "{1}" when trying to talk to the Docker daemon: {0}'.format(e, container)),
                e,
            )

    return f


def _execute_command(client, container, command, log=None, check_rc=False):
    if log:
        log('Executing {command} in {container}'.format(command=command, container=container))

    data = {
        'Container': container,
        'User': '',
        'Privileged': False,
        'Tty': False,
        'AttachStdin': False,
        'AttachStdout': True,
        'AttachStderr': True,
        'Cmd': command,
    }

    if 'detachKeys' in client._general_configs:
        data['detachKeys'] = client._general_configs['detachKeys']

    try:
        exec_data = client.post_json_to_json('/containers/{0}/exec', container, data=data)
    except APIError as e:
        if e.response is not None and e.response.status_code == 409:
            raise_from(
                DockerFileCopyError('Cannot execute command in paused container "{0}"'.format(container)),
                e,
            )
        raise
    exec_id = exec_data['Id']

    data = {
        'Tty': False,
        'Detach': False
    }
    stdout, stderr = client.post_json_to_stream('/exec/{0}/start', exec_id, stream=False, demux=True, tty=False)

    result = client.get_json('/exec/{0}/json', exec_id)

    rc = result.get('ExitCode') or 0
    stdout = stdout or b''
    stderr = stderr or b''

    if log:
        log('Exit code {rc}, stdout {stdout!r}, stderr {stderr!r}'.format(rc=rc, stdout=stdout, stderr=stderr))

    if check_rc and rc != 0:
        raise DockerFileCopyError(
            'Obtained unexpected exit code {rc} when running "{command}" in {container}.\nSTDOUT: {stdout}\nSTDERR: {stderr}'
            .format(command=' '.join(command), container=container, rc=rc, stdout=stdout, stderr=stderr)
        )

    return rc, stdout, stderr


def determine_user_group(client, container, log=None):
    dummy, stdout, stderr = _execute_command(client, container, ['/bin/sh', '-c', 'id -u && id -g'], check_rc=True, log=log)

    stdout_lines = stdout.splitlines()
    if len(stdout_lines) != 2:
        raise DockerFileCopyError(
            'Expected two-line output to obtain user and group ID for container {container}, but got {lc} lines:\n{stdout}'
            .format(container=container, lc=len(stdout_lines), stdout=stdout)
        )

    user_id, group_id = stdout_lines
    try:
        return int(user_id), int(group_id)
    except ValueError:
        raise DockerFileCopyError(
            'Expected two-line output with numeric IDs to obtain user and group ID for container {container}, but got "{l1}" and "{l2}" instead'
            .format(container=container, l1=user_id, l2=group_id)
        )
