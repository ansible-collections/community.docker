# Copyright (c) 2019-2020, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import fcntl
import os
import os.path
import socket as pysocket

from ansible.compat import selectors
from ansible.module_utils.six import PY3

try:
    from docker.utils import socket as docker_socket
    import struct
except Exception:
    # missing Docker SDK for Python handled in ansible_collections.community.docker.plugins.module_utils.common
    pass


PARAMIKO_POLL_TIMEOUT = 0.01  # 10 milliseconds


class DockerSocketHandler:
    def __init__(self, display, sock, container=None):
        if hasattr(sock, '_sock'):
            sock._sock.setblocking(0)
        elif hasattr(sock, 'setblocking'):
            sock.setblocking(0)
        else:
            fcntl.fcntl(sock.fileno(), fcntl.F_SETFL, fcntl.fcntl(sock.fileno(), fcntl.F_GETFL) | os.O_NONBLOCK)

        self._display = display
        self._paramiko_read_workaround = hasattr(sock, 'send_ready') and 'paramiko' in str(type(sock))

        self._container = container

        self._sock = sock
        self._block_done_callback = None
        self._block_buffer = []
        self._eof = False
        self._read_buffer = b''
        self._write_buffer = b''
        self._end_of_writing = False

        self._current_stream = None
        self._current_missing = 0
        self._current_buffer = b''

        self._selector = selectors.DefaultSelector()
        self._selector.register(self._sock, selectors.EVENT_READ)

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self._selector.close()

    def set_block_done_callback(self, block_done_callback):
        self._block_done_callback = block_done_callback
        if self._block_done_callback is not None:
            while self._block_buffer:
                elt = self._block_buffer.remove(0)
                self._block_done_callback(*elt)

    def _add_block(self, stream_id, data):
        if self._block_done_callback is not None:
            self._block_done_callback(stream_id, data)
        else:
            self._block_buffer.append((stream_id, data))

    def _read(self):
        if self._eof:
            return
        if hasattr(self._sock, 'recv'):
            try:
                data = self._sock.recv(262144)
            except Exception as e:
                # After calling self._sock.shutdown(), OpenSSL's/urllib3's
                # WrappedSocket seems to eventually raise ZeroReturnError in
                # case of EOF
                if 'OpenSSL.SSL.ZeroReturnError' in str(type(e)):
                    self._eof = True
                    return
                else:
                    raise
        elif PY3 and isinstance(self._sock, getattr(pysocket, 'SocketIO')):
            data = self._sock.read()
        else:
            data = os.read(self._sock.fileno())
        if data is None:
            # no data available
            return
        self._display.vvvv('read {0} bytes'.format(len(data)), host=self._container)
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
                    self._add_block(self._current_stream, self._current_buffer)
                    self._current_buffer = b''
            if len(self._read_buffer) < 8:
                break
            self._current_stream, self._current_missing = struct.unpack('>BxxxL', self._read_buffer[:8])
            self._read_buffer = self._read_buffer[8:]
            if self._current_missing < 0:
                # Stream EOF (as reported by docker daemon)
                self._eof = True
                break

    def _handle_end_of_writing(self):
        if self._end_of_writing and len(self._write_buffer) == 0:
            self._end_of_writing = False
            self._display.vvvv('Shutting socket down for writing', host=self._container)
            if hasattr(self._sock, 'shutdown_write'):
                self._sock.shutdown_write()
            elif hasattr(self._sock, 'shutdown'):
                try:
                    self._sock.shutdown(pysocket.SHUT_WR)
                except TypeError as e:
                    # probably: "TypeError: shutdown() takes 1 positional argument but 2 were given"
                    self._display.vvvv('Shutting down for writing not possible; trying shutdown instead: {0}'.format(e), host=self._container)
                    self._sock.shutdown()
            elif PY3 and isinstance(self._sock, getattr(pysocket, 'SocketIO')):
                self._sock._sock.shutdown(pysocket.SHUT_WR)
            else:
                self._display.vvvv('No idea how to signal end of writing', host=self._container)

    def _write(self):
        if len(self._write_buffer) > 0:
            if hasattr(self._sock, '_send_until_done'):
                # WrappedSocket (urllib3/contrib/pyopenssl) doesn't have `send`, but
                # only `sendall`, which uses `_send_until_done` under the hood.
                written = self._sock._send_until_done(self._write_buffer)
            elif hasattr(self._sock, 'send'):
                written = self._sock.send(self._write_buffer)
            else:
                written = os.write(self._sock.fileno(), self._write_buffer)
            self._write_buffer = self._write_buffer[written:]
            self._display.vvvv('wrote {0} bytes, {1} are left'.format(written, len(self._write_buffer)), host=self._container)
            if len(self._write_buffer) > 0:
                self._selector.modify(self._sock, selectors.EVENT_READ | selectors.EVENT_WRITE)
            else:
                self._selector.modify(self._sock, selectors.EVENT_READ)
            self._handle_end_of_writing()

    def select(self, timeout=None, _internal_recursion=False):
        if not _internal_recursion and self._paramiko_read_workaround and len(self._write_buffer) > 0:
            # When the SSH transport is used, docker-py internally uses Paramiko, whose
            # Channel object supports select(), but only for reading
            # (https://github.com/paramiko/paramiko/issues/695).
            if self._sock.send_ready():
                self._write()
                return True
            while timeout is None or timeout > PARAMIKO_POLL_TIMEOUT:
                result = self.select(PARAMIKO_POLL_TIMEOUT, _internal_recursion=True)
                if self._sock.send_ready():
                    self._read()
                    result += 1
                if result > 0:
                    return True
                if timeout is not None:
                    timeout -= PARAMIKO_POLL_TIMEOUT
        self._display.vvvv('select... ({0})'.format(timeout), host=self._container)
        events = self._selector.select(timeout)
        for key, event in events:
            if key.fileobj == self._sock:
                self._display.vvvv(
                    'select event read:{0} write:{1}'.format(event & selectors.EVENT_READ != 0, event & selectors.EVENT_WRITE != 0),
                    host=self._container)
                if event & selectors.EVENT_READ != 0:
                    self._read()
                if event & selectors.EVENT_WRITE != 0:
                    self._write()
        result = len(events)
        if self._paramiko_read_workaround and len(self._write_buffer) > 0:
            if self._sock.send_ready():
                self._write()
                result += 1
        return result > 0

    def is_eof(self):
        return self._eof

    def end_of_writing(self):
        self._end_of_writing = True
        self._handle_end_of_writing()

    def consume(self):
        stdout = []
        stderr = []

        def append_block(stream_id, data):
            if stream_id == docker_socket.STDOUT:
                stdout.append(data)
            elif stream_id == docker_socket.STDERR:
                stderr.append(data)
            else:
                raise ValueError('{0} is not a valid stream ID'.format(stream_id))

        self.end_of_writing()

        self.set_block_done_callback(append_block)
        while not self._eof:
            self.select()
        return b''.join(stdout), b''.join(stderr)

    def write(self, str):
        self._write_buffer += str
        if len(self._write_buffer) == len(str):
            self._write()
