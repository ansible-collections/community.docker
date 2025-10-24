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

import typing as t
from queue import Empty

from .. import constants
from .._import_helper import HTTPAdapter, urllib3, urllib3_connection
from .basehttpadapter import BaseHTTPAdapter
from .npipesocket import NpipeSocket


if t.TYPE_CHECKING:
    from collections.abc import Mapping

    from requests import PreparedRequest


RecentlyUsedContainer = urllib3._collections.RecentlyUsedContainer


class NpipeHTTPConnection(urllib3_connection.HTTPConnection):
    def __init__(self, npipe_path: str, timeout: int | float = 60) -> None:
        super().__init__("localhost", timeout=timeout)
        self.npipe_path = npipe_path
        self.timeout = timeout

    def connect(self) -> None:
        sock = NpipeSocket()
        sock.settimeout(self.timeout)
        sock.connect(self.npipe_path)
        self.sock = sock


class NpipeHTTPConnectionPool(urllib3.connectionpool.HTTPConnectionPool):
    def __init__(
        self, npipe_path: str, timeout: int | float = 60, maxsize: int = 10
    ) -> None:
        super().__init__("localhost", timeout=timeout, maxsize=maxsize)
        self.npipe_path = npipe_path
        self.timeout = timeout

    def _new_conn(self) -> NpipeHTTPConnection:
        return NpipeHTTPConnection(self.npipe_path, self.timeout)

    # When re-using connections, urllib3 tries to call select() on our
    # NpipeSocket instance, causing a crash. To circumvent this, we override
    # _get_conn, where that check happens.
    def _get_conn(self, timeout: int | float) -> NpipeHTTPConnection:
        conn = None
        try:
            conn = self.pool.get(block=self.block, timeout=timeout)

        except AttributeError as exc:  # self.pool is None
            raise urllib3.exceptions.ClosedPoolError(self, "Pool is closed.") from exc

        except Empty as exc:
            if self.block:
                raise urllib3.exceptions.EmptyPoolError(
                    self,
                    "Pool reached maximum size and no more connections are allowed.",
                ) from exc
            # Oh well, we'll create a new connection then

        return conn or self._new_conn()


class NpipeHTTPAdapter(BaseHTTPAdapter):
    __attrs__ = HTTPAdapter.__attrs__ + [
        "npipe_path",
        "pools",
        "timeout",
        "max_pool_size",
    ]

    def __init__(
        self,
        base_url: str,
        timeout: int | float = 60,
        pool_connections: int = constants.DEFAULT_NUM_POOLS,
        max_pool_size: int = constants.DEFAULT_MAX_POOL_SIZE,
    ) -> None:
        self.npipe_path = base_url.replace("npipe://", "")
        self.timeout = timeout
        self.max_pool_size = max_pool_size
        self.pools = RecentlyUsedContainer(
            pool_connections, dispose_func=lambda p: p.close()
        )
        super().__init__()

    def get_connection(
        self, url: str | bytes, proxies: Mapping[str, str] | None = None
    ) -> NpipeHTTPConnectionPool:
        with self.pools.lock:
            pool = self.pools.get(url)
            if pool:
                return pool

            pool = NpipeHTTPConnectionPool(
                self.npipe_path, self.timeout, maxsize=self.max_pool_size
            )
            self.pools[url] = pool

        return pool

    def request_url(
        self, request: PreparedRequest, proxies: Mapping[str, str] | None
    ) -> str:
        # The select_proxy utility in requests errors out when the provided URL
        # does not have a hostname, like is the case when using a UNIX socket.
        # Since proxies are an irrelevant notion in the case of UNIX sockets
        # anyway, we simply return the path URL directly.
        # See also: https://github.com/docker/docker-sdk-python/issues/811
        return request.path_url
