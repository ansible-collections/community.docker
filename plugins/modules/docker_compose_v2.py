#!/usr/bin/python
#
# Copyright (c) 2023, Felix Fontein <felix@fontein.de>
# Copyright (c) 2023, Léo El Amri (@lel-amri)
# Copyright 2016 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''

module: docker_compose_v2

short_description: Manage multi-container Docker applications with Docker Compose CLI plugin

version_added: 3.6.0

description:
  - Uses Docker Compose to start or shutdown services.

extends_documentation_fragment:
  - community.docker.docker.cli_documentation
  - community.docker.attributes
  - community.docker.attributes.actiongroup_docker

attributes:
  check_mode:
    support: full
  diff_mode:
    support: none

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
  state:
    description:
      - Desired state of the project.
      - V(present) is equivalent to running C(docker compose up).
      - V(stopped) is equivalent to running C(docker compose stop).
      - V(absent) is equivalent to running C(docker compose down).
      - V(restarted) is equivalent to running C(docker compose restart).
    type: str
    default: present
    choices:
      - absent
      - stopped
      - restarted
      - present
  pull:
    description:
      - Whether to pull images before running. This is used when C(docker compose up) is ran.
      - V(always) ensures that the images are always pulled, even when already present on the Docker daemon.
      - V(missing) only pulls them when they are not present on the Docker daemon.
      - V(never) never pulls images. If they are not present, the module will fail when trying to create the containers that need them.
      - V(policy) use the C(pull_policy) defined for the service to figure out what to do.
    type: str
    choices:
      - always
      - missing
      - never
      - policy
    default: policy
  dependencies:
    description:
      - When O(state) is V(present) or V(restarted), specify whether or not to include linked services.
    type: bool
    default: true
  recreate:
    description:
      - By default containers will be recreated when their configuration differs from the service definition.
      - Setting to V(never) ignores configuration differences and leaves existing containers unchanged.
      - Setting to V(always) forces recreation of all existing containers.
    type: str
    default: auto
    choices:
      - always
      - never
      - auto
  remove_images:
    description:
      - Use with O(state=absent) to remove all images or only local images.
    type: str
    choices:
      - all
      - local
  remove_volumes:
    description:
      - Use with O(state=absent) to remove data volumes.
    type: bool
    default: false
  remove_orphans:
    description:
      - Remove containers for services not defined in the Compose file.
    type: bool
    default: false
  timeout:
    description:
      - Timeout in seconds for container shutdown when attached or when containers are already running.
    type: int

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

import os
import traceback

from ansible.module_utils.common.text.converters import to_native

from ansible_collections.community.docker.plugins.module_utils.common_cli import (
    AnsibleModuleDockerClient,
    DockerException,
)

from ansible_collections.community.docker.plugins.module_utils.compose_v2 import (
    parse_events,
    has_changes,
    extract_actions,
    emit_warnings,
    is_failed,
    update_failed,
)

from ansible_collections.community.docker.plugins.module_utils.util import DockerBaseClass
from ansible_collections.community.docker.plugins.module_utils.version import LooseVersion


DOCKER_COMPOSE_MINIMAL_VERSION = '2.18.0'
DOCKER_COMPOSE_FILES = 'docker-compose.yml', 'docker-compose.yaml'


class ContainerManager(DockerBaseClass):
    def __init__(self, client):
        super(ContainerManager, self).__init__()
        self.client = client
        self.check_mode = self.client.check_mode
        parameters = self.client.module.params

        self.project_src = parameters['project_src']
        self.project_name = parameters['project_name']
        self.env_files = parameters['env_files']
        self.profiles = parameters['profiles']
        self.state = parameters['state']
        self.dependencies = parameters['dependencies']
        self.pull = parameters['pull']
        self.recreate = parameters['recreate']
        self.remove_images = parameters['remove_images']
        self.remove_volumes = parameters['remove_volumes']
        self.remove_orphans = parameters['remove_orphans']
        self.timeout = parameters['timeout']

        compose = self.client.get_client_plugin_info('compose')
        if compose is None:
            self.client.fail('Docker CLI {0} does not have the compose plugin installed'.format(self.client.get_cli()))
        compose_version = compose['Version'].lstrip('v')
        self.compose_version = LooseVersion(compose_version)
        if self.compose_version < LooseVersion(DOCKER_COMPOSE_MINIMAL_VERSION):
            self.client.fail('Docker CLI {cli} has the compose plugin with version {version}; need version {min_version} or later'.format(
                cli=self.client.get_cli(),
                version=compose_version,
                min_version=DOCKER_COMPOSE_MINIMAL_VERSION,
            ))

        if not os.path.isdir(self.project_src):
            self.client.fail('"{0}" is not a directory'.format(self.project_src))

        if all(not os.path.isfile(os.path.join(self.project_src, f)) for f in DOCKER_COMPOSE_FILES):
            self.client.fail('"{0}" does not contain {1}'.format(self.project_src, ' or '.join(DOCKER_COMPOSE_FILES)))

    def get_base_args(self):
        args = ['compose', '--ansi', 'never']
        if self.compose_version >= LooseVersion('2.19.0'):
            # https://github.com/docker/compose/pull/10690
            args.extend(['--progress', 'plain'])
        args.extend(['--project-directory', self.project_src])
        if self.project_name:
            args.extend(['--project-name', self.project_name])
        for env_file in self.env_files or []:
            args.extend(['--env-file', env_file])
        for profile in self.profiles or []:
            args.extend(['--profile', profile])
        return args

    def list_containers_raw(self):
        args = self.get_base_args() + ['ps', '--format', 'json', '--all']
        if self.compose_version >= LooseVersion('2.23.0'):
            # https://github.com/docker/compose/pull/11038
            args.append('--no-trunc')
        kwargs = dict(cwd=self.project_src, check_rc=True)
        if self.compose_version >= LooseVersion('2.21.0'):
            # Breaking change in 2.21.0: https://github.com/docker/compose/pull/10918
            dummy, containers, dummy = self.client.call_cli_json_stream(*args, **kwargs)
        else:
            dummy, containers, dummy = self.client.call_cli_json(*args, **kwargs)
        return containers

    def list_containers(self):
        result = []
        for container in self.list_containers_raw():
            labels = {}
            if container.get('Labels'):
                for part in container['Labels'].split(','):
                    label_value = part.split('=', 1)
                    labels[label_value[0]] = label_value[1] if len(label_value) > 1 else ''
            container['Labels'] = labels
            container['Names'] = container.get('Names', container['Name']).split(',')
            container['Networks'] = container.get('Networks', '').split(',')
            container['Publishers'] = container.get('Publishers') or []
            result.append(container)
        return result

    def list_images(self):
        args = self.get_base_args() + ['images', '--format', 'json']
        kwargs = dict(cwd=self.project_src, check_rc=True)
        dummy, images, dummy = self.client.call_cli_json(*args, **kwargs)
        return images

    def run(self):
        if self.state == 'present':
            result = self.cmd_up()
        elif self.state == 'stopped':
            result = self.cmd_stop()
        elif self.state == 'restarted':
            result = self.cmd_restart()
        elif self.state == 'absent':
            result = self.cmd_down()

        result['containers'] = self.list_containers()
        result['images'] = self.list_images()
        if not result.get('failed'):
            # Only return stdout and stderr if it's not empty
            for res in ('stdout', 'stderr'):
                if result.get(res) == '':
                    result.pop(res)
        return result

    def parse_events(self, stderr, dry_run=False):
        return parse_events(stderr, dry_run=dry_run, warn_function=self.client.warn)

    def emit_warnings(self, events):
        emit_warnings(events, warn_function=self.client.warn)

    def update_failed(self, result, events, args, stdout, stderr, rc):
        return update_failed(
            result,
            events,
            args=args,
            stdout=stdout,
            stderr=stderr,
            rc=rc,
            cli=self.client.get_cli(),
        )

    def get_up_cmd(self, dry_run, no_start=False):
        args = self.get_base_args() + ['up', '--detach', '--no-color', '--quiet-pull']
        if self.pull != 'policy':
            args.extend(['--pull', self.pull])
        if self.remove_orphans:
            args.append('--remove-orphans')
        if self.recreate == 'always':
            args.append('--force-recreate')
        if self.recreate == 'never':
            args.append('--no-recreate')
        if not self.dependencies:
            args.append('--no-deps')
        if self.timeout is not None:
            args.extend(['--timeout', '%d' % self.timeout])
        if no_start:
            args.append('--no-start')
        if dry_run:
            args.append('--dry-run')
        args.append('--')
        return args

    def cmd_up(self):
        result = dict()
        args = self.get_up_cmd(self.check_mode)
        rc, stdout, stderr = self.client.call_cli(*args, cwd=self.project_src)
        events = self.parse_events(stderr, dry_run=self.check_mode)
        self.emit_warnings(events)
        result['changed'] = has_changes(events)
        result['actions'] = extract_actions(events)
        result['stdout'] = to_native(stdout)
        result['stderr'] = to_native(stderr)
        self.update_failed(result, events, args, stdout, stderr, rc)
        return result

    def get_stop_cmd(self, dry_run):
        args = self.get_base_args() + ['stop']
        if self.timeout is not None:
            args.extend(['--timeout', '%d' % self.timeout])
        if dry_run:
            args.append('--dry-run')
        args.append('--')
        return args

    def _are_containers_stopped(self):
        for container in self.list_containers_raw():
            if container['State'] not in ('created', 'exited', 'stopped', 'killed'):
                return False
        return True

    @staticmethod
    def _combine_output(*outputs):
        return b'\n'.join(out for out in outputs if out)

    def cmd_stop(self):
        # Since 'docker compose stop' **always** claims its stopping containers, even if they are already
        # stopped, we have to do this a bit more complicated.

        result = dict()
        # Make sure all containers are created
        args_1 = self.get_up_cmd(self.check_mode, no_start=True)
        rc_1, stdout_1, stderr_1 = self.client.call_cli(*args_1, cwd=self.project_src)
        events_1 = self.parse_events(stderr_1, dry_run=self.check_mode)
        self.emit_warnings(events_1)
        is_failed_1 = is_failed(events_1, rc_1)
        if not is_failed_1 and not self._are_containers_stopped():
            # Make sure all containers are stopped
            args_2 = self.get_stop_cmd(self.check_mode)
            rc_2, stdout_2, stderr_2 = self.client.call_cli(*args_2, cwd=self.project_src)
            events_2 = self.parse_events(stderr_2, dry_run=self.check_mode)
            self.emit_warnings(events_2)
        else:
            args_2 = []
            rc_2, stdout_2, stderr_2 = 0, b'', b''
            events_2 = []
        # Compose result
        result['changed'] = has_changes(events_1) or has_changes(events_2)
        result['actions'] = extract_actions(events_1) + extract_actions(events_2)
        result['stdout'] = to_native(self._combine_output(stdout_1, stdout_2))
        result['stderr'] = to_native(self._combine_output(stderr_1, stderr_2))
        self.update_failed(
            result,
            events_1 + events_2,
            args_1 if is_failed_1 else args_2,
            stdout_1 if is_failed_1 else stdout_2,
            stderr_1 if is_failed_1 else stderr_2,
            rc_1 if is_failed_1 else rc_2,
        )
        return result

    def get_restart_cmd(self, dry_run):
        args = self.get_base_args() + ['restart']
        if not self.dependencies:
            args.append('--no-deps')
        if self.timeout is not None:
            args.extend(['--timeout', '%d' % self.timeout])
        if dry_run:
            args.append('--dry-run')
        args.append('--')
        return args

    def cmd_restart(self):
        result = dict()
        args = self.get_restart_cmd(self.check_mode)
        rc, stdout, stderr = self.client.call_cli(*args, cwd=self.project_src)
        events = self.parse_events(stderr, dry_run=self.check_mode)
        self.emit_warnings(events)
        result['changed'] = has_changes(events)
        result['actions'] = extract_actions(events)
        result['stdout'] = to_native(stdout)
        result['stderr'] = to_native(stderr)
        self.update_failed(result, events, args, stdout, stderr, rc)
        return result

    def get_down_cmd(self, dry_run):
        args = self.get_base_args() + ['down']
        if self.remove_orphans:
            args.append('--remove-orphans')
        if self.remove_images:
            args.extend(['--rmi', self.remove_images])
        if self.remove_volumes:
            args.append('--volumes')
        if self.timeout is not None:
            args.extend(['--timeout', '%d' % self.timeout])
        if dry_run:
            args.append('--dry-run')
        args.append('--')
        return args

    def cmd_down(self):
        result = dict()
        args = self.get_down_cmd(self.check_mode)
        rc, stdout, stderr = self.client.call_cli(*args, cwd=self.project_src)
        events = self.parse_events(stderr, dry_run=self.check_mode)
        self.emit_warnings(events)
        result['changed'] = has_changes(events)
        result['actions'] = extract_actions(events)
        result['stdout'] = to_native(stdout)
        result['stderr'] = to_native(stderr)
        self.update_failed(result, events, args, stdout, stderr, rc)
        return result


def main():
    argument_spec = dict(
        project_src=dict(type='path', required=True),
        project_name=dict(type='str'),
        env_files=dict(type='list', elements='path'),
        profiles=dict(type='list', elements='str'),
        state=dict(type='str', default='present', choices=['absent', 'present', 'stopped', 'restarted']),
        dependencies=dict(type='bool', default=True),
        pull=dict(type='str', choices=['always', 'missing', 'never', 'policy'], default='policy'),
        recreate=dict(type='str', default='auto', choices=['always', 'never', 'auto']),
        remove_images=dict(type='str', choices=['all', 'local']),
        remove_volumes=dict(type='bool', default=False),
        remove_orphans=dict(type='bool', default=False),
        timeout=dict(type='int'),
    )

    client = AnsibleModuleDockerClient(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    try:
        result = ContainerManager(client).run()
        client.module.exit_json(**result)
    except DockerException as e:
        client.fail('An unexpected docker error occurred: {0}'.format(to_native(e)), exception=traceback.format_exc())


if __name__ == '__main__':
    main()
