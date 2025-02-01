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

from ansible_collections.community.docker.plugins.module_utils._api import constants
from ansible_collections.community.docker.tests.unit.plugins.module_utils._api.constants import DEFAULT_DOCKER_API_VERSION

from . import fake_stat

CURRENT_VERSION = 'v{api_version}'.format(api_version=DEFAULT_DOCKER_API_VERSION)

FAKE_CONTAINER_ID = '3cc2351ab11b'
FAKE_IMAGE_ID = 'e9aa60c60128'
FAKE_EXEC_ID = 'd5d177f121dc'
FAKE_NETWORK_ID = '33fb6a3462b8'
FAKE_IMAGE_NAME = 'test_image'
FAKE_TARBALL_PATH = '/path/to/tarball'
FAKE_REPO_NAME = 'repo'
FAKE_TAG_NAME = 'tag'
FAKE_FILE_NAME = 'file'
FAKE_URL = 'myurl'
FAKE_PATH = '/path'
FAKE_VOLUME_NAME = 'perfectcherryblossom'
FAKE_NODE_ID = '24ifsmvkjbyhk'
FAKE_SECRET_ID = 'epdyrw4tsi03xy3deu8g8ly6o'
FAKE_SECRET_NAME = 'super_secret'

# Each method is prefixed with HTTP method (get, post...)
# for clarity and readability


def get_fake_version():
    status_code = 200
    response = {
        'ApiVersion': '1.35',
        'Arch': 'amd64',
        'BuildTime': '2018-01-10T20:09:37.000000000+00:00',
        'Components': [{
            'Details': {
                'ApiVersion': '1.35',
                'Arch': 'amd64',
                'BuildTime': '2018-01-10T20:09:37.000000000+00:00',
                'Experimental': 'false',
                'GitCommit': '03596f5',
                'GoVersion': 'go1.9.2',
                'KernelVersion': '4.4.0-112-generic',
                'MinAPIVersion': '1.12',
                'Os': 'linux'
            },
            'Name': 'Engine',
            'Version': '18.01.0-ce'
        }],
        'GitCommit': '03596f5',
        'GoVersion': 'go1.9.2',
        'KernelVersion': '4.4.0-112-generic',
        'MinAPIVersion': '1.12',
        'Os': 'linux',
        'Platform': {'Name': ''},
        'Version': '18.01.0-ce'
    }

    return status_code, response


def get_fake_info():
    status_code = 200
    response = {'Containers': 1, 'Images': 1, 'Debug': False,
                'MemoryLimit': False, 'SwapLimit': False,
                'IPv4Forwarding': True}
    return status_code, response


def post_fake_auth():
    status_code = 200
    response = {'Status': 'Login Succeeded',
                'IdentityToken': '9cbaf023786cd7'}
    return status_code, response


def get_fake_ping():
    return 200, "OK"


def get_fake_search():
    status_code = 200
    response = [{'Name': 'busybox', 'Description': 'Fake Description'}]
    return status_code, response


def get_fake_images():
    status_code = 200
    response = [{
        'Id': FAKE_IMAGE_ID,
        'Created': '2 days ago',
        'Repository': 'busybox',
        'RepoTags': ['busybox:latest', 'busybox:1.0'],
    }]
    return status_code, response


def get_fake_image_history():
    status_code = 200
    response = [
        {
            "Id": "b750fe79269d",
            "Created": 1364102658,
            "CreatedBy": "/bin/bash"
        },
        {
            "Id": "27cf78414709",
            "Created": 1364068391,
            "CreatedBy": ""
        }
    ]

    return status_code, response


def post_fake_import_image():
    status_code = 200
    response = 'Import messages...'

    return status_code, response


def get_fake_containers():
    status_code = 200
    response = [{
        'Id': FAKE_CONTAINER_ID,
        'Image': 'busybox:latest',
        'Created': '2 days ago',
        'Command': 'true',
        'Status': 'fake status'
    }]
    return status_code, response


def post_fake_start_container():
    status_code = 200
    response = {'Id': FAKE_CONTAINER_ID}
    return status_code, response


def post_fake_resize_container():
    status_code = 200
    response = {'Id': FAKE_CONTAINER_ID}
    return status_code, response


def post_fake_create_container():
    status_code = 200
    response = {'Id': FAKE_CONTAINER_ID}
    return status_code, response


def get_fake_inspect_container(tty=False):
    status_code = 200
    response = {
        'Id': FAKE_CONTAINER_ID,
        'Config': {'Labels': {'foo': 'bar'}, 'Privileged': True, 'Tty': tty},
        'ID': FAKE_CONTAINER_ID,
        'Image': 'busybox:latest',
        'Name': 'foobar',
        "State": {
            "Status": "running",
            "Running": True,
            "Pid": 0,
            "ExitCode": 0,
            "StartedAt": "2013-09-25T14:01:18.869545111+02:00",
            "Ghost": False
        },
        "HostConfig": {
            "LogConfig": {
                "Type": "json-file",
                "Config": {}
            },
        },
        "MacAddress": "02:42:ac:11:00:0a"
    }
    return status_code, response


def get_fake_inspect_image():
    status_code = 200
    response = {
        'Id': FAKE_IMAGE_ID,
        'Parent': "27cf784147099545",
        'Created': "2013-03-23T22:24:18.818426-07:00",
        'Container': FAKE_CONTAINER_ID,
        'Config': {'Labels': {'bar': 'foo'}},
        'ContainerConfig':
        {
            "Hostname": "",
            "User": "",
            "Memory": 0,
            "MemorySwap": 0,
            "AttachStdin": False,
            "AttachStdout": False,
            "AttachStderr": False,
            "PortSpecs": "",
            "Tty": True,
            "OpenStdin": True,
            "StdinOnce": False,
            "Env": "",
            "Cmd": ["/bin/bash"],
            "Dns": "",
            "Image": "base",
            "Volumes": "",
            "VolumesFrom": "",
            "WorkingDir": ""
        },
        'Size': 6823592
    }
    return status_code, response


def get_fake_insert_image():
    status_code = 200
    response = {'StatusCode': 0}
    return status_code, response


def get_fake_wait():
    status_code = 200
    response = {'StatusCode': 0}
    return status_code, response


def get_fake_logs():
    status_code = 200
    response = (b'\x01\x00\x00\x00\x00\x00\x00\x00'
                b'\x02\x00\x00\x00\x00\x00\x00\x00'
                b'\x01\x00\x00\x00\x00\x00\x00\x11Flowering Nights\n'
                b'\x01\x00\x00\x00\x00\x00\x00\x10(Sakuya Iyazoi)\n')
    return status_code, response


def get_fake_diff():
    status_code = 200
    response = [{'Path': '/test', 'Kind': 1}]
    return status_code, response


def get_fake_events():
    status_code = 200
    response = [{'status': 'stop', 'id': FAKE_CONTAINER_ID,
                 'from': FAKE_IMAGE_ID, 'time': 1423247867}]
    return status_code, response


def get_fake_export():
    status_code = 200
    response = 'Byte Stream....'
    return status_code, response


def post_fake_exec_create():
    status_code = 200
    response = {'Id': FAKE_EXEC_ID}
    return status_code, response


def post_fake_exec_start():
    status_code = 200
    response = (b'\x01\x00\x00\x00\x00\x00\x00\x11bin\nboot\ndev\netc\n'
                b'\x01\x00\x00\x00\x00\x00\x00\x12lib\nmnt\nproc\nroot\n'
                b'\x01\x00\x00\x00\x00\x00\x00\x0csbin\nusr\nvar\n')
    return status_code, response


def post_fake_exec_resize():
    status_code = 201
    return status_code, ''


def get_fake_exec_inspect():
    return 200, {
        'OpenStderr': True,
        'OpenStdout': True,
        'Container': get_fake_inspect_container()[1],
        'Running': False,
        'ProcessConfig': {
            'arguments': ['hello world'],
            'tty': False,
            'entrypoint': 'echo',
            'privileged': False,
            'user': ''
        },
        'ExitCode': 0,
        'ID': FAKE_EXEC_ID,
        'OpenStdin': False
    }


def post_fake_stop_container():
    status_code = 200
    response = {'Id': FAKE_CONTAINER_ID}
    return status_code, response


def post_fake_kill_container():
    status_code = 200
    response = {'Id': FAKE_CONTAINER_ID}
    return status_code, response


def post_fake_pause_container():
    status_code = 200
    response = {'Id': FAKE_CONTAINER_ID}
    return status_code, response


def post_fake_unpause_container():
    status_code = 200
    response = {'Id': FAKE_CONTAINER_ID}
    return status_code, response


def post_fake_restart_container():
    status_code = 200
    response = {'Id': FAKE_CONTAINER_ID}
    return status_code, response


def post_fake_rename_container():
    status_code = 204
    return status_code, None


def delete_fake_remove_container():
    status_code = 200
    response = {'Id': FAKE_CONTAINER_ID}
    return status_code, response


def post_fake_image_create():
    status_code = 200
    response = {'Id': FAKE_IMAGE_ID}
    return status_code, response


def delete_fake_remove_image():
    status_code = 200
    response = {'Id': FAKE_IMAGE_ID}
    return status_code, response


def get_fake_get_image():
    status_code = 200
    response = 'Byte Stream....'
    return status_code, response


def post_fake_load_image():
    status_code = 200
    response = {'Id': FAKE_IMAGE_ID}
    return status_code, response


def post_fake_commit():
    status_code = 200
    response = {'Id': FAKE_CONTAINER_ID}
    return status_code, response


def post_fake_push():
    status_code = 200
    response = {'Id': FAKE_IMAGE_ID}
    return status_code, response


def post_fake_build_container():
    status_code = 200
    response = {'Id': FAKE_CONTAINER_ID}
    return status_code, response


def post_fake_tag_image():
    status_code = 200
    response = {'Id': FAKE_IMAGE_ID}
    return status_code, response


def get_fake_stats():
    status_code = 200
    response = fake_stat.OBJ
    return status_code, response


def get_fake_top():
    return 200, {
        'Processes': [
            [
                'root',
                '26501',
                '6907',
                '0',
                '10:32',
                'pts/55',
                '00:00:00',
                'sleep 60',
            ],
        ],
        'Titles': [
            'UID',
            'PID',
            'PPID',
            'C',
            'STIME',
            'TTY',
            'TIME',
            'CMD',
        ],
    }


def get_fake_volume_list():
    status_code = 200
    response = {
        'Volumes': [
            {
                'Name': 'perfectcherryblossom',
                'Driver': 'local',
                'Mountpoint': '/var/lib/docker/volumes/perfectcherryblossom',
                'Scope': 'local'
            }, {
                'Name': 'subterraneananimism',
                'Driver': 'local',
                'Mountpoint': '/var/lib/docker/volumes/subterraneananimism',
                'Scope': 'local'
            }
        ]
    }
    return status_code, response


def get_fake_volume():
    status_code = 200
    response = {
        'Name': 'perfectcherryblossom',
        'Driver': 'local',
        'Mountpoint': '/var/lib/docker/volumes/perfectcherryblossom',
        'Labels': {
            'com.example.some-label': 'some-value'
        },
        'Scope': 'local'
    }
    return status_code, response


def fake_remove_volume():
    return 204, None


def post_fake_update_container():
    return 200, {'Warnings': []}


def post_fake_update_node():
    return 200, None


def post_fake_join_swarm():
    return 200, None


def get_fake_network_list():
    return 200, [{
        "Name": "bridge",
        "Id": FAKE_NETWORK_ID,
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": False,
        "Internal": False,
        "IPAM": {
            "Driver": "default",
            "Config": [
                {
                    "Subnet": "172.17.0.0/16"
                }
            ]
        },
        "Containers": {
            FAKE_CONTAINER_ID: {
                "EndpointID": "ed2419a97c1d99",
                "MacAddress": "02:42:ac:11:00:02",
                "IPv4Address": "172.17.0.2/16",
                "IPv6Address": ""
            }
        },
        "Options": {
            "com.docker.network.bridge.default_bridge": "true",
            "com.docker.network.bridge.enable_icc": "true",
            "com.docker.network.bridge.enable_ip_masquerade": "true",
            "com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
            "com.docker.network.bridge.name": "docker0",
            "com.docker.network.driver.mtu": "1500"
        }
    }]


def get_fake_network():
    return 200, get_fake_network_list()[1][0]


def post_fake_network():
    return 201, {"Id": FAKE_NETWORK_ID, "Warnings": []}


def delete_fake_network():
    return 204, None


def post_fake_network_connect():
    return 200, None


def post_fake_network_disconnect():
    return 200, None


def post_fake_secret():
    status_code = 200
    response = {'ID': FAKE_SECRET_ID}
    return status_code, response


# Maps real api url to fake response callback
prefix = 'http+docker://localhost'
if constants.IS_WINDOWS_PLATFORM:
    prefix = 'http+docker://localnpipe'

fake_responses = {
    '{prefix}/version'.format(prefix=prefix):
    get_fake_version,
    '{prefix}/{CURRENT_VERSION}/version'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    get_fake_version,
    '{prefix}/{CURRENT_VERSION}/info'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    get_fake_info,
    '{prefix}/{CURRENT_VERSION}/auth'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    post_fake_auth,
    '{prefix}/{CURRENT_VERSION}/_ping'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    get_fake_ping,
    '{prefix}/{CURRENT_VERSION}/images/search'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    get_fake_search,
    '{prefix}/{CURRENT_VERSION}/images/json'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    get_fake_images,
    '{prefix}/{CURRENT_VERSION}/images/test_image/history'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    get_fake_image_history,
    '{prefix}/{CURRENT_VERSION}/images/create'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    post_fake_import_image,
    '{prefix}/{CURRENT_VERSION}/containers/json'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    get_fake_containers,
    '{prefix}/{CURRENT_VERSION}/containers/3cc2351ab11b/start'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    post_fake_start_container,
    '{prefix}/{CURRENT_VERSION}/containers/3cc2351ab11b/resize'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    post_fake_resize_container,
    '{prefix}/{CURRENT_VERSION}/containers/3cc2351ab11b/json'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    get_fake_inspect_container,
    '{prefix}/{CURRENT_VERSION}/containers/3cc2351ab11b/rename'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    post_fake_rename_container,
    '{prefix}/{CURRENT_VERSION}/images/e9aa60c60128/tag'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    post_fake_tag_image,
    '{prefix}/{CURRENT_VERSION}/containers/3cc2351ab11b/wait'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    get_fake_wait,
    '{prefix}/{CURRENT_VERSION}/containers/3cc2351ab11b/logs'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    get_fake_logs,
    '{prefix}/{CURRENT_VERSION}/containers/3cc2351ab11b/changes'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    get_fake_diff,
    '{prefix}/{CURRENT_VERSION}/containers/3cc2351ab11b/export'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    get_fake_export,
    '{prefix}/{CURRENT_VERSION}/containers/3cc2351ab11b/update'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    post_fake_update_container,
    '{prefix}/{CURRENT_VERSION}/containers/3cc2351ab11b/exec'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    post_fake_exec_create,
    '{prefix}/{CURRENT_VERSION}/exec/d5d177f121dc/start'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    post_fake_exec_start,
    '{prefix}/{CURRENT_VERSION}/exec/d5d177f121dc/json'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    get_fake_exec_inspect,
    '{prefix}/{CURRENT_VERSION}/exec/d5d177f121dc/resize'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    post_fake_exec_resize,

    '{prefix}/{CURRENT_VERSION}/containers/3cc2351ab11b/stats'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    get_fake_stats,
    '{prefix}/{CURRENT_VERSION}/containers/3cc2351ab11b/top'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    get_fake_top,
    '{prefix}/{CURRENT_VERSION}/containers/3cc2351ab11b/stop'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    post_fake_stop_container,
    '{prefix}/{CURRENT_VERSION}/containers/3cc2351ab11b/kill'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    post_fake_kill_container,
    '{prefix}/{CURRENT_VERSION}/containers/3cc2351ab11b/pause'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    post_fake_pause_container,
    '{prefix}/{CURRENT_VERSION}/containers/3cc2351ab11b/unpause'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    post_fake_unpause_container,
    '{prefix}/{CURRENT_VERSION}/containers/3cc2351ab11b/restart'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    post_fake_restart_container,
    '{prefix}/{CURRENT_VERSION}/containers/3cc2351ab11b'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    delete_fake_remove_container,
    '{prefix}/{CURRENT_VERSION}/images/create'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    post_fake_image_create,
    '{prefix}/{CURRENT_VERSION}/images/e9aa60c60128'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    delete_fake_remove_image,
    '{prefix}/{CURRENT_VERSION}/images/e9aa60c60128/get'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    get_fake_get_image,
    '{prefix}/{CURRENT_VERSION}/images/load'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    post_fake_load_image,
    '{prefix}/{CURRENT_VERSION}/images/test_image/json'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    get_fake_inspect_image,
    '{prefix}/{CURRENT_VERSION}/images/test_image/insert'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    get_fake_insert_image,
    '{prefix}/{CURRENT_VERSION}/images/test_image/push'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    post_fake_push,
    '{prefix}/{CURRENT_VERSION}/commit'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    post_fake_commit,
    '{prefix}/{CURRENT_VERSION}/containers/create'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    post_fake_create_container,
    '{prefix}/{CURRENT_VERSION}/build'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    post_fake_build_container,
    '{prefix}/{CURRENT_VERSION}/events'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    get_fake_events,
    ('{prefix}/{CURRENT_VERSION}/volumes'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION), 'GET'):
    get_fake_volume_list,
    ('{prefix}/{CURRENT_VERSION}/volumes/create'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION), 'POST'):
    get_fake_volume,
    ('{1}/{0}/volumes/{2}'.format(
        CURRENT_VERSION, prefix, FAKE_VOLUME_NAME
    ), 'GET'):
    get_fake_volume,
    ('{1}/{0}/volumes/{2}'.format(
        CURRENT_VERSION, prefix, FAKE_VOLUME_NAME
    ), 'DELETE'):
    fake_remove_volume,
    ('{1}/{0}/nodes/{2}/update?version=1'.format(
        CURRENT_VERSION, prefix, FAKE_NODE_ID
    ), 'POST'):
    post_fake_update_node,
    ('{prefix}/{CURRENT_VERSION}/swarm/join'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION), 'POST'):
    post_fake_join_swarm,
    ('{prefix}/{CURRENT_VERSION}/networks'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION), 'GET'):
    get_fake_network_list,
    ('{prefix}/{CURRENT_VERSION}/networks/create'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION), 'POST'):
    post_fake_network,
    ('{1}/{0}/networks/{2}'.format(
        CURRENT_VERSION, prefix, FAKE_NETWORK_ID
    ), 'GET'):
    get_fake_network,
    ('{1}/{0}/networks/{2}'.format(
        CURRENT_VERSION, prefix, FAKE_NETWORK_ID
    ), 'DELETE'):
    delete_fake_network,
    ('{1}/{0}/networks/{2}/connect'.format(
        CURRENT_VERSION, prefix, FAKE_NETWORK_ID
    ), 'POST'):
    post_fake_network_connect,
    ('{1}/{0}/networks/{2}/disconnect'.format(
        CURRENT_VERSION, prefix, FAKE_NETWORK_ID
    ), 'POST'):
    post_fake_network_disconnect,
    '{prefix}/{CURRENT_VERSION}/secrets/create'.format(prefix=prefix, CURRENT_VERSION=CURRENT_VERSION):
    post_fake_secret,
}
