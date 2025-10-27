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

import json
import logging
import os
import struct
import typing as t
from urllib.parse import quote

from .. import auth
from .._import_helper import HTTPError as _HTTPError
from .._import_helper import InvalidSchema as _InvalidSchema
from .._import_helper import Session as _Session
from .._import_helper import fail_on_missing_imports
from ..constants import (
    DEFAULT_DATA_CHUNK_SIZE,
    DEFAULT_MAX_POOL_SIZE,
    DEFAULT_NUM_POOLS,
    DEFAULT_NUM_POOLS_SSH,
    DEFAULT_TIMEOUT_SECONDS,
    DEFAULT_USER_AGENT,
    IS_WINDOWS_PLATFORM,
    MINIMUM_DOCKER_API_VERSION,
    STREAM_HEADER_SIZE_BYTES,
)
from ..errors import (
    DockerException,
    InvalidVersion,
    MissingRequirementException,
    TLSParameterError,
    create_api_error_from_http_exception,
)
from ..tls import TLSConfig
from ..transport.npipeconn import NpipeHTTPAdapter
from ..transport.npipesocket import PYWIN32_IMPORT_ERROR
from ..transport.sshconn import PARAMIKO_IMPORT_ERROR, SSHHTTPAdapter
from ..transport.ssladapter import SSLHTTPAdapter
from ..transport.unixconn import UnixHTTPAdapter
from ..utils import config, json_stream, utils
from ..utils.decorators import minimum_version, update_headers
from ..utils.proxy import ProxyConfig
from ..utils.socket import consume_socket_output, demux_adaptor, frames_iter


if t.TYPE_CHECKING:
    from requests import Response
    from requests.adapters import BaseAdapter

    from ..._socket_helper import SocketLike


log = logging.getLogger(__name__)


class APIClient(_Session):
    """
    A low-level client for the Docker Engine API.

    Example:

        >>> import docker
        >>> client = docker.APIClient(base_url='unix://var/run/docker.sock')
        >>> client.version()
        {'ApiVersion': '1.33',
         'Arch': 'amd64',
         'BuildTime': '2017-11-19T18:46:37.000000000+00:00',
         'GitCommit': 'f4ffd2511c',
         'GoVersion': 'go1.9.2',
         'KernelVersion': '4.14.3-1-ARCH',
         'MinAPIVersion': '1.12',
         'Os': 'linux',
         'Version': '17.10.0-ce'}

    Args:
        base_url (str): URL to the Docker server. For example,
            ``unix:///var/run/docker.sock`` or ``tcp://127.0.0.1:1234``.
        version (str): The version of the API to use. Set to ``auto`` to
            automatically detect the server's version. Default: ``1.35``
        timeout (int): Default timeout for API calls, in seconds.
        tls (bool or :py:class:`~docker.tls.TLSConfig`): Enable TLS. Pass
            ``True`` to enable it with default options, or pass a
            :py:class:`~docker.tls.TLSConfig` object to use custom
            configuration.
        user_agent (str): Set a custom user agent for requests to the server.
        credstore_env (dict): Override environment variables when calling the
            credential store process.
        use_ssh_client (bool): If set to `True`, an ssh connection is made
            via shelling out to the ssh client. Ensure the ssh client is
            installed and configured on the host.
        max_pool_size (int): The maximum number of connections
            to save in the pool.
    """

    __attrs__ = _Session.__attrs__ + [
        "_auth_configs",
        "_general_configs",
        "_version",
        "base_url",
        "timeout",
    ]

    def __init__(
        self,
        base_url: str | None = None,
        version: str | None = None,
        timeout: int | float = DEFAULT_TIMEOUT_SECONDS,
        tls: bool | TLSConfig = False,
        user_agent: str = DEFAULT_USER_AGENT,
        num_pools: int | None = None,
        credstore_env: dict[str, str] | None = None,
        use_ssh_client: bool = False,
        max_pool_size: int = DEFAULT_MAX_POOL_SIZE,
    ) -> None:
        super().__init__()

        fail_on_missing_imports()

        if tls and not base_url:
            raise TLSParameterError(
                "If using TLS, the base_url argument must be provided."
            )

        self.timeout = timeout
        self.headers["User-Agent"] = user_agent

        self._general_configs = config.load_general_config()

        proxy_config = self._general_configs.get("proxies", {})
        try:
            proxies = proxy_config[base_url]
        except KeyError:
            proxies = proxy_config.get("default", {})

        self._proxy_configs = ProxyConfig.from_dict(proxies)

        self._auth_configs = auth.load_config(
            config_dict=self._general_configs,
            credstore_env=credstore_env,
        )
        self.credstore_env = credstore_env

        base_url = utils.parse_host(base_url, IS_WINDOWS_PLATFORM, tls=bool(tls))
        self.base_url = base_url
        # SSH has a different default for num_pools to all other adapters
        num_pools = (
            num_pools or DEFAULT_NUM_POOLS_SSH
            if base_url.startswith("ssh://")
            else DEFAULT_NUM_POOLS
        )

        self._custom_adapter: (
            UnixHTTPAdapter | NpipeHTTPAdapter | SSHHTTPAdapter | SSLHTTPAdapter | None
        ) = None
        if base_url.startswith("http+unix://"):
            self._custom_adapter = UnixHTTPAdapter(
                base_url,
                timeout,
                pool_connections=num_pools,
                max_pool_size=max_pool_size,
            )
            self.mount("http+docker://", self._custom_adapter)
            self._unmount("http://", "https://")
            # host part of URL should be unused, but is resolved by requests
            # module in proxy_bypass_macosx_sysconf()
            self.base_url = "http+docker://localhost"
        elif base_url.startswith("npipe://"):
            if not IS_WINDOWS_PLATFORM:
                raise DockerException(
                    "The npipe:// protocol is only supported on Windows"
                )
            if PYWIN32_IMPORT_ERROR is not None:
                raise MissingRequirementException(
                    "Install pypiwin32 package to enable npipe:// support",
                    "pywin32",
                    PYWIN32_IMPORT_ERROR,
                )
            self._custom_adapter = NpipeHTTPAdapter(
                base_url,
                timeout,
                pool_connections=num_pools,
                max_pool_size=max_pool_size,
            )
            self.mount("http+docker://", self._custom_adapter)
            self.base_url = "http+docker://localnpipe"
        elif base_url.startswith("ssh://"):
            if PARAMIKO_IMPORT_ERROR is not None and not use_ssh_client:
                raise MissingRequirementException(
                    "Install paramiko package to enable ssh:// support",
                    "paramiko",
                    PARAMIKO_IMPORT_ERROR,
                )
            self._custom_adapter = SSHHTTPAdapter(
                base_url,
                timeout,
                pool_connections=num_pools,
                max_pool_size=max_pool_size,
                shell_out=use_ssh_client,
            )
            self.mount("http+docker://ssh", self._custom_adapter)
            self._unmount("http://", "https://")
            self.base_url = "http+docker://ssh"
        else:
            # Use SSLAdapter for the ability to specify SSL version
            if isinstance(tls, TLSConfig):
                tls.configure_client(self)
            elif tls:
                self._custom_adapter = SSLHTTPAdapter(pool_connections=num_pools)
                self.mount("https://", self._custom_adapter)
            self.base_url = base_url

        # version detection needs to be after unix adapter mounting
        if version is None or (isinstance(version, str) and version.lower() == "auto"):
            self._version = self._retrieve_server_version()
        else:
            self._version = version
        if not isinstance(self._version, str):
            raise DockerException(
                f"Version parameter must be a string or None. Found {type(version).__name__}"
            )
        if utils.version_lt(self._version, MINIMUM_DOCKER_API_VERSION):
            raise InvalidVersion(
                f"API versions below {MINIMUM_DOCKER_API_VERSION} are no longer supported by this library."
            )

    def _retrieve_server_version(self) -> str:
        try:
            version_result = self.version(api_version=False)
        except Exception as e:
            raise DockerException(
                f"Error while fetching server API version: {e}"
            ) from e

        try:
            return version_result["ApiVersion"]
        except KeyError:
            raise DockerException(
                'Invalid response from docker daemon: key "ApiVersion" is missing.'
            ) from None
        except Exception as e:
            raise DockerException(
                f"Error while fetching server API version: {e}. Response seems to be broken."
            ) from e

    def _set_request_timeout(self, kwargs: dict[str, t.Any]) -> dict[str, t.Any]:
        """Prepare the kwargs for an HTTP request by inserting the timeout
        parameter, if not already present."""
        kwargs.setdefault("timeout", self.timeout)
        return kwargs

    @update_headers
    def _post(self, url: str, **kwargs: t.Any) -> Response:
        return self.post(url, **self._set_request_timeout(kwargs))

    @update_headers
    def _get(self, url: str, **kwargs: t.Any) -> Response:
        return self.get(url, **self._set_request_timeout(kwargs))

    @update_headers
    def _head(self, url: str, **kwargs: t.Any) -> Response:
        return self.head(url, **self._set_request_timeout(kwargs))

    @update_headers
    def _put(self, url: str, **kwargs: t.Any) -> Response:
        return self.put(url, **self._set_request_timeout(kwargs))

    @update_headers
    def _delete(self, url: str, **kwargs: t.Any) -> Response:
        return self.delete(url, **self._set_request_timeout(kwargs))

    def _url(self, pathfmt: str, *args: str, versioned_api: bool = True) -> str:
        for arg in args:
            if not isinstance(arg, str):
                raise ValueError(
                    f"Expected a string but found {arg} ({type(arg)}) instead"
                )

        q_args = [quote(arg, safe="/:") for arg in args]

        if versioned_api:
            return f"{self.base_url}/v{self._version}{pathfmt.format(*q_args)}"
        return f"{self.base_url}{pathfmt.format(*q_args)}"

    def _raise_for_status(self, response: Response) -> None:
        """Raises stored :class:`APIError`, if one occurred."""
        try:
            response.raise_for_status()
        except _HTTPError as e:
            create_api_error_from_http_exception(e)

    @t.overload
    def _result(
        self,
        response: Response,
        *,
        get_json: t.Literal[False] = False,
        get_binary: t.Literal[False] = False,
    ) -> str: ...

    @t.overload
    def _result(
        self,
        response: Response,
        *,
        get_json: t.Literal[True],
        get_binary: t.Literal[False] = False,
    ) -> t.Any: ...

    @t.overload
    def _result(
        self,
        response: Response,
        *,
        get_json: t.Literal[False] = False,
        get_binary: t.Literal[True],
    ) -> bytes: ...

    @t.overload
    def _result(
        self, response: Response, *, get_json: bool = False, get_binary: bool = False
    ) -> t.Any | str | bytes: ...

    def _result(
        self, response: Response, *, get_json: bool = False, get_binary: bool = False
    ) -> t.Any | str | bytes:
        if get_json and get_binary:
            raise AssertionError("json and binary must not be both True")
        self._raise_for_status(response)

        if get_json:
            return response.json()
        if get_binary:
            return response.content
        return response.text

    def _post_json(
        self, url: str, data: dict[str, str | None] | t.Any, **kwargs: t.Any
    ) -> Response:
        # Go <1.1 cannot unserialize null to a string
        # so we do this disgusting thing here.
        data2: dict[str, t.Any] = {}
        if data is not None and isinstance(data, dict):
            for k, v in data.items():
                if v is not None:
                    data2[k] = v
        elif data is not None:
            data2 = data

        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"]["Content-Type"] = "application/json"
        return self._post(url, data=json.dumps(data2), **kwargs)

    def _attach_params(self, override: dict[str, int] | None = None) -> dict[str, int]:
        return override or {"stdout": 1, "stderr": 1, "stream": 1}

    def _get_raw_response_socket(self, response: Response) -> SocketLike:
        self._raise_for_status(response)
        if self.base_url == "http+docker://localnpipe":
            sock = response.raw._fp.fp.raw.sock  # type: ignore[union-attr]
        elif self.base_url.startswith("http+docker://ssh"):
            sock = response.raw._fp.fp.channel  # type: ignore[union-attr]
        else:
            sock = response.raw._fp.fp.raw  # type: ignore[union-attr]
            if self.base_url.startswith("https://"):
                sock = sock._sock  # type: ignore[union-attr]
        try:
            # Keep a reference to the response to stop it being garbage
            # collected. If the response is garbage collected, it will
            # close TLS sockets.
            sock._response = response
        except AttributeError:
            # UNIX sockets cannot have attributes set on them, but that's
            # fine because we will not be doing TLS over them
            pass

        return sock

    @t.overload
    def _stream_helper(
        self, response: Response, *, decode: t.Literal[False] = False
    ) -> t.Generator[bytes]: ...

    @t.overload
    def _stream_helper(
        self, response: Response, *, decode: t.Literal[True]
    ) -> t.Generator[t.Any]: ...

    def _stream_helper(
        self, response: Response, *, decode: bool = False
    ) -> t.Generator[t.Any]:
        """Generator for data coming from a chunked-encoded HTTP response."""

        if response.raw._fp.chunked:  # type: ignore[union-attr]
            if decode:
                yield from json_stream.json_stream(
                    self._stream_helper(response, decode=False)
                )
            else:
                reader = response.raw
                while not reader.closed:
                    # this read call will block until we get a chunk
                    data = reader.read(1)
                    if not data:
                        break
                    if reader._fp.chunk_left:  # type: ignore[union-attr]
                        data += reader.read(reader._fp.chunk_left)  # type: ignore[union-attr]
                    yield data
        else:
            # Response is not chunked, meaning we probably
            # encountered an error immediately
            yield self._result(response, get_json=decode)

    def _multiplexed_buffer_helper(self, response: Response) -> t.Generator[bytes]:
        """A generator of multiplexed data blocks read from a buffered
        response."""
        buf = self._result(response, get_binary=True)
        buf_length = len(buf)
        walker = 0
        while True:
            if buf_length - walker < STREAM_HEADER_SIZE_BYTES:
                break
            header = buf[walker : walker + STREAM_HEADER_SIZE_BYTES]
            dummy, length = struct.unpack_from(">BxxxL", header)
            start = walker + STREAM_HEADER_SIZE_BYTES
            end = start + length
            walker = end
            yield buf[start:end]

    def _multiplexed_response_stream_helper(
        self, response: Response
    ) -> t.Generator[bytes]:
        """A generator of multiplexed data blocks coming from a response
        stream."""

        # Disable timeout on the underlying socket to prevent
        # Read timed out(s) for long running processes
        socket = self._get_raw_response_socket(response)
        self._disable_socket_timeout(socket)

        while True:
            header = response.raw.read(STREAM_HEADER_SIZE_BYTES)
            if not header:
                break
            dummy, length = struct.unpack(">BxxxL", header)
            if not length:
                continue
            data = response.raw.read(length)
            if not data:
                break
            yield data

    @t.overload
    def _stream_raw_result(
        self, response: Response, *, chunk_size: int = 1, decode: t.Literal[True] = True
    ) -> t.Generator[str]: ...

    @t.overload
    def _stream_raw_result(
        self, response: Response, *, chunk_size: int = 1, decode: t.Literal[False]
    ) -> t.Generator[bytes]: ...

    def _stream_raw_result(
        self, response: Response, *, chunk_size: int = 1, decode: bool = True
    ) -> t.Generator[str | bytes]:
        """Stream result for TTY-enabled container and raw binary data"""
        self._raise_for_status(response)

        # Disable timeout on the underlying socket to prevent
        # Read timed out(s) for long running processes
        socket = self._get_raw_response_socket(response)
        self._disable_socket_timeout(socket)

        yield from response.iter_content(chunk_size, decode)

    @t.overload
    def _read_from_socket(
        self,
        response: Response,
        *,
        stream: t.Literal[True],
        tty: bool = True,
        demux: t.Literal[False] = False,
    ) -> t.Generator[bytes]: ...

    @t.overload
    def _read_from_socket(
        self,
        response: Response,
        *,
        stream: t.Literal[True],
        tty: t.Literal[True] = True,
        demux: t.Literal[True],
    ) -> t.Generator[tuple[bytes, None]]: ...

    @t.overload
    def _read_from_socket(
        self,
        response: Response,
        *,
        stream: t.Literal[True],
        tty: t.Literal[False],
        demux: t.Literal[True],
    ) -> t.Generator[tuple[bytes, None] | tuple[None, bytes]]: ...

    @t.overload
    def _read_from_socket(
        self,
        response: Response,
        *,
        stream: t.Literal[False],
        tty: bool = True,
        demux: t.Literal[False] = False,
    ) -> bytes: ...

    @t.overload
    def _read_from_socket(
        self,
        response: Response,
        *,
        stream: t.Literal[False],
        tty: t.Literal[True] = True,
        demux: t.Literal[True],
    ) -> tuple[bytes, None]: ...

    @t.overload
    def _read_from_socket(
        self,
        response: Response,
        *,
        stream: t.Literal[False],
        tty: t.Literal[False],
        demux: t.Literal[True],
    ) -> tuple[bytes, bytes]: ...

    @t.overload
    def _read_from_socket(
        self, response: Response, *, stream: bool, tty: bool = True, demux: bool = False
    ) -> t.Any: ...

    def _read_from_socket(
        self, response: Response, *, stream: bool, tty: bool = True, demux: bool = False
    ) -> t.Any:
        """Consume all data from the socket, close the response and return the
        data. If stream=True, then a generator is returned instead and the
        caller is responsible for closing the response.
        """
        socket = self._get_raw_response_socket(response)

        gen = frames_iter(socket, tty)

        if demux:
            # The generator will output tuples (stdout, stderr)
            demux_gen: t.Generator[tuple[bytes | None, bytes | None]] = (
                demux_adaptor(*frame) for frame in gen
            )
            if stream:
                return demux_gen
            try:
                # Wait for all the frames, concatenate them, and return the result
                return consume_socket_output(demux_gen, demux=True)
            finally:
                response.close()
        else:
            # The generator will output strings
            mux_gen: t.Generator[bytes] = (data for (dummy, data) in gen)
            if stream:
                return mux_gen
            try:
                # Wait for all the frames, concatenate them, and return the result
                return consume_socket_output(mux_gen, demux=False)
            finally:
                response.close()

    def _disable_socket_timeout(self, socket: SocketLike) -> None:
        """Depending on the combination of python version and whether we are
        connecting over http or https, we might need to access _sock, which
        may or may not exist; or we may need to just settimeout on socket
        itself, which also may or may not have settimeout on it. To avoid
        missing the correct one, we try both.

        We also do not want to set the timeout if it is already disabled, as
        you run the risk of changing a socket that was non-blocking to
        blocking, for example when using gevent.
        """
        sockets = [socket, getattr(socket, "_sock", None)]

        for s in sockets:
            if not hasattr(s, "settimeout"):
                continue

            timeout: int | float | None = -1

            if hasattr(s, "gettimeout"):
                timeout = s.gettimeout()  # type: ignore[union-attr]

            # Do not change the timeout if it is already disabled.
            if timeout is None or timeout == 0.0:
                continue

            s.settimeout(None)  # type: ignore[union-attr]

    @t.overload
    def _get_result_tty(
        self, stream: t.Literal[True], res: Response, is_tty: t.Literal[True]
    ) -> t.Generator[str]: ...

    @t.overload
    def _get_result_tty(
        self, stream: t.Literal[True], res: Response, is_tty: t.Literal[False]
    ) -> t.Generator[bytes]: ...

    @t.overload
    def _get_result_tty(
        self, stream: t.Literal[False], res: Response, is_tty: t.Literal[True]
    ) -> bytes: ...

    @t.overload
    def _get_result_tty(
        self, stream: t.Literal[False], res: Response, is_tty: t.Literal[False]
    ) -> bytes: ...

    def _get_result_tty(self, stream: bool, res: Response, is_tty: bool) -> t.Any:
        # We should also use raw streaming (without keep-alive)
        # if we are dealing with a tty-enabled container.
        if is_tty:
            return (
                self._stream_raw_result(res)
                if stream
                else self._result(res, get_binary=True)
            )

        self._raise_for_status(res)
        sep = b""
        if stream:
            return self._multiplexed_response_stream_helper(res)
        return sep.join(list(self._multiplexed_buffer_helper(res)))

    def _unmount(self, *args: t.Any) -> None:
        for proto in args:
            self.adapters.pop(proto)

    def get_adapter(self, url: str) -> BaseAdapter:
        try:
            # pylint finds our Session stub instead of requests.Session:
            # pylint: disable-next=no-member
            return super().get_adapter(url)
        except _InvalidSchema as e:
            if self._custom_adapter:
                return self._custom_adapter
            raise e

    @property
    def api_version(self) -> str:
        return self._version

    def reload_config(self, dockercfg_path: str | None = None) -> None:
        """
        Force a reload of the auth configuration

        Args:
            dockercfg_path (str): Use a custom path for the Docker config file
                (default ``$HOME/.docker/config.json`` if present,
                otherwise ``$HOME/.dockercfg``)

        Returns:
            None
        """
        self._auth_configs = auth.load_config(
            dockercfg_path, credstore_env=self.credstore_env
        )

    def _set_auth_headers(self, headers: dict[str, str | bytes]) -> None:
        log.debug("Looking for auth config")

        # If we do not have any auth data so far, try reloading the config
        # file one more time in case anything showed up in there.
        if not self._auth_configs or self._auth_configs.is_empty:
            log.debug("No auth config in memory - loading from filesystem")
            self._auth_configs = auth.load_config(credstore_env=self.credstore_env)

        # Send the full auth configuration (if any exists), since the build
        # could use any (or all) of the registries.
        if self._auth_configs:
            auth_data = self._auth_configs.get_all_credentials()

            # See https://github.com/docker/docker-py/issues/1683
            if auth.INDEX_URL not in auth_data and auth.INDEX_NAME in auth_data:
                auth_data[auth.INDEX_URL] = auth_data.get(auth.INDEX_NAME, {})

            log.debug("Sending auth config (%s)", ", ".join(repr(k) for k in auth_data))

            if auth_data:
                headers["X-Registry-Config"] = auth.encode_header(auth_data)
        else:
            log.debug("No auth config found")

    def get_binary(self, pathfmt: str, *args: str, **kwargs: t.Any) -> bytes:
        return self._result(
            self._get(self._url(pathfmt, *args, versioned_api=True), **kwargs),
            get_binary=True,
        )

    def get_json(self, pathfmt: str, *args: str, **kwargs: t.Any) -> t.Any:
        return self._result(
            self._get(self._url(pathfmt, *args, versioned_api=True), **kwargs),
            get_json=True,
        )

    def get_text(self, pathfmt: str, *args: str, **kwargs: t.Any) -> str:
        return self._result(
            self._get(self._url(pathfmt, *args, versioned_api=True), **kwargs)
        )

    def get_raw_stream(
        self,
        pathfmt: str,
        *args: str,
        chunk_size: int = DEFAULT_DATA_CHUNK_SIZE,
        **kwargs: t.Any,
    ) -> t.Generator[bytes]:
        res = self._get(
            self._url(pathfmt, *args, versioned_api=True), stream=True, **kwargs
        )
        self._raise_for_status(res)
        return self._stream_raw_result(res, chunk_size=chunk_size, decode=False)

    def delete_call(self, pathfmt: str, *args: str, **kwargs: t.Any) -> None:
        self._raise_for_status(
            self._delete(self._url(pathfmt, *args, versioned_api=True), **kwargs)
        )

    def delete_json(self, pathfmt: str, *args: str, **kwargs: t.Any) -> t.Any:
        return self._result(
            self._delete(self._url(pathfmt, *args, versioned_api=True), **kwargs),
            get_json=True,
        )

    def post_call(self, pathfmt: str, *args: str, **kwargs: t.Any) -> None:
        self._raise_for_status(
            self._post(self._url(pathfmt, *args, versioned_api=True), **kwargs)
        )

    def post_json(
        self, pathfmt: str, *args: str, data: t.Any = None, **kwargs: t.Any
    ) -> None:
        self._raise_for_status(
            self._post_json(
                self._url(pathfmt, *args, versioned_api=True), data, **kwargs
            )
        )

    def post_json_to_binary(
        self, pathfmt: str, *args: str, data: t.Any = None, **kwargs: t.Any
    ) -> bytes:
        return self._result(
            self._post_json(
                self._url(pathfmt, *args, versioned_api=True), data, **kwargs
            ),
            get_binary=True,
        )

    def post_json_to_json(
        self, pathfmt: str, *args: str, data: t.Any = None, **kwargs: t.Any
    ) -> t.Any:
        return self._result(
            self._post_json(
                self._url(pathfmt, *args, versioned_api=True), data, **kwargs
            ),
            get_json=True,
        )

    def post_json_to_text(
        self, pathfmt: str, *args: str, data: t.Any = None, **kwargs: t.Any
    ) -> str:
        return self._result(
            self._post_json(
                self._url(pathfmt, *args, versioned_api=True), data, **kwargs
            ),
        )

    def post_json_to_stream_socket(
        self,
        pathfmt: str,
        *args: str,
        data: t.Any = None,
        headers: dict[str, str] | None = None,
        **kwargs: t.Any,
    ) -> SocketLike:
        headers = headers.copy() if headers else {}
        headers.update(
            {
                "Connection": "Upgrade",
                "Upgrade": "tcp",
            }
        )
        return self._get_raw_response_socket(
            self._post_json(
                self._url(pathfmt, *args, versioned_api=True),
                data,
                headers=headers,
                stream=True,
                **kwargs,
            )
        )

    @t.overload
    def post_json_to_stream(
        self,
        pathfmt: str,
        *args: str,
        data: t.Any = None,
        headers: dict[str, str] | None = None,
        stream: t.Literal[True],
        tty: bool = True,
        demux: t.Literal[False] = False,
        **kwargs: t.Any,
    ) -> t.Generator[bytes]: ...

    @t.overload
    def post_json_to_stream(
        self,
        pathfmt: str,
        *args: str,
        data: t.Any = None,
        headers: dict[str, str] | None = None,
        stream: t.Literal[True],
        tty: t.Literal[True] = True,
        demux: t.Literal[True],
        **kwargs: t.Any,
    ) -> t.Generator[tuple[bytes, None]]: ...

    @t.overload
    def post_json_to_stream(
        self,
        pathfmt: str,
        *args: str,
        data: t.Any = None,
        headers: dict[str, str] | None = None,
        stream: t.Literal[True],
        tty: t.Literal[False],
        demux: t.Literal[True],
        **kwargs: t.Any,
    ) -> t.Generator[tuple[bytes, None] | tuple[None, bytes]]: ...

    @t.overload
    def post_json_to_stream(
        self,
        pathfmt: str,
        *args: str,
        data: t.Any = None,
        headers: dict[str, str] | None = None,
        stream: t.Literal[False],
        tty: bool = True,
        demux: t.Literal[False] = False,
        **kwargs: t.Any,
    ) -> bytes: ...

    @t.overload
    def post_json_to_stream(
        self,
        pathfmt: str,
        *args: str,
        data: t.Any = None,
        headers: dict[str, str] | None = None,
        stream: t.Literal[False],
        tty: t.Literal[True] = True,
        demux: t.Literal[True],
        **kwargs: t.Any,
    ) -> tuple[bytes, None]: ...

    @t.overload
    def post_json_to_stream(
        self,
        pathfmt: str,
        *args: str,
        data: t.Any = None,
        headers: dict[str, str] | None = None,
        stream: t.Literal[False],
        tty: t.Literal[False],
        demux: t.Literal[True],
        **kwargs: t.Any,
    ) -> tuple[bytes, bytes]: ...

    def post_json_to_stream(
        self,
        pathfmt: str,
        *args: str,
        data: t.Any = None,
        headers: dict[str, str] | None = None,
        stream: bool = False,
        demux: bool = False,
        tty: bool = False,
        **kwargs: t.Any,
    ) -> t.Any:
        headers = headers.copy() if headers else {}
        headers.update(
            {
                "Connection": "Upgrade",
                "Upgrade": "tcp",
            }
        )
        return self._read_from_socket(
            self._post_json(
                self._url(pathfmt, *args, versioned_api=True),
                data,
                headers=headers,
                stream=True,
                **kwargs,
            ),
            stream=stream,
            tty=tty,
            demux=demux,
        )

    def post_to_json(self, pathfmt: str, *args: str, **kwargs: t.Any) -> t.Any:
        return self._result(
            self._post(self._url(pathfmt, *args, versioned_api=True), **kwargs),
            get_json=True,
        )

    @minimum_version("1.25")
    def df(self) -> dict[str, t.Any]:
        """
        Get data usage information.

        Returns:
            (dict): A dictionary representing different resource categories
            and their respective data usage.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        url = self._url("/system/df")
        return self._result(self._get(url), get_json=True)

    def info(self) -> dict[str, t.Any]:
        """
        Display system-wide information. Identical to the ``docker info``
        command.

        Returns:
            (dict): The info as a dict

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        return self._result(self._get(self._url("/info")), get_json=True)

    def login(
        self,
        username: str,
        password: str | None = None,
        email: str | None = None,
        registry: str | None = None,
        reauth: bool = False,
        dockercfg_path: str | None = None,
    ) -> dict[str, t.Any]:
        """
        Authenticate with a registry. Similar to the ``docker login`` command.

        Args:
            username (str): The registry username
            password (str): The plaintext password
            email (str): The email for the registry account
            registry (str): URL to the registry.  E.g.
                ``https://index.docker.io/v1/``
            reauth (bool): Whether or not to refresh existing authentication on
                the Docker server.
            dockercfg_path (str): Use a custom path for the Docker config file
                (default ``$HOME/.docker/config.json`` if present,
                otherwise ``$HOME/.dockercfg``)

        Returns:
            (dict): The response from the login request

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

        # If we do not have any auth data so far, try reloading the config file
        # one more time in case anything showed up in there.
        # If dockercfg_path is passed check to see if the config file exists,
        # if so load that config.
        if dockercfg_path and os.path.exists(dockercfg_path):
            self._auth_configs = auth.load_config(
                dockercfg_path, credstore_env=self.credstore_env
            )
        elif not self._auth_configs or self._auth_configs.is_empty:
            self._auth_configs = auth.load_config(credstore_env=self.credstore_env)

        authcfg = self._auth_configs.resolve_authconfig(registry)
        # If we found an existing auth config for this registry and username
        # combination, we can return it immediately unless reauth is requested.
        if authcfg and authcfg.get("username", None) == username and not reauth:
            return authcfg

        req_data = {
            "username": username,
            "password": password,
            "email": email,
            "serveraddress": registry,
        }

        response = self._post_json(self._url("/auth"), data=req_data)
        if response.status_code == 200:
            self._auth_configs.add_auth(registry or auth.INDEX_NAME, req_data)
        return self._result(response, get_json=True)

    def ping(self) -> bool:
        """
        Checks the server is responsive. An exception will be raised if it
        is not responding.

        Returns:
            (bool) The response from the server.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        return self._result(self._get(self._url("/_ping"))) == "OK"

    def version(self, api_version: bool = True) -> dict[str, t.Any]:
        """
        Returns version information from the server. Similar to the ``docker
        version`` command.

        Returns:
            (dict): The server version information

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        url = self._url("/version", versioned_api=api_version)
        return self._result(self._get(url), get_json=True)
