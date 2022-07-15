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

from ansible_collections.community.docker.plugins.module_utils._api.api.client import APIClient
from ansible_collections.community.docker.plugins.module_utils._api.constants import DEFAULT_DOCKER_API_VERSION
from ansible_collections.community.docker.plugins.module_utils._api.utils.decorators import update_headers


class DecoratorsTest(unittest.TestCase):
    def test_update_headers(self):
        sample_headers = {
            'X-Docker-Locale': 'en-US',
        }

        def f(self, headers=None):
            return headers

        client = APIClient(version=DEFAULT_DOCKER_API_VERSION)
        client._general_configs = {}

        g = update_headers(f)
        assert g(client, headers=None) is None
        assert g(client, headers={}) == {}
        assert g(client, headers={'Content-type': 'application/json'}) == {
            'Content-type': 'application/json',
        }

        client._general_configs = {
            'HttpHeaders': sample_headers
        }

        assert g(client, headers=None) == sample_headers
        assert g(client, headers={}) == sample_headers
        assert g(client, headers={'Content-type': 'application/json'}) == {
            'Content-type': 'application/json',
            'X-Docker-Locale': 'en-US',
        }
