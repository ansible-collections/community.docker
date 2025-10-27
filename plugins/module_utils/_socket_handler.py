# Copyright (c) 2019-2021, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Note that this module util is **PRIVATE** to the collection. It can have breaking changes at any time.
# Do not use this from other collections or standalone plugins/modules!

from __future__ import annotations

import os
import os.path
import selectors
import socket as pysocket
import struct
import typing as t

from ansible_collections.community.docker.plugins.module_utils._api.utils import (
    socket as docker_socket,
)
from ansible_collections.community.docker.plugins.module_utils._socket_helper import (
    make_unblocking,
    shutdown_writing,
    write_to_socket,
)


if t.TYPE_CHECKING:
    from collections.abc import Callable
    from types import TracebackType

    from ansible.module_utils.basic import AnsibleModule

    from ansible_collections.community.docker.plugins.module_utils._socket_helper import (
        SocketLike,
    )


PARAMIKO_POLL_TIMEOUT = 0.01  # 10 milliseconds


def _empty_writer(msg: str) -> None:
    pass


class DockerSocketHandlerBase:
    def __init__(
        self, sock: SocketLike, log: Callable[[str], None] | None = None
    ) -> None:
        make_unblocking(sock)

        self._log = log or _empty_writer
        self._paramiko_read_workaround = hasattr(
            sock, "send_ready"
        ) and "paramiko" in str(type(sock))

        self._sock = sock
        self._block_done_callback: Callable[[int, bytes], None] | None = None
        self._block_buffer: list[tuple[int, bytes]] = []
        self._eof = False
        self._read_buffer = b""
        self._write_buffer = b""
        self._end_of_writing = False

        self._current_stream: int | None = None
        self._current_missing = 0
        self._current_buffer = b""

        self._selector = selectors.DefaultSelector()
        self._selector.register(self._sock, selectors.EVENT_READ)

    def __enter__(self) -> t.Self:
        return self

    def __exit__(
        self,
        type_: type[BaseException] | None,
        value: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self._selector.close()

    def set_block_done_callback(
        self, block_done_callback: Callable[[int, bytes], None]
    ) -> None:
        self._block_done_callback = block_done_callback
        if self._block_done_callback is not None:
            while self._block_buffer:
                elt = self._block_buffer.pop(0)
                self._block_done_callback(*elt)

    def _add_block(self, stream_id: int, data: bytes) -> None:
        if self._block_done_callback is not None:
            self._block_done_callback(stream_id, data)
        else:
            self._block_buffer.append((stream_id, data))

    def _read(self) -> None:
        if self._eof:
            return
        data: bytes | None
        if hasattr(self._sock, "recv"):
            try:
                data = self._sock.recv(262144)
            except Exception as e:  # pylint: disable=broad-exception-caught
                # After calling self._sock.shutdown(), OpenSSL's/urllib3's
                # WrappedSocket seems to eventually raise ZeroReturnError in
                # case of EOF
                if "OpenSSL.SSL.ZeroReturnError" in str(type(e)):
                    self._eof = True
                    return
                raise
        elif isinstance(self._sock, pysocket.SocketIO):  # type: ignore[unreachable]
            data = self._sock.read()  # type: ignore
        else:
            data = os.read(self._sock.fileno())  # type: ignore  # TODO does this really work?!
        if data is None:
            # no data available
            return  # type: ignore[unreachable]
        self._log(f"read {len(data)} bytes")
        if len(data) == 0:
            # Stream EOF
            self._eof = True
            return
        self._read_buffer += data
        while len(self._read_buffer) > 0:
            if self._current_missing > 0:
                n = min(len(self._read_buffer), self._current_missing)
                self._current_buffer += self._read_buffer[:n]
                self._read_buffer = self._read_buffer[n:]
                self._current_missing -= n
                if self._current_missing == 0:
                    assert self._current_stream is not None
                    self._add_block(self._current_stream, self._current_buffer)
                    self._current_buffer = b""
            if len(self._read_buffer) < 8:
                break
            self._current_stream, self._current_missing = struct.unpack(
                ">BxxxL", self._read_buffer[:8]
            )
            self._read_buffer = self._read_buffer[8:]
            if self._current_missing < 0:
                # Stream EOF (as reported by docker daemon)
                self._eof = True
                break

    def _handle_end_of_writing(self) -> None:
        if self._end_of_writing and len(self._write_buffer) == 0:
            self._end_of_writing = False
            self._log("Shutting socket down for writing")
            shutdown_writing(self._sock, self._log)

    def _write(self) -> None:
        if len(self._write_buffer) > 0:
            written = write_to_socket(self._sock, self._write_buffer)
            self._write_buffer = self._write_buffer[written:]
            self._log(f"wrote {written} bytes, {len(self._write_buffer)} are left")
            if len(self._write_buffer) > 0:
                self._selector.modify(
                    self._sock, selectors.EVENT_READ | selectors.EVENT_WRITE
                )
            else:
                self._selector.modify(self._sock, selectors.EVENT_READ)
            self._handle_end_of_writing()

    def select(
        self, timeout: int | float | None = None, _internal_recursion: bool = False
    ) -> bool:
        if (
            not _internal_recursion
            and self._paramiko_read_workaround
            and len(self._write_buffer) > 0
        ):
            # When the SSH transport is used, Docker SDK for Python internally uses Paramiko, whose
            # Channel object supports select(), but only for reading
            # (https://github.com/paramiko/paramiko/issues/695).
            if self._sock.send_ready():  # type: ignore
                self._write()
                return True
            while timeout is None or timeout > PARAMIKO_POLL_TIMEOUT:
                result = int(
                    self.select(PARAMIKO_POLL_TIMEOUT, _internal_recursion=True)
                )
                if self._sock.send_ready():  # type: ignore
                    self._read()
                    result += 1
                if result > 0:
                    return True
                if timeout is not None:
                    timeout -= PARAMIKO_POLL_TIMEOUT
        self._log(f"select... ({timeout})")
        events = self._selector.select(timeout)
        for key, event in events:
            if key.fileobj == self._sock:
                ev_read = event & selectors.EVENT_READ != 0
                ev_write = event & selectors.EVENT_WRITE != 0
                self._log(f"select event read:{ev_read} write:{ev_write}")
                if event & selectors.EVENT_READ != 0:
                    self._read()
                if event & selectors.EVENT_WRITE != 0:
                    self._write()
        result = len(events)
        if self._paramiko_read_workaround and len(self._write_buffer) > 0 and self._sock.send_ready():  # type: ignore
            self._write()
            result += 1
        return result > 0

    def is_eof(self) -> bool:
        return self._eof

    def end_of_writing(self) -> None:
        self._end_of_writing = True
        self._handle_end_of_writing()

    def consume(self) -> tuple[bytes, bytes]:
        stdout = []
        stderr = []

        def append_block(stream_id: int, data: bytes) -> None:
            if stream_id == docker_socket.STDOUT:
                stdout.append(data)
            elif stream_id == docker_socket.STDERR:
                stderr.append(data)
            else:
                raise ValueError(f"{stream_id} is not a valid stream ID")

        self.end_of_writing()

        self.set_block_done_callback(append_block)
        while not self._eof:
            self.select()
        return b"".join(stdout), b"".join(stderr)

    def write(self, str_to_write: bytes) -> None:
        self._write_buffer += str_to_write
        if len(self._write_buffer) == len(str_to_write):
            self._write()


class DockerSocketHandlerModule(DockerSocketHandlerBase):
    def __init__(self, sock: SocketLike, module: AnsibleModule) -> None:
        super().__init__(sock, module.debug)
