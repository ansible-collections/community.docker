# Copyright 2022 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations


__metaclass__ = type

import pytest
from ansible_collections.community.docker.plugins.module_utils._scramble import (
    scramble,
    unscramble,
)


@pytest.mark.parametrize(
    "plaintext, key, scrambled",
    [
        ("", b"0", "=S="),
        ("hello", b"\x00", "=S=aGVsbG8="),
        ("hello", b"\x01", "=S=aWRtbW4="),
    ],
)
def test_scramble_unscramble(plaintext, key, scrambled):
    scrambled_ = scramble(plaintext, key)
    print(f"{scrambled_!r} == {scrambled!r}")
    assert scrambled_ == scrambled

    plaintext_ = unscramble(scrambled, key)
    print(f"{plaintext_!r} == {plaintext!r}")
    assert plaintext_ == plaintext
