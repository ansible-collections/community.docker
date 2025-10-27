# This code is part of the Ansible collection community.docker, but is an independent component.
# This particular file, and this file only, is based on the Docker SDK for Python (https://github.com/docker/docker-py/)
#
# Copyright (c) 2016-2022 Docker, Inc.
#
# It is licensed under the Apache 2.0 license (see LICENSES/Apache-2.0.txt in this collection)
# SPDX-License-Identifier: Apache-2.0

# Note that this module util is **PRIVATE** to the collection. It can have breaking changes at any time.
# Do not use this from other collections or standalone plugins/modules!

from __future__ import annotations

import errno
import os
import select
import socket as pysocket
import struct
import typing as t

from ..transport.npipesocket import NpipeSocket


if t.TYPE_CHECKING:
    from collections.abc import Sequence

    from ..._socket_helper import SocketLike


STDOUT = 1
STDERR = 2


class SocketError(Exception):
    pass


# NpipeSockets have their own error types
# pywintypes.error: (109, 'ReadFile', 'The pipe has been ended.')
NPIPE_ENDED = 109


def read(socket: SocketLike, n: int = 4096) -> bytes | None:
    """
    Reads at most n bytes from socket
    """

    recoverable_errors = (errno.EINTR, errno.EDEADLK, errno.EWOULDBLOCK)

    if not isinstance(socket, NpipeSocket):  # type: ignore[unreachable]
        if not hasattr(select, "poll"):
            # Limited to 1024
            select.select([socket], [], [])
        else:
            poll = select.poll()
            poll.register(socket, select.POLLIN | select.POLLPRI)
            poll.poll()

    try:
        if hasattr(socket, "recv"):
            return socket.recv(n)
        if isinstance(socket, pysocket.SocketIO):  # type: ignore
            return socket.read(n)  # type: ignore[unreachable]
        return os.read(socket.fileno(), n)
    except EnvironmentError as e:
        if e.errno not in recoverable_errors:
            raise
        return None  # TODO ???
    except Exception as e:
        is_pipe_ended = (
            isinstance(socket, NpipeSocket)  # type: ignore[unreachable]
            and len(e.args) > 0
            and e.args[0] == NPIPE_ENDED
        )
        if is_pipe_ended:
            # npipes do not support duplex sockets, so we interpret
            # a PIPE_ENDED error as a close operation (0-length read).
            return b""
        raise


def read_exactly(socket: SocketLike, n: int) -> bytes:
    """
    Reads exactly n bytes from socket
    Raises SocketError if there is not enough data
    """
    data = b""
    while len(data) < n:
        next_data = read(socket, n - len(data))
        if not next_data:
            raise SocketError("Unexpected EOF")
        data += next_data
    return data


def next_frame_header(socket: SocketLike) -> tuple[int, int]:
    """
    Returns the stream and size of the next frame of data waiting to be read
    from socket, according to the protocol defined here:

    https://docs.docker.com/engine/api/v1.24/#attach-to-a-container
    """
    try:
        data = read_exactly(socket, 8)
    except SocketError:
        return (-1, -1)

    stream, actual = struct.unpack(">BxxxL", data)
    return (stream, actual)


def frames_iter(socket: SocketLike, tty: bool) -> t.Generator[tuple[int, bytes]]:
    """
    Return a generator of frames read from socket. A frame is a tuple where
    the first item is the stream number and the second item is a chunk of data.

    If the tty setting is enabled, the streams are multiplexed into the stdout
    stream.
    """
    if tty:
        return ((STDOUT, frame) for frame in frames_iter_tty(socket))
    return frames_iter_no_tty(socket)


def frames_iter_no_tty(socket: SocketLike) -> t.Generator[tuple[int, bytes]]:
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


def frames_iter_tty(socket: SocketLike) -> t.Generator[bytes]:
    """
    Return a generator of data read from the socket when the tty setting is
    enabled.
    """
    while True:
        result = read(socket)
        if not result:
            # We have reached EOF
            return
        yield result


@t.overload
def consume_socket_output(
    frames: Sequence[bytes] | t.Generator[bytes], demux: t.Literal[False] = False
) -> bytes: ...


@t.overload
def consume_socket_output(
    frames: (
        Sequence[tuple[bytes | None, bytes | None]]
        | t.Generator[tuple[bytes | None, bytes | None]]
    ),
    demux: t.Literal[True],
) -> tuple[bytes, bytes]: ...


@t.overload
def consume_socket_output(
    frames: (
        Sequence[bytes]
        | Sequence[tuple[bytes | None, bytes | None]]
        | t.Generator[bytes]
        | t.Generator[tuple[bytes | None, bytes | None]]
    ),
    demux: bool = False,
) -> bytes | tuple[bytes, bytes]: ...


def consume_socket_output(
    frames: (
        Sequence[bytes]
        | Sequence[tuple[bytes | None, bytes | None]]
        | t.Generator[bytes]
        | t.Generator[tuple[bytes | None, bytes | None]]
    ),
    demux: bool = False,
) -> bytes | tuple[bytes, bytes]:
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
        return b"".join(frames)  # type: ignore

    # If the streams are demultiplexed, the generator yields tuples
    # (stdout, stderr)
    out: list[bytes | None] = [None, None]
    frame: tuple[bytes | None, bytes | None]
    for frame in frames:  # type: ignore
        # It is guaranteed that for each frame, one and only one stream
        # is not None.
        if frame == (None, None):
            raise AssertionError(f"frame must be (None, None), but got {frame}")
        if frame[0] is not None:
            if out[0] is None:
                out[0] = frame[0]
            else:
                out[0] += frame[0]
        else:
            if out[1] is None:
                out[1] = frame[1]
            else:
                out[1] += frame[1]  # type: ignore[operator]
    return tuple(out)  # type: ignore


def demux_adaptor(stream_id: int, data: bytes) -> tuple[bytes | None, bytes | None]:
    """
    Utility to demultiplex stdout and stderr when reading frames from the
    socket.
    """
    if stream_id == STDOUT:
        return (data, None)
    if stream_id == STDERR:
        return (None, data)
    raise ValueError(f"{stream_id} is not a valid stream")
