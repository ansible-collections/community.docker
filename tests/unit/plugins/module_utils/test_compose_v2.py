# Copyright 2022 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest

from ansible_collections.community.docker.plugins.module_utils.compose_v2 import (
    parse_events,
)

from .compose_v2_test_cases import EVENT_TEST_CASES


@pytest.mark.parametrize(
    'test_id, compose_version, dry_run, stderr, events, warnings',
    EVENT_TEST_CASES,
    ids=[tc[0] for tc in EVENT_TEST_CASES],
)
def test_parse_events(test_id, compose_version, dry_run, stderr, events, warnings):
    collected_warnings = []

    def collect_warning(msg):
        collected_warnings.append(msg)

    collected_events = parse_events(stderr, dry_run=dry_run, warn_function=collect_warning)

    assert events == collected_events
    assert warnings == collected_warnings
