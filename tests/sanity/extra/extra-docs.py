#!/usr/bin/env python
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Check extra collection docs with antsibull-lint."""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import sys
import subprocess


def main():
    """Main entry point."""
    if not os.path.isdir(os.path.join('docs', 'docsite')):
        return
    p = subprocess.run(['antsibull-lint', 'collection-docs', '.'], check=False)
    if p.check_call not in (0, 3):
        print('{0}:0:0: unexpected return code {1}'.format(sys.argv[0], p.check_call))


if __name__ == '__main__':
    main()
