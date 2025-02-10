# -*- coding: utf-8 -*-
# This code is part of the Ansible collection community.docker, but is an independent component.
# This particular file, and this file only, is based on the Docker SDK for Python (https://github.com/docker/docker-py/)
#
# Copyright (c) 2016-2025 Docker, Inc.
#
# It is licensed under the Apache 2.0 license (see LICENSES/Apache-2.0.txt in this collection)
# SPDX-License-Identifier: Apache-2.0

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest

import pytest

from ansible_collections.community.docker.plugins.module_utils._api import errors
from ansible_collections.community.docker.plugins.module_utils._api.constants import (
    DEFAULT_NPIPE,
    DEFAULT_UNIX_SOCKET,
    IS_WINDOWS_PLATFORM,
)
from ansible_collections.community.docker.plugins.module_utils._api.context.api import ContextAPI
from ansible_collections.community.docker.plugins.module_utils._api.context.context import Context


class BaseContextTest(unittest.TestCase):
    @pytest.mark.skipif(
        IS_WINDOWS_PLATFORM, reason='Linux specific path check'
    )
    def test_url_compatibility_on_linux(self):
        c = Context("test")
        assert c.Host == DEFAULT_UNIX_SOCKET[5:]

    @pytest.mark.skipif(
        not IS_WINDOWS_PLATFORM, reason='Windows specific path check'
    )
    def test_url_compatibility_on_windows(self):
        c = Context("test")
        assert c.Host == DEFAULT_NPIPE

    def test_fail_on_default_context_create(self):
        with pytest.raises(errors.ContextException):
            ContextAPI.create_context("default")

    def test_default_in_context_list(self):
        found = False
        ctx = ContextAPI.contexts()
        for c in ctx:
            if c.Name == "default":
                found = True
        assert found is True

    def test_get_current_context(self):
        assert ContextAPI.get_current_context().Name == "default"

    def test_https_host(self):
        c = Context("test", host="tcp://testdomain:8080", tls=True)
        assert c.Host == "https://testdomain:8080"

    def test_context_inspect_without_params(self):
        ctx = ContextAPI.inspect_context()
        assert ctx["Name"] == "default"
        assert ctx["Metadata"]["StackOrchestrator"] == "swarm"
        assert ctx["Endpoints"]["docker"]["Host"] in (
            DEFAULT_NPIPE,
            DEFAULT_UNIX_SOCKET[5:],
        )
