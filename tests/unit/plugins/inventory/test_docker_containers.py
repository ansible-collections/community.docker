# Copyright (c), Felix Fontein <felix@fontein.de>, 2020
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import json
import textwrap

import pytest

from ansible_collections.community.docker.tests.unit.compat.mock import MagicMock

from ansible import constants as C
from ansible.errors import AnsibleError
from ansible.inventory.data import InventoryData
from ansible.inventory.manager import InventoryManager

from ansible_collections.community.docker.plugins.inventory.docker_containers import InventoryModule


@pytest.fixture(scope="module")
def inventory():
    r = InventoryModule()
    r.inventory = InventoryData()
    return r


LOVING_THARP = {
    'Id': '7bd547963679e3209cafd52aff21840b755c96fd37abcd7a6e19da8da6a7f49a',
    'Name': '/loving_tharp',
    'Image': 'sha256:349f492ff18add678364a62a67ce9a13487f14293ae0af1baf02398aa432f385',
    'State': {
        'Running': True,
    },
    'Config': {
        'Image': 'quay.io/ansible/ubuntu1804-test-container:1.21.0',
    },
}


LOVING_THARP_STACK = {
    'Id': '7bd547963679e3209cafd52aff21840b755c96fd37abcd7a6e19da8da6a7f49a',
    'Name': '/loving_tharp',
    'Image': 'sha256:349f492ff18add678364a62a67ce9a13487f14293ae0af1baf02398aa432f385',
    'State': {
        'Running': True,
    },
    'Config': {
        'Image': 'quay.io/ansible/ubuntu1804-test-container:1.21.0',
        'Labels': {
            'com.docker.stack.namespace': 'my_stack',
        },
    },
    'NetworkSettings': {
        'Ports': {
            '22/tcp': [
                {
                    'HostIp': '0.0.0.0',
                    'HostPort': '32802'
                }
            ],
        },
    },
}


LOVING_THARP_SERVICE = {
    'Id': '7bd547963679e3209cafd52aff21840b755c96fd37abcd7a6e19da8da6a7f49a',
    'Name': '/loving_tharp',
    'Image': 'sha256:349f492ff18add678364a62a67ce9a13487f14293ae0af1baf02398aa432f385',
    'State': {
        'Running': True,
    },
    'Config': {
        'Image': 'quay.io/ansible/ubuntu1804-test-container:1.21.0',
        'Labels': {
            'com.docker.swarm.service.name': 'my_service',
        },
    },
}


def create_get_option(options, default=False):
    def get_option(option):
        if option in options:
            return options[option]
        return default

    return get_option


class FakeClient(object):
    def __init__(self, *hosts):
        self.get_results = {}
        list_reply = []
        for host in hosts:
            list_reply.append({
                'Id': host['Id'],
                'Names': [host['Name']] if host['Name'] else [],
                'Image': host['Config']['Image'],
                'ImageId': host['Image'],
            })
            self.get_results['/containers/{0}/json'.format(host['Name'])] = host
            self.get_results['/containers/{0}/json'.format(host['Id'])] = host
        self.get_results['/containers/json'] = list_reply

    def get_json(self, url, *param, **kwargs):
        url = url.format(*param)
        return self.get_results[url]


def test_populate(inventory, mocker):
    client = FakeClient(LOVING_THARP)

    inventory.get_option = mocker.MagicMock(side_effect=create_get_option({
        'verbose_output': True,
        'connection_type': 'docker-api',
        'add_legacy_groups': False,
        'compose': {},
        'groups': {},
        'keyed_groups': {},
    }))
    inventory._populate(client)

    host_1 = inventory.inventory.get_host('loving_tharp')
    host_1_vars = host_1.get_vars()

    assert host_1_vars['ansible_host'] == 'loving_tharp'
    assert host_1_vars['ansible_connection'] == 'community.docker.docker_api'
    assert 'ansible_ssh_host' not in host_1_vars
    assert 'ansible_ssh_port' not in host_1_vars
    assert 'docker_state' in host_1_vars
    assert 'docker_config' in host_1_vars
    assert 'docker_image' in host_1_vars

    assert len(inventory.inventory.groups['ungrouped'].hosts) == 0
    assert len(inventory.inventory.groups['all'].hosts) == 0
    assert len(inventory.inventory.groups) == 2
    assert len(inventory.inventory.hosts) == 1


def test_populate_service(inventory, mocker):
    client = FakeClient(LOVING_THARP_SERVICE)

    inventory.get_option = mocker.MagicMock(side_effect=create_get_option({
        'verbose_output': False,
        'connection_type': 'docker-cli',
        'add_legacy_groups': True,
        'compose': {},
        'groups': {},
        'keyed_groups': {},
        'docker_host': 'unix://var/run/docker.sock',
    }))
    inventory._populate(client)

    host_1 = inventory.inventory.get_host('loving_tharp')
    host_1_vars = host_1.get_vars()

    assert host_1_vars['ansible_host'] == 'loving_tharp'
    assert host_1_vars['ansible_connection'] == 'community.docker.docker'
    assert 'ansible_ssh_host' not in host_1_vars
    assert 'ansible_ssh_port' not in host_1_vars
    assert 'docker_state' not in host_1_vars
    assert 'docker_config' not in host_1_vars
    assert 'docker_image' not in host_1_vars

    assert len(inventory.inventory.groups['ungrouped'].hosts) == 0
    assert len(inventory.inventory.groups['all'].hosts) == 0
    assert len(inventory.inventory.groups['7bd547963679e'].hosts) == 1
    assert len(inventory.inventory.groups['7bd547963679e3209cafd52aff21840b755c96fd37abcd7a6e19da8da6a7f49a'].hosts) == 1
    assert len(inventory.inventory.groups['image_quay.io/ansible/ubuntu1804-test-container:1.21.0'].hosts) == 1
    assert len(inventory.inventory.groups['loving_tharp'].hosts) == 1
    assert len(inventory.inventory.groups['running'].hosts) == 1
    assert len(inventory.inventory.groups['stopped'].hosts) == 0
    assert len(inventory.inventory.groups['service_my_service'].hosts) == 1
    assert len(inventory.inventory.groups['unix://var/run/docker.sock'].hosts) == 1
    assert len(inventory.inventory.groups) == 10
    assert len(inventory.inventory.hosts) == 1


def test_populate_stack(inventory, mocker):
    client = FakeClient(LOVING_THARP_STACK)

    inventory.get_option = mocker.MagicMock(side_effect=create_get_option({
        'verbose_output': False,
        'connection_type': 'ssh',
        'add_legacy_groups': True,
        'compose': {},
        'groups': {},
        'keyed_groups': {},
        'docker_host': 'unix://var/run/docker.sock',
        'default_ip': '127.0.0.1',
        'private_ssh_port': 22,
    }))
    inventory._populate(client)

    host_1 = inventory.inventory.get_host('loving_tharp')
    host_1_vars = host_1.get_vars()

    assert host_1_vars['ansible_ssh_host'] == '127.0.0.1'
    assert host_1_vars['ansible_ssh_port'] == '32802'
    assert 'ansible_host' not in host_1_vars
    assert 'ansible_connection' not in host_1_vars
    assert 'docker_state' not in host_1_vars
    assert 'docker_config' not in host_1_vars
    assert 'docker_image' not in host_1_vars

    assert len(inventory.inventory.groups['ungrouped'].hosts) == 0
    assert len(inventory.inventory.groups['all'].hosts) == 0
    assert len(inventory.inventory.groups['7bd547963679e'].hosts) == 1
    assert len(inventory.inventory.groups['7bd547963679e3209cafd52aff21840b755c96fd37abcd7a6e19da8da6a7f49a'].hosts) == 1
    assert len(inventory.inventory.groups['image_quay.io/ansible/ubuntu1804-test-container:1.21.0'].hosts) == 1
    assert len(inventory.inventory.groups['loving_tharp'].hosts) == 1
    assert len(inventory.inventory.groups['running'].hosts) == 1
    assert len(inventory.inventory.groups['stopped'].hosts) == 0
    assert len(inventory.inventory.groups['stack_my_stack'].hosts) == 1
    assert len(inventory.inventory.groups['unix://var/run/docker.sock'].hosts) == 1
    assert len(inventory.inventory.groups) == 10
    assert len(inventory.inventory.hosts) == 1
