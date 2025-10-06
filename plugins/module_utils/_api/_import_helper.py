# -*- coding: utf-8 -*-
# This code is part of the Ansible collection community.docker, but is an independent component.
# This particular file, and this file only, is based on the Docker SDK for Python (https://github.com/docker/docker-py/)
#
# Copyright (c) 2016-2022 Docker, Inc.
#
# It is licensed under the Apache 2.0 license (see LICENSES/Apache-2.0.txt in this collection)
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import traceback


REQUESTS_IMPORT_ERROR = None
URLLIB3_IMPORT_ERROR = None


try:
    from requests import Session  # noqa: F401, pylint: disable=unused-import
    from requests.adapters import (  # noqa: F401, pylint: disable=unused-import
        HTTPAdapter,
    )
    from requests.exceptions import (  # noqa: F401, pylint: disable=unused-import
        HTTPError,
        InvalidSchema,
    )
except ImportError:
    REQUESTS_IMPORT_ERROR = traceback.format_exc()

    class Session(object):
        __attrs__ = []

    class HTTPAdapter(object):
        __attrs__ = []

    class HTTPError(Exception):
        pass

    class InvalidSchema(Exception):
        pass


try:
    from requests.packages import urllib3  # pylint: disable=unused-import

    # pylint: disable-next=unused-import
    from requests.packages.urllib3 import connection as urllib3_connection
except ImportError:
    try:
        import urllib3  # pylint: disable=unused-import
        from urllib3 import (
            connection as urllib3_connection,  # pylint: disable=unused-import
        )
    except ImportError:
        URLLIB3_IMPORT_ERROR = traceback.format_exc()

        class _HTTPConnectionPool(object):
            pass

        class _HTTPConnection(object):
            pass

        class FakeURLLIB3(object):
            def __init__(self):
                self._collections = self
                self.poolmanager = self
                self.connection = self
                self.connectionpool = self

                self.RecentlyUsedContainer = object()
                self.PoolManager = object()
                self.match_hostname = object()
                self.HTTPConnectionPool = _HTTPConnectionPool

        class FakeURLLIB3Connection(object):
            def __init__(self):
                self.HTTPConnection = _HTTPConnection

        urllib3 = FakeURLLIB3()
        urllib3_connection = FakeURLLIB3Connection()


def fail_on_missing_imports():
    if REQUESTS_IMPORT_ERROR is not None:
        from .errors import MissingRequirementException

        raise MissingRequirementException(
            "You have to install requests", "requests", REQUESTS_IMPORT_ERROR
        )
    if URLLIB3_IMPORT_ERROR is not None:
        from .errors import MissingRequirementException

        raise MissingRequirementException(
            "You have to install urllib3", "urllib3", URLLIB3_IMPORT_ERROR
        )
