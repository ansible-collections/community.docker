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
          - Path to a directory containing a Compose file
            (C(compose.yml), C(compose.yaml), C(docker-compose.yml), or C(docker-compose.yaml)).
          - If O(files) is provided, will look for these files in this directory instead.
        type: path
        required: true
    project_name:
        description:
          - Provide a project name. If not provided, the project name is taken from the basename of O(project_src).
        type: str
    files:
        description:
          - List of Compose file names relative to O(project_src) to be used instead of the main Compose file
            (C(compose.yml), C(compose.yaml), C(docker-compose.yml), or C(docker-compose.yaml)).
          - Files are loaded and merged in the order given.
        type: list
        elements: path
        version_added: 3.7.0
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
notes:
  - |-
    The Docker compose CLI plugin has no stable output format (see for example U(https://github.com/docker/compose/issues/10872)),
    and for the main operations also no machine friendly output format. The module tries to accomodate this with various
    version-dependent behavior adjustments and with testing older and newer versions of the Docker compose CLI plugin.

    Currently the module is tested with multiple plugin versions between 2.18.1 and 2.23.3. The exact list of plugin versions
    will change over time. New releases of the Docker compose CLI plugin can break this module at any time.
'''

    # The following needs to be kept in sync with the compose_v2 module utils
    MINIMUM_VERSION = r'''
options: {}
requirements:
  - "Docker CLI with Docker compose plugin 2.18.0 or later"
'''
