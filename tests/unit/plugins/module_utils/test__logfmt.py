# Copyright (c) 2024, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest

from ansible_collections.community.docker.plugins.module_utils._logfmt import (
    InvalidLogFmt,
    parse_line,
)


SUCCESS_TEST_CASES = [
    (
        'time="2024-02-02T08:14:10+01:00" level=warning msg="a network with name influxNetwork exists but was not'
        ' created for project \\"influxdb\\".\\nSet `external: true` to use an existing network"',
        {},
        {
            'time': '2024-02-02T08:14:10+01:00',
            'level': 'warning',
            'msg': 'a network with name influxNetwork exists but was not created for project "influxdb".\nSet `external: true` to use an existing network',
        },
    ),
    (
        'time="2024-02-02T08:14:10+01:00" level=warning msg="a network with name influxNetwork exists but was not'
        ' created for project \\"influxdb\\".\\nSet `external: true` to use an existing network"',
        {'logrus_mode': True},
        {
            'time': '2024-02-02T08:14:10+01:00',
            'level': 'warning',
            'msg': 'a network with name influxNetwork exists but was not created for project "influxdb".\nSet `external: true` to use an existing network',
        },
    ),
    (
        'foo=bar a=14 baz="hello kitty" cool%story=bro f %^asdf',
        {},
        {
            'foo': 'bar',
            'a': '14',
            'baz': 'hello kitty',
            'cool%story': 'bro',
            'f': None,
            '%^asdf': None,
        },
    ),
    (
        '{"foo":"bar"}',
        {},
        {
            '{': None,
            'foo': None,
            ':': None,
            'bar': None,
            '}': None,
        },
    ),
]


FAILURE_TEST_CASES = [
    (
        'foo=bar a=14 baz="hello kitty" cool%story=bro f %^asdf',
        {'logrus_mode': True},
        'Key must always be followed by "=" in logrus mode',
    ),
    (
        '{}',
        {'logrus_mode': True},
        'Key must always be followed by "=" in logrus mode',
    ),
    (
        '[]',
        {'logrus_mode': True},
        'Key must always be followed by "=" in logrus mode',
    ),
    (
        '{"foo=bar": "baz=bam"}',
        {'logrus_mode': True},
        'Key must always be followed by "=" in logrus mode',
    ),
]


@pytest.mark.parametrize('line, kwargs, result', SUCCESS_TEST_CASES)
def test_parse_line_success(line, kwargs, result):
    res = parse_line(line, **kwargs)
    print(repr(res))
    assert res == result


@pytest.mark.parametrize('line, kwargs, message', FAILURE_TEST_CASES)
def test_parse_line_success(line, kwargs, message):
    with pytest.raises(InvalidLogFmt) as exc:
        parse_line(line, **kwargs)

    print(repr(exc.value.args[0]))
    assert exc.value.args[0] == message
