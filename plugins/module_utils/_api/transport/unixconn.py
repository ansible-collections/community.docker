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

import socket
import typing as t

from .. import constants
from .._import_helper import HTTPAdapter, urllib3, urllib3_connection
from .basehttpadapter import BaseHTTPAdapter


if t.TYPE_CHECKING:
    from collections.abc import Mapping

    from requests import PreparedRequest

    from ..._socket_helper import SocketLike


RecentlyUsedContainer = urllib3._collections.RecentlyUsedContainer


class UnixHTTPConnection(urllib3_connection.HTTPConnection):
    def __init__(
        self, base_url: str | bytes, unix_socket: str, timeout: int | float = 60
    ) -> None:
        super().__init__("localhost", timeout=timeout)
        self.base_url = base_url
        self.unix_socket = unix_socket
        self.timeout = timeout
        self.disable_buffering = False

    def connect(self) -> None:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        sock.connect(self.unix_socket)
        self.sock = sock

    def putheader(self, header: str, *values: str) -> None:
        super().putheader(header, *values)
        if header == "Connection" and "Upgrade" in values:
            self.disable_buffering = True

    def response_class(self, sock: SocketLike, *args: t.Any, **kwargs: t.Any) -> t.Any:
        # FIXME: We may need to disable buffering on Py3,
        # but there's no clear way to do it at the moment. See:
        # https://github.com/docker/docker-py/issues/1799
        return super().response_class(sock, *args, **kwargs)


class UnixHTTPConnectionPool(urllib3.connectionpool.HTTPConnectionPool):
    def __init__(
        self,
        base_url: str | bytes,
        socket_path: str,
        timeout: int | float = 60,
        maxsize: int = 10,
    ) -> None:
        super().__init__("localhost", timeout=timeout, maxsize=maxsize)
        self.base_url = base_url
        self.socket_path = socket_path
        self.timeout = timeout

    def _new_conn(self) -> UnixHTTPConnection:
        return UnixHTTPConnection(self.base_url, self.socket_path, self.timeout)


class UnixHTTPAdapter(BaseHTTPAdapter):
    __attrs__ = HTTPAdapter.__attrs__ + [
        "pools",
        "socket_path",
        "timeout",
        "max_pool_size",
    ]

    def __init__(
        self,
        socket_url: str,
        timeout: int | float = 60,
        pool_connections: int = constants.DEFAULT_NUM_POOLS,
        max_pool_size: int = constants.DEFAULT_MAX_POOL_SIZE,
    ) -> None:
        socket_path = socket_url.replace("http+unix://", "")
        if not socket_path.startswith("/"):
            socket_path = "/" + socket_path
        self.socket_path = socket_path
        self.timeout = timeout
        self.max_pool_size = max_pool_size

        def f(p: t.Any) -> None:
            p.close()

        self.pools = RecentlyUsedContainer(pool_connections, dispose_func=f)
        super().__init__()

    def get_connection(
        self, url: str | bytes, proxies: Mapping[str, str] | None = None
    ) -> UnixHTTPConnectionPool:
        with self.pools.lock:
            pool = self.pools.get(url)
            if pool:
                return pool

            pool = UnixHTTPConnectionPool(
                url, self.socket_path, self.timeout, maxsize=self.max_pool_size
            )
            self.pools[url] = pool

        return pool

    def request_url(self, request: PreparedRequest, proxies: Mapping[str, str]) -> str:
        # The select_proxy utility in requests errors out when the provided URL
        # does not have a hostname, like is the case when using a UNIX socket.
        # Since proxies are an irrelevant notion in the case of UNIX sockets
        # anyway, we simply return the path URL directly.
        # See also: https://github.com/docker/docker-py/issues/811
        return request.path_url
