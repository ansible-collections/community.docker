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

from .._import_helper import HTTPAdapter, urllib3
from .basehttpadapter import BaseHTTPAdapter


# Resolves OpenSSL issues in some servers:
#   https://lukasa.co.uk/2013/01/Choosing_SSL_Version_In_Requests/
#   https://github.com/kennethreitz/requests/pull/799


PoolManager = urllib3.poolmanager.PoolManager


class SSLHTTPAdapter(BaseHTTPAdapter):
    """An HTTPS Transport Adapter that uses an arbitrary SSL version."""

    __attrs__ = HTTPAdapter.__attrs__ + ["assert_hostname"]

    def __init__(
        self,
        assert_hostname: bool | None = None,
        **kwargs: t.Any,
    ) -> None:
        self.assert_hostname = assert_hostname
        super().__init__(**kwargs)

    def init_poolmanager(
        self, connections: int, maxsize: int, block: bool = False, **kwargs: t.Any
    ) -> None:
        kwargs = {
            "num_pools": connections,
            "maxsize": maxsize,
            "block": block,
        }
        if self.assert_hostname is not None:
            kwargs["assert_hostname"] = self.assert_hostname

        self.poolmanager = PoolManager(**kwargs)

    def get_connection(self, *args: t.Any, **kwargs: t.Any) -> urllib3.ConnectionPool:
        """
        Ensure assert_hostname is set correctly on our pool

        We already take care of a normal poolmanager via init_poolmanager

        But we still need to take care of when there is a proxy poolmanager

        Note that this method is no longer called for newer requests versions.
        """
        # pylint finds our HTTPAdapter stub instead of requests.adapters.HTTPAdapter:
        # pylint: disable-next=no-member
        conn = super().get_connection(*args, **kwargs)
        if (
            self.assert_hostname is not None
            and conn.assert_hostname != self.assert_hostname  # type: ignore
        ):
            conn.assert_hostname = self.assert_hostname  # type: ignore
        return conn
