# Copyright (c) 2020, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type


def _normalize_ipaddr(ipaddr):
    # Import when needed, to allow installation of that module in the test setup
    import ipaddress
    return ipaddress.ip_address(ipaddr).compressed


class FilterModule(object):
    """ IP address and network manipulation filters """

    def filters(self):
        return {
            'normalize_ipaddr': _normalize_ipaddr,
        }
