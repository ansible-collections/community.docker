# Copyright 2016 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import base64

from ansible.module_utils.common.text.converters import to_bytes, to_native, to_text
from ansible.module_utils.six import PY2


def scramble(value, key):
    if len(key) < 1:
        raise ValueError('Key must be at least one byte')
    value = to_bytes(value)
    if PY2:
        k = ord(key[0])
        value = b''.join([chr(k ^ ord(b)) for b in value])
    else:
        k = key[0]
        value = bytes([k ^ b for b in value])
    return '=S=' + to_native(base64.b64encode(value))


def unscramble(value, key):
    if len(key) < 1:
        raise ValueError('Key must be at least one byte')
    if not value.startswith(u'=S='):
        raise ValueError('Value does not start with indicator')
    value = base64.b64decode(value[3:])
    if PY2:
        k = ord(key[0])
        value = b''.join([chr(k ^ ord(b)) for b in value])
    else:
        k = key[0]
        value = bytes([k ^ b for b in value])
    return to_text(value)
