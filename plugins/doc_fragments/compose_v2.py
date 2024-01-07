# -*- coding: utf-8 -*-

# Copyright (c) 2023, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):

    # Docker doc fragment
    DOCUMENTATION = r'''
options:
    project_src:
        description:
          - Path to a directory containing a C(docker-compose.yml) or C(docker-compose.yaml) file.
        type: path
        required: true
    project_name:
        description:
          - Provide a project name. If not provided, the project name is taken from the basename of O(project_src).
        type: str
    env_files:
        description:
          - By default environment files are loaded from a C(.env) file located directly under the O(project_src) directory.
          - O(env_files) can be used to specify the path of one or multiple custom environment files instead.
          - The path is relative to the O(project_src) directory.
        type: list
        elements: path
    profiles:
        description:
          - List of profiles to enable when starting services.
          - Equivalent to C(docker compose --profile).
        type: list
        elements: str
'''
