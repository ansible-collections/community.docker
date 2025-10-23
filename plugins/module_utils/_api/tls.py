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

import os
import typing as t

from . import errors
from .transport.ssladapter import SSLHTTPAdapter


if t.TYPE_CHECKING:
    from ansible_collections.community.docker.plugins.module_utils._api.api.client import (
        APIClient,
    )


class TLSConfig:
    """
    TLS configuration.

    Args:
        client_cert (tuple of str): Path to client cert, path to client key.
        ca_cert (str): Path to CA cert file.
        verify (bool or str): This can be ``False`` or a path to a CA cert
            file.
        assert_hostname (bool): Verify the hostname of the server.

    .. _`SSL version`:
        https://docs.python.org/3.5/library/ssl.html#ssl.PROTOCOL_TLSv1
    """

    cert: tuple[str, str] | None = None
    ca_cert: str | None = None
    verify: bool | None = None

    def __init__(
        self,
        client_cert: tuple[str, str] | None = None,
        ca_cert: str | None = None,
        verify: bool | None = None,
        assert_hostname: bool | None = None,
    ):
        # Argument compatibility/mapping with
        # https://docs.docker.com/engine/articles/https/
        # This diverges from the Docker CLI in that users can specify 'tls'
        # here, but also disable any public/default CA pool verification by
        # leaving verify=False

        self.assert_hostname = assert_hostname

        # "client_cert" must have both or neither cert/key files. In
        # either case, Alert the user when both are expected, but any are
        # missing.

        if client_cert:
            try:
                tls_cert, tls_key = client_cert
            except ValueError:
                raise errors.TLSParameterError(
                    "client_cert must be a tuple of (client certificate, key file)"
                ) from None

            if not (tls_cert and tls_key) or (
                not os.path.isfile(tls_cert) or not os.path.isfile(tls_key)
            ):
                raise errors.TLSParameterError(
                    "Path to a certificate and key files must be provided"
                    " through the client_cert param"
                )
            self.cert = (tls_cert, tls_key)

        # If verify is set, make sure the cert exists
        self.verify = verify
        self.ca_cert = ca_cert
        if self.verify and self.ca_cert and not os.path.isfile(self.ca_cert):
            raise errors.TLSParameterError(
                "Invalid CA certificate provided for `ca_cert`."
            )

    def configure_client(self, client: APIClient) -> None:
        """
        Configure a client with these TLS options.
        """

        if self.verify and self.ca_cert:
            client.verify = self.ca_cert
        else:
            client.verify = self.verify

        if self.cert:
            client.cert = self.cert

        client.mount(
            "https://",
            SSLHTTPAdapter(
                assert_hostname=self.assert_hostname,
            ),
        )
