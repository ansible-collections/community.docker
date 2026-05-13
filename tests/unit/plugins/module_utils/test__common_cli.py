# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import typing as t

import pytest

from ansible_collections.community.docker.plugins.module_utils._common_cli import (
    AnsibleDockerClientBase,
)


class _FailCalled(Exception):
    """Raised by the test stub's fail() so tests can inspect the failure."""

    def __init__(self, msg: str, **kwargs: t.Any) -> None:
        super().__init__(msg)
        self.msg = msg
        self.kwargs = kwargs


class _StubClient(AnsibleDockerClientBase):
    """Minimal AnsibleDockerClientBase subclass for unit testing the JSON
    helpers without spinning up an AnsibleModule or invoking the real docker
    CLI. We deliberately skip the parent __init__ since it calls call_cli_json
    against `docker version` during construction.
    """

    def __init__(self, rc: int, stdout: bytes, stderr: bytes) -> None:  # pylint: disable=super-init-not-called
        self._rc = rc
        self._stdout = stdout
        self._stderr = stderr
        self._cli = "/usr/bin/docker"
        self._cli_base = [self._cli]
        self.warnings: list[str] = []

    def call_cli(
        self,
        *args: str,
        check_rc: bool = False,
        data: bytes | None = None,
        cwd: str | None = None,
        environ_update: dict[str, str] | None = None,
    ) -> tuple[int, bytes, bytes]:
        return self._rc, self._stdout, self._stderr

    def fail(self, msg: str, **kwargs: t.Any) -> t.NoReturn:
        raise _FailCalled(msg, **kwargs)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def deprecate(
        self,
        msg: str,
        version: str | None = None,
        date: str | None = None,
        collection_name: str | None = None,
    ) -> None:
        pass


# --- call_cli_json -----------------------------------------------------------


def test_call_cli_json_success_returns_parsed_data() -> None:
    client = _StubClient(rc=0, stdout=b'{"foo": "bar"}', stderr=b"")
    rc, data, stderr = client.call_cli_json("anything")
    assert rc == 0
    assert data == {"foo": "bar"}
    assert stderr == b""


def test_call_cli_json_nonzero_rc_with_valid_json_still_returns() -> None:
    """`docker image inspect <missing>` returns rc=1 with stdout `[]`; the
    helper must keep returning so callers can detect the missing image."""
    client = _StubClient(rc=1, stdout=b"[]", stderr=b"Error: No such image: foo")
    rc, data, stderr = client.call_cli_json("image", "inspect", "foo")
    assert rc == 1
    assert data == []
    assert b"No such image" in stderr


def test_call_cli_json_nonzero_rc_with_empty_stdout_surfaces_cli_error() -> None:
    """Regression test for the bug where rc!=0 + empty stdout produced an
    opaque "Expecting value: line 1 column 1 (char 0)" JSONDecodeError that
    hid the real CLI failure that lived in stderr."""
    stderr = b"Error response from daemon: No such image: sha256:c02a671fd71657"
    client = _StubClient(rc=1, stdout=b"", stderr=stderr)
    with pytest.raises(_FailCalled) as excinfo:
        client.call_cli_json("compose", "images", "--format", "json")

    msg = excinfo.value.msg
    # The user-facing message must lead with the CLI failure and include
    # stderr; it must NOT be a generic JSON parsing error.
    assert "rc=1" in msg
    assert "No such image" in msg
    assert "Expecting value" not in msg
    assert "Error while parsing JSON output" not in msg
    # Machine-readable fields should still be populated.
    assert excinfo.value.kwargs["rc"] == 1
    assert excinfo.value.kwargs["stderr"] == stderr
    assert excinfo.value.kwargs["stdout"] == b""


def test_call_cli_json_zero_rc_with_unparseable_stdout_keeps_json_error() -> None:
    """When the CLI succeeded but emitted garbage, the JSON parse error is
    actually the relevant message -- preserve the existing behavior."""
    client = _StubClient(rc=0, stdout=b"not json", stderr=b"")
    with pytest.raises(_FailCalled) as excinfo:
        client.call_cli_json("info", "--format", "{{ json . }}")
    assert "Error while parsing JSON output" in excinfo.value.msg


# --- call_cli_json_stream ----------------------------------------------------


def test_call_cli_json_stream_success_returns_parsed_lines() -> None:
    client = _StubClient(
        rc=0, stdout=b'{"a": 1}\n{"b": 2}\n', stderr=b""
    )
    rc, data, stderr = client.call_cli_json_stream("ps", "--format", "json")
    assert rc == 0
    assert data == [{"a": 1}, {"b": 2}]
    assert stderr == b""


def test_call_cli_json_stream_nonzero_rc_with_bad_line_surfaces_cli_error() -> None:
    """Regression test: the streaming variant of call_cli_json must also
    surface the CLI's stderr when rc!=0 and a JSON line fails to parse."""
    stderr = b"Error response from daemon: connection refused"
    client = _StubClient(rc=2, stdout=b"{this is not json}\n", stderr=stderr)
    with pytest.raises(_FailCalled) as excinfo:
        client.call_cli_json_stream("ps", "--format", "json")
    msg = excinfo.value.msg
    assert "rc=2" in msg
    assert "connection refused" in msg
    assert "Error while parsing JSON output" not in msg
    assert excinfo.value.kwargs["rc"] == 2
    assert excinfo.value.kwargs["stderr"] == stderr


def test_call_cli_json_stream_zero_rc_with_bad_line_keeps_json_error() -> None:
    client = _StubClient(rc=0, stdout=b"{this is not json}\n", stderr=b"")
    with pytest.raises(_FailCalled) as excinfo:
        client.call_cli_json_stream("ps", "--format", "json")
    assert "Error while parsing JSON output" in excinfo.value.msg


# --- warn_on_stderr behaviour preserved -------------------------------------


def test_call_cli_json_warn_on_stderr_still_warns() -> None:
    client = _StubClient(rc=0, stdout=b"{}", stderr=b"some warning")
    rc, data, stderr = client.call_cli_json("any", warn_on_stderr=True)
    assert rc == 0
    assert data == {}
    assert "some warning" in client.warnings
