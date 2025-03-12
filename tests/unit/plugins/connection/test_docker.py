# Copyright (c) 2020 Red Hat, Inc.
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from io import StringIO

from ansible_collections.community.internal_test_tools.tests.unit.compat import mock
from ansible_collections.community.internal_test_tools.tests.unit.compat import unittest

from ansible.errors import AnsibleError
from ansible.playbook.play_context import PlayContext
from ansible.plugins.loader import connection_loader
from ansible.module_utils.six import PY2


class TestDockerConnectionClass(unittest.TestCase):

    def setUp(self):
        self.play_context = PlayContext()
        self.play_context.prompt = (
            '[sudo via ansible, key=ouzmdnewuhucvuaabtjmweasarviygqq] password: '
        )
        self.in_stream = StringIO()
        with mock.patch('ansible_collections.community.docker.plugins.connection.docker.get_bin_path', return_value='docker'):
            self.dc = connection_loader.get('community.docker.docker', self.play_context, self.in_stream)

    def tearDown(self):
        pass

    @mock.patch('ansible_collections.community.docker.plugins.connection.docker.Connection._old_docker_version',
                return_value=('false', 'garbage', '', 1))
    @mock.patch('ansible_collections.community.docker.plugins.connection.docker.Connection._new_docker_version',
                return_value=('docker version', '1.2.3', '', 0))
    def test_docker_connection_module_too_old(self, mock_new_docker_version, mock_old_docker_version):
        self.dc._version = None
        self.dc.remote_user = 'foo'
        (self.assertRaisesRegexp if PY2 else self.assertRaisesRegex)(
            AnsibleError, '^docker connection type requires docker 1.3 or higher$', self.dc._get_actual_user)

    @mock.patch('ansible_collections.community.docker.plugins.connection.docker.Connection._old_docker_version',
                return_value=('false', 'garbage', '', 1))
    @mock.patch('ansible_collections.community.docker.plugins.connection.docker.Connection._new_docker_version',
                return_value=('docker version', '1.7.0', '', 0))
    def test_docker_connection_module(self, mock_new_docker_version, mock_old_docker_version):
        self.dc._version = None
        version = self.dc.docker_version

    # old version and new version fail
    @mock.patch('ansible_collections.community.docker.plugins.connection.docker.Connection._old_docker_version',
                return_value=('false', 'garbage', '', 1))
    @mock.patch('ansible_collections.community.docker.plugins.connection.docker.Connection._new_docker_version',
                return_value=('false', 'garbage', '', 1))
    def test_docker_connection_module_wrong_cmd(self, mock_new_docker_version, mock_old_docker_version):
        self.dc._version = None
        self.dc.remote_user = 'foo'
        (self.assertRaisesRegexp if PY2 else self.assertRaisesRegex)(
            AnsibleError, '^Docker version check (.*?) failed:', self.dc._get_actual_user)
