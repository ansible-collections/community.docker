# Copyright 2022 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest

from ansible_collections.community.docker.plugins.module_utils.compose_v2 import (
    Event,
    parse_events,
)

from .compose_v2_test_cases import EVENT_TEST_CASES


EXTRA_TEST_CASES = [
    (
        '2.24.2-manual-build-dry-run',
        '2.24.2',
        True,
        ' DRY-RUN MODE -    build service foobar \n'
        ' DRY-RUN MODE -  ==> ==> writing image dryRun-8843d7f92416211de9ebb963ff4ce28125932878 \n'
        ' DRY-RUN MODE -  ==> ==> naming to my-python \n'
        ' DRY-RUN MODE -  Network compose_default  Creating\n'
        ' DRY-RUN MODE -  Network compose_default  Created\n'
        ' DRY-RUN MODE -  Container compose-foobar-1  Creating\n'
        ' DRY-RUN MODE -  Container compose-foobar-1  Created\n'
        ' DRY-RUN MODE -  Container ompose-foobar-1  Starting\n'
        ' DRY-RUN MODE -  Container ompose-foobar-1  Started\n',
        [
            Event(
                'service',
                'foobar',
                'Building',
                None,
            ),
            Event(
                'network',
                'compose_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'compose_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'compose-foobar-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'compose-foobar-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'ompose-foobar-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'ompose-foobar-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
]

_ALL_TEST_CASES = EVENT_TEST_CASES + EXTRA_TEST_CASES


@pytest.mark.parametrize(
    'test_id, compose_version, dry_run, stderr, events, warnings',
    _ALL_TEST_CASES,
    ids=[tc[0] for tc in _ALL_TEST_CASES],
)
def test_parse_events(test_id, compose_version, dry_run, stderr, events, warnings):
    collected_warnings = []

    def collect_warning(msg):
        collected_warnings.append(msg)

    collected_events = parse_events(stderr, dry_run=dry_run, warn_function=collect_warning)

    assert events == collected_events
    assert warnings == collected_warnings
