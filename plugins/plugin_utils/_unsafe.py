# Copyright (c) 2023, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Note that this module util is **PRIVATE** to the collection. It can have breaking changes at any time.
# Do not use this from other collections or standalone plugins/modules!

from __future__ import annotations

import re
import typing as t
from collections.abc import Mapping, Set

from ansible.module_utils.common.collections import is_sequence
from ansible.utils.unsafe_proxy import (
    AnsibleUnsafe,
)
from ansible.utils.unsafe_proxy import wrap_var as _make_unsafe


_RE_TEMPLATE_CHARS = re.compile("[{}]")
_RE_TEMPLATE_CHARS_BYTES = re.compile(b"[{}]")


def make_unsafe(value: t.Any) -> t.Any:
    if value is None or isinstance(value, AnsibleUnsafe):
        return value

    if isinstance(value, Mapping):
        return dict((make_unsafe(key), make_unsafe(val)) for key, val in value.items())
    if isinstance(value, Set):
        return set(make_unsafe(elt) for elt in value)
    if is_sequence(value):
        return type(value)(make_unsafe(elt) for elt in value)
    if isinstance(value, bytes):
        if _RE_TEMPLATE_CHARS_BYTES.search(value):
            value = _make_unsafe(value)
        return value
    if isinstance(value, str):
        if _RE_TEMPLATE_CHARS.search(value):
            value = _make_unsafe(value)
        return value

    return value
