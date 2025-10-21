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
import typing as t

from .. import errors
from . import utils


if t.TYPE_CHECKING:
    from collections.abc import Callable

    from ..api.client import APIClient

    _Self = t.TypeVar("_Self")
    _P = t.ParamSpec("_P")
    _R = t.TypeVar("_R")


def minimum_version(
    version: str,
) -> Callable[
    [Callable[t.Concatenate[_Self, _P], _R]],
    Callable[t.Concatenate[_Self, _P], _R],
]:
    def decorator(
        f: Callable[t.Concatenate[_Self, _P], _R],
    ) -> Callable[t.Concatenate[_Self, _P], _R]:
        @functools.wraps(f)
        def wrapper(self: _Self, *args: _P.args, **kwargs: _P.kwargs) -> _R:
            # We use _Self instead of APIClient since this is used for mixins for APIClient.
            # This unfortunately means that self._version does not exist in the mixin,
            # it only exists after mixing in. This is why we ignore types here.
            if utils.version_lt(self._version, version):  # type: ignore
                raise errors.InvalidVersion(
                    f"{f.__name__} is not available for version < {version}"
                )
            return f(self, *args, **kwargs)

        return wrapper

    return decorator


def update_headers(
    f: Callable[t.Concatenate[APIClient, _P], _R],
) -> Callable[t.Concatenate[APIClient, _P], _R]:
    def inner(self: APIClient, *args: _P.args, **kwargs: _P.kwargs) -> _R:
        if "HttpHeaders" in self._general_configs:
            if not kwargs.get("headers"):
                kwargs["headers"] = self._general_configs["HttpHeaders"]
            else:
                # We cannot (yet) model that kwargs["headers"] should be a dictionary
                kwargs["headers"].update(self._general_configs["HttpHeaders"])  # type: ignore
        return f(self, *args, **kwargs)

    return inner
