#!/usr/bin/python
#
# Copyright (c) 2022 Sid Sun <sid@dronk.dev>
# Based on Ansible docker compose module by:
# Copyright 2016 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
---
module: docker_compose_v2

short_description: Manage multi-container Docker applications with Docker Compose v2.

version_added: "3.5.0"

description:
  - Uses Docker Compose v2 to manage docker services. B(This module requires docker-compose >= 2.0.0. and python >= 3.7)
  - Configuration can be read from a C(docker-compose.yaml) file.
  - See the examples for more details.
  - Supports check mode.

extends_documentation_fragment:
  - community.docker.attributes

attributes:
  check_mode:
    support: full
  diff_mode:
    support: none

options:
  project_src:
    description:
      - Path to a directory containing a C(docker-compose.yaml) file.
      - Required.
    type: path
  state:
    description:
      - Desired state of the project.
      - Specifying C(present) is the same as running C(docker-compose up) resp. C(docker-compose stop) (with I(stopped)) resp. C(docker-compose restart)
        (with I(restarted)).
      - Specifying C(absent) is the same as running C(docker-compose down).
    type: str
    default: present
    choices:
      - absent
      - present
  recreate:
    description:
      - By default containers will be recreated when their configuration differs from the service definition.
      - Setting to C(never) ignores configuration differences and leaves existing containers unchanged.
      - Setting to C(always) forces recreation of all existing containers.
    type: str
    default: smart
    choices:
      - always
      - never
      - smart
  build:
    description:
      - Use with I(state) C(present) to always build images prior to starting the application.
      - Same as running C(docker-compose build) with the pull option.
      - Images will only be rebuilt if Docker detects a change in the Dockerfile or build directory contents.
      - Use the I(nocache) option to ignore the image cache when performing the build.
      - If an existing image is replaced, services using the image will be recreated unless I(recreate) is C(never).
    type: bool
    default: false
  pull:
    description:
      - Use with I(state) C(present) to always pull images prior to starting the application.
      - Same as running C(docker-compose pull).
      - When a new image is pulled, services using the image will be recreated unless I(recreate) is C(never).
    type: bool
    default: false
  nocache:
    description:
      - Use with the I(build) option to ignore the cache during the image build process.
    type: bool
    default: false
  remove_images:
    description:
      - Use with I(state) C(absent) to remove all images or only local images.
    type: str
    choices:
        - 'all'
        - 'local'
  remove_volumes:
    description:
      - Use with I(state) C(absent) to remove data volumes.
    type: bool
    default: false
  remove_orphans:
    description:
      - Remove containers for services not defined in the Compose file when not C(restarted) or C(stopped).
    type: bool
    default: false
  stopped:
    description:
      - Use with I(state) C(present) to stop all containers defined in the Compose file.
    type: bool
    default: false
  restarted:
    description:
      - Use with I(state) C(present) to restart all containers defined in the Compose file.
    type: bool
    default: false

requirements:
  - "L(Python on Whales,https://pypi.org/project/python-on-whales/) >= 0.55.0"
  - "docker-compose >= 2.0.0"
  - "python >= 3.7"

author:
    - Sid Sun (@SidSun)
'''

EXAMPLES = '''
# Set up a virtual environment for the module and install python on whales
- name: Set up virtual env for compose v2
  ansible.builtin.pip:
    name: 
    - python-on-whales
    virtualenv: ~/ansible-compose-v2

# Ensure project directory is present
- name: Create directory if it does not exist
  ansible.builtin.file:
    path: uptime-kuma
    state: directory
# Create the docker compose file 
- name: Create compose file with content
  ansible.builtin.copy:
    dest: "uptime-kuma/docker-compose.yaml"
    content: |
      version: '3.3'

      services:
        uptime-kuma:
          image: louislam/uptime-kuma:1
          container_name: uptime-kuma
          volumes:
            - ./uptime-kuma-data:/app/data
          ports:
            - 3001:3001
          restart: always

# Tear down any containers, remove images and volumes
- name: Tear down all existing containers
  vars:
    ansible_python_interpreter: ansible-compose-v2/bin/python
  community.docker.docker_compose_v2:
    project_src: uptime-kuma/docker-compose.yaml
    remove_volumes: true
    remove_orphans: true
    remove_images: all
    state: absent

# Pull the latest image and then start services
- name: Pull image and start service
  vars:
    ansible_python_interpreter: ansible-compose-v2/bin/python
  community.docker.docker_compose_v2:
    project_src: uptime-kuma/docker-compose.yaml
    pull: true
    state: present

# Restart services
- name: Restart service
  vars:
    ansible_python_interpreter: ansible-compose-v2/bin/python
  community.docker.docker_compose_v2:
    project_src: uptime-kuma/docker-compose.yaml
    restarted: true
    state: present

# Stop services
- name: Stop service
  vars:
    ansible_python_interpreter: ansible-compose-v2/bin/python
  community.docker.docker_compose_v2:
    project_src: uptime-kuma/docker-compose.yaml
    stopped: true
    state: present

# Start services, recreating all containers
- name: Recreate service
  vars:
    ansible_python_interpreter: ansible-compose-v2/bin/python
  community.docker.docker_compose_v2:
    project_src: uptime-kuma/docker-compose.yaml
    recreate: always
    state: present
'''

RETURN = '''
# returns are a bit finicky at the moment, see: https://github.com/gabrieldemarmiesse/python-on-whales/issues/395
msg:
    description: In docker failures, has docker command + some description. In other failures, stringified exception is returned. In success, descriptive message of what happened.
    type: bool
    returned: always
    sample: true
changed:
    description: If something was changed (currently, changed is (almost) always true as there is no check of current state).
    type: bool
    returned: always
    sample: true
actions:
    description: List stating which compose commands were run (not the entire command itself).
    type: list
    returned: success
    sample: ["pull", "up"]
rc:
    description: Return code of executed docker command.
    type: str
    returned: failure from docker
    sample: 12
'''

import os
import traceback
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native

try:
  from python_on_whales.docker_client import DockerClient
  from python_on_whales.exceptions import (
      DockerException,
  )
  HAS_POW = True
  HAS_POW_EXC = None
except ImportError as e:
  HAS_POW = False
  HAS_POW_EXC = traceback.format_exc()

class ComposeV2Module:
    module: AnsibleModule

    def __init__(self, module: AnsibleModule):
        self.module = module
        self.remove_images = None
        self.remove_orphans = None
        self.remove_volumes = None
        self.restarted = None
        self.nocache = None
        self.stopped = None
        self.build = None
        self.project_src = None
        self.state = None
        self.pull = None
        self.recreate = None

        for key, value in module.params.items():
            setattr(self, key, value)

        self.check_mode = module.check_mode

        if not HAS_POW:
            self.client.fail("Unable to load python-on-whales. Try `pip install python-on-whales`. Error: %s" %
                             to_native(HAS_POW_EXC))


    def exec_module(self):
        if self.state == 'present':
            return self.cmd_up()
        elif self.state == 'absent':
            return self.cmd_down()

    def cmd_up(self):
        result = dict(
            changed=False,
            msg='',
            actions=[]
        )
        client = DockerClient(compose_files=[os.path.join(
            self.project_src, "docker-compose.yaml")])

        if self.build:
            if not self.check_mode:
                result['changed'] |= True
                client.compose.build(
                    cache=not self.nocache, pull=True, quiet=True)
            result['actions'].append("build")

        if self.pull:
            if not self.check_mode:
                result['changed'] |= True
                client.compose.pull(quiet=True)
            result['actions'].append("pull")

        if self.restarted:
            if not self.check_mode:
                result['changed'] |= True
                client.compose.restart(quiet=True)
            result['actions'].append("restart")

        if self.stopped:
            if not self.check_mode:
                result['changed'] |= True
                client.compose.stop(quiet=True)
            result['actions'].append("stop")

        if not self.restarted and not self.stopped:
            recreate = self.recreate != "never"
            force_recreate = self.recreate == "always"
            if not self.check_mode:
                result['changed'] |= True
                client.compose.up(detach=True, recreate=recreate,
                                  force_recreate=force_recreate, remove_orphans=self.remove_orphans, quiet=True)
            result['actions'].append("up")

        return result

    def cmd_down(self):
        result = dict(
            changed=False,
            msg='',
            actions=[]
        )
        client = DockerClient(compose_files=[os.path.join(
            self.project_src, "docker-compose.yaml")])

        if not self.check_mode:
            result['changed'] |= True
            client.compose.down(remove_orphans=self.remove_orphans,
                                remove_images=self.remove_images, volumes=self.remove_volumes, quiet=True)
        result['actions'].append("down")

        return result


def main():
    module_args = dict(
        project_src=dict(type='path'),
        pull=dict(type='bool', default=False),
        build=dict(type='bool', default=False),
        nocache=dict(type='bool', default=False),
        stopped=dict(type='bool', default=False),
        restarted=dict(type='bool', default=False),
        remove_volumes=dict(type='bool', default=False),
        remove_orphans=dict(type='bool', default=False),
        remove_images=dict(type='str', choices=['all', 'local']),
        state=dict(type='str', default='present',
                   choices=['absent', 'present']),
        recreate=dict(type='str', default='smart', choices=[
                      'always', 'never', 'smart']),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    try:
        v2module = ComposeV2Module(module)
    except Exception as e:
        module.fail_json(str(e))

    try:
        result = v2module.exec_module()
        module.exit_json(**result)
    except DockerException as e:
        failure = dict(
            msg=f"something went wrong, stderr, stdout and return code is printed, command executed: {e.docker_command}",
            changed=True,
            failed=True,
            stderr=e.stderr,
            stdout=e.stdout,
            rc=e.return_code,
            err=str(e),
        )
        module.fail_json(**failure)
    except Exception as e:
        module.fail_json(str(e))


if __name__ == '__main__':
    main()
