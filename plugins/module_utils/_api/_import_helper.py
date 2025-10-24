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

import traceback
import typing as t


REQUESTS_IMPORT_ERROR: str | None  # pylint: disable=invalid-name
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
    REQUESTS_IMPORT_ERROR = traceback.format_exc()  # pylint: disable=invalid-name

    class Session:  # type: ignore
        __attrs__: list[t.Never] = []

    class HTTPAdapter:  # type: ignore
        __attrs__: list[t.Never] = []

    class HTTPError(Exception):  # type: ignore
        pass

    class InvalidSchema(Exception):  # type: ignore
        pass

else:
    REQUESTS_IMPORT_ERROR = None  # pylint: disable=invalid-name


URLLIB3_IMPORT_ERROR: str | None = None  # pylint: disable=invalid-name
try:
    from requests.packages import urllib3  # pylint: disable=unused-import

    from requests.packages.urllib3 import (  # type: ignore  # pylint: disable=unused-import  # isort: skip
        connection as urllib3_connection,
    )
except ImportError:
    try:
        import urllib3  # pylint: disable=unused-import
        from urllib3 import (
            connection as urllib3_connection,  # pylint: disable=unused-import
        )
    except ImportError:
        URLLIB3_IMPORT_ERROR = traceback.format_exc()  # pylint: disable=invalid-name

        class _HTTPConnectionPool:
            pass

        class _HTTPConnection:
            pass

        class FakeURLLIB3:
            def __init__(self) -> None:
                self._collections = self
                self.poolmanager = self
                self.connection = self
                self.connectionpool = self

                self.RecentlyUsedContainer = object()  # pylint: disable=invalid-name
                self.PoolManager = object()  # pylint: disable=invalid-name
                self.match_hostname = object()
                self.HTTPConnectionPool = (  # pylint: disable=invalid-name
                    _HTTPConnectionPool
                )

        class FakeURLLIB3Connection:
            def __init__(self) -> None:
                self.HTTPConnection = _HTTPConnection  # pylint: disable=invalid-name

        urllib3 = FakeURLLIB3()
        urllib3_connection = FakeURLLIB3Connection()


def fail_on_missing_imports() -> None:
    if REQUESTS_IMPORT_ERROR is not None:
        from .errors import MissingRequirementException  # pylint: disable=cyclic-import

        raise MissingRequirementException(
            "You have to install requests", "requests", REQUESTS_IMPORT_ERROR
        )
    if URLLIB3_IMPORT_ERROR is not None:
        from .errors import MissingRequirementException  # pylint: disable=cyclic-import

        raise MissingRequirementException(
            "You have to install urllib3", "urllib3", URLLIB3_IMPORT_ERROR
        )
