# Copyright (c) 2026 Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import typing as t
from io import StringIO
from unittest import mock

import pytest
from ansible.playbook.play_context import PlayContext
from ansible.plugins.loader import connection_loader


def _run_command(options: dict[str, t.Any]) -> bytes:
    play_context = PlayContext()
    conn = connection_loader.get("community.docker.nsenter", play_context, StringIO())
    assert conn is not None
    conn.set_options(direct=options)
    conn._connect()

    process = mock.MagicMock()
    process.returncode = 0
    process.communicate.return_value = (b"out", b"err")
    popen = mock.MagicMock()
    popen.return_value.__enter__.return_value = process

    with mock.patch(
        "ansible_collections.community.docker.plugins.connection.nsenter.subprocess.Popen",
        popen,
    ):
        rc, stdout, stderr = conn.exec_command("/bin/true", sudoable=False)

    assert (rc, stdout, stderr) == (0, b"out", b"err")
    return popen.call_args[0][0]


@pytest.mark.parametrize(
    "options, expected_cmd",
    [
        (
            {},
            b"nsenter --ipc --mount --net --pid --uts --preserve-credentials --target=1 -- /bin/true",
        ),
        (
            {"nsenter_pid": 42, "nsenter_env": False},
            b"nsenter --ipc --mount --net --pid --uts --preserve-credentials --target=42 -- /bin/true",
        ),
        (
            {"nsenter_env": True},
            b"nsenter --ipc --mount --net --pid --uts --preserve-credentials --target=1 --env -- /bin/true",
        ),
    ],
)
def test_nsenter_command(options: dict[str, t.Any], expected_cmd: bytes) -> None:
    assert _run_command(options) == expected_cmd
