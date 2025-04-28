# Copyright 2025 Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest

from ansible_collections.community.docker.plugins.modules.docker_container_copy_into import parse_modern, parse_octal_string_only


@pytest.mark.parametrize("input, expected", [
    ('0777', 0o777),
    ('777', 0o777),
    ('0o777', 0o777),
    ('0755', 0o755),
    ('755', 0o755),
    ('0o755', 0o755),
    ('0644', 0o644),
    ('644', 0o644),
    ('0o644', 0o644),
    (' 0644 ', 0o644),
    (' 644 ', 0o644),
    (' 0o644 ', 0o644),
    ('-1', -1),
])
def test_parse_string(input, expected):
    assert parse_modern(input) == expected
    assert parse_octal_string_only(input) == expected


@pytest.mark.parametrize("input", [
    0o777,
    0o755,
    0o644,
    12345,
    123456789012345678901234567890123456789012345678901234567890,
])
def test_parse_int(input):
    assert parse_modern(input) == input
    with pytest.raises(TypeError, match="^must be an octal string, got {value}L?$".format(value=input)):
        parse_octal_string_only(input)


@pytest.mark.parametrize("input", [
    1.0,
    755.5,
    [],
    {},
])
def test_parse_bad_type(input):
    with pytest.raises(TypeError, match="^must be an octal string or an integer, got "):
        parse_modern(input)
    with pytest.raises(TypeError, match="^must be an octal string, got "):
        parse_octal_string_only(input)


@pytest.mark.parametrize("input", [
    "foo",
    "8",
    "9",
])
def test_parse_bad_value(input):
    with pytest.raises(ValueError):
        parse_modern(input)
    with pytest.raises(ValueError):
        parse_octal_string_only(input)
