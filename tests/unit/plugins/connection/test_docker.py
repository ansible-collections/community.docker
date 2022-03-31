# (c) 2020 Red Hat, Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from io import StringIO
import pytest

from ansible_collections.community.docker.tests.unit.compat import mock
from ansible_collections.community.docker.tests.unit.compat import unittest
from ansible.errors import AnsibleError
from ansible.playbook.play_context import PlayContext
from ansible_collections.community.docker.plugins.connection.docker import Connection as DockerConnection
from ansible.plugins.loader import connection_loader


class TestDockerConnectionClass(unittest.TestCase):

    def setUp(self):
        self.play_context = PlayContext()
        self.play_context.prompt = (
            '[sudo via ansible, key=ouzmdnewuhucvuaabtjmweasarviygqq] password: '
        )
        self.in_stream = StringIO()
        self.mock_get_bin_path = mock.patch(
            'ansible_collections.community.docker.plugins.connection.docker.get_bin_path', return_value='docker')
        self.mock_get_bin_path.start()
        dc = connection_loader.get('community.docker.docker', self.play_context, self.in_stream)

    def tearDown(self):
        pass

    @mock.patch('ansible_collections.community.docker.plugins.connection.docker.Connection._old_docker_version',
                return_value=('false', 'garbage', '', 1))
    @mock.patch('ansible_collections.community.docker.plugins.connection.docker.Connection._new_docker_version',
                return_value=('docker version', '1.2.3', '', 0))
    def test_docker_connection_module_too_old(self, mock_new_docker_verison, mock_old_docker_version):
        connection = connection_loader.get(
            'community.docker.docker', self.play_context, self.in_stream, docker_command='/fake/docker')
        self.assertRaisesRegexp(
            AnsibleError, '^docker connection type requires docker 1.3 or higher$', connection._connect)

    @mock.patch('ansible_collections.community.docker.plugins.connection.docker.Connection._old_docker_version',
                return_value=('false', 'garbage', '', 1))
    @mock.patch('ansible_collections.community.docker.plugins.connection.docker.Connection._new_docker_version',
                return_value=('docker version', '1.3.4', '', 0))
    def test_docker_connection_module(self, mock_new_docker_verison, mock_old_docker_version):
        connection = connection_loader.get(
            'community.docker.docker', self.play_context, self.in_stream, docker_command='/fake/docker')
        self.assertIsInstance(connection, DockerConnection)
        connection._connect()

    # old version and new version fail
    @mock.patch('ansible_collections.community.docker.plugins.connection.docker.Connection._old_docker_version',
                return_value=('false', 'garbage', '', 1))
    @mock.patch('ansible_collections.community.docker.plugins.connection.docker.Connection._new_docker_version',
                return_value=('false', 'garbage', '', 1))
    def test_docker_connection_module_wrong_cmd(self, mock_new_docker_version, mock_old_docker_version):
        connection = connection_loader.get(
            'community.docker.docker', self.play_context, self.in_stream, docker_command='/fake/docker')
        self.assertRaisesRegexp(
            AnsibleError, '^Docker version check (.*?) failed: ', connection._connect)
