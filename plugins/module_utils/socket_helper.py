# Copyright (c) 2019-2021, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import fcntl
import os
import os.path
import socket as pysocket

from ansible.module_utils.six import PY3


def make_unblocking(sock):
    if hasattr(sock, '_sock'):
        sock._sock.setblocking(0)
    elif hasattr(sock, 'setblocking'):
        sock.setblocking(0)
    else:
        fcntl.fcntl(sock.fileno(), fcntl.F_SETFL, fcntl.fcntl(sock.fileno(), fcntl.F_GETFL) | os.O_NONBLOCK)


def _empty_writer(msg):
    pass


def shutdown_writing(sock, log=_empty_writer):
    if hasattr(sock, 'shutdown_write'):
        sock.shutdown_write()
    elif hasattr(sock, 'shutdown'):
        try:
            sock.shutdown(pysocket.SHUT_WR)
        except TypeError as e:
            # probably: "TypeError: shutdown() takes 1 positional argument but 2 were given"
            log('Shutting down for writing not possible; trying shutdown instead: {0}'.format(e))
            sock.shutdown()
    elif PY3 and isinstance(sock, getattr(pysocket, 'SocketIO')):
        sock._sock.shutdown(pysocket.SHUT_WR)
    else:
        log('No idea how to signal end of writing')


def write_to_socket(sock, data):
    if hasattr(sock, '_send_until_done'):
        # WrappedSocket (urllib3/contrib/pyopenssl) doesn't have `send`, but
        # only `sendall`, which uses `_send_until_done` under the hood.
        return sock._send_until_done(data)
    elif hasattr(sock, 'send'):
        return sock.send(data)
    else:
        return os.write(sock.fileno(), data)
