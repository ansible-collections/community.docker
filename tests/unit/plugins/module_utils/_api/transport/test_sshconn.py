# -*- coding: utf-8 -*-
# This code is part of the Ansible collection community.docker, but is an independent component.
# This particular file, and this file only, is based on the Docker SDK for Python (https://github.com/docker/docker-py/)
#
# Copyright (c) 2016-2022 Docker, Inc.
#
# It is licensed under the Apache 2.0 license (see LICENSES/Apache-2.0.txt in this collection)
# SPDX-License-Identifier: Apache-2.0

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest
import sys

import pytest

if sys.version_info < (2, 7):
    pytestmark = pytest.mark.skip('Python 2.6 is not supported')

from ansible_collections.community.docker.plugins.module_utils._api.transport.sshconn import SSHSocket, SSHHTTPAdapter


class SSHAdapterTest(unittest.TestCase):
    @staticmethod
    def test_ssh_hostname_prefix_trim():
        conn = SSHHTTPAdapter(
            base_url="ssh://user@hostname:1234", shell_out=True)
        assert conn.ssh_host == "user@hostname:1234"

    @staticmethod
    def test_ssh_parse_url():
        c = SSHSocket(host="user@hostname:1234")
        assert c.host == "hostname"
        assert c.port == "1234"
        assert c.user == "user"

    @staticmethod
    def test_ssh_parse_hostname_only():
        c = SSHSocket(host="hostname")
        assert c.host == "hostname"
        assert c.port is None
        assert c.user is None

    @staticmethod
    def test_ssh_parse_user_and_hostname():
        c = SSHSocket(host="user@hostname")
        assert c.host == "hostname"
        assert c.port is None
        assert c.user == "user"

    @staticmethod
    def test_ssh_parse_hostname_and_port():
        c = SSHSocket(host="hostname:22")
        assert c.host == "hostname"
        assert c.port == "22"
        assert c.user is None
