# -*- coding: utf-8 -*-
# Copyright (c) 2020, Felix Fontein <felix@fontein.de>
# For the parts taken from the docker inventory script:
# Copyright (c) 2016, Paul Durivage <paul.durivage@gmail.com>
# Copyright (c) 2016, Chris Houseknecht <house@redhat.com>
# Copyright (c) 2016, James Tanner <jtanner@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


DOCUMENTATION = '''
name: docker_containers
short_description: Ansible dynamic inventory plugin for Docker containers.
version_added: 1.1.0
author:
    - Felix Fontein (@felixfontein)
requirements:
    - L(Docker SDK for Python,https://docker-py.readthedocs.io/en/stable/) >= 1.10.0
extends_documentation_fragment:
    - ansible.builtin.constructed
    - community.docker.docker
    - community.docker.docker.docker_py_1_documentation
description:
    - Reads inventories from the Docker API.
    - Uses a YAML configuration file that ends with C(docker.[yml|yaml]).
options:
    plugin:
        description:
            - The name of this plugin, it should always be set to C(community.docker.docker_containers)
              for this plugin to recognize it as it's own.
        type: str
        required: true
        choices: [ community.docker.docker_containers ]

    connection_type:
        description:
            - Which connection type to use the containers.
            - Default is to use SSH (C(ssh)). For this, the options I(default_ip) and
              I(private_ssh_port) are used.
            - Alternatively, C(docker-cli) selects the
              R(docker connection plugin,ansible_collections.community.docker.docker_connection),
              and C(docker-api) selects the
              R(docker_api connection plugin,ansible_collections.community.docker.docker_api_connection).
        type: str
        default: docker-api
        choices:
            - ssh
            - docker-cli
            - docker-api

    verbose_output:
        description:
            - Toggle to (not) include all available inspection metadata.
            - Note that all top-level keys will be transformed to the format C(docker_xxx).
              For example, C(HostConfig) is converted to C(docker_hostconfig).
            - If this is C(false), these values can only be used during I(constructed), I(groups), and I(keyed_groups).
            - The C(docker) inventory script always added these variables, so for compatibility set this to C(true).
        type: bool
        default: false

    default_ip:
        description:
            - The IP address to assign to ansible_host when the container's SSH port is mapped to interface
              '0.0.0.0'.
            - Only used if I(connection_type) is C(ssh).
        type: str
        default: 127.0.0.1

    private_ssh_port:
        description:
            - The port containers use for SSH.
            - Only used if I(connection_type) is C(ssh).
        type: int
        default: 22

    add_legacy_groups:
        description:
            - "Add the same groups as the C(docker) inventory script does. These are the following:"
            - "C(<container id>): contains the container of this ID."
            - "C(<container name>): contains the container that has this name."
            - "C(<container short id>): contains the containers that have this short ID (first 13 letters of ID)."
            - "C(image_<image name>): contains the containers that have the image C(<image name>)."
            - "C(stack_<stack name>): contains the containers that belong to the stack C(<stack name>)."
            - "C(service_<service name>): contains the containers that belong to the service C(<service name>)"
            - "C(<docker_host>): contains the containers which belong to the Docker daemon I(docker_host).
              Useful if you run this plugin against multiple Docker daemons."
            - "C(running): contains all containers that are running."
            - "C(stopped): contains all containers that are not running."
            - If this is not set to C(true), you should use keyed groups to add the containers to groups.
              See the examples for how to do that.
        type: bool
        default: false
'''

EXAMPLES = '''
# Minimal example using local Docker daemon
plugin: community.docker.docker_containers
docker_host: unix://var/run/docker.sock

# Minimal example using remote Docker daemon
plugin: community.docker.docker_containers
docker_host: tcp://my-docker-host:2375

# Example using remote Docker daemon with unverified TLS
plugin: community.docker.docker_containers
docker_host: tcp://my-docker-host:2376
tls: true

# Example using remote Docker daemon with verified TLS and client certificate verification
plugin: community.docker.docker_containers
docker_host: tcp://my-docker-host:2376
validate_certs: true
ca_cert: /somewhere/ca.pem
client_key: /somewhere/key.pem
client_cert: /somewhere/cert.pem

# Example using constructed features to create groups
plugin: community.docker.docker_containers
docker_host: tcp://my-docker-host:2375
strict: false
keyed_groups:
  # Add containers with primary network foo to a network_foo group
  - prefix: network
    key: 'docker_hostconfig.NetworkMode'
  # Add Linux hosts to an os_linux group
  - prefix: os
    key: docker_platform
'''

import re

from ansible.errors import AnsibleError
from ansible.module_utils._text import to_native
from ansible_collections.community.docker.plugins.module_utils.common import update_tls_hostname, get_connect_params
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable
from ansible.parsing.utils.addresses import parse_address

from ansible_collections.community.docker.plugins.module_utils.common import (
    RequestException,
)
from ansible_collections.community.docker.plugins.plugin_utils.common import (
    AnsibleDockerClient,
)

try:
    from docker.errors import DockerException, APIError, NotFound
except Exception:
    # missing Docker SDK for Python handled in ansible_collections.community.docker.plugins.module_utils.common
    pass

MIN_DOCKER_PY = '1.7.0'
MIN_DOCKER_API = None


class InventoryModule(BaseInventoryPlugin, Constructable):
    ''' Host inventory parser for ansible using Docker daemon as source. '''

    NAME = 'community.docker.docker_containers'

    def _slugify(self, value):
        return 'docker_%s' % (re.sub(r'[^\w-]', '_', value).lower().lstrip('_'))

    def _populate(self, client):
        strict = self.get_option('strict')

        ssh_port = self.get_option('private_ssh_port')
        default_ip = self.get_option('default_ip')
        hostname = self.get_option('docker_host')
        verbose_output = self.get_option('verbose_output')
        connection_type = self.get_option('connection_type')
        add_legacy_groups = self.get_option('add_legacy_groups')

        try:
            containers = client.containers(all=True)
        except APIError as exc:
            raise AnsibleError("Error listing containers: %s" % to_native(exc))

        if add_legacy_groups:
            self.inventory.add_group('running')
            self.inventory.add_group('stopped')

        for container in containers:
            id = container.get('Id')
            short_id = id[:13]

            try:
                name = container.get('Names', list())[0].lstrip('/')
                full_name = name
            except IndexError:
                name = short_id
                full_name = id

            self.inventory.add_host(name)
            facts = dict(
                docker_name=name,
                docker_short_id=short_id
            )
            full_facts = dict()

            try:
                inspect = client.inspect_container(id)
            except APIError as exc:
                raise AnsibleError("Error inspecting container %s - %s" % (name, str(exc)))

            state = inspect.get('State') or dict()
            config = inspect.get('Config') or dict()
            labels = config.get('Labels') or dict()

            running = state.get('Running')

            # Add container to groups
            image_name = config.get('Image')
            if image_name and add_legacy_groups:
                self.inventory.add_group('image_{0}'.format(image_name))
                self.inventory.add_host(name, group='image_{0}'.format(image_name))

            stack_name = labels.get('com.docker.stack.namespace')
            if stack_name:
                full_facts['docker_stack'] = stack_name
                if add_legacy_groups:
                    self.inventory.add_group('stack_{0}'.format(stack_name))
                    self.inventory.add_host(name, group='stack_{0}'.format(stack_name))

            service_name = labels.get('com.docker.swarm.service.name')
            if service_name:
                full_facts['docker_service'] = service_name
                if add_legacy_groups:
                    self.inventory.add_group('service_{0}'.format(service_name))
                    self.inventory.add_host(name, group='service_{0}'.format(service_name))

            if connection_type == 'ssh':
                # Figure out ssh IP and Port
                try:
                    # Lookup the public facing port Nat'ed to ssh port.
                    port = client.port(container, ssh_port)[0]
                except (IndexError, AttributeError, TypeError):
                    port = dict()

                try:
                    ip = default_ip if port['HostIp'] == '0.0.0.0' else port['HostIp']
                except KeyError:
                    ip = ''

                facts.update(dict(
                    ansible_ssh_host=ip,
                    ansible_ssh_port=port.get('HostPort', 0),
                ))
            elif connection_type == 'docker-cli':
                facts.update(dict(
                    ansible_host=full_name,
                    ansible_connection='community.docker.docker',
                ))
            elif connection_type == 'docker-api':
                facts.update(dict(
                    ansible_host=full_name,
                    ansible_connection='community.docker.docker_api',
                ))

            full_facts.update(facts)
            for key, value in inspect.items():
                fact_key = self._slugify(key)
                full_facts[fact_key] = value

            if verbose_output:
                facts.update(full_facts)

            for key, value in facts.items():
                self.inventory.set_variable(name, key, value)

            # Use constructed if applicable
            # Composed variables
            self._set_composite_vars(self.get_option('compose'), full_facts, name, strict=strict)
            # Complex groups based on jinja2 conditionals, hosts that meet the conditional are added to group
            self._add_host_to_composed_groups(self.get_option('groups'), full_facts, name, strict=strict)
            # Create groups based on variable values and add the corresponding hosts to it
            self._add_host_to_keyed_groups(self.get_option('keyed_groups'), full_facts, name, strict=strict)

            # We need to do this last since we also add a group called `name`.
            # When we do this before a set_variable() call, the variables are assigned
            # to the group, and not to the host.
            if add_legacy_groups:
                self.inventory.add_group(id)
                self.inventory.add_host(name, group=id)
                self.inventory.add_group(name)
                self.inventory.add_host(name, group=name)
                self.inventory.add_group(short_id)
                self.inventory.add_host(name, group=short_id)
                self.inventory.add_group(hostname)
                self.inventory.add_host(name, group=hostname)

                if running is True:
                    self.inventory.add_host(name, group='running')
                else:
                    self.inventory.add_host(name, group='stopped')

    def verify_file(self, path):
        """Return the possibly of a file being consumable by this plugin."""
        return (
            super(InventoryModule, self).verify_file(path) and
            path.endswith(('docker.yaml', 'docker.yml')))

    def _create_client(self):
        return AnsibleDockerClient(self, min_docker_version=MIN_DOCKER_PY, min_docker_api_version=MIN_DOCKER_API)

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        self._read_config_data(path)
        client = self._create_client()
        try:
            self._populate(client)
        except DockerException as e:
            raise AnsibleError(
                'An unexpected docker error occurred: {0}'.format(e)
            )
        except RequestException as e:
            raise AnsibleError(
                'An unexpected requests error occurred when docker-py tried to talk to the docker daemon: {0}'.format(e)
            )
