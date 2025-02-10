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

import base64
import json
import os
import os.path
import shutil
import tempfile
import unittest
import sys

from ansible.module_utils.six import PY3

import pytest

if sys.version_info < (2, 7):
    pytestmark = pytest.mark.skip('Python 2.6 is not supported')

from ansible_collections.community.docker.plugins.module_utils._api.api.client import APIClient
from ansible_collections.community.docker.plugins.module_utils._api.constants import IS_WINDOWS_PLATFORM
from ansible_collections.community.docker.plugins.module_utils._api.errors import DockerException
from ansible_collections.community.docker.plugins.module_utils._api.utils.utils import (
    convert_filters, convert_volume_binds,
    decode_json_header, kwargs_from_env, parse_bytes,
    parse_devices, parse_env_file, parse_host,
    parse_repository_tag, split_command, format_environment,
)
from ansible_collections.community.docker.tests.unit.plugins.module_utils._api.constants import DEFAULT_DOCKER_API_VERSION


TEST_CERT_DIR = os.path.join(
    os.path.dirname(__file__),
    'testdata/certs',
)


class KwargsFromEnvTest(unittest.TestCase):
    def setUp(self):
        self.os_environ = os.environ.copy()

    def tearDown(self):
        os.environ = self.os_environ

    def test_kwargs_from_env_empty(self):
        os.environ.update(DOCKER_HOST='',
                          DOCKER_CERT_PATH='')
        os.environ.pop('DOCKER_TLS_VERIFY', None)

        kwargs = kwargs_from_env()
        assert kwargs.get('base_url') is None
        assert kwargs.get('tls') is None

    def test_kwargs_from_env_tls(self):
        os.environ.update(DOCKER_HOST='tcp://192.168.59.103:2376',
                          DOCKER_CERT_PATH=TEST_CERT_DIR,
                          DOCKER_TLS_VERIFY='1')
        kwargs = kwargs_from_env(assert_hostname=False)
        assert 'tcp://192.168.59.103:2376' == kwargs['base_url']
        assert 'ca.pem' in kwargs['tls'].ca_cert
        assert 'cert.pem' in kwargs['tls'].cert[0]
        assert 'key.pem' in kwargs['tls'].cert[1]
        assert kwargs['tls'].assert_hostname is False
        assert kwargs['tls'].verify

        parsed_host = parse_host(kwargs['base_url'], IS_WINDOWS_PLATFORM, True)
        kwargs['version'] = DEFAULT_DOCKER_API_VERSION
        try:
            client = APIClient(**kwargs)
            assert parsed_host == client.base_url
            assert kwargs['tls'].ca_cert == client.verify
            assert kwargs['tls'].cert == client.cert
        except TypeError as e:
            self.fail(e)

    def test_kwargs_from_env_tls_verify_false(self):
        os.environ.update(DOCKER_HOST='tcp://192.168.59.103:2376',
                          DOCKER_CERT_PATH=TEST_CERT_DIR,
                          DOCKER_TLS_VERIFY='')
        kwargs = kwargs_from_env(assert_hostname=True)
        assert 'tcp://192.168.59.103:2376' == kwargs['base_url']
        assert 'ca.pem' in kwargs['tls'].ca_cert
        assert 'cert.pem' in kwargs['tls'].cert[0]
        assert 'key.pem' in kwargs['tls'].cert[1]
        assert kwargs['tls'].assert_hostname is True
        assert kwargs['tls'].verify is False
        parsed_host = parse_host(kwargs['base_url'], IS_WINDOWS_PLATFORM, True)
        kwargs['version'] = DEFAULT_DOCKER_API_VERSION
        try:
            client = APIClient(**kwargs)
            assert parsed_host == client.base_url
            assert kwargs['tls'].cert == client.cert
            assert not kwargs['tls'].verify
        except TypeError as e:
            self.fail(e)

    def test_kwargs_from_env_tls_verify_false_no_cert(self):
        temp_dir = tempfile.mkdtemp()
        cert_dir = os.path.join(temp_dir, '.docker')
        shutil.copytree(TEST_CERT_DIR, cert_dir)

        os.environ.update(DOCKER_HOST='tcp://192.168.59.103:2376',
                          HOME=temp_dir,
                          DOCKER_TLS_VERIFY='')
        os.environ.pop('DOCKER_CERT_PATH', None)
        kwargs = kwargs_from_env(assert_hostname=True)
        assert 'tcp://192.168.59.103:2376' == kwargs['base_url']

    def test_kwargs_from_env_no_cert_path(self):
        try:
            temp_dir = tempfile.mkdtemp()
            cert_dir = os.path.join(temp_dir, '.docker')
            shutil.copytree(TEST_CERT_DIR, cert_dir)

            os.environ.update(HOME=temp_dir,
                              DOCKER_CERT_PATH='',
                              DOCKER_TLS_VERIFY='1')

            kwargs = kwargs_from_env()
            assert kwargs['tls'].verify
            assert cert_dir in kwargs['tls'].ca_cert
            assert cert_dir in kwargs['tls'].cert[0]
            assert cert_dir in kwargs['tls'].cert[1]
        finally:
            if temp_dir:
                shutil.rmtree(temp_dir)

    def test_kwargs_from_env_alternate_env(self):
        # Values in os.environ are entirely ignored if an alternate is
        # provided
        os.environ.update(
            DOCKER_HOST='tcp://192.168.59.103:2376',
            DOCKER_CERT_PATH=TEST_CERT_DIR,
            DOCKER_TLS_VERIFY=''
        )
        kwargs = kwargs_from_env(environment={
            'DOCKER_HOST': 'http://docker.gensokyo.jp:2581',
        })
        assert 'http://docker.gensokyo.jp:2581' == kwargs['base_url']
        assert 'tls' not in kwargs


class ConverVolumeBindsTest(unittest.TestCase):
    def test_convert_volume_binds_empty(self):
        assert convert_volume_binds({}) == []
        assert convert_volume_binds([]) == []

    def test_convert_volume_binds_list(self):
        data = ['/a:/a:ro', '/b:/c:z']
        assert convert_volume_binds(data) == data

    def test_convert_volume_binds_complete(self):
        data = {
            '/mnt/vol1': {
                'bind': '/data',
                'mode': 'ro'
            }
        }
        assert convert_volume_binds(data) == ['/mnt/vol1:/data:ro']

    def test_convert_volume_binds_compact(self):
        data = {
            '/mnt/vol1': '/data'
        }
        assert convert_volume_binds(data) == ['/mnt/vol1:/data:rw']

    def test_convert_volume_binds_no_mode(self):
        data = {
            '/mnt/vol1': {
                'bind': '/data'
            }
        }
        assert convert_volume_binds(data) == ['/mnt/vol1:/data:rw']

    def test_convert_volume_binds_unicode_bytes_input(self):
        expected = [u'/mnt/지연:/unicode/박:rw']

        data = {
            u'/mnt/지연'.encode('utf-8'): {
                'bind': u'/unicode/박'.encode('utf-8'),
                'mode': u'rw'
            }
        }
        assert convert_volume_binds(data) == expected

    def test_convert_volume_binds_unicode_unicode_input(self):
        expected = [u'/mnt/지연:/unicode/박:rw']

        data = {
            u'/mnt/지연': {
                'bind': u'/unicode/박',
                'mode': u'rw'
            }
        }
        assert convert_volume_binds(data) == expected


class ParseEnvFileTest(unittest.TestCase):
    def generate_tempfile(self, file_content=None):
        """
        Generates a temporary file for tests with the content
        of 'file_content' and returns the filename.
        Don't forget to unlink the file with os.unlink() after.
        """
        local_tempfile = tempfile.NamedTemporaryFile(delete=False)
        local_tempfile.write(file_content.encode('UTF-8'))
        local_tempfile.close()
        return local_tempfile.name

    def test_parse_env_file_proper(self):
        env_file = self.generate_tempfile(
            file_content='USER=jdoe\nPASS=secret')
        get_parse_env_file = parse_env_file(env_file)
        assert get_parse_env_file == {'USER': 'jdoe', 'PASS': 'secret'}
        os.unlink(env_file)

    def test_parse_env_file_with_equals_character(self):
        env_file = self.generate_tempfile(
            file_content='USER=jdoe\nPASS=sec==ret')
        get_parse_env_file = parse_env_file(env_file)
        assert get_parse_env_file == {'USER': 'jdoe', 'PASS': 'sec==ret'}
        os.unlink(env_file)

    def test_parse_env_file_commented_line(self):
        env_file = self.generate_tempfile(
            file_content='USER=jdoe\n#PASS=secret')
        get_parse_env_file = parse_env_file(env_file)
        assert get_parse_env_file == {'USER': 'jdoe'}
        os.unlink(env_file)

    def test_parse_env_file_newline(self):
        env_file = self.generate_tempfile(
            file_content='\nUSER=jdoe\n\n\nPASS=secret')
        get_parse_env_file = parse_env_file(env_file)
        assert get_parse_env_file == {'USER': 'jdoe', 'PASS': 'secret'}
        os.unlink(env_file)

    def test_parse_env_file_invalid_line(self):
        env_file = self.generate_tempfile(
            file_content='USER jdoe')
        with pytest.raises(DockerException):
            parse_env_file(env_file)
        os.unlink(env_file)


class ParseHostTest(unittest.TestCase):
    def test_parse_host(self):
        invalid_hosts = [
            'foo://0.0.0.0',
            'tcp://',
            'udp://127.0.0.1',
            'udp://127.0.0.1:2375',
            'ssh://:22/path',
            'tcp://netloc:3333/path?q=1',
            'unix:///sock/path#fragment',
            'https://netloc:3333/path;params',
            'ssh://:clearpassword@host:22',
        ]

        valid_hosts = {
            '0.0.0.1:5555': 'http://0.0.0.1:5555',
            ':6666': 'http://127.0.0.1:6666',
            'tcp://:7777': 'http://127.0.0.1:7777',
            'http://:7777': 'http://127.0.0.1:7777',
            'https://kokia.jp:2375': 'https://kokia.jp:2375',
            'unix:///var/run/docker.sock': 'http+unix:///var/run/docker.sock',
            'unix://': 'http+unix:///var/run/docker.sock',
            '12.234.45.127:2375/docker/engine': (
                'http://12.234.45.127:2375/docker/engine'
            ),
            'somehost.net:80/service/swarm': (
                'http://somehost.net:80/service/swarm'
            ),
            'npipe:////./pipe/docker_engine': 'npipe:////./pipe/docker_engine',
            '[fd12::82d1]:2375': 'http://[fd12::82d1]:2375',
            'https://[fd12:5672::12aa]:1090': 'https://[fd12:5672::12aa]:1090',
            '[fd12::82d1]:2375/docker/engine': (
                'http://[fd12::82d1]:2375/docker/engine'
            ),
            'ssh://[fd12::82d1]': 'ssh://[fd12::82d1]:22',
            'ssh://user@[fd12::82d1]:8765': 'ssh://user@[fd12::82d1]:8765',
            'ssh://': 'ssh://127.0.0.1:22',
            'ssh://user@localhost:22': 'ssh://user@localhost:22',
            'ssh://user@remote': 'ssh://user@remote:22',
        }

        for host in invalid_hosts:
            msg = 'Should have failed to parse invalid host: {0}'.format(host)
            with self.assertRaises(DockerException, msg=msg):
                parse_host(host, None)

        for host, expected in valid_hosts.items():
            self.assertEqual(
                parse_host(host, None),
                expected,
                msg='Failed to parse valid host: {0}'.format(host),
            )

    def test_parse_host_empty_value(self):
        unix_socket = 'http+unix:///var/run/docker.sock'
        npipe = 'npipe:////./pipe/docker_engine'

        for val in [None, '']:
            assert parse_host(val, is_win32=False) == unix_socket
            assert parse_host(val, is_win32=True) == npipe

    def test_parse_host_tls(self):
        host_value = 'myhost.docker.net:3348'
        expected_result = 'https://myhost.docker.net:3348'
        assert parse_host(host_value, tls=True) == expected_result

    def test_parse_host_tls_tcp_proto(self):
        host_value = 'tcp://myhost.docker.net:3348'
        expected_result = 'https://myhost.docker.net:3348'
        assert parse_host(host_value, tls=True) == expected_result

    def test_parse_host_trailing_slash(self):
        host_value = 'tcp://myhost.docker.net:2376/'
        expected_result = 'http://myhost.docker.net:2376'
        assert parse_host(host_value) == expected_result


class ParseRepositoryTagTest(unittest.TestCase):
    sha = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

    def test_index_image_no_tag(self):
        assert parse_repository_tag("root") == ("root", None)

    def test_index_image_tag(self):
        assert parse_repository_tag("root:tag") == ("root", "tag")

    def test_index_user_image_no_tag(self):
        assert parse_repository_tag("user/repo") == ("user/repo", None)

    def test_index_user_image_tag(self):
        assert parse_repository_tag("user/repo:tag") == ("user/repo", "tag")

    def test_private_reg_image_no_tag(self):
        assert parse_repository_tag("url:5000/repo") == ("url:5000/repo", None)

    def test_private_reg_image_tag(self):
        assert parse_repository_tag("url:5000/repo:tag") == (
            "url:5000/repo", "tag"
        )

    def test_index_image_sha(self):
        assert parse_repository_tag("root@sha256:{sha}".format(sha=self.sha)) == (
            "root", "sha256:{sha}".format(sha=self.sha)
        )

    def test_private_reg_image_sha(self):
        assert parse_repository_tag(
            "url:5000/repo@sha256:{sha}".format(sha=self.sha)
        ) == ("url:5000/repo", "sha256:{sha}".format(sha=self.sha))


class ParseDeviceTest(unittest.TestCase):
    def test_dict(self):
        devices = parse_devices([{
            'PathOnHost': '/dev/sda1',
            'PathInContainer': '/dev/mnt1',
            'CgroupPermissions': 'r'
        }])
        assert devices[0] == {
            'PathOnHost': '/dev/sda1',
            'PathInContainer': '/dev/mnt1',
            'CgroupPermissions': 'r'
        }

    def test_partial_string_definition(self):
        devices = parse_devices(['/dev/sda1'])
        assert devices[0] == {
            'PathOnHost': '/dev/sda1',
            'PathInContainer': '/dev/sda1',
            'CgroupPermissions': 'rwm'
        }

    def test_permissionless_string_definition(self):
        devices = parse_devices(['/dev/sda1:/dev/mnt1'])
        assert devices[0] == {
            'PathOnHost': '/dev/sda1',
            'PathInContainer': '/dev/mnt1',
            'CgroupPermissions': 'rwm'
        }

    def test_full_string_definition(self):
        devices = parse_devices(['/dev/sda1:/dev/mnt1:r'])
        assert devices[0] == {
            'PathOnHost': '/dev/sda1',
            'PathInContainer': '/dev/mnt1',
            'CgroupPermissions': 'r'
        }

    def test_hybrid_list(self):
        devices = parse_devices([
            '/dev/sda1:/dev/mnt1:rw',
            {
                'PathOnHost': '/dev/sda2',
                'PathInContainer': '/dev/mnt2',
                'CgroupPermissions': 'r'
            }
        ])

        assert devices[0] == {
            'PathOnHost': '/dev/sda1',
            'PathInContainer': '/dev/mnt1',
            'CgroupPermissions': 'rw'
        }
        assert devices[1] == {
            'PathOnHost': '/dev/sda2',
            'PathInContainer': '/dev/mnt2',
            'CgroupPermissions': 'r'
        }


class ParseBytesTest(unittest.TestCase):
    def test_parse_bytes_valid(self):
        assert parse_bytes("512MB") == 536870912
        assert parse_bytes("512M") == 536870912
        assert parse_bytes("512m") == 536870912

    def test_parse_bytes_invalid(self):
        with pytest.raises(DockerException):
            parse_bytes("512MK")
        with pytest.raises(DockerException):
            parse_bytes("512L")
        with pytest.raises(DockerException):
            parse_bytes("127.0.0.1K")

    def test_parse_bytes_float(self):
        assert parse_bytes("1.5k") == 1536


class UtilsTest(unittest.TestCase):
    longMessage = True

    def test_convert_filters(self):
        tests = [
            ({'dangling': True}, '{"dangling": ["true"]}'),
            ({'dangling': "true"}, '{"dangling": ["true"]}'),
            ({'exited': 0}, '{"exited": ["0"]}'),
            ({'exited': [0, 1]}, '{"exited": ["0", "1"]}'),
        ]

        for filters, expected in tests:
            assert convert_filters(filters) == expected

    def test_decode_json_header(self):
        obj = {'a': 'b', 'c': 1}
        data = None
        if PY3:
            data = base64.urlsafe_b64encode(bytes(json.dumps(obj), 'utf-8'))
        else:
            data = base64.urlsafe_b64encode(json.dumps(obj))
        decoded_data = decode_json_header(data)
        assert obj == decoded_data


class SplitCommandTest(unittest.TestCase):
    def test_split_command_with_unicode(self):
        assert split_command(u'echo μμ') == ['echo', 'μμ']

    @pytest.mark.skipif(PY3, reason="shlex doesn't support bytes in py3")
    def test_split_command_with_bytes(self):
        assert split_command('echo μμ') == ['echo', 'μμ']


class FormatEnvironmentTest(unittest.TestCase):
    def test_format_env_binary_unicode_value(self):
        env_dict = {
            'ARTIST_NAME': b'\xec\x86\xa1\xec\xa7\x80\xec\x9d\x80'
        }
        assert format_environment(env_dict) == [u'ARTIST_NAME=송지은']

    def test_format_env_no_value(self):
        env_dict = {
            'FOO': None,
            'BAR': '',
        }
        assert sorted(format_environment(env_dict)) == ['BAR=', 'FOO']
