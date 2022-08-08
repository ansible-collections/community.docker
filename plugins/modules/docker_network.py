#!/usr/bin/python
#
# Copyright 2016 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
module: docker_network
short_description: Manage Docker networks
description:
  - Create/remove Docker networks and connect containers to them.
  - Performs largely the same function as the C(docker network) CLI subcommand.
options:
  name:
    description:
      - Name of the network to operate on.
    type: str
    required: true
    aliases:
      - network_name

  connected:
    description:
      - List of container names or container IDs to connect to a network.
      - Please note that the module only makes sure that these containers are connected to the network,
        but does not care about connection options. If you rely on specific IP addresses etc., use the
        M(community.docker.docker_container) module to ensure your containers are correctly connected to this network.
    type: list
    elements: str
    aliases:
      - containers

  driver:
    description:
      - Specify the type of network. Docker provides bridge and overlay drivers, but 3rd party drivers can also be used.
    type: str
    default: bridge

  driver_options:
    description:
      - Dictionary of network settings. Consult docker docs for valid options and values.
    type: dict

  force:
    description:
      - With state C(absent) forces disconnecting all containers from the
        network prior to deleting the network. With state C(present) will
        disconnect all containers, delete the network and re-create the
        network.
      - This option is required if you have changed the IPAM or driver options
        and want an existing network to be updated to use the new options.
    type: bool
    default: false

  appends:
    description:
      - By default the connected list is canonical, meaning containers not on the list are removed from the network.
      - Use I(appends) to leave existing containers connected.
    type: bool
    default: false
    aliases:
      - incremental

  enable_ipv6:
    description:
      - Enable IPv6 networking.
    type: bool

  ipam_driver:
    description:
      - Specify an IPAM driver.
    type: str

  ipam_driver_options:
    description:
      - Dictionary of IPAM driver options.
    type: dict

  ipam_config:
    description:
      - List of IPAM config blocks. Consult
        L(Docker docs,https://docs.docker.com/compose/compose-file/compose-file-v2/#ipam) for valid options and values.
        Note that I(iprange) is spelled differently here (we use the notation from the Docker SDK for Python).
    type: list
    elements: dict
    suboptions:
      subnet:
        description:
          - IP subset in CIDR notation.
        type: str
      iprange:
        description:
          - IP address range in CIDR notation.
        type: str
      gateway:
        description:
          - IP gateway address.
        type: str
      aux_addresses:
        description:
          - Auxiliary IP addresses used by Network driver, as a mapping from hostname to IP.
        type: dict

  state:
    description:
      - C(absent) deletes the network. If a network has connected containers, it
        cannot be deleted. Use the I(force) option to disconnect all containers
        and delete the network.
      - C(present) creates the network, if it does not already exist with the
        specified parameters, and connects the list of containers provided via
        the connected parameter. Containers not on the list will be disconnected.
        An empty list will leave no containers connected to the network. Use the
        I(appends) option to leave existing containers connected. Use the I(force)
        options to force re-creation of the network.
    type: str
    default: present
    choices:
      - absent
      - present

  internal:
    description:
      - Restrict external access to the network.
    type: bool

  labels:
    description:
      - Dictionary of labels.
    type: dict

  scope:
    description:
      - Specify the network's scope.
    type: str
    choices:
      - local
      - global
      - swarm

  attachable:
    description:
      - If enabled, and the network is in the global scope, non-service containers on worker nodes will be able to connect to the network.
    type: bool

extends_documentation_fragment:
- community.docker.docker.api_documentation


notes:
  - When network options are changed, the module disconnects all containers from the network, deletes the network, and re-creates the network.
    It does not try to reconnect containers, except the ones listed in (I(connected), and even for these, it does not consider specific
    connection options like fixed IP addresses or MAC addresses. If you need more control over how the containers are connected to the
    network, loop the M(community.docker.docker_container) module to loop over your containers to make sure they are connected properly.
  - The module does not support Docker Swarm. This means that it will not try to disconnect or reconnect services. If services are connected to the
    network, deleting the network will fail. When network options are changed, the network has to be deleted and recreated, so this will
    fail as well.

author:
  - "Ben Keith (@keitwb)"
  - "Chris Houseknecht (@chouseknecht)"
  - "Dave Bendit (@DBendit)"

requirements:
  - "Docker API >= 1.25"
'''

EXAMPLES = '''
- name: Create a network
  community.docker.docker_network:
    name: network_one

- name: Remove all but selected list of containers
  community.docker.docker_network:
    name: network_one
    connected:
      - container_a
      - container_b
      - container_c

- name: Remove a single container
  community.docker.docker_network:
    name: network_one
    connected: "{{ fulllist|difference(['container_a']) }}"

- name: Add a container to a network, leaving existing containers connected
  community.docker.docker_network:
    name: network_one
    connected:
      - container_a
    appends: true

- name: Create a network with driver options
  community.docker.docker_network:
    name: network_two
    driver_options:
      com.docker.network.bridge.name: net2

- name: Create a network with custom IPAM config
  community.docker.docker_network:
    name: network_three
    ipam_config:
      - subnet: 172.23.27.0/24
        gateway: 172.23.27.2
        iprange: 172.23.27.0/26
        aux_addresses:
          host1: 172.23.27.3
          host2: 172.23.27.4

- name: Create a network with labels
  community.docker.docker_network:
    name: network_four
    labels:
      key1: value1
      key2: value2

- name: Create a network with IPv6 IPAM config
  community.docker.docker_network:
    name: network_ipv6_one
    enable_ipv6: true
    ipam_config:
      - subnet: fdd1:ac8c:0557:7ce1::/64

- name: Create a network with IPv6 and custom IPv4 IPAM config
  community.docker.docker_network:
    name: network_ipv6_two
    enable_ipv6: true
    ipam_config:
      - subnet: 172.24.27.0/24
      - subnet: fdd1:ac8c:0557:7ce2::/64

- name: Delete a network, disconnecting all containers
  community.docker.docker_network:
    name: network_one
    state: absent
    force: true
'''

RETURN = '''
network:
    description:
    - Network inspection results for the affected network.
    returned: success
    type: dict
    sample: {}
'''

import re
import traceback

from ansible.module_utils.common.text.converters import to_native

from ansible_collections.community.docker.plugins.module_utils.common_api import (
    AnsibleDockerClient,
    RequestException,
)
from ansible_collections.community.docker.plugins.module_utils.util import (
    DockerBaseClass,
    DifferenceTracker,
    clean_dict_booleans_for_docker_api,
)
from ansible_collections.community.docker.plugins.module_utils._api.errors import DockerException


class TaskParameters(DockerBaseClass):
    def __init__(self, client):
        super(TaskParameters, self).__init__()
        self.client = client

        self.name = None
        self.connected = None
        self.driver = None
        self.driver_options = None
        self.ipam_driver = None
        self.ipam_driver_options = None
        self.ipam_config = None
        self.appends = None
        self.force = None
        self.internal = None
        self.labels = None
        self.debug = None
        self.enable_ipv6 = None
        self.scope = None
        self.attachable = None

        for key, value in client.module.params.items():
            setattr(self, key, value)


def container_names_in_network(network):
    return [c['Name'] for c in network['Containers'].values()] if network['Containers'] else []


CIDR_IPV4 = re.compile(r'^([0-9]{1,3}\.){3}[0-9]{1,3}/([0-9]|[1-2][0-9]|3[0-2])$')
CIDR_IPV6 = re.compile(r'^[0-9a-fA-F:]+/([0-9]|[1-9][0-9]|1[0-2][0-9])$')


def validate_cidr(cidr):
    """Validate CIDR. Return IP version of a CIDR string on success.

    :param cidr: Valid CIDR
    :type cidr: str
    :return: ``ipv4`` or ``ipv6``
    :rtype: str
    :raises ValueError: If ``cidr`` is not a valid CIDR
    """
    if CIDR_IPV4.match(cidr):
        return 'ipv4'
    elif CIDR_IPV6.match(cidr):
        return 'ipv6'
    raise ValueError('"{0}" is not a valid CIDR'.format(cidr))


def normalize_ipam_config_key(key):
    """Normalizes IPAM config keys returned by Docker API to match Ansible keys.

    :param key: Docker API key
    :type key: str
    :return Ansible module key
    :rtype str
    """
    special_cases = {
        'AuxiliaryAddresses': 'aux_addresses'
    }
    return special_cases.get(key, key.lower())


def dicts_are_essentially_equal(a, b):
    """Make sure that a is a subset of b, where None entries of a are ignored."""
    for k, v in a.items():
        if v is None:
            continue
        if b.get(k) != v:
            return False
    return True


class DockerNetworkManager(object):

    def __init__(self, client):
        self.client = client
        self.parameters = TaskParameters(client)
        self.check_mode = self.client.check_mode
        self.results = {
            u'changed': False,
            u'actions': []
        }
        self.diff = self.client.module._diff
        self.diff_tracker = DifferenceTracker()
        self.diff_result = dict()

        self.existing_network = self.get_existing_network()

        if not self.parameters.connected and self.existing_network:
            self.parameters.connected = container_names_in_network(self.existing_network)

        if self.parameters.ipam_config:
            try:
                for ipam_config in self.parameters.ipam_config:
                    validate_cidr(ipam_config['subnet'])
            except ValueError as e:
                self.client.fail(to_native(e))

        if self.parameters.driver_options:
            self.parameters.driver_options = clean_dict_booleans_for_docker_api(self.parameters.driver_options)

        state = self.parameters.state
        if state == 'present':
            self.present()
        elif state == 'absent':
            self.absent()

        if self.diff or self.check_mode or self.parameters.debug:
            if self.diff:
                self.diff_result['before'], self.diff_result['after'] = self.diff_tracker.get_before_after()
            self.results['diff'] = self.diff_result

    def get_existing_network(self):
        return self.client.get_network(name=self.parameters.name)

    def has_different_config(self, net):
        '''
        Evaluates an existing network and returns a tuple containing a boolean
        indicating if the configuration is different and a list of differences.

        :param net: the inspection output for an existing network
        :return: (bool, list)
        '''
        differences = DifferenceTracker()
        if self.parameters.driver and self.parameters.driver != net['Driver']:
            differences.add('driver',
                            parameter=self.parameters.driver,
                            active=net['Driver'])
        if self.parameters.driver_options:
            if not net.get('Options'):
                differences.add('driver_options',
                                parameter=self.parameters.driver_options,
                                active=net.get('Options'))
            else:
                for key, value in self.parameters.driver_options.items():
                    if not (key in net['Options']) or value != net['Options'][key]:
                        differences.add('driver_options.%s' % key,
                                        parameter=value,
                                        active=net['Options'].get(key))

        if self.parameters.ipam_driver:
            if not net.get('IPAM') or net['IPAM']['Driver'] != self.parameters.ipam_driver:
                differences.add('ipam_driver',
                                parameter=self.parameters.ipam_driver,
                                active=net.get('IPAM'))

        if self.parameters.ipam_driver_options is not None:
            ipam_driver_options = net['IPAM'].get('Options') or {}
            if ipam_driver_options != self.parameters.ipam_driver_options:
                differences.add('ipam_driver_options',
                                parameter=self.parameters.ipam_driver_options,
                                active=ipam_driver_options)

        if self.parameters.ipam_config is not None and self.parameters.ipam_config:
            if not net.get('IPAM') or not net['IPAM']['Config']:
                differences.add('ipam_config',
                                parameter=self.parameters.ipam_config,
                                active=net.get('IPAM', {}).get('Config'))
            else:
                # Put network's IPAM config into the same format as module's IPAM config
                net_ipam_configs = []
                for net_ipam_config in net['IPAM']['Config']:
                    config = dict()
                    for k, v in net_ipam_config.items():
                        config[normalize_ipam_config_key(k)] = v
                    net_ipam_configs.append(config)
                # Compare lists of dicts as sets of dicts
                for idx, ipam_config in enumerate(self.parameters.ipam_config):
                    net_config = dict()
                    for net_ipam_config in net_ipam_configs:
                        if dicts_are_essentially_equal(ipam_config, net_ipam_config):
                            net_config = net_ipam_config
                            break
                    for key, value in ipam_config.items():
                        if value is None:
                            # due to recursive argument_spec, all keys are always present
                            # (but have default value None if not specified)
                            continue
                        if value != net_config.get(key):
                            differences.add('ipam_config[%s].%s' % (idx, key),
                                            parameter=value,
                                            active=net_config.get(key))

        if self.parameters.enable_ipv6 is not None and self.parameters.enable_ipv6 != net.get('EnableIPv6', False):
            differences.add('enable_ipv6',
                            parameter=self.parameters.enable_ipv6,
                            active=net.get('EnableIPv6', False))

        if self.parameters.internal is not None and self.parameters.internal != net.get('Internal', False):
            differences.add('internal',
                            parameter=self.parameters.internal,
                            active=net.get('Internal'))

        if self.parameters.scope is not None and self.parameters.scope != net.get('Scope'):
            differences.add('scope',
                            parameter=self.parameters.scope,
                            active=net.get('Scope'))

        if self.parameters.attachable is not None and self.parameters.attachable != net.get('Attachable', False):
            differences.add('attachable',
                            parameter=self.parameters.attachable,
                            active=net.get('Attachable'))
        if self.parameters.labels:
            if not net.get('Labels'):
                differences.add('labels',
                                parameter=self.parameters.labels,
                                active=net.get('Labels'))
            else:
                for key, value in self.parameters.labels.items():
                    if not (key in net['Labels']) or value != net['Labels'][key]:
                        differences.add('labels.%s' % key,
                                        parameter=value,
                                        active=net['Labels'].get(key))

        return not differences.empty, differences

    def create_network(self):
        if not self.existing_network:
            data = {
                'Name': self.parameters.name,
                'Driver': self.parameters.driver,
                'Options': self.parameters.driver_options,
                'IPAM': None,
                'CheckDuplicate': None,
            }

            if self.parameters.enable_ipv6:
                data['EnableIPv6'] = True
            if self.parameters.internal:
                data['Internal'] = True
            if self.parameters.scope is not None:
                data['Scope'] = self.parameters.scope
            if self.parameters.attachable is not None:
                data['Attachable'] = self.parameters.attachable
            if self.parameters.labels is not None:
                data["Labels"] = self.parameters.labels

            ipam_pools = []
            if self.parameters.ipam_config:
                for ipam_pool in self.parameters.ipam_config:
                    ipam_pools.append({
                        'Subnet': ipam_pool['subnet'],
                        'IPRange': ipam_pool['iprange'],
                        'Gateway': ipam_pool['gateway'],
                        'AuxiliaryAddresses': ipam_pool['aux_addresses'],
                    })

            if self.parameters.ipam_driver or self.parameters.ipam_driver_options or ipam_pools:
                # Only add IPAM if a driver was specified or if IPAM parameters were
                # specified. Leaving this parameter out can significantly speed up
                # creation; on my machine creation with this option needs ~15 seconds,
                # and without just a few seconds.
                data['IPAM'] = {
                    'Driver': self.parameters.ipam_driver,
                    'Config': ipam_pools or [],
                    'Options': self.parameters.ipam_driver_options,
                }

            if not self.check_mode:
                resp = self.client.post_json_to_json('/networks/create', data=data)
                self.client.report_warnings(resp, ['Warning'])
                self.existing_network = self.client.get_network(network_id=resp['Id'])
            self.results['actions'].append("Created network %s with driver %s" % (self.parameters.name, self.parameters.driver))
            self.results['changed'] = True

    def remove_network(self):
        if self.existing_network:
            self.disconnect_all_containers()
            if not self.check_mode:
                self.client.delete_call('/networks/{0}', self.parameters.name)
            self.results['actions'].append("Removed network %s" % (self.parameters.name,))
            self.results['changed'] = True

    def is_container_connected(self, container_name):
        if not self.existing_network:
            return False
        return container_name in container_names_in_network(self.existing_network)

    def connect_containers(self):
        for name in self.parameters.connected:
            if not self.is_container_connected(name):
                if not self.check_mode:
                    data = {
                        "Container": name,
                        "EndpointConfig": None,
                    }
                    self.client.post_json('/networks/{0}/connect', self.parameters.name, data=data)
                self.results['actions'].append("Connected container %s" % (name,))
                self.results['changed'] = True
                self.diff_tracker.add('connected.{0}'.format(name), parameter=True, active=False)

    def disconnect_missing(self):
        if not self.existing_network:
            return
        containers = self.existing_network['Containers']
        if not containers:
            return
        for c in containers.values():
            name = c['Name']
            if name not in self.parameters.connected:
                self.disconnect_container(name)

    def disconnect_all_containers(self):
        containers = self.client.get_network(name=self.parameters.name)['Containers']
        if not containers:
            return
        for cont in containers.values():
            self.disconnect_container(cont['Name'])

    def disconnect_container(self, container_name):
        if not self.check_mode:
            data = {"Container": container_name}
            self.client.post_json('/networks/{0}/disconnect', self.parameters.name, data=data)
        self.results['actions'].append("Disconnected container %s" % (container_name,))
        self.results['changed'] = True
        self.diff_tracker.add('connected.{0}'.format(container_name),
                              parameter=False,
                              active=True)

    def present(self):
        different = False
        differences = DifferenceTracker()
        if self.existing_network:
            different, differences = self.has_different_config(self.existing_network)

        self.diff_tracker.add('exists', parameter=True, active=self.existing_network is not None)
        if self.parameters.force or different:
            self.remove_network()
            self.existing_network = None

        self.create_network()
        self.connect_containers()
        if not self.parameters.appends:
            self.disconnect_missing()

        if self.diff or self.check_mode or self.parameters.debug:
            self.diff_result['differences'] = differences.get_legacy_docker_diffs()
            self.diff_tracker.merge(differences)

        if not self.check_mode and not self.parameters.debug:
            self.results.pop('actions')

        network_facts = self.get_existing_network()
        self.results['network'] = network_facts

    def absent(self):
        self.diff_tracker.add('exists', parameter=False, active=self.existing_network is not None)
        self.remove_network()


def main():
    argument_spec = dict(
        name=dict(type='str', required=True, aliases=['network_name']),
        connected=dict(type='list', default=[], elements='str', aliases=['containers']),
        state=dict(type='str', default='present', choices=['present', 'absent']),
        driver=dict(type='str', default='bridge'),
        driver_options=dict(type='dict', default={}),
        force=dict(type='bool', default=False),
        appends=dict(type='bool', default=False, aliases=['incremental']),
        ipam_driver=dict(type='str'),
        ipam_driver_options=dict(type='dict'),
        ipam_config=dict(type='list', elements='dict', options=dict(
            subnet=dict(type='str'),
            iprange=dict(type='str'),
            gateway=dict(type='str'),
            aux_addresses=dict(type='dict'),
        )),
        enable_ipv6=dict(type='bool'),
        internal=dict(type='bool'),
        labels=dict(type='dict', default={}),
        debug=dict(type='bool', default=False),
        scope=dict(type='str', choices=['local', 'global', 'swarm']),
        attachable=dict(type='bool'),
    )

    option_minimal_versions = dict(
        scope=dict(docker_api_version='1.30'),
        attachable=dict(docker_api_version='1.26'),
    )

    client = AnsibleDockerClient(
        argument_spec=argument_spec,
        supports_check_mode=True,
        # "The docker server >= 1.10.0"
        option_minimal_versions=option_minimal_versions,
    )

    try:
        cm = DockerNetworkManager(client)
        client.module.exit_json(**cm.results)
    except DockerException as e:
        client.fail('An unexpected Docker error occurred: {0}'.format(to_native(e)), exception=traceback.format_exc())
    except RequestException as e:
        client.fail(
            'An unexpected requests error occurred when trying to talk to the Docker daemon: {0}'.format(to_native(e)),
            exception=traceback.format_exc())


if __name__ == '__main__':
    main()
