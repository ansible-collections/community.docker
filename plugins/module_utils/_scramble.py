# Copyright 2016 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Note that this module util is **PRIVATE** to the collection. It can have breaking changes at any time.
# Do not use this from other collections or standalone plugins/modules!

from __future__ import annotations

import base64
import random

from ansible.module_utils.common.text.converters import to_bytes, to_text


def generate_insecure_key() -> bytes:
    """Do NOT use this for cryptographic purposes!"""
    while True:
        # Generate a one-byte key. Right now the functions below do not use more
        # than one byte, so this is sufficient.
        key = bytes([random.randint(0, 255)])
        # Return anything that is not zero
        if key != b"\x00":
            return key


def scramble(value: str, key: bytes) -> str:
    """Do NOT use this for cryptographic purposes!"""
    if len(key) < 1:
        raise ValueError("Key must be at least one byte")
    b_value = to_bytes(value)
    k = key[0]
    b_value = bytes([k ^ b for b in b_value])
    return f"=S={to_text(base64.b64encode(b_value))}"


def unscramble(value: str, key: bytes) -> str:
    """Do NOT use this for cryptographic purposes!"""
    if len(key) < 1:
        raise ValueError("Key must be at least one byte")
    if not value.startswith("=S="):
        raise ValueError("Value does not start with indicator")
    b_value = base64.b64decode(value[3:])
    k = key[0]
    b_value = bytes([k ^ b for b in b_value])
    return to_text(b_value)
