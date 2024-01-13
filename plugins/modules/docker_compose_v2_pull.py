#!/usr/bin/python
#
# Copyright (c) 2023, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''

module: docker_compose_v2_pull

short_description: Pull a Docker compose project

version_added: 3.6.0

description:
  - Uses Docker Compose to pull images for a project.

extends_documentation_fragment:
  - community.docker.compose_v2
  - community.docker.docker.cli_documentation
  - community.docker.attributes
  - community.docker.attributes.actiongroup_docker

attributes:
  check_mode:
    support: full
  diff_mode:
    support: none

options:
  policy:
    description:
      - Whether to pull images before running. This is used when C(docker compose up) is ran.
      - V(always) ensures that the images are always pulled, even when already present on the Docker daemon.
      - V(missing) only pulls them when they are not present on the Docker daemon.
    type: str
    choices:
      - always
      - missing
    default: always

requirements:
  - "Docker CLI with Docker compose plugin 2.18.0 or later"

author:
  - Felix Fontein (@felixfontein)

notes:
  - |-
    The Docker compose CLI plugin has no stable output format (see for example U(https://github.com/docker/compose/issues/10872)),
    and for the main operations also no machine friendly output format. The module tries to accomodate this with various
    version-dependent behavior adjustments and with testing older and newer versions of the Docker compose CLI plugin.

    Currently the module is tested with multiple plugin versions between 2.18.1 and 2.23.3. The exact list of plugin versions
    will change over time. New releases of the Docker compose CLI plugin can break this module at any time.

seealso:
  - module: community.docker.docker_compose
'''

EXAMPLES = '''
# Examples use the django example at https://docs.docker.com/compose/django. Follow it to create the
# flask directory

- name: Run using a project directory
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Tear down existing services
      community.docker.docker_compose_v2:
        project_src: flask
        state: absent

    - name: Create and start services
      community.docker.docker_compose_v2:
        project_src: flask
      register: output

    - name: Show results
      ansible.builtin.debug:
        var: output

    - name: Run `docker-compose up` again
      community.docker.docker_compose_v2:
        project_src: flask
      register: output

    - name: Show results
      ansible.builtin.debug:
        var: output

    - ansible.builtin.assert:
        that: not output.changed

    - name: Stop all services
      community.docker.docker_compose_v2:
        project_src: flask
        state: stopped
      register: output

    - name: Show results
      ansible.builtin.debug:
        var: output

    - name: Verify that web and db services are not running
      ansible.builtin.assert:
        that:
          - "not output.services.web.flask_web_1.state.running"
          - "not output.services.db.flask_db_1.state.running"

    - name: Restart services
      community.docker.docker_compose_v2:
        project_src: flask
        state: restarted
      register: output

    - name: Show results
      ansible.builtin.debug:
        var: output

    - name: Verify that web and db services are running
      ansible.builtin.assert:
        that:
          - "output.services.web.flask_web_1.state.running"
          - "output.services.db.flask_db_1.state.running"
'''

RETURN = '''
containers:
  description:
    - A list of containers associated to the service.
  returned: success
  type: list
  elements: dict
  contains:
    Command:
      description:
        - The container's command.
      type: raw
    CreatedAt:
      description:
        - The timestamp when the container was created.
      type: str
      sample: "2024-01-02 12:20:41 +0100 CET"
    ExitCode:
      description:
        - The container's exit code.
      type: int
    Health:
      description:
        - The container's health check.
      type: raw
    ID:
      description:
        - The container's ID.
      type: str
      sample: "44a7d607219a60b7db0a4817fb3205dce46e91df2cb4b78a6100b6e27b0d3135"
    Image:
      description:
        - The container's image.
      type: str
    Labels:
      description:
        - Labels for this container.
      type: dict
    LocalVolumes:
      description:
        - The local volumes count.
      type: str
    Mounts:
      description:
        - Mounts.
      type: str
    Name:
      description:
        - The container's primary name.
      type: str
    Names:
      description:
        - List of names of the container.
      type: list
      elements: str
    Networks:
      description:
        - List of networks attached to this container.
      type: list
      elements: str
    Ports:
      description:
        - List of port assignments as a string.
      type: str
    Publishers:
      description:
        - List of port assigments.
      type: list
      elements: dict
      contains:
        URL:
          description:
            - Interface the port is bound to.
          type: str
        TargetPort:
          description:
            - The container's port the published port maps to.
          type: int
        PublishedPort:
          description:
            - The port that is published.
          type: int
        Protocol:
          description:
            - The protocol.
          type: str
          choices:
            - tcp
            - udp
    RunningFor:
      description:
        - Amount of time the container runs.
      type: str
    Service:
      description:
        - The name of the service.
      type: str
    Size:
      description:
        - The container's size.
      type: str
      sample: "0B"
    State:
      description:
        - The container's state.
      type: str
      sample: running
    Status:
      description:
        - The container's status.
      type: str
      sample: Up About a minute
images:
  description:
    - A list of images associated to the service.
  returned: success
  type: list
  elements: dict
  contains:
    ID:
      description:
        - The image's ID.
      type: str
      sample: sha256:c8bccc0af9571ec0d006a43acb5a8d08c4ce42b6cc7194dd6eb167976f501ef1
    ContainerName:
      description:
        - Name of the conainer this image is used by.
      type: str
    Repository:
      description:
        - The repository where this image belongs to.
      type: str
    Tag:
      description:
        - The tag of the image.
      type: str
    Size:
      description:
        - The image's size in bytes.
      type: int
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
        - container
        - image
        - network
        - service
        - unknown
        - volume
    id:
      description:
        - The ID of the resource that was changed.
      type: str
      sample: container
    status:
      description:
        - The status change that happened.
      type: str
      sample: Creating
      choices:
        - Starting
        - Exiting
        - Restarting
        - Creating
        - Stopping
        - Killing
        - Removing
        - Recreating
        - Pulling
'''

import traceback

from ansible.module_utils.common.text.converters import to_native

from ansible_collections.community.docker.plugins.module_utils.common_cli import (
    AnsibleModuleDockerClient,
    DockerException,
)

from ansible_collections.community.docker.plugins.module_utils.compose_v2 import (
    BaseComposeManager,
    common_compose_argspec,
)


DOCKER_COMPOSE_MINIMAL_VERSION = '2.18.0'


class PullManager(BaseComposeManager):
    def __init__(self, client):
        super(PullManager, self).__init__(client, min_version=DOCKER_COMPOSE_MINIMAL_VERSION)
        parameters = self.client.module.params

        self.policy = parameters['policy']

    def get_pull_cmd(self, dry_run, no_start=False):
        args = self.get_base_args() + ['pull', '--policy', self.policy]
        if dry_run:
            args.append('--dry-run')
        args.append('--')
        return args

    def run(self):
        result = dict()
        args = self.get_pull_cmd(self.check_mode)
        rc, stdout, stderr = self.client.call_cli(*args, cwd=self.project_src)
        events = self.parse_events(stderr, dry_run=self.check_mode)
        self.emit_warnings(events)
        self.update_result(result, events, stdout, stderr)
        self.update_failed(result, events, args, stdout, stderr, rc)
        self.cleanup_result(result)
        return result


def main():
    argument_spec = dict(
        policy=dict(type='str', choices=['always', 'missing'], default='always'),
    )
    argument_spec.update(common_compose_argspec())

    client = AnsibleModuleDockerClient(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    try:
        result = PullManager(client).run()
        client.module.exit_json(**result)
    except DockerException as e:
        client.fail('An unexpected docker error occurred: {0}'.format(to_native(e)), exception=traceback.format_exc())


if __name__ == '__main__':
    main()
