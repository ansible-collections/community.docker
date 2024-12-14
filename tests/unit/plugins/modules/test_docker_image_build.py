# Copyright 2024 Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest

from ansible_collections.community.docker.plugins.modules.docker_image_build import _quote_csv


@pytest.mark.parametrize("input, expected", [
    ('', ''),
    (' ', '" "'),
    (',', '","'),
    ('"', '""""'),
    ('\rhello, "hi" !\n', '"\rhello, ""hi"" !\n"'),
])
def test__quote_csv(input, expected):
    assert _quote_csv(input) == expected
