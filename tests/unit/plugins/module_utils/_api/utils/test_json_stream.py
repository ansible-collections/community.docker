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

import sys

import pytest

if sys.version_info < (2, 7):
    pytestmark = pytest.mark.skip('Python 2.6 is not supported')

from ansible_collections.community.docker.plugins.module_utils._api.utils.json_stream import json_splitter, stream_as_text, json_stream


class TestJsonSplitter:

    def test_json_splitter_no_object(self):
        data = '{"foo": "bar'
        assert json_splitter(data) is None

    def test_json_splitter_with_object(self):
        data = '{"foo": "bar"}\n  \n{"next": "obj"}'
        assert json_splitter(data) == ({'foo': 'bar'}, '{"next": "obj"}')

    def test_json_splitter_leading_whitespace(self):
        data = '\n   \r{"foo": "bar"}\n\n   {"next": "obj"}'
        assert json_splitter(data) == ({'foo': 'bar'}, '{"next": "obj"}')


class TestStreamAsText:

    def test_stream_with_non_utf_unicode_character(self):
        stream = [b'\xed\xf3\xf3']
        output, = stream_as_text(stream)
        assert output == u'���'

    def test_stream_with_utf_character(self):
        stream = [u'ěĝ'.encode('utf-8')]
        output, = stream_as_text(stream)
        assert output == u'ěĝ'


class TestJsonStream:

    def test_with_falsy_entries(self):
        stream = [
            '{"one": "two"}\n{}\n',
            "[1, 2, 3]\n[]\n",
        ]
        output = list(json_stream(stream))
        assert output == [
            {'one': 'two'},
            {},
            [1, 2, 3],
            [],
        ]

    def test_with_leading_whitespace(self):
        stream = [
            '\n  \r\n  {"one": "two"}{"x": 1}',
            '  {"three": "four"}\t\t{"x": 2}'
        ]
        output = list(json_stream(stream))
        assert output == [
            {'one': 'two'},
            {'x': 1},
            {'three': 'four'},
            {'x': 2}
        ]
