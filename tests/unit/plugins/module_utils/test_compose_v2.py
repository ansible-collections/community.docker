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
    (
        # https://github.com/ansible-collections/community.docker/issues/785
        '2.20.0-manual-pull',
        '2.20.0',
        False,
        '4f4fb700ef54 Waiting\n'
        '238022553356 Downloading     541B/541B\n'
        '972e292d3a60 Downloading    106kB/10.43MB\n'
        'f2543dc9f0a9 Downloading  25.36kB/2.425MB\n'
        '972e292d3a60 Downloading  5.925MB/10.43MB\n'
        'f2543dc9f0a9 Downloading  2.219MB/2.425MB\n'
        'f2543dc9f0a9 Extracting  32.77kB/2.425MB\n'
        '4f4fb700ef54 Downloading      32B/32B\n'
        'f2543dc9f0a9 Extracting  2.425MB/2.425MB\n'
        '972e292d3a60 Extracting  131.1kB/10.43MB\n'
        '972e292d3a60 Extracting  10.43MB/10.43MB\n'
        '238022553356 Extracting     541B/541B\n'
        '4f4fb700ef54 Extracting      32B/32B\n',
        [
            Event(
                'image-layer',
                '4f4fb700ef54',
                'Waiting',
                None,
            ),
            Event(
                'image-layer',
                '238022553356',
                'Downloading',
                None,
            ),
            Event(
                'image-layer',
                '972e292d3a60',
                'Downloading',
                None,
            ),
            Event(
                'image-layer',
                'f2543dc9f0a9',
                'Downloading',
                None,
            ),
            Event(
                'image-layer',
                '972e292d3a60',
                'Downloading',
                None,
            ),
            Event(
                'image-layer',
                'f2543dc9f0a9',
                'Downloading',
                None,
            ),
            Event(
                'image-layer',
                'f2543dc9f0a9',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '4f4fb700ef54',
                'Downloading',
                None,
            ),
            Event(
                'image-layer',
                'f2543dc9f0a9',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '972e292d3a60',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '972e292d3a60',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '238022553356',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '4f4fb700ef54',
                'Extracting',
                None,
            ),
        ],
        [],
    ),
    (
        # https://github.com/ansible-collections/community.docker/issues/787
        '2.20.3-logrus-warn',
        '2.20.3',
        False,
        'time="2024-02-02T08:14:10+01:00" level=warning msg="a network with name influxNetwork exists but was not'
        ' created for project \\"influxdb\\".\\nSet `external: true` to use an existing network"\n',
        [],
        [
            'a network with name influxNetwork exists but was not created for project "influxdb".\nSet `external: true` to use an existing network',
        ],
    ),
    (
        # https://github.com/ansible-collections/community.docker/issues/807
        '2.20.3-image-warning-error',
        '2.20.3',
        False,
        " dummy3 Warning \n"
        " dummy2 Warning \n"
        " dummy Error \n"
        " dummy4 Warning Foo bar \n"
        " dummy5 Error Bar baz bam \n",
        [
            Event(
                'unknown',
                'dummy',
                'Error',
                None,
            ),
            Event(
                'unknown',
                'dummy5',
                'Error',
                'Bar baz bam',
            ),
        ],
        [
            'Unspecified warning for dummy3',
            'Unspecified warning for dummy2',
            'dummy4: Foo bar',
        ],
    ),
    (
        # https://github.com/ansible-collections/community.docker/issues/911
        '2.28.1-image-pull-skipped',
        '2.28.1',
        False,
        " bash_1 Skipped \n"
        " bash_2 Pulling \n"
        " bash_2 Pulled \n",
        [
            Event(
                'unknown',
                'bash_1',
                'Skipped',
                None,
            ),
            Event(
                'service',
                'bash_2',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'bash_2',
                'Pulled',
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

    print(collected_events)
    print(collected_warnings)

    assert collected_events == events
    assert collected_warnings == warnings
