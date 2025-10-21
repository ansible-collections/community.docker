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


if t.TYPE_CHECKING:
    from subprocess import CalledProcessError


class StoreError(RuntimeError):
    pass


class CredentialsNotFound(StoreError):
    pass


class InitializationError(StoreError):
    pass


def process_store_error(cpe: CalledProcessError, program: str) -> StoreError:
    message = cpe.output.decode("utf-8")
    if "credentials not found in native keychain" in message:
        return CredentialsNotFound(f"No matching credentials in {program}")
    return StoreError(
        f'Credentials store {program} exited with "{cpe.output.decode("utf-8").strip()}".'
    )
