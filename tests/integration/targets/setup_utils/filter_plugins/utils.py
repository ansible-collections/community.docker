# Copyright (c) 2026, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from collections.abc import Mapping, Sequence


def _normalize_image_impl(data):
    identity = data.get("Identity")
    if not isinstance(identity, Mapping):
        return data
    pull = identity.get("Pull")
    if not isinstance(pull, Sequence):
        return data
    new_identity = dict(identity)
    new_identity["Pull"] = sorted(identity["Pull"], key=lambda entry: entry.get("Repository") or "")
    new_data = dict(data)
    new_data["Identity"] = new_identity
    return new_data


def _process(data, place_parts, place_index, processor):
    if place_index == len(place_parts):
        return processor(data)
    new_data = dict(data)
    new_data[place_parts[place_index]] = _process(data[place_parts[place_index]], place_parts, place_index + 1, processor)
    return new_data


def normalize_image(data, *places):
    if not places:
        return _normalize_image_impl(data)
    for place in places:
        data = _process(data, place.split("."), 0, _normalize_image_impl)
    return data


class FilterModule:
    """Utilities for community.docker tests."""

    def filters(self):
        return {
            'internal__normalize_image': normalize_image,
        }
