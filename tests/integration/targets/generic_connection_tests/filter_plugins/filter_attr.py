# Copyright (c) 2022 Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


def sanitize_host_info(data):
    data = data.copy()
    for key in ('SystemTime', 'NFd', 'NGoroutines', ):
        data.pop(key, None)
    return data


class FilterModule:
    def filters(self):
        return {
            'sanitize_host_info': sanitize_host_info,
        }
