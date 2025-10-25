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

from ansible.module_utils.common.text.converters import to_text

from ._import_helper import HTTPError as _HTTPError


if t.TYPE_CHECKING:
    from requests import Response


class DockerException(Exception):
    """
    A base class from which all other exceptions inherit.

    If you want to catch all errors that the Docker SDK might raise,
    catch this base exception.
    """


def create_api_error_from_http_exception(e: _HTTPError) -> t.NoReturn:
    """
    Create a suitable APIError from requests.exceptions.HTTPError.
    """
    response = e.response
    try:
        explanation = response.json()["message"]
    except ValueError:
        explanation = to_text((response.content or "").strip())
    cls = APIError
    if response.status_code == 404:
        if explanation and (
            "No such image" in str(explanation)
            or "not found: does not exist or no pull access" in str(explanation)
            or "repository does not exist" in str(explanation)
        ):
            cls = ImageNotFound
        else:
            cls = NotFound
    raise cls(e, response=response, explanation=explanation) from e


class APIError(_HTTPError, DockerException):
    """
    An HTTP error from the API.
    """

    def __init__(
        self,
        message: str | Exception,
        response: Response | None = None,
        explanation: str | None = None,
    ) -> None:
        # requests 1.2 supports response as a keyword argument, but
        # requests 1.1 does not
        super().__init__(message)
        self.response = response
        self.explanation = explanation or ""

    def __str__(self) -> str:
        message = super().__str__()

        if self.is_client_error():
            message = f"{self.response.status_code} Client Error for {self.response.url}: {self.response.reason}"

        elif self.is_server_error():
            message = f"{self.response.status_code} Server Error for {self.response.url}: {self.response.reason}"

        if self.explanation:
            message = f'{message} ("{self.explanation}")'

        return message

    @property
    def status_code(self) -> int | None:
        if self.response is not None:
            return self.response.status_code
        return None

    def is_error(self) -> bool:
        return self.is_client_error() or self.is_server_error()

    def is_client_error(self) -> bool:
        if self.status_code is None:
            return False
        return 400 <= self.status_code < 500

    def is_server_error(self) -> bool:
        if self.status_code is None:
            return False
        return 500 <= self.status_code < 600


class NotFound(APIError):
    pass


class ImageNotFound(NotFound):
    pass


class InvalidVersion(DockerException):
    pass


class InvalidRepository(DockerException):
    pass


class InvalidConfigFile(DockerException):
    pass


class InvalidArgument(DockerException):
    pass


class DeprecatedMethod(DockerException):
    pass


class TLSParameterError(DockerException):
    def __init__(self, msg: str) -> None:
        self.msg = msg

    def __str__(self) -> str:
        return self.msg + (
            ". TLS configurations should map the Docker CLI "
            "client configurations. See "
            "https://docs.docker.com/engine/articles/https/ "
            "for API details."
        )


class NullResource(DockerException, ValueError):
    pass


class ContainerError(DockerException):
    """
    Represents a container that has exited with a non-zero exit code.
    """

    def __init__(
        self,
        container: str,
        exit_status: int,
        command: list[str],
        image: str,
        stderr: str | None,
    ):
        self.container = container
        self.exit_status = exit_status
        self.command = command
        self.image = image
        self.stderr = stderr

        err = f": {stderr}" if stderr is not None else ""
        msg = f"Command '{command}' in image '{image}' returned non-zero exit status {exit_status}{err}"

        super().__init__(msg)


class StreamParseError(RuntimeError):
    def __init__(self, reason: Exception) -> None:
        self.msg = reason


class BuildError(DockerException):
    def __init__(self, reason: str, build_log: str) -> None:
        super().__init__(reason)
        self.msg = reason
        self.build_log = build_log


class ImageLoadError(DockerException):
    pass


def create_unexpected_kwargs_error(name: str, kwargs: dict[str, t.Any]) -> TypeError:
    quoted_kwargs = [f"'{k}'" for k in sorted(kwargs)]
    text = [f"{name}() "]
    if len(quoted_kwargs) == 1:
        text.append("got an unexpected keyword argument ")
    else:
        text.append("got unexpected keyword arguments ")
    text.append(", ".join(quoted_kwargs))
    return TypeError("".join(text))


class MissingContextParameter(DockerException):
    def __init__(self, param: str) -> None:
        self.param = param

    def __str__(self) -> str:
        return f"missing parameter: {self.param}"


class ContextAlreadyExists(DockerException):
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return f"context {self.name} already exists"


class ContextException(DockerException):
    def __init__(self, msg: str) -> None:
        self.msg = msg

    def __str__(self) -> str:
        return self.msg


class ContextNotFound(DockerException):
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return f"context '{self.name}' not found"


class MissingRequirementException(DockerException):
    def __init__(
        self, msg: str, requirement: str, import_exception: ImportError | str
    ) -> None:
        self.msg = msg
        self.requirement = requirement
        self.import_exception = import_exception

    def __str__(self) -> str:
        return self.msg
