# Copyright (c) 2026 Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import typing as t
from collections.abc import Mapping, Sequence

try:
    from ansible.module_utils.secrets import register_secret, register_secrets  # type: ignore[import-not-found]

    HAS_SECRETS_API = True
except ImportError:
    HAS_SECRETS_API = False


def _collect_recursively(
    value: t.Any, collected_values: list[str], *, int_to_string: bool = False
) -> None:
    if isinstance(value, Mapping):
        for v in value.items():
            _collect_recursively(v, collected_values, int_to_string=int_to_string)
    elif isinstance(value, str):
        collected_values.append(value)
    elif isinstance(value, Sequence):
        for v in value:
            _collect_recursively(v, collected_values, int_to_string=int_to_string)
    elif int_to_string and isinstance(value, int):
        collected_values.append(str(value))


def mark_values_as_secrets(value: t.Any, *, int_to_string: bool = False) -> t.Any:
    """Register all strings appearing in the (potentially nested) data structure ``value`` as secrets."""
    if HAS_SECRETS_API:
        collected_values: list[str] = []
        _collect_recursively(value, collected_values, int_to_string=int_to_string)
        if collected_values:
            register_secrets(collected_values)
    return value


def mark_as_secret(value: str) -> str:
    """Register a string as a secret."""
    if HAS_SECRETS_API:
        value = register_secret(value)
    return value
