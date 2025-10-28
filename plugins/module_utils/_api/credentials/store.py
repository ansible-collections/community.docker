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

import errno
import json
import subprocess
import typing as t

from . import constants, errors
from .utils import create_environment_dict, find_executable


class Store:
    def __init__(self, program: str, environment: dict[str, str] | None = None) -> None:
        """Create a store object that acts as an interface to
        perform the basic operations for storing, retrieving
        and erasing credentials using `program`.
        """
        self.program = constants.PROGRAM_PREFIX + program
        self.exe = find_executable(self.program)
        self.environment = environment
        if self.exe is None:
            raise errors.InitializationError(
                f"{self.program} not installed or not available in PATH"
            )

    def get(self, server: str | bytes) -> dict[str, t.Any]:
        """Retrieve credentials for `server`. If no credentials are found,
        a `StoreError` will be raised.
        """
        if not isinstance(server, bytes):
            server = server.encode("utf-8")
        data = self._execute("get", server)
        result = json.loads(data.decode("utf-8"))

        # docker-credential-pass will return an object for inexistent servers
        # whereas other helpers will exit with returncode != 0. For
        # consistency, if no significant data is returned,
        # raise CredentialsNotFound
        if result["Username"] == "" and result["Secret"] == "":
            raise errors.CredentialsNotFound(
                f"No matching credentials in {self.program}"
            )

        return result

    def store(self, server: str, username: str, secret: str) -> bytes:
        """Store credentials for `server`. Raises a `StoreError` if an error
        occurs.
        """
        data_input = json.dumps(
            {"ServerURL": server, "Username": username, "Secret": secret}
        ).encode("utf-8")
        return self._execute("store", data_input)

    def erase(self, server: str | bytes) -> None:
        """Erase credentials for `server`. Raises a `StoreError` if an error
        occurs.
        """
        if not isinstance(server, bytes):
            server = server.encode("utf-8")
        self._execute("erase", server)

    def list(self) -> t.Any:
        """List stored credentials. Requires v0.4.0+ of the helper."""
        data = self._execute("list", None)
        return json.loads(data.decode("utf-8"))

    def _execute(self, subcmd: str, data_input: bytes | None) -> bytes:
        if self.exe is None:
            raise errors.StoreError(
                f"{self.program} not installed or not available in PATH"
            )
        output = None
        env = create_environment_dict(self.environment)
        try:
            output = subprocess.check_output(
                [self.exe, subcmd],
                input=data_input,
                env=env,
            )
        except subprocess.CalledProcessError as e:
            raise errors.process_store_error(e, self.program) from e
        except OSError as e:
            if e.errno == errno.ENOENT:
                raise errors.StoreError(
                    f"{self.program} not installed or not available in PATH"
                ) from e
            raise errors.StoreError(
                f'Unexpected OS error "{e.strerror}", errno={e.errno}'
            ) from e
        return output
