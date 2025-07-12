#!/usr/bin/python
#
# Copyright (c) 2023, Felix Fontein <felix@fontein.de>
# Copyright (c) 2025, Maciej Bogusz (@mjbogusz)
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r"""
module: docker_compose_v2_build

short_description: Build a Docker compose project

version_added: 4.7.0

description:
  - Uses Docker Compose to build images for a project.
extends_documentation_fragment:
  - community.docker.compose_v2
  - community.docker.compose_v2.minimum_version
  - community.docker.docker.cli_documentation
  - community.docker.attributes
  - community.docker.attributes.actiongroup_docker

attributes:
  check_mode:
    support: full
  diff_mode:
    support: none
  idempotent:
    support: full

options:
  no_cache:
    description:
      - If set to V(true), will not use cache when building the images.
    type: bool
    default: false
  pull:
    description:
      - If set to V(true), will attempt to pull newer version of the image.
    type: bool
    default: false
  with_dependencies:
    description:
      - If set to V(true), also build services that are declared as dependencies.
      - This only makes sense if O(services) is used.
    type: bool
    default: false
  memory_limit:
    description:
      - Memory limit for the build container, in bytes. Not supported by BuildKit.
    type: int
  services:
    description:
      - Specifies a subset of services to be targeted.
    type: list
    elements: str

author:
  - Maciej Bogusz (@mjbogusz)

seealso:
  - module: community.docker.docker_compose_v2
"""

EXAMPLES = r"""
---
- name: Build images for flask project
  community.docker.docker_compose_v2_build:
    project_src: /path/to/flask
"""

RETURN = r"""
actions:
  description:
    - A list of actions that have been applied.
  returned: success
  type: list
  elements: dict
  contains:
    what:
      description:
        - What kind of resource was changed.
      type: str
      sample: container
      choices:
        - image
        - unknown
    id:
      description:
        - The ID of the resource that was changed.
      type: str
      sample: container
    status:
      description:
        - The status change that happened.
      type: str
      sample: Building
      choices:
        - Building
"""

import traceback

from ansible.module_utils.common.text.converters import to_native

from ansible_collections.community.docker.plugins.module_utils.common_cli import (
    AnsibleModuleDockerClient,
    DockerException,
)

from ansible_collections.community.docker.plugins.module_utils.compose_v2 import (
    BaseComposeManager,
    common_compose_argspec_ex,
)


class BuildManager(BaseComposeManager):
    def __init__(self, client):
        super(BuildManager, self).__init__(client)
        parameters = self.client.module.params

        self.no_cache = parameters['no_cache']
        self.pull = parameters['pull']
        self.with_dependencies = parameters['with_dependencies']
        self.memory_limit = parameters['memory_limit']
        self.services = parameters['services'] or []

    def get_build_cmd(self, dry_run):
        args = self.get_base_args() + ['build']
        if self.no_cache:
            args.append('--no-cache')
        if self.pull:
            args.append('--pull')
        if self.with_dependencies:
            args.append('--with-dependencies')
        if self.memory_limit:
            args.extend(['--memory', str(self.memory_limit)])
        if dry_run:
            args.append('--dry-run')
        args.append('--')
        for service in self.services:
            args.append(service)
        return args

    def run(self):
        result = dict()
        args = self.get_build_cmd(self.check_mode)
        rc, stdout, stderr = self.client.call_cli(*args, cwd=self.project_src)
        events = self.parse_events(stderr, dry_run=self.check_mode, nonzero_rc=rc != 0)
        self.emit_warnings(events)
        self.update_result(result, events, stdout, stderr, ignore_build_events=False)
        self.update_failed(result, events, args, stdout, stderr, rc)
        self.cleanup_result(result)
        return result


def main():
    argument_spec = dict(
        no_cache=dict(type='bool', default=False),
        pull=dict(type='bool', default=False),
        with_dependencies=dict(type='bool', default=False),
        memory_limit=dict(type='int'),
        services=dict(type='list', elements='str'),
    )
    argspec_ex = common_compose_argspec_ex()
    argument_spec.update(argspec_ex.pop('argspec'))

    client = AnsibleModuleDockerClient(
        argument_spec=argument_spec,
        supports_check_mode=True,
        needs_api_version=False,
        **argspec_ex
    )

    try:
        manager = BuildManager(client)
        result = manager.run()
        manager.cleanup()
        client.module.exit_json(**result)
    except DockerException as e:
        client.fail('An unexpected docker error occurred: {0}'.format(to_native(e)), exception=traceback.format_exc())


if __name__ == '__main__':
    main()
