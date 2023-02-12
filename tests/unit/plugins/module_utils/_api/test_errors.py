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
import requests

if sys.version_info < (2, 7):
    pytestmark = pytest.mark.skip('Python 2.6 is not supported')

from ansible_collections.community.docker.plugins.module_utils._api.errors import (
    APIError, DockerException,
    create_unexpected_kwargs_error,
    create_api_error_from_http_exception,
)


class APIErrorTest(unittest.TestCase):
    def test_api_error_is_caught_by_dockerexception(self):
        try:
            raise APIError("this should be caught by DockerException")
        except DockerException:
            pass

    def test_status_code_200(self):
        """The status_code property is present with 200 response."""
        resp = requests.Response()
        resp.status_code = 200
        err = APIError('', response=resp)
        assert err.status_code == 200

    def test_status_code_400(self):
        """The status_code property is present with 400 response."""
        resp = requests.Response()
        resp.status_code = 400
        err = APIError('', response=resp)
        assert err.status_code == 400

    def test_status_code_500(self):
        """The status_code property is present with 500 response."""
        resp = requests.Response()
        resp.status_code = 500
        err = APIError('', response=resp)
        assert err.status_code == 500

    def test_is_server_error_200(self):
        """Report not server error on 200 response."""
        resp = requests.Response()
        resp.status_code = 200
        err = APIError('', response=resp)
        assert err.is_server_error() is False

    def test_is_server_error_300(self):
        """Report not server error on 300 response."""
        resp = requests.Response()
        resp.status_code = 300
        err = APIError('', response=resp)
        assert err.is_server_error() is False

    def test_is_server_error_400(self):
        """Report not server error on 400 response."""
        resp = requests.Response()
        resp.status_code = 400
        err = APIError('', response=resp)
        assert err.is_server_error() is False

    def test_is_server_error_500(self):
        """Report server error on 500 response."""
        resp = requests.Response()
        resp.status_code = 500
        err = APIError('', response=resp)
        assert err.is_server_error() is True

    def test_is_client_error_500(self):
        """Report not client error on 500 response."""
        resp = requests.Response()
        resp.status_code = 500
        err = APIError('', response=resp)
        assert err.is_client_error() is False

    def test_is_client_error_400(self):
        """Report client error on 400 response."""
        resp = requests.Response()
        resp.status_code = 400
        err = APIError('', response=resp)
        assert err.is_client_error() is True

    def test_is_error_300(self):
        """Report no error on 300 response."""
        resp = requests.Response()
        resp.status_code = 300
        err = APIError('', response=resp)
        assert err.is_error() is False

    def test_is_error_400(self):
        """Report error on 400 response."""
        resp = requests.Response()
        resp.status_code = 400
        err = APIError('', response=resp)
        assert err.is_error() is True

    def test_is_error_500(self):
        """Report error on 500 response."""
        resp = requests.Response()
        resp.status_code = 500
        err = APIError('', response=resp)
        assert err.is_error() is True

    def test_create_error_from_exception(self):
        resp = requests.Response()
        resp.status_code = 500
        err = APIError('')
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                create_api_error_from_http_exception(e)
            except APIError as e:
                err = e
        assert err.is_server_error() is True


class CreateUnexpectedKwargsErrorTest(unittest.TestCase):
    def test_create_unexpected_kwargs_error_single(self):
        e = create_unexpected_kwargs_error('f', {'foo': 'bar'})
        assert str(e) == "f() got an unexpected keyword argument 'foo'"

    def test_create_unexpected_kwargs_error_multiple(self):
        e = create_unexpected_kwargs_error('f', {'foo': 'bar', 'baz': 'bosh'})
        assert str(e) == "f() got unexpected keyword arguments 'baz', 'foo'"
