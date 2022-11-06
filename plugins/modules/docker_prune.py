#!/usr/bin/python
#
# Copyright 2016 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: docker_prune

short_description: Allows to prune various docker objects

description:
  - Allows to run C(docker container prune), C(docker image prune), C(docker network prune)
    and C(docker volume prune) via the Docker API.

extends_documentation_fragment:
  - community.docker.docker.api_documentation
  - community.docker.attributes
  - community.docker.attributes.actiongroup_docker

attributes:
  check_mode:
    support: none
  diff_mode:
    support: none

options:
  containers:
    description:
      - Whether to prune containers.
    type: bool
    default: false
  containers_filters:
    description:
      - A dictionary of filter values used for selecting containers to delete.
      - "For example, C(until: 24h)."
      - See L(the docker documentation,https://docs.docker.com/engine/reference/commandline/container_prune/#filtering)
        for more information on possible filters.
    type: dict
  images:
    description:
      - Whether to prune images.
    type: bool
    default: false
  images_filters:
    description:
      - A dictionary of filter values used for selecting images to delete.
      - "For example, C(dangling: true)."
      - See L(the docker documentation,https://docs.docker.com/engine/reference/commandline/image_prune/#filtering)
        for more information on possible filters.
    type: dict
  networks:
    description:
      - Whether to prune networks.
    type: bool
    default: false
  networks_filters:
    description:
      - A dictionary of filter values used for selecting networks to delete.
      - See L(the docker documentation,https://docs.docker.com/engine/reference/commandline/network_prune/#filtering)
        for more information on possible filters.
    type: dict
  volumes:
    description:
      - Whether to prune volumes.
    type: bool
    default: false
  volumes_filters:
    description:
      - A dictionary of filter values used for selecting volumes to delete.
      - See L(the docker documentation,https://docs.docker.com/engine/reference/commandline/volume_prune/#filtering)
        for more information on possible filters.
    type: dict
  builder_cache:
    description:
      - Whether to prune the builder cache.
    type: bool
    default: false

author:
  - "Felix Fontein (@felixfontein)"

requirements:
  - "Docker API >= 1.25"
'''

EXAMPLES = '''
- name: Prune containers older than 24h
  community.docker.docker_prune:
    containers: true
    containers_filters:
      # only consider containers created more than 24 hours ago
      until: 24h

- name: Prune everything
  community.docker.docker_prune:
    containers: true
    images: true
    networks: true
    volumes: true
    builder_cache: true

- name: Prune everything (including non-dangling images)
  community.docker.docker_prune:
    containers: true
    images: true
    images_filters:
      dangling: false
    networks: true
    volumes: true
    builder_cache: true
'''

RETURN = '''
# containers
containers:
    description:
      - List of IDs of deleted containers.
    returned: I(containers) is C(true)
    type: list
    elements: str
    sample: []
containers_space_reclaimed:
    description:
      - Amount of reclaimed disk space from container pruning in bytes.
    returned: I(containers) is C(true)
    type: int
    sample: 0

# images
images:
    description:
      - List of IDs of deleted images.
    returned: I(images) is C(true)
    type: list
    elements: str
    sample: []
images_space_reclaimed:
    description:
      - Amount of reclaimed disk space from image pruning in bytes.
    returned: I(images) is C(true)
    type: int
    sample: 0

# networks
networks:
    description:
      - List of IDs of deleted networks.
    returned: I(networks) is C(true)
    type: list
    elements: str
    sample: []

# volumes
volumes:
    description:
      - List of IDs of deleted volumes.
    returned: I(volumes) is C(true)
    type: list
    elements: str
    sample: []
volumes_space_reclaimed:
    description:
      - Amount of reclaimed disk space from volumes pruning in bytes.
    returned: I(volumes) is C(true)
    type: int
    sample: 0

# builder_cache
builder_cache_space_reclaimed:
    description:
      - Amount of reclaimed disk space from builder cache pruning in bytes.
    returned: I(builder_cache) is C(true)
    type: int
    sample: 0
'''

import traceback

from ansible.module_utils.common.text.converters import to_native

from ansible_collections.community.docker.plugins.module_utils.common_api import (
    AnsibleDockerClient,
    RequestException,
)

from ansible_collections.community.docker.plugins.module_utils.util import clean_dict_booleans_for_docker_api

from ansible_collections.community.docker.plugins.module_utils._api.errors import DockerException
from ansible_collections.community.docker.plugins.module_utils._api.utils.utils import convert_filters


def main():
    argument_spec = dict(
        containers=dict(type='bool', default=False),
        containers_filters=dict(type='dict'),
        images=dict(type='bool', default=False),
        images_filters=dict(type='dict'),
        networks=dict(type='bool', default=False),
        networks_filters=dict(type='dict'),
        volumes=dict(type='bool', default=False),
        volumes_filters=dict(type='dict'),
        builder_cache=dict(type='bool', default=False),
    )

    client = AnsibleDockerClient(
        argument_spec=argument_spec,
        # supports_check_mode=True,
    )

    try:
        result = dict()

        if client.module.params['containers']:
            filters = clean_dict_booleans_for_docker_api(client.module.params.get('containers_filters'))
            params = {'filters': convert_filters(filters)}
            res = client.post_to_json('/containers/prune', params=params)
            result['containers'] = res.get('ContainersDeleted') or []
            result['containers_space_reclaimed'] = res['SpaceReclaimed']

        if client.module.params['images']:
            filters = clean_dict_booleans_for_docker_api(client.module.params.get('images_filters'))
            params = {'filters': convert_filters(filters)}
            res = client.post_to_json('/images/prune', params=params)
            result['images'] = res.get('ImagesDeleted') or []
            result['images_space_reclaimed'] = res['SpaceReclaimed']

        if client.module.params['networks']:
            filters = clean_dict_booleans_for_docker_api(client.module.params.get('networks_filters'))
            params = {'filters': convert_filters(filters)}
            res = client.post_to_json('/networks/prune', params=params)
            result['networks'] = res.get('NetworksDeleted') or []

        if client.module.params['volumes']:
            filters = clean_dict_booleans_for_docker_api(client.module.params.get('volumes_filters'))
            params = {'filters': convert_filters(filters)}
            res = client.post_to_json('/volumes/prune', params=params)
            result['volumes'] = res.get('VolumesDeleted') or []
            result['volumes_space_reclaimed'] = res['SpaceReclaimed']

        if client.module.params['builder_cache']:
            res = client.post_to_json('/build/prune')
            result['builder_cache_space_reclaimed'] = res['SpaceReclaimed']

        client.module.exit_json(**result)
    except DockerException as e:
        client.fail('An unexpected Docker error occurred: {0}'.format(to_native(e)), exception=traceback.format_exc())
    except RequestException as e:
        client.fail(
            'An unexpected requests error occurred when trying to talk to the Docker daemon: {0}'.format(to_native(e)),
            exception=traceback.format_exc())


if __name__ == '__main__':
    main()
