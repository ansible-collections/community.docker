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
from shutil import which


def find_executable(executable: str, path: str | None = None) -> str | None:
    """
    As distutils.spawn.find_executable, but on Windows, look up
    every extension declared in PATHEXT instead of just `.exe`
    """
    # shutil.which() already uses PATHEXT on Windows, so on
    # Python 3 we can simply use shutil.which() in all cases.
    # (https://github.com/docker/docker-py/commit/42789818bed5d86b487a030e2e60b02bf0cfa284)
    return which(executable, path=path)


def create_environment_dict(overrides: dict[str, str] | None) -> dict[str, str]:
    """
    Create and return a copy of os.environ with the specified overrides
    """
    result = os.environ.copy()
    result.update(overrides or {})
    return result
