# Copyright (c) 2019-2021, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Note that this module util is **PRIVATE** to the collection. It can have breaking changes at any time.
# Do not use this from other collections or standalone plugins/modules!

from __future__ import annotations

import fcntl
import os
import os.path
import socket as pysocket
import typing as t
from collections.abc import Callable


if t.TYPE_CHECKING:
    SocketLike = pysocket.socket


def make_file_unblocking(file: SocketLike) -> None:
    fcntl.fcntl(
        file.fileno(),
        fcntl.F_SETFL,
        fcntl.fcntl(file.fileno(), fcntl.F_GETFL) | os.O_NONBLOCK,
    )


def make_file_blocking(file: SocketLike) -> None:
    fcntl.fcntl(
        file.fileno(),
        fcntl.F_SETFL,
        fcntl.fcntl(file.fileno(), fcntl.F_GETFL) & ~os.O_NONBLOCK,
    )


def make_unblocking(sock: SocketLike) -> None:
    if hasattr(sock, "_sock"):
        sock._sock.setblocking(0)
    elif hasattr(sock, "setblocking"):
        sock.setblocking(0)  # type: ignore  # TODO: CHECK!
    else:
        make_file_unblocking(sock)


def _empty_writer(msg: str) -> None:
    pass


def shutdown_writing(
    sock: SocketLike, log: Callable[[str], None] = _empty_writer
) -> None:
    # FIXME: This does **not work with SSLSocket**! Apparently SSLSocket does not allow to send
    #        a close_notify TLS alert without completely shutting down the connection.
    #        Calling sock.shutdown(pysocket.SHUT_WR) simply turns of TLS encryption and from that
    #        point on the raw encrypted data is returned when sock.recv() is called. :-(
    if hasattr(sock, "shutdown_write"):
        sock.shutdown_write()
    elif hasattr(sock, "shutdown"):
        try:
            sock.shutdown(pysocket.SHUT_WR)
        except TypeError as e:
            # probably: "TypeError: shutdown() takes 1 positional argument but 2 were given"
            log(f"Shutting down for writing not possible; trying shutdown instead: {e}")
            sock.shutdown()  # type: ignore
    elif isinstance(sock, pysocket.SocketIO):  # type: ignore
        sock._sock.shutdown(pysocket.SHUT_WR)  # type: ignore[unreachable]
    else:
        log("No idea how to signal end of writing")


def write_to_socket(sock: SocketLike, data: bytes) -> int:
    if hasattr(sock, "_send_until_done"):
        # WrappedSocket (urllib3/contrib/pyopenssl) does not have `send`, but
        # only `sendall`, which uses `_send_until_done` under the hood.
        return sock._send_until_done(data)
    if hasattr(sock, "send"):
        return sock.send(data)
    return os.write(sock.fileno(), data)
