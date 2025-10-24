# This code is part of the Ansible collection community.docker, but is an independent component.
# This particular file, and this file only, is based on the Docker SDK for Python (https://github.com/docker/docker-py/)
#
# Copyright (c) 2016-2022 Docker, Inc.
#
# It is licensed under the Apache 2.0 license (see LICENSES/Apache-2.0.txt in this collection)
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import datetime
import io
import json
import os
import re
import shutil
import socket
import struct
import tempfile
import threading
import time
import typing as t
import unittest
from http.server import BaseHTTPRequestHandler
from socketserver import ThreadingTCPServer
from unittest import mock

import pytest
import requests
from requests.packages import urllib3

from ansible_collections.community.docker.plugins.module_utils._api import (
    constants,
    errors,
)
from ansible_collections.community.docker.plugins.module_utils._api.api.client import (
    APIClient,
)
from ansible_collections.community.docker.tests.unit.plugins.module_utils._api.constants import (
    DEFAULT_DOCKER_API_VERSION,
)

from .. import fake_api


DEFAULT_TIMEOUT_SECONDS = constants.DEFAULT_TIMEOUT_SECONDS


def response(
    status_code: int = 200,
    content: bytes | dict[str, t.Any] | list[dict[str, t.Any]] = b"",
    headers: dict[str, str] | None = None,
    reason: str = "",
    elapsed: int = 0,
    request=None,
    raw=None,
) -> requests.Response:
    res = requests.Response()
    res.status_code = status_code
    if not isinstance(content, bytes):
        content = json.dumps(content).encode("ascii")
    res._content = content
    res.headers = requests.structures.CaseInsensitiveDict(headers or {})
    res.reason = reason
    res.elapsed = datetime.timedelta(elapsed)
    res.request = request
    res.raw = raw
    return res


def fake_resolve_authconfig(  # pylint: disable=keyword-arg-before-vararg
    authconfig, *args, registry=None, **kwargs
) -> None:
    return None


def fake_inspect_container(self, container: str, tty: bool = False):
    return fake_api.get_fake_inspect_container(tty=tty)[1]


def fake_resp(
    method: str, url: str, *args: t.Any, **kwargs: t.Any
) -> requests.Response:
    key: str | tuple[str, str] | None = None
    if url in fake_api.fake_responses:
        key = url
    elif (url, method) in fake_api.fake_responses:
        key = (url, method)
    if not key:
        raise NotImplementedError(f"{method} {url}")
    status_code, content = fake_api.fake_responses[key]()
    return response(status_code=status_code, content=content)


fake_request = mock.Mock(side_effect=fake_resp)


def fake_get(self, url: str, *args, **kwargs) -> requests.Response:
    return fake_request("GET", url, *args, **kwargs)


def fake_post(self, url: str, *args, **kwargs) -> requests.Response:
    return fake_request("POST", url, *args, **kwargs)


def fake_put(self, url: str, *args, **kwargs) -> requests.Response:
    return fake_request("PUT", url, *args, **kwargs)


def fake_delete(self, url: str, *args, **kwargs) -> requests.Response:
    return fake_request("DELETE", url, *args, **kwargs)


def fake_read_from_socket(
    self,
    response: requests.Response,
    stream: bool,
    tty: bool = False,
    demux: bool = False,
) -> bytes:
    return b""


url_base = f"{fake_api.prefix}/"  # pylint: disable=invalid-name
url_prefix = f"{url_base}v{DEFAULT_DOCKER_API_VERSION}/"  # pylint: disable=invalid-name


class BaseAPIClientTest(unittest.TestCase):
    def setUp(self) -> None:
        self.patcher = mock.patch.multiple(
            "ansible_collections.community.docker.plugins.module_utils._api.api.client.APIClient",
            get=fake_get,
            post=fake_post,
            put=fake_put,
            delete=fake_delete,
            _read_from_socket=fake_read_from_socket,
        )
        self.patcher.start()
        self.client = APIClient(version=DEFAULT_DOCKER_API_VERSION)

    def tearDown(self) -> None:
        self.client.close()
        self.patcher.stop()

    def base_create_payload(
        self, img: str = "busybox", cmd: list[str] | None = None
    ) -> dict[str, t.Any]:
        if not cmd:
            cmd = ["true"]
        return {
            "Tty": False,
            "Image": img,
            "Cmd": cmd,
            "AttachStdin": False,
            "AttachStderr": True,
            "AttachStdout": True,
            "StdinOnce": False,
            "OpenStdin": False,
            "NetworkDisabled": False,
        }


class DockerApiTest(BaseAPIClientTest):
    def test_ctor(self) -> None:
        with pytest.raises(errors.DockerException) as excinfo:
            APIClient(version=1.12)  # type: ignore

        assert (
            str(excinfo.value)
            == "Version parameter must be a string or None. Found float"
        )

    def test_url_valid_resource(self) -> None:
        url = self.client._url("/hello/{0}/world", "somename")
        assert url == f"{url_prefix}hello/somename/world"

        url = self.client._url("/hello/{0}/world/{1}", "somename", "someothername")
        assert url == f"{url_prefix}hello/somename/world/someothername"

        url = self.client._url("/hello/{0}/world", "some?name")
        assert url == f"{url_prefix}hello/some%3Fname/world"

        url = self.client._url("/images/{0}/push", "localhost:5000/image")
        assert url == f"{url_prefix}images/localhost:5000/image/push"

    def test_url_invalid_resource(self) -> None:
        with pytest.raises(ValueError):
            self.client._url("/hello/{0}/world", ["sakuya", "izayoi"])  # type: ignore

    def test_url_no_resource(self) -> None:
        url = self.client._url("/simple")
        assert url == f"{url_prefix}simple"

    def test_url_unversioned_api(self) -> None:
        url = self.client._url("/hello/{0}/world", "somename", versioned_api=False)
        assert url == f"{url_base}hello/somename/world"

    def test_version(self) -> None:
        self.client.version()

        fake_request.assert_called_with(
            "GET", url_prefix + "version", timeout=DEFAULT_TIMEOUT_SECONDS
        )

    def test_version_no_api_version(self) -> None:
        self.client.version(False)

        fake_request.assert_called_with(
            "GET", url_base + "version", timeout=DEFAULT_TIMEOUT_SECONDS
        )

    def test_retrieve_server_version(self) -> None:
        client = APIClient(version="auto")
        assert isinstance(client._version, str)
        assert not (client._version == "auto")
        client.close()

    def test_auto_retrieve_server_version(self) -> None:
        version = self.client._retrieve_server_version()
        assert isinstance(version, str)

    def test_info(self) -> None:
        self.client.info()

        fake_request.assert_called_with(
            "GET", url_prefix + "info", timeout=DEFAULT_TIMEOUT_SECONDS
        )

    def test_search(self) -> None:
        self.client.get_json("/images/search", params={"term": "busybox"})

        fake_request.assert_called_with(
            "GET",
            url_prefix + "images/search",
            params={"term": "busybox"},
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )

    def test_login(self) -> None:
        self.client.login("sakuya", "izayoi")
        args = fake_request.call_args
        assert args[0][0] == "POST"
        assert args[0][1] == url_prefix + "auth"
        assert json.loads(args[1]["data"]) == {
            "username": "sakuya",
            "password": "izayoi",
        }
        assert args[1]["headers"] == {"Content-Type": "application/json"}
        assert self.client._auth_configs.auths["docker.io"] == {
            "email": None,
            "password": "izayoi",
            "username": "sakuya",
            "serveraddress": None,
        }

    def _socket_path_for_client_session(self, client) -> str:
        socket_adapter = client.get_adapter("http+docker://")
        return socket_adapter.socket_path

    def test_url_compatibility_unix(self) -> None:
        c = APIClient(base_url="unix://socket", version=DEFAULT_DOCKER_API_VERSION)

        assert self._socket_path_for_client_session(c) == "/socket"

    def test_url_compatibility_unix_triple_slash(self) -> None:
        c = APIClient(base_url="unix:///socket", version=DEFAULT_DOCKER_API_VERSION)

        assert self._socket_path_for_client_session(c) == "/socket"

    def test_url_compatibility_http_unix_triple_slash(self) -> None:
        c = APIClient(
            base_url="http+unix:///socket", version=DEFAULT_DOCKER_API_VERSION
        )

        assert self._socket_path_for_client_session(c) == "/socket"

    def test_url_compatibility_http(self) -> None:
        c = APIClient(
            base_url="http://hostname:1234", version=DEFAULT_DOCKER_API_VERSION
        )

        assert c.base_url == "http://hostname:1234"

    def test_url_compatibility_tcp(self) -> None:
        c = APIClient(
            base_url="tcp://hostname:1234", version=DEFAULT_DOCKER_API_VERSION
        )

        assert c.base_url == "http://hostname:1234"

    def test_remove_link(self) -> None:
        self.client.delete_call(
            "/containers/{0}",
            "3cc2351ab11b",
            params={"v": False, "link": True, "force": False},
        )

        fake_request.assert_called_with(
            "DELETE",
            url_prefix + "containers/3cc2351ab11b",
            params={"v": False, "link": True, "force": False},
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )

    def test_stream_helper_decoding(self) -> None:
        status_code, content = fake_api.fake_responses[url_prefix + "events"]()
        content_str = json.dumps(content).encode("utf-8")
        body = io.BytesIO(content_str)

        # mock a stream interface
        raw_resp = urllib3.HTTPResponse(body=body)
        setattr(raw_resp._fp, "chunked", True)
        setattr(raw_resp._fp, "chunk_left", len(body.getvalue()) - 1)

        # pass `decode=False` to the helper
        raw_resp._fp.seek(0)
        resp = response(status_code=status_code, content=content, raw=raw_resp)
        result = next(self.client._stream_helper(resp))
        assert result == content_str

        # pass `decode=True` to the helper
        raw_resp._fp.seek(0)
        resp = response(status_code=status_code, content=content, raw=raw_resp)
        result = next(self.client._stream_helper(resp, decode=True))
        assert result == content

        # non-chunked response, pass `decode=False` to the helper
        setattr(raw_resp._fp, "chunked", False)
        raw_resp._fp.seek(0)
        resp = response(status_code=status_code, content=content, raw=raw_resp)
        result = next(self.client._stream_helper(resp))
        assert result == content_str.decode("utf-8")  # type: ignore

        # non-chunked response, pass `decode=True` to the helper
        raw_resp._fp.seek(0)
        resp = response(status_code=status_code, content=content, raw=raw_resp)
        result = next(self.client._stream_helper(resp, decode=True))
        assert result == content


class UnixSocketStreamTest(unittest.TestCase):
    def setUp(self) -> None:
        socket_dir = tempfile.mkdtemp()
        self.build_context = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, socket_dir)
        self.addCleanup(shutil.rmtree, self.build_context)
        self.socket_file = os.path.join(socket_dir, "test_sock.sock")
        self.server_socket = self._setup_socket()
        self.stop_server = False
        server_thread = threading.Thread(target=self.run_server)
        server_thread.daemon = True
        server_thread.start()
        self.response: t.Any = None
        self.request_handler: t.Any = None
        self.addCleanup(server_thread.join)
        self.addCleanup(self.stop)

    def stop(self) -> None:
        self.stop_server = True

    def _setup_socket(self) -> socket.socket:
        server_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server_sock.bind(self.socket_file)
        # Non-blocking mode so that we can shut the test down easily
        server_sock.setblocking(0)  # type: ignore
        server_sock.listen(5)
        return server_sock

    def run_server(self) -> None:
        try:
            while not self.stop_server:
                try:
                    connection, dummy_client_address = self.server_socket.accept()
                except socket.error:
                    # Probably no connection to accept yet
                    time.sleep(0.01)
                    continue

                connection.setblocking(1)  # type: ignore
                try:
                    self.request_handler(connection)
                finally:
                    connection.close()
        finally:
            self.server_socket.close()

    def early_response_sending_handler(self, connection) -> None:
        data = b""
        headers = None

        connection.sendall(self.response)
        while not headers:
            data += connection.recv(2048)
            parts = data.split(b"\r\n\r\n", 1)
            if len(parts) == 2:
                headers, data = parts

        mo = re.search(r"Content-Length: ([0-9]+)", headers.decode())
        assert mo
        content_length = int(mo.group(1))

        while True:
            if len(data) >= content_length:
                break

            data += connection.recv(2048)

    @pytest.mark.skipif(constants.IS_WINDOWS_PLATFORM, reason="Unix only")
    def test_early_stream_response(self) -> None:
        self.request_handler = self.early_response_sending_handler
        lines = []
        for i in range(0, 50):
            line = str(i).encode()
            lines += [f"{len(line):x}".encode(), line]
        lines.append(b"0")
        lines.append(b"")

        self.response = (
            b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n"
        ) + b"\r\n".join(lines)

        with APIClient(
            base_url="http+unix://" + self.socket_file,
            version=DEFAULT_DOCKER_API_VERSION,
        ) as client:
            for i in range(5):
                try:
                    params = {
                        "t": None,
                        "remote": None,
                        "q": False,
                        "nocache": False,
                        "rm": False,
                        "forcerm": False,
                        "pull": False,
                        "dockerfile": "Dockerfile",
                    }
                    headers = {"Content-Type": "application/tar"}
                    data = b"..."
                    response = client._post(
                        client._url("/build"),
                        params=params,
                        headers=headers,
                        data=data,
                        stream=True,
                    )
                    stream = client._stream_helper(response, decode=False)
                    break
                except requests.ConnectionError as e:
                    if i == 4:
                        raise e

            assert list(stream) == [str(i).encode() for i in range(50)]


@pytest.mark.skip(
    "This test requires starting a networking server and tries to access it. "
    "This does not work with network separation with Docker-based unit tests, "
    "but it does work with podman-based unit tests."
)
class TCPSocketStreamTest(unittest.TestCase):
    stdout_data = b"""
    Now, those children out there, they're jumping through the
    flames in the hope that the god of the fire will make them fruitful.
    Really, you can't blame them. After all, what girl would not prefer the
    child of a god to that of some acne-scarred artisan?
    """
    stderr_data = b"""
    And what of the true God? To whose glory churches and monasteries have been
    built on these islands for generations past? Now shall what of Him?
    """

    server: ThreadingTCPServer
    thread: threading.Thread
    address: str

    @classmethod
    def setup_class(cls) -> None:
        cls.server = ThreadingTCPServer(("", 0), cls.get_handler_class())
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()
        cls.address = f"http://{socket.gethostname()}:{cls.server.server_address[1]}"

    @classmethod
    def teardown_class(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    @classmethod
    def get_handler_class(cls) -> t.Type[BaseHTTPRequestHandler]:
        stdout_data = cls.stdout_data
        stderr_data = cls.stderr_data

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):  # pylint: disable=invalid-name
                resp_data = self.get_resp_data()
                self.send_response(101)
                self.send_header("Content-Type", "application/vnd.docker.raw-stream")
                self.send_header("Connection", "Upgrade")
                self.send_header("Upgrade", "tcp")
                self.end_headers()
                self.wfile.flush()
                time.sleep(0.2)
                self.wfile.write(resp_data)
                self.wfile.flush()

            def get_resp_data(self):
                path = self.path.split("/")[-1]
                if path == "tty":
                    return stdout_data + stderr_data
                if path == "no-tty":
                    data = b""
                    data += self.frame_header(1, stdout_data)
                    data += stdout_data
                    data += self.frame_header(2, stderr_data)
                    data += stderr_data
                    return data
                raise NotImplementedError(f"Unknown path {path}")

            @staticmethod
            def frame_header(stream, data):
                return struct.pack(">BxxxL", stream, len(data))

        return Handler

    def request(
        self,
        stream: bool | None = None,
        tty: bool | None = None,
        demux: bool | None = None,
    ) -> t.Any:
        assert stream is not None and tty is not None and demux is not None
        with APIClient(
            base_url=self.address,
            version=DEFAULT_DOCKER_API_VERSION,
        ) as client:
            if tty:
                url = client._url("/tty")
            else:
                url = client._url("/no-tty")
            resp = client._post(url, stream=True)
            return client._read_from_socket(resp, stream=stream, tty=tty, demux=demux)

    def test_read_from_socket_tty(self) -> None:
        res = self.request(stream=True, tty=True, demux=False)
        assert next(res) == self.stdout_data + self.stderr_data
        with self.assertRaises(StopIteration):
            next(res)

    def test_read_from_socket_tty_demux(self) -> None:
        res = self.request(stream=True, tty=True, demux=True)
        assert next(res) == (self.stdout_data + self.stderr_data, None)
        with self.assertRaises(StopIteration):
            next(res)

    def test_read_from_socket_no_tty(self) -> None:
        res = self.request(stream=True, tty=False, demux=False)
        assert next(res) == self.stdout_data
        assert next(res) == self.stderr_data
        with self.assertRaises(StopIteration):
            next(res)

    def test_read_from_socket_no_tty_demux(self) -> None:
        res = self.request(stream=True, tty=False, demux=True)
        assert (self.stdout_data, None) == next(res)
        assert (None, self.stderr_data) == next(res)
        with self.assertRaises(StopIteration):
            next(res)

    def test_read_from_socket_no_stream_tty(self) -> None:
        res = self.request(stream=False, tty=True, demux=False)
        assert res == self.stdout_data + self.stderr_data

    def test_read_from_socket_no_stream_tty_demux(self) -> None:
        res = self.request(stream=False, tty=True, demux=True)
        assert res == (self.stdout_data + self.stderr_data, None)

    def test_read_from_socket_no_stream_no_tty(self) -> None:
        res = self.request(stream=False, tty=False, demux=False)
        assert res == self.stdout_data + self.stderr_data

    def test_read_from_socket_no_stream_no_tty_demux(self) -> None:
        res = self.request(stream=False, tty=False, demux=True)
        assert res == (self.stdout_data, self.stderr_data)


class UserAgentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.patcher = mock.patch.object(
            APIClient,
            "send",
            return_value=fake_resp("GET", f"{fake_api.prefix}/version"),
        )
        self.mock_send = self.patcher.start()

    def tearDown(self) -> None:
        self.patcher.stop()

    def test_default_user_agent(self) -> None:
        client = APIClient(version=DEFAULT_DOCKER_API_VERSION)
        client.version()

        assert self.mock_send.call_count == 1
        headers = self.mock_send.call_args[0][0].headers
        expected = "ansible-community.docker"
        assert headers["User-Agent"] == expected

    def test_custom_user_agent(self) -> None:
        client = APIClient(user_agent="foo/bar", version=DEFAULT_DOCKER_API_VERSION)
        client.version()

        assert self.mock_send.call_count == 1
        headers = self.mock_send.call_args[0][0].headers
        assert headers["User-Agent"] == "foo/bar"


class DisableSocketTest(unittest.TestCase):
    class DummySocket:
        def __init__(self, timeout: int | float | None = 60) -> None:
            self.timeout = timeout
            self._sock: t.Any = None

        def settimeout(self, timeout: int | float | None) -> None:
            self.timeout = timeout

        def gettimeout(self) -> int | float | None:
            return self.timeout

    def setUp(self) -> None:
        self.client = APIClient(version=DEFAULT_DOCKER_API_VERSION)

    def test_disable_socket_timeout(self) -> None:
        """Test that the timeout is disabled on a generic socket object."""
        the_socket = self.DummySocket()

        self.client._disable_socket_timeout(the_socket)  # type: ignore

        assert the_socket.timeout is None

    def test_disable_socket_timeout2(self) -> None:
        """Test that the timeouts are disabled on a generic socket object
        and it's _sock object if present."""
        the_socket = self.DummySocket()
        the_socket._sock = self.DummySocket()  # type: ignore

        self.client._disable_socket_timeout(the_socket)  # type: ignore

        assert the_socket.timeout is None
        assert the_socket._sock.timeout is None

    def test_disable_socket_timout_non_blocking(self) -> None:
        """Test that a non-blocking socket does not get set to blocking."""
        the_socket = self.DummySocket()
        the_socket._sock = self.DummySocket(0.0)  # type: ignore

        self.client._disable_socket_timeout(the_socket)  # type: ignore

        assert the_socket.timeout is None
        assert the_socket._sock.timeout == 0.0
