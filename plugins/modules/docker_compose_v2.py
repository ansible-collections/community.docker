#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright Léo El Amri
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: docker_compose_v2

short_description: Manage multi-container Docker applications with Docker Compose.

description:
  - Uses Docker Compose to start and shutdown services.
  - Swarm mode is not supported (thus secrets and configs are not supported).
  - Configuration can be read from a Compose file or inline using the I(definition) option.
  - See the examples for more details.

attributes:
  check_mode:
    support: none
    description: Check mode is not supported because the `docker-compose` CLI doesn't allow it.
  diff_mode:
    support: none
    description: Diff mode is not supported.

options:
  docker_host:
    description:
      - The URL or Unix socket path used to connect to the Docker API. To connect to a remote host, provide the
        TCP connection string. For example, C(tcp://192.0.2.23:2376). If TLS is used to encrypt the connection,
        the module will automatically replace C(tcp) in the connection URL with C(https).
      - If the value is not specified in the task, the value of environment variable C(DOCKER_HOST) will be used
        instead. If the environment variable is not set, the default value will be used.
    type: str
    default: unix://var/run/docker.sock
    aliases: [ docker_url ]
  project_src:
    description:
      - Path to the root directory of the Compose project.
      - Required when I(definition) is provided.
    type: path
  project_name:
    description:
      - Provide a project name.
      - Equivalent to C(docker-compose --project-name).
    type: str
  env_file:
    description:
      - By default environment files are loaded from a C(.env) file located directly under the I(project_src) directory.
      - I(env_file) can be used to specify the path of a custom environment file instead.
      - The path is relative to the I(project_src) directory.
      - Equivalent to C(docker-compose --env-file).
    type: path
  files:
    description:
      - List of Compose files.
      - Files are passed to docker-compose in the order given.
      - Equivalent to C(docker-compose -f).
    type: list
    elements: path
  profiles:
    description:
      - List of profiles to enable when starting services.
      - Equivalent to C(docker-compose --profile).
    type: list
    elements: str
  state:
    description:
      - Desired state of the project.
      - Specifying C(pulled) is the same as running C(docker-compose pull).
      - Specifying C(built) is the same as running C(docker-compose build).
      - Specifying C(stopped) is the same as running C(docker-compose stop).
      - Specifying C(present) is the same as running C(docker-compose up).
      - Specifying C(restarted) is the same as running C(docker-compose restart).
      - Specifying C(absent) is the same as running C(docker-compose down).
    type: str
    default: present
    choices:
      - absent
      - built
      - present
      - pulled
      - restarted
      - stopped
  services:
    description:
      - When I(state) is C(present) run C(docker-compose up) resp. C(docker-compose stop) (with I(stopped)) resp. C(docker-compose restart) (with I(restarted))
        on a subset of services.
      - If empty, which is the default, the operation will be performed on all services defined in the Compose file (or inline I(definition)).
    type: list
    elements: str
  dependencies:
    description:
      - When I(state) is C(present) specify whether or not to include linked services.
      - When false, equivalent to C(docker-compose up --no-deps).
      - When I(state) is C(pull) specify whether or not to also pull for linked services.
      - When true, equivalent to C(docker-compose pull --include-deps).
    type: bool
    default: true
  definition:
    description:
      - Compose file describing one or more services, networks and volumes.
      - Mutually exclusive with I(files).
    type: dict
  recreate:
    description:
      - By default containers will be recreated when their configuration differs from the service definition.
      - Setting to C(never) ignores configuration differences and leaves existing containers unchanged.
      - Setting to C(always) forces recreation of all existing containers.
      - When set to C(never), equivalent to C(docker-compose up --no-recreate).
      - When set to C(always), equivalent to C(docker-compose up --force-recreate).
    type: str
    default: smart
    choices:
      - always
      - never
      - smart
  build:
    description:
      - Use with I(state) C(present) to always build images prior to starting the application.
      - Equivalent to C(docker-compose up --build).
      - Images will only be rebuilt if Docker detects a change in the Dockerfile or build directory contents.
      - If an existing image is replaced, services using the image will be recreated unless I(recreate) is C(never).
    type: bool
    default: false
  pull:
    description:
      - Use with I(state) C(present) to always pull images prior to starting the application.
      - Equivalent to C(docker-compose up --pull always).
      - When a new image is pulled, services using the image will be recreated unless I(recreate) is C(never).
    type: bool
    default: false
  nocache:
    description:
      - Use with the I(build) option to ignore the cache during the image build process.
      - Equivalent to C(docker-compose build --no-cache).
    type: bool
    default: false
  remove_images:
    description:
      - Use with I(state) C(absent) to remove all images or only local images.
      - Equivalent to C(docker-compose down --rmi all|local).
    type: str
    choices:
      - all
      - local
  remove_volumes:
    description:
      - Use with I(state) C(absent) to remove data volumes.
      - Equivalent to C(docker-compose down --volumes).
    type: bool
    default: false
  remove_orphans:
    description:
      - Remove containers for services not defined in the Compose file.
      - Equivalent to C(docker-compose up --remove-orphans) or C(docker-compose down --remove-orphans).
    type: bool
    default: false
  timeout:
    description:
      - Timeout in seconds for container shutdown when attached or when containers are already running.
      - By default C(compose) will use a C(10s) timeout unless C(default_grace_period) is defined for a
        particular service in the I(project_src).
    type: int
    default: null

requirements:
  - "docker-compose >= 2.0.0"

author:
  - Léo El Amri (@lel-amri)
'''

EXAMPLES = '''
# Examples use the django example at https://docs.docker.com/compose/django. Follow it to create the
# flask directory

- name: Run using a project directory
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Tear down existing services
      community.docker.docker_compose:
        project_src: flask
        state: absent

    - name: Create and start services
      community.docker.docker_compose:
        project_src: flask
      register: output

    - ansible.builtin.debug:
        var: output

    - name: Run `docker-compose up` again
      community.docker.docker_compose:
        project_src: flask
        build: false
      register: output

    - ansible.builtin.debug:
        var: output

    - ansible.builtin.assert:
        that: not output.changed

    - name: Stop all services
      community.docker.docker_compose:
        project_src: flask
        build: false
        stopped: true
      register: output

    - ansible.builtin.debug:
        var: output

    - ansible.builtin.assert:
        that:
          - "'stopped' in containers['flask_web_1'] | default([])"
          - "'stopped' in containers['flask_db_1'] | default([])"

    - name: Restart services
      community.docker.docker_compose:
        project_src: flask
        build: false
        restarted: true
      register: output

    - ansible.builtin.debug:
        var: output

    - ansible.builtin.assert:
        that:
          - "'started' in containers['flask_web_1'] | default([])"
          - "'started' in containers['flask_db_1'] | default([])"

- name: Run with inline Compose file version 2
  # https://docs.docker.com/compose/compose-file/compose-file-v2/
  hosts: localhost
  gather_facts: false
  tasks:
    - community.docker.docker_compose:
        project_src: flask
        state: absent

    - community.docker.docker_compose:
        project_name: flask
        definition:
          version: '2'
          services:
            db:
              image: postgres
            web:
              build: "{{ playbook_dir }}/flask"
              command: "python manage.py runserver 0.0.0.0:8000"
              volumes:
                - "{{ playbook_dir }}/flask:/code"
              ports:
                - "8000:8000"
              depends_on:
                - db
      register: output

    - ansible.builtin.debug:
        var: output

    - ansible.builtin.assert:
        that:
          - "'started' in containers['flask_web_1'] | default([])"
          - "'started' in containers['flask_db_1'] | default([])"

- name: Run with inline Compose file version 1
  # https://docs.docker.com/compose/compose-file/compose-file-v1/
  hosts: localhost
  gather_facts: false
  tasks:
    - community.docker.docker_compose:
        project_src: flask
        state: absent

    - community.docker.docker_compose:
        project_name: flask
        definition:
            db:
              image: postgres
            web:
              build: "{{ playbook_dir }}/flask"
              command: "python manage.py runserver 0.0.0.0:8000"
              volumes:
                - "{{ playbook_dir }}/flask:/code"
              ports:
                - "8000:8000"
              links:
                - db
      register: output

    - ansible.builtin.debug:
        var: output

    - ansible.builtin.assert:
        that:
          - "'started' in containers['flask_web_1'] | default([])"
          - "'started' in containers['flask_db_1'] | default([])"
'''

RETURN = '''
stdout:
  description:
    - The stdout from docker-compose.
  returned: always, unless when C(docker-compose) was not given the chance to run
  type: str
stderr:
  description:
    - The stderr from docker-compose.
  returned: always, unless when C(docker-compose) was not given the chance to run
  type: str
containers:
  description:
    - A dictionary mapping the various status of containers during C(docker-compose) operation.
  returned: always, unless when C(docker-compose) was not given the chance to run
  type: complex
  contains:
    container_name:
      description: Name of the container.
      returned: always, unless when C(docker-compose) was not given the chance to run
      type: list
      elements: str
      example: ["stopped", "removed"]
volumes:
  description:
    - A dictionary mapping the various status of volumes during C(docker-compose) operation.
  returned: always, unless when C(docker-compose) was not given the chance to run
  type: complex
  contains:
    volume_name:
      description: Name of the volume.
      returned: always, unless when C(docker-compose) was not given the chance to run
      type: list
      elements: str
      example: ["created"]
images:
  description:
    - A dictionary mapping the various status of volumes during C(docker-compose) operation.
  returned: always, unless when C(docker-compose) was not given the chance to run
  type: complex
  contains:
    image_name:
      description: Name of the image.
      returned: always, unless when C(docker-compose) was not given the chance to run
      type: list
      elements: str
      example: ["removed"]
networks:
  description:
    - A dictionary mapping the various status of networks during C(docker-compose) operation.
  returned: always, unless when C(docker-compose) was not given the chance to run
  type: complex
  contains:
    image_name:
      description: Name of the image.
      returned: always, unless when C(docker-compose) was not given the chance to run
      type: list
      elements: str
      example: ["created"]
'''


import sys
if sys.version_info[0] == 3 and sys.version_info[1] >= 5:
    from typing import List, Optional, Tuple, Union, FrozenSet, Dict, Type, TYPE_CHECKING, Any
    if sys.version_info[1] >= 8:
        from typing import Literal, Final
    else:
        try:
            from typing_extensions import Literal, Final
        except ImportError:
            pass
    # `Text` can be removed and replaced by `str` once Python 2 support is dropped
    if sys.version_info[1] < 11:
        # pylint: disable-next=deprecated-class
        from typing import Text
    else:
        Text = str
else:
    TYPE_CHECKING = False
import re
from collections import defaultdict, namedtuple
from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.community.docker.plugins.module_utils.util import (
    DOCKER_COMMON_ARGS,
)
from ansible.module_utils.common.yaml import HAS_YAML, yaml_dump


STATUS_DONE = frozenset({
    'Started',
    'Healthy',
    'Exited',
    'Restarted',
    'Running',
    'Created',
    'Stopped',
    'Killed',
    'Removed',
    # An extra, specific to containers
    'Recreated',
})  # type: Final[FrozenSet[Text]]


STATUS_WORKING = frozenset({
    'Creating',
    'Starting',
    'Waiting',
    'Restarting',
    'Stopping',
    'Killing',
    'Removing',
    # An extra, specific to containers
    'Recreate',
})  # type: Final[FrozenSet[Text]]


STATUS_ERROR = frozenset({
    'Error',
})  # type: Final[FrozenSet[Text]]


STATUS_THAT_CAUSE_A_CHANGE = frozenset({
    'Started',
    'Exited',
    'Restarted',
    'Created',
    'Stopped',
    'Killed',
    'Removed',
})  # type: Final[FrozenSet[Text]]


STATUS_DOCKERCOMPOSE_TO_COMMUNITYDOCKER = {
    'Started': 'started',
    'Healthy': 'healthy',
    'Exited': 'exited',
    'Restarted': 'restarted',
    'Running': 'running',
    'Created': 'created',
    'Stopped': 'stopped',
    'Killed': 'killed',
    'Removed': 'removed',
    'Recreated': 'recreated',
}  # type: Final[Dict[Text, Text]]


class ResourceType(object):
    NETWORK = object()
    IMAGE = object()
    VOLUME = object()
    CONTAINER = object()

    @classmethod
    def from_docker_compose_event(cls, resource_type):
        # type: (Type[ResourceType], Text) -> Any
        return {
            "Network": cls.NETWORK,
            "Image": cls.IMAGE,
            "Volume": cls.VOLUME,
            "Container": cls.CONTAINER,
        }[resource_type]


if TYPE_CHECKING:
    EVENT = Tuple[Any, Text, Text]

ResourceEvent = namedtuple(
    'ResourceEvent',
    ['resource_type', 'resource_id', 'status']
)


_re_resource_event = re.compile(
    r'^'
    r'(?P<resource_type>Network|Image|Volume|Container)'
    r' '
    r'(?P<resource_id>.+)'
    r'  '
    r'(?P<status>%s)' % (
        "|".join(STATUS_DONE | STATUS_WORKING | STATUS_ERROR)
    )
)


DOCKER_COMPOSE_EXECUTABLE = 'docker-compose'


class ComposeManager(object):
    def __init__(self, module, docker_host):
        # type: (ComposeManager, AnsibleModule, Text) -> None
        self._docker_host = docker_host
        self._module = module

    @staticmethod
    def _parse_stderr(stderr):
        # type: (Text) -> List[EVENT]
        events = []  # type: List[EVENT]
        for line in stderr.splitlines():
            line = line.strip()
            match = _re_resource_event.match(line)
            if (match is not None):
                events.append(ResourceEvent(
                    ResourceType.from_docker_compose_event(match.group('resource_type')),
                    match.group('resource_id'),
                    match.group('status')
                ))
        return events

    def _run_subcommand(
        self,
        subcommand,  # type: List[Text]
        files,  # type: List[Text]
        content=None,  # type: Optional[Text]
        project_name=None,  # type: Optional[Text]
        project_directory=None,  # type: Optional[Text]
        profiles=None,  # type: Optional[List[Text]]
        env_file=None,  # type: Optional[Text]
    ):
        # type: (...) -> Tuple[int, Text, Text, List[EVENT]]
        if profiles is None:
            profiles = []
        command = [DOCKER_COMPOSE_EXECUTABLE, '--ansi', 'never']
        for file in files:
            command.extend(['-f', file])
        if project_name is not None:
            command.extend(['-p', project_name])
        if project_directory is not None:
            command.extend(['--project-directory', project_directory])
        if env_file is not None:
            command.extend(['--env-file', env_file])
        for profile in profiles:
            command.extend(['--profile', profile])
        command += subcommand
        kwargs = {}
        if content is not None:
            kwargs['data'] = content
        env = {
            'DOCKER_HOST': self._docker_host
        }
        self._module.debug('DOCKER-COMPOSE command: %s' % (repr(command)))
        self._module.debug('DOCKER-COMPOSE stdin: %s' % (repr(content)))
        self._module.debug('DOCKER-COMPOSE env: %s' % (repr(env)))
        rc, out, err = self._module.run_command(
            command,
            environ_update=env,
            **kwargs
        )
        self._module.debug('DOCKER-COMPOSE rc: %d' % (rc))
        self._module.debug('DOCKER-COMPOSE stdout: %s' % (repr(out)))
        self._module.debug('DOCKER-COMPOSE stderr: %s' % (repr(err)))
        events = self._parse_stderr(err)
        return rc, out, err, events

    def up(
        self,
        # Common arguments
        files,  # type: List[Text]
        content=None,  # type: Optional[Text]
        project_name=None,  # type: Optional[Text]
        project_directory=None,  # type: Optional[Text]
        profiles=None,  # type: Optional[List[Text]]
        env_file=None,  # type: Optional[Text]
        # Specific arguments
        services=None,  # type: Optional[List[Text]]
        no_deps=False,  # type: bool
        pull=None,  # type: Optional[Union[Literal['always'], Literal['missing'], Literal['never']]]
        build=False,  # type: bool
        force_recreate=False,  # type: bool
        no_recreate=False,  # type: bool
        remove_orphans=False,  # type: bool
        timeout=None,  # type: Optional[int]
    ):
        # type: (...) -> Tuple[int, Text, Text, List[EVENT]]
        if profiles is None:
            profiles = []
        if services is None:
            services = []
        subcommand = ['up', '-d']
        if no_deps:
            subcommand.append('--no-deps')
        if pull:
            subcommand.extend(['--pull', pull])
        if build:
            subcommand.append('--build')
        if force_recreate:
            subcommand.append('--force-recreate')
        if no_recreate:
            subcommand.append('--no-recreate')
        if remove_orphans:
            subcommand.append('--remove-orphans')
        if timeout is not None:
            subcommand.extend(['--timeout', '%d' % (timeout)])
        for service in services:
            subcommand.append(service)
        return self._run_subcommand(
            subcommand,
            files,
            content,
            project_name=project_name,
            project_directory=project_directory,
            profiles=profiles,
            env_file=env_file,
        )

    def down(
        self,
        # Common arguments
        files,  # type: List[Text]
        content=None,  # type: Optional[Text]
        project_name=None,  # type: Optional[Text]
        project_directory=None,  # type: Optional[Text]
        profiles=None,  # type: Optional[List[Text]]
        env_file=None,  # type: Optional[Text]
        # Specific arguments
        remove_orphans=False,  # type: bool
        rmi=None,  # type: Optional[Union[Literal['all'], Literal['local']]]
        volumes=False,  # type: bool
        timeout=None,  # type: Optional[int]
    ):
        # type: (...) -> Tuple[int, Text, Text, List[EVENT]]
        if profiles is None:
            profiles = []
        subcommand = ['down']
        if remove_orphans:
            subcommand.append('--remove-orphans')
        if rmi:
            subcommand.extend(['--rmi', rmi])
        if volumes:
            subcommand.extend(['--volumes'])
        if timeout is not None:
            subcommand.extend(['--timeout', '%d' % (timeout)])
        return self._run_subcommand(
            subcommand,
            files,
            content,
            project_name=project_name,
            project_directory=project_directory,
            profiles=profiles,
            env_file=env_file,
        )

    def stop(
        self,
        # Common arguments
        files,  # type: List[Text]
        content=None,  # type: Optional[Text]
        project_name=None,  # type: Optional[Text]
        project_directory=None,  # type: Optional[Text]
        profiles=None,  # type: Optional[List[Text]]
        env_file=None,  # type: Optional[Text]
        # Specific arguments
        timeout=None,  # type: Optional[int]
    ):
        # type: (...) -> Tuple[int, Text, Text, List[EVENT]]
        if profiles is None:
            profiles = []
        subcommand = ['stop']
        if timeout is not None:
            subcommand.extend(['--timeout', '%d' % (timeout)])
        return self._run_subcommand(
            subcommand,
            files,
            content,
            project_name=project_name,
            project_directory=project_directory,
            profiles=profiles,
            env_file=env_file,
        )

    def restart(
        self,
        # Common arguments
        files,  # type: List[Text]
        content=None,  # type: Optional[Text]
        project_name=None,  # type: Optional[Text]
        project_directory=None,  # type: Optional[Text]
        profiles=None,  # type: Optional[List[Text]]
        env_file=None,  # type: Optional[Text]
        # Specific arguments
        services=None,  # type: Optional[List[Text]]
        timeout=None,  # type: Optional[int]
    ):
        # type: (...) -> Tuple[int, Text, Text, List[EVENT]]
        if profiles is None:
            profiles = []
        if services is None:
            services = []
        subcommand = ['restart']
        if timeout is not None:
            subcommand.extend(['--timeout', '%d' % (timeout)])
        for service in services:
            subcommand.append(service)
        return self._run_subcommand(
            subcommand,
            files,
            content,
            project_name=project_name,
            project_directory=project_directory,
            profiles=profiles,
            env_file=env_file,
        )

    def build(
        self,
        # Common arguments
        files,  # type: List[Text]
        content=None,  # type: Optional[Text]
        project_name=None,  # type: Optional[Text]
        project_directory=None,  # type: Optional[Text]
        profiles=None,  # type: Optional[List[Text]]
        env_file=None,  # type: Optional[Text]
        # Specific arguments
        services=None,  # type: Optional[List[Text]]
        no_cache=False,  # type: bool
        pull=False,  # type: bool
    ):
        # type: (...) -> Tuple[int, Text, Text, List[EVENT]]
        if profiles is None:
            profiles = []
        if services is None:
            services = []
        subcommand = ['build']
        if no_cache:
            subcommand.append('--no-cache')
        if pull:
            subcommand.append('--pull')
        for service in services:
            subcommand.append(service)
        return self._run_subcommand(
            subcommand,
            files,
            content,
            project_name=project_name,
            project_directory=project_directory,
            profiles=profiles,
            env_file=env_file,
        )

    def pull(
        self,
        # Common arguments
        files,  # type: List[Text]
        content=None,  # type: Optional[Text]
        project_name=None,  # type: Optional[Text]
        project_directory=None,  # type: Optional[Text]
        profiles=None,  # type: Optional[List[Text]]
        env_file=None,  # type: Optional[Text]
        # Specific arguments
        services=None,  # type: Optional[List[Text]]
        include_deps=False,  # type: bool
    ):
        # type: (...) -> Tuple[int, Text, Text, List[EVENT]]
        if profiles is None:
            profiles = []
        if services is None:
            services = []
        subcommand = ['pull']
        if include_deps:
            subcommand.append('--include-deps')
        for service in services:
            subcommand.append(service)
        return self._run_subcommand(
            subcommand,
            files,
            content,
            project_name=project_name,
            project_directory=project_directory,
            profiles=profiles,
            env_file=env_file,
        )


def main():
    module = AnsibleModule(
        argument_spec=dict(
            docker_host=DOCKER_COMMON_ARGS['docker_host'],
            project_src=dict(type='path'),
            project_name=dict(type='str',),
            env_file=dict(type='path'),
            files=dict(type='list', elements='path'),
            profiles=dict(type='list', elements='str'),
            state=dict(type='str', default='present', choices=['absent', 'present', 'built', 'pulled', 'restarted', 'stopped']),
            definition=dict(type='dict'),
            recreate=dict(type='str', default='smart', choices=['always', 'never', 'smart']),
            build=dict(type='bool', default=False),
            remove_images=dict(type='str', choices=['all', 'local']),
            remove_volumes=dict(type='bool', default=False),
            remove_orphans=dict(type='bool', default=False),
            services=dict(type='list', elements='str'),
            dependencies=dict(type='bool', default=True),
            pull=dict(type='bool', default=False),
            nocache=dict(type='bool', default=False),
            timeout=dict(type='int')
        ),
        mutually_exclusive=[
            ('definition', 'files'),
        ],
        required_by={
            'definition': ('project_src', ),
        },
        required_one_of=[
            ('files', 'definition'),
        ],
    )
    changed = False
    compose = ComposeManager(module, module.params['docker_host'])
    if module.params['definition'] is not None:
        if not HAS_YAML:
            module.fail_json(
                changed=False,
                msg=missing_required_lib('PyYAML', reason='when using the "definition" argument.')
            )
        common_args = [
            ['-'],
            yaml_dump(module.params['definition']),
        ]
    else:
        common_args = [
            module.params['files'],
        ]
    common_kwargs = dict(
        project_name=module.params['project_name'],
        project_directory=module.params['project_src'],
        profiles=module.params['profiles'] or [],
        env_file=module.params['env_file'],
    )
    if module.params['state'] == 'present':
        rc, out, err, events = compose.up(
            *common_args,
            services=module.params['services'] or [],
            no_deps=not module.params['dependencies'],
            pull='always' if module.params['pull'] else None,
            build=module.params['build'],
            force_recreate=module.params['recreate'] == "always",
            no_recreate=module.params['recreate'] == "never",
            remove_orphans=module.params['remove_orphans'],
            timeout=module.params['timeout'],
            **common_kwargs
        )
    elif module.params['state'] == 'stopped':
        rc, out, err, events = compose.stop(
            *common_args,
            timeout=module.params['timeout'],
            **common_kwargs
        )
    elif module.params['state'] == 'restarted':
        rc, out, err, events = compose.restart(
            *common_args,
            services=module.params['services'] or [],
            timeout=module.params['timeout'],
            **common_kwargs
        )
    elif module.params['state'] == 'built':
        rc, out, err, events = compose.build(
            *common_args,
            services=module.params['services'] or [],
            no_cache=not module.params['nocache'],
            pull=module.params['pull'],
            **common_kwargs
        )
    elif module.params['state'] == 'pulled':
        rc, out, err, events = compose.pull(
            *common_args,
            services=module.params['services'] or [],
            include_deps=module.params['dependencies'],
            **common_kwargs
        )
        changed = True  # We cannot detect change from docker-compose stderr
    elif module.params['state'] == 'absent':
        rc, out, err, events = compose.down(
            *common_args,
            remove_orphans=module.params['remove_orphans'],
            rmi=module.params['remove_images'],
            volumes=module.params['remove_volumes'],
            timeout=module.params['timeout'],
            **common_kwargs
        )
    else:
        raise AssertionError("THIS IS DEAD CODE")
    networks_states = defaultdict(list)
    images_states = defaultdict(list)
    volumes_states = defaultdict(list)
    containers_states = defaultdict(list)
    for event in events:
        collection = {
            ResourceType.NETWORK: networks_states,
            ResourceType.IMAGE: images_states,
            ResourceType.VOLUME: volumes_states,
            ResourceType.CONTAINER: containers_states,
        }[event.resource_type]
        if event.status not in STATUS_DONE:
            continue
        if event.status in STATUS_THAT_CAUSE_A_CHANGE:
            changed = True
        collection[event.resource_id].append(STATUS_DOCKERCOMPOSE_TO_COMMUNITYDOCKER[event.status])
    result = dict(
        changed=changed,
        networks={k: list(v) for k, v in networks_states.items()},
        images={k: list(v) for k, v in images_states.items()},
        volumes={k: list(v) for k, v in volumes_states.items()},
        containers={k: list(v) for k, v in containers_states.items()},
        stdout=out,
        stderr=err,
    )
    if rc != 0:
        result['msg'] = "docker-compose exited with code %d. Read stderr for more information." % (rc)
        module.fail_json(**result)
    else:
        module.exit_json(**result)


if __name__ == '__main__':
    main()
