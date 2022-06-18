# -*- coding: utf-8 -*-
# This code is part of the Ansible collection community.docker, but is an independent component.
# This particular file, and this file only, is based on the Docker SDK for Python (https://github.com/docker/docker-py/)
#
# Copyright (c) 2016-2022 Docker, Inc.
#
# It is licensed under the Apache 2.0 license (see Apache-2.0.txt in this collection)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import errno
import os
import select
import socket as pysocket
import struct

from ansible.module_utils.six import PY3, binary_type

from ..transport.npipesocket import NpipeSocket


STDOUT = 1
STDERR = 2


class SocketError(Exception):
    pass


def read(socket, n=4096):
    """
    Reads at most n bytes from socket
    """

    recoverable_errors = (errno.EINTR, errno.EDEADLK, errno.EWOULDBLOCK)

    if PY3 and not isinstance(socket, NpipeSocket):
        select.select([socket], [], [])

    try:
        if hasattr(socket, 'recv'):
            return socket.recv(n)
        if PY3 and isinstance(socket, getattr(pysocket, 'SocketIO')):
            return socket.read(n)
        return os.read(socket.fileno(), n)
    except EnvironmentError as e:
        if e.errno not in recoverable_errors:
            raise


def read_exactly(socket, n):
    """
    Reads exactly n bytes from socket
    Raises SocketError if there isn't enough data
    """
    data = binary_type()
    while len(data) < n:
        next_data = read(socket, n - len(data))
        if not next_data:
            raise SocketError("Unexpected EOF")
        data += next_data
    return data


def next_frame_header(socket):
    """
    Returns the stream and size of the next frame of data waiting to be read
    from socket, according to the protocol defined here:

    https://docs.docker.com/engine/api/v1.24/#attach-to-a-container
    """
    try:
        data = read_exactly(socket, 8)
    except SocketError:
        return (-1, -1)

    stream, actual = struct.unpack('>BxxxL', data)
    return (stream, actual)


def frames_iter(socket, tty):
    """
    Return a generator of frames read from socket. A frame is a tuple where
    the first item is the stream number and the second item is a chunk of data.

    If the tty setting is enabled, the streams are multiplexed into the stdout
    stream.
    """
    if tty:
        return ((STDOUT, frame) for frame in frames_iter_tty(socket))
    else:
        return frames_iter_no_tty(socket)


def frames_iter_no_tty(socket):
    """
    Returns a generator of data read from the socket when the tty setting is
    not enabled.
    """
    while True:
        (stream, n) = next_frame_header(socket)
        if n < 0:
            break
        while n > 0:
            result = read(socket, n)
            if result is None:
                continue
            data_length = len(result)
            if data_length == 0:
                # We have reached EOF
                return
            n -= data_length
            yield (stream, result)


def frames_iter_tty(socket):
    """
    Return a generator of data read from the socket when the tty setting is
    enabled.
    """
    while True:
        result = read(socket)
        if len(result) == 0:
            # We have reached EOF
            return
        yield result


def consume_socket_output(frames, demux=False):
    """
    Iterate through frames read from the socket and return the result.

    Args:

        demux (bool):
            If False, stdout and stderr are multiplexed, and the result is the
            concatenation of all the frames. If True, the streams are
            demultiplexed, and the result is a 2-tuple where each item is the
            concatenation of frames belonging to the same stream.
    """
    if demux is False:
        # If the streams are multiplexed, the generator returns strings, that
        # we just need to concatenate.
        return binary_type().join(frames)

    # If the streams are demultiplexed, the generator yields tuples
    # (stdout, stderr)
    out = [None, None]
    for frame in frames:
        # It is guaranteed that for each frame, one and only one stream
        # is not None.
        if frame == (None, None):
            raise AssertionError('frame must be (None, None), but got %s' % (frame, ))
        if frame[0] is not None:
            if out[0] is None:
                out[0] = frame[0]
            else:
                out[0] += frame[0]
        else:
            if out[1] is None:
                out[1] = frame[1]
            else:
                out[1] += frame[1]
    return tuple(out)


def demux_adaptor(stream_id, data):
    """
    Utility to demultiplex stdout and stderr when reading frames from the
    socket.
    """
    if stream_id == STDOUT:
        return (data, None)
    elif stream_id == STDERR:
        return (None, data)
    else:
        raise ValueError('{0} is not a valid stream'.format(stream_id))
