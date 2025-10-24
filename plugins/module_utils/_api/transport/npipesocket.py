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

import functools
import io
import time
import traceback
import typing as t


PYWIN32_IMPORT_ERROR: str | None  # pylint: disable=invalid-name
try:
    import pywintypes
    import win32api
    import win32event
    import win32file
    import win32pipe
except ImportError:
    PYWIN32_IMPORT_ERROR = traceback.format_exc()  # pylint: disable=invalid-name
else:
    PYWIN32_IMPORT_ERROR = None  # pylint: disable=invalid-name

if t.TYPE_CHECKING:
    from collections.abc import Buffer, Callable

    _Self = t.TypeVar("_Self")
    _P = t.ParamSpec("_P")
    _R = t.TypeVar("_R")


ERROR_PIPE_BUSY = 0xE7
SECURITY_SQOS_PRESENT = 0x100000
SECURITY_ANONYMOUS = 0

MAXIMUM_RETRY_COUNT = 10


def check_closed(
    f: Callable[t.Concatenate[_Self, _P], _R],
) -> Callable[t.Concatenate[_Self, _P], _R]:
    @functools.wraps(f)
    def wrapped(self: _Self, *args: _P.args, **kwargs: _P.kwargs) -> _R:
        if self._closed:  # type: ignore
            raise RuntimeError("Can not reuse socket after connection was closed.")
        return f(self, *args, **kwargs)

    return wrapped


class NpipeSocket:
    """Partial implementation of the socket API over windows named pipes.
    This implementation is only designed to be used as a client socket,
    and server-specific methods (bind, listen, accept...) are not
    implemented.
    """

    def __init__(self, handle: t.Any | None = None) -> None:
        self._timeout = win32pipe.NMPWAIT_USE_DEFAULT_WAIT
        self._handle = handle
        self._address: str | None = None
        self._closed = False
        self.flags: int | None = None

    def accept(self) -> t.NoReturn:
        raise NotImplementedError()

    def bind(self, address: t.Any) -> t.NoReturn:
        raise NotImplementedError()

    def close(self) -> None:
        if self._handle is None:
            raise ValueError("Handle not present")
        self._handle.Close()
        self._closed = True

    @check_closed
    def connect(self, address: str, retry_count: int = 0) -> None:
        try:
            handle = win32file.CreateFile(
                address,
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                (
                    SECURITY_ANONYMOUS
                    | SECURITY_SQOS_PRESENT
                    | win32file.FILE_FLAG_OVERLAPPED
                ),
                0,
            )
        except win32pipe.error as e:
            # See Remarks:
            # https://msdn.microsoft.com/en-us/library/aa365800.aspx
            if e.winerror == ERROR_PIPE_BUSY:
                # Another program or thread has grabbed our pipe instance
                # before we got to it. Wait for availability and attempt to
                # connect again.
                retry_count = retry_count + 1
                if retry_count < MAXIMUM_RETRY_COUNT:
                    time.sleep(1)
                    return self.connect(address, retry_count)
            raise e

        self.flags = win32pipe.GetNamedPipeInfo(handle)[0]  # type: ignore

        self._handle = handle
        self._address = address

    @check_closed
    def connect_ex(self, address: str) -> None:
        self.connect(address)

    @check_closed
    def detach(self) -> t.Any:
        self._closed = True
        return self._handle

    @check_closed
    def dup(self) -> NpipeSocket:
        return NpipeSocket(self._handle)

    def getpeername(self) -> str | None:
        return self._address

    def getsockname(self) -> str | None:
        return self._address

    def getsockopt(
        self, level: t.Any, optname: t.Any, buflen: t.Any = None
    ) -> t.NoReturn:
        raise NotImplementedError()

    def ioctl(self, control: t.Any, option: t.Any) -> t.NoReturn:
        raise NotImplementedError()

    def listen(self, backlog: t.Any) -> t.NoReturn:
        raise NotImplementedError()

    def makefile(self, mode: str, bufsize: int | None = None) -> t.IO[bytes]:
        if mode.strip("b") != "r":
            raise NotImplementedError()
        rawio = NpipeFileIOBase(self)
        if bufsize is None or bufsize <= 0:
            bufsize = io.DEFAULT_BUFFER_SIZE
        return io.BufferedReader(rawio, buffer_size=bufsize)

    @check_closed
    def recv(self, bufsize: int, flags: int = 0) -> str:
        if self._handle is None:
            raise ValueError("Handle not present")
        dummy_err, data = win32file.ReadFile(self._handle, bufsize)
        return data

    @check_closed
    def recvfrom(self, bufsize: int, flags: int = 0) -> tuple[str, str | None]:
        data = self.recv(bufsize, flags)
        return (data, self._address)

    @check_closed
    def recvfrom_into(
        self, buf: Buffer, nbytes: int = 0, flags: int = 0
    ) -> tuple[int, str | None]:
        return self.recv_into(buf, nbytes), self._address

    @check_closed
    def recv_into(self, buf: Buffer, nbytes: int = 0) -> int:
        if self._handle is None:
            raise ValueError("Handle not present")
        readbuf = buf if isinstance(buf, memoryview) else memoryview(buf)

        event = win32event.CreateEvent(None, True, True, None)
        try:
            overlapped = pywintypes.OVERLAPPED()
            overlapped.hEvent = event
            dummy_err, dummy_data = win32file.ReadFile(  # type: ignore
                self._handle, readbuf[:nbytes] if nbytes else readbuf, overlapped
            )
            wait_result = win32event.WaitForSingleObject(event, self._timeout)
            if wait_result == win32event.WAIT_TIMEOUT:
                win32file.CancelIo(self._handle)
                raise TimeoutError
            return win32file.GetOverlappedResult(self._handle, overlapped, 0)
        finally:
            win32api.CloseHandle(event)

    @check_closed
    def send(self, string: Buffer, flags: int = 0) -> int:
        if self._handle is None:
            raise ValueError("Handle not present")
        event = win32event.CreateEvent(None, True, True, None)
        try:
            overlapped = pywintypes.OVERLAPPED()
            overlapped.hEvent = event
            win32file.WriteFile(self._handle, string, overlapped)  # type: ignore
            wait_result = win32event.WaitForSingleObject(event, self._timeout)
            if wait_result == win32event.WAIT_TIMEOUT:
                win32file.CancelIo(self._handle)
                raise TimeoutError
            return win32file.GetOverlappedResult(self._handle, overlapped, 0)
        finally:
            win32api.CloseHandle(event)

    @check_closed
    def sendall(self, string: Buffer, flags: int = 0) -> int:
        return self.send(string, flags)

    @check_closed
    def sendto(self, string: Buffer, address: str) -> int:
        self.connect(address)
        return self.send(string)

    def setblocking(self, flag: bool) -> None:
        if flag:
            return self.settimeout(None)
        return self.settimeout(0)

    def settimeout(self, value: int | float | None) -> None:
        if value is None:
            # Blocking mode
            self._timeout = win32event.INFINITE
        elif not isinstance(value, (float, int)) or value < 0:
            raise ValueError("Timeout value out of range")
        else:
            # Timeout mode - Value converted to milliseconds
            self._timeout = int(value * 1000)

    def gettimeout(self) -> int | float | None:
        return self._timeout

    def setsockopt(self, level: t.Any, optname: t.Any, value: t.Any) -> t.NoReturn:
        raise NotImplementedError()

    @check_closed
    def shutdown(self, how: t.Any) -> None:
        return self.close()


class NpipeFileIOBase(io.RawIOBase):
    def __init__(self, npipe_socket: NpipeSocket | None) -> None:
        self.sock = npipe_socket

    def close(self) -> None:
        super().close()
        self.sock = None

    def fileno(self) -> int:
        if self.sock is None:
            raise RuntimeError("socket is closed")
        # TODO: This is definitely a bug, NpipeSocket.fileno() does not exist!
        return self.sock.fileno()  # type: ignore

    def isatty(self) -> bool:
        return False

    def readable(self) -> bool:
        return True

    def readinto(self, buf: Buffer) -> int:
        if self.sock is None:
            raise RuntimeError("socket is closed")
        return self.sock.recv_into(buf)

    def seekable(self) -> bool:
        return False

    def writable(self) -> bool:
        return False
