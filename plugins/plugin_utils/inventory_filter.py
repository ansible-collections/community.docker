# -*- coding: utf-8 -*-

# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.module_utils.common._collections_compat import Mapping
from ansible.module_utils.common.text.converters import to_native
from ansible.module_utils.parsing.convert_bool import boolean
from ansible.module_utils.six import string_types


_ALLOWED_KEYS = ('include', 'exclude')


def parse_filters(filters):
    """
    Parse get_option('filter') and return normalized version to be fed into filter_host().
    """
    result = []
    if filters is None:
        return result
    for index, filter in enumerate(filters):
        if not isinstance(filter, Mapping):
            raise AnsibleError('filter[{index}] must be a dictionary'.format(
                index=index + 1,
            ))
        if len(filter) != 1:
            raise AnsibleError('filter[{index}] must have exactly one key-value pair'.format(
                index=index + 1,
            ))
        key, value = list(filter.items())[0]
        if key not in _ALLOWED_KEYS:
            raise AnsibleError('filter[{index}] must have a {allowed_keys} key, not "{key}"'.format(
                index=index + 1,
                key=key,
                allowed_keys=' or '.join('"{key}"'.format(key=key) for key in _ALLOWED_KEYS),
            ))
        if not isinstance(value, (string_types, bool)):
            raise AnsibleError('filter[{index}].{key} must be a string, not {value_type}'.format(
                index=index + 1,
                key=key,
                value_type=type(value),
            ))
        result.append(filter)
    return result


def filter_host(inventory_plugin, host, host_vars, filters):
    """
    Determine whether a host should be accepted (``True``) or not (``False``).
    """
    vars = {
        'inventory_hostname': host,
    }
    if host_vars:
        vars.update(host_vars)

    def evaluate(condition):
        if isinstance(condition, bool):
            return condition
        conditional = "{%% if %s %%} True {%% else %%} False {%% endif %%}" % condition
        templar = inventory_plugin.templar
        old_vars = templar.available_variables
        try:
            templar.available_variables = vars
            return boolean(templar.template(conditional))
        except Exception as e:
            raise AnsibleParserError("Could not evaluate filter condition {condition!r} for host {host}: {err}".format(
                host=host,
                condition=condition,
                err=to_native(e),
            ))
        finally:
            templar.available_variables = old_vars

    for filter in filters:
        if 'include' in filter:
            expr = filter['include']
            if evaluate(expr):
                return True
        if 'exclude' in filter:
            expr = filter['exclude']
            if evaluate(expr):
                return False

    return True
