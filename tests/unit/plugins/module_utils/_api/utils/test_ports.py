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

from ansible_collections.community.docker.plugins.module_utils._api.utils.ports import build_port_bindings, split_port


class PortsTest(unittest.TestCase):
    def test_split_port_with_host_ip(self):
        internal_port, external_port = split_port("127.0.0.1:1000:2000")
        assert internal_port == ["2000"]
        assert external_port == [("127.0.0.1", "1000")]

    def test_split_port_with_protocol(self):
        for protocol in ['tcp', 'udp', 'sctp']:
            internal_port, external_port = split_port(
                "127.0.0.1:1000:2000/" + protocol
            )
            assert internal_port == ["2000/" + protocol]
            assert external_port == [("127.0.0.1", "1000")]

    def test_split_port_with_host_ip_no_port(self):
        internal_port, external_port = split_port("127.0.0.1::2000")
        assert internal_port == ["2000"]
        assert external_port == [("127.0.0.1", None)]

    def test_split_port_range_with_host_ip_no_port(self):
        internal_port, external_port = split_port("127.0.0.1::2000-2001")
        assert internal_port == ["2000", "2001"]
        assert external_port == [("127.0.0.1", None), ("127.0.0.1", None)]

    def test_split_port_with_host_port(self):
        internal_port, external_port = split_port("1000:2000")
        assert internal_port == ["2000"]
        assert external_port == ["1000"]

    def test_split_port_range_with_host_port(self):
        internal_port, external_port = split_port("1000-1001:2000-2001")
        assert internal_port == ["2000", "2001"]
        assert external_port == ["1000", "1001"]

    def test_split_port_random_port_range_with_host_port(self):
        internal_port, external_port = split_port("1000-1001:2000")
        assert internal_port == ["2000"]
        assert external_port == ["1000-1001"]

    def test_split_port_no_host_port(self):
        internal_port, external_port = split_port("2000")
        assert internal_port == ["2000"]
        assert external_port is None

    def test_split_port_range_no_host_port(self):
        internal_port, external_port = split_port("2000-2001")
        assert internal_port == ["2000", "2001"]
        assert external_port is None

    def test_split_port_range_with_protocol(self):
        internal_port, external_port = split_port(
            "127.0.0.1:1000-1001:2000-2001/udp")
        assert internal_port == ["2000/udp", "2001/udp"]
        assert external_port == [("127.0.0.1", "1000"), ("127.0.0.1", "1001")]

    def test_split_port_with_ipv6_address(self):
        internal_port, external_port = split_port(
            "2001:abcd:ef00::2:1000:2000")
        assert internal_port == ["2000"]
        assert external_port == [("2001:abcd:ef00::2", "1000")]

    def test_split_port_with_ipv6_square_brackets_address(self):
        internal_port, external_port = split_port(
            "[2001:abcd:ef00::2]:1000:2000")
        assert internal_port == ["2000"]
        assert external_port == [("2001:abcd:ef00::2", "1000")]

    def test_split_port_invalid(self):
        with pytest.raises(ValueError):
            split_port("0.0.0.0:1000:2000:tcp")

    def test_split_port_invalid_protocol(self):
        with pytest.raises(ValueError):
            split_port("0.0.0.0:1000:2000/ftp")

    def test_non_matching_length_port_ranges(self):
        with pytest.raises(ValueError):
            split_port("0.0.0.0:1000-1010:2000-2002/tcp")

    def test_port_and_range_invalid(self):
        with pytest.raises(ValueError):
            split_port("0.0.0.0:1000:2000-2002/tcp")

    def test_port_only_with_colon(self):
        with pytest.raises(ValueError):
            split_port(":80")

    def test_host_only_with_colon(self):
        with pytest.raises(ValueError):
            split_port("localhost:")

    def test_with_no_container_port(self):
        with pytest.raises(ValueError):
            split_port("localhost:80:")

    def test_split_port_empty_string(self):
        with pytest.raises(ValueError):
            split_port("")

    def test_split_port_non_string(self):
        assert split_port(1243) == (['1243'], None)

    def test_build_port_bindings_with_one_port(self):
        port_bindings = build_port_bindings(["127.0.0.1:1000:1000"])
        assert port_bindings["1000"] == [("127.0.0.1", "1000")]

    def test_build_port_bindings_with_matching_internal_ports(self):
        port_bindings = build_port_bindings(
            ["127.0.0.1:1000:1000", "127.0.0.1:2000:1000"])
        assert port_bindings["1000"] == [
            ("127.0.0.1", "1000"), ("127.0.0.1", "2000")
        ]

    def test_build_port_bindings_with_nonmatching_internal_ports(self):
        port_bindings = build_port_bindings(
            ["127.0.0.1:1000:1000", "127.0.0.1:2000:2000"])
        assert port_bindings["1000"] == [("127.0.0.1", "1000")]
        assert port_bindings["2000"] == [("127.0.0.1", "2000")]

    def test_build_port_bindings_with_port_range(self):
        port_bindings = build_port_bindings(["127.0.0.1:1000-1001:1000-1001"])
        assert port_bindings["1000"] == [("127.0.0.1", "1000")]
        assert port_bindings["1001"] == [("127.0.0.1", "1001")]

    def test_build_port_bindings_with_matching_internal_port_ranges(self):
        port_bindings = build_port_bindings(
            ["127.0.0.1:1000-1001:1000-1001", "127.0.0.1:2000-2001:1000-1001"])
        assert port_bindings["1000"] == [
            ("127.0.0.1", "1000"), ("127.0.0.1", "2000")
        ]
        assert port_bindings["1001"] == [
            ("127.0.0.1", "1001"), ("127.0.0.1", "2001")
        ]

    def test_build_port_bindings_with_nonmatching_internal_port_ranges(self):
        port_bindings = build_port_bindings(
            ["127.0.0.1:1000:1000", "127.0.0.1:2000:2000"])
        assert port_bindings["1000"] == [("127.0.0.1", "1000")]
        assert port_bindings["2000"] == [("127.0.0.1", "2000")]
