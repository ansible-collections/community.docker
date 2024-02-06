#!/usr/bin/python
#
# Copyright (c) 2023, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: docker_image_build

short_description: Build Docker images using Docker buildx

version_added: 3.6.0

description:
  - This module allows you to build Docker images using Docker's buildx plugin (BuildKit).

extends_documentation_fragment:
  - community.docker.docker.cli_documentation
  - community.docker.attributes
  - community.docker.attributes.actiongroup_docker

attributes:
  check_mode:
    support: full
  diff_mode:
    support: none

options:
  name:
    description:
      - "Image name. Name format will be one of: C(name), C(repository/name), C(registry_server:port/name).
        When pushing or pulling an image the name can optionally include the tag by appending C(:tag_name)."
      - Note that image IDs (hashes) and names with digest cannot be used.
    type: str
    required: true
  tag:
    description:
      - Tag for the image name O(name) that is to be tagged.
      - If O(name)'s format is C(name:tag), then the tag value from O(name) will take precedence.
    type: str
    default: latest
  path:
    description:
      - The path for the build environment.
    type: path
    required: true
  dockerfile:
    description:
      - Provide an alternate name for the Dockerfile to use when building an image.
      - This can also include a relative path (relative to O(path)).
    type: str
  cache_from:
    description:
      - List of image names to consider as cache source.
    type: list
    elements: str
  pull:
    description:
      - When building an image downloads any updates to the FROM image in Dockerfile.
    type: bool
    default: false
  network:
    description:
      - The network to use for C(RUN) build instructions.
    type: str
  nocache:
    description:
      - Do not use cache when building an image.
    type: bool
    default: false
  etc_hosts:
    description:
      - Extra hosts to add to C(/etc/hosts) in building containers, as a mapping of hostname to IP address.
    type: dict
  args:
    description:
      - Provide a dictionary of C(key:value) build arguments that map to Dockerfile ARG directive.
      - Docker expects the value to be a string. For convenience any non-string values will be converted to strings.
    type: dict
  target:
    description:
      - When building an image specifies an intermediate build stage by
        name as a final stage for the resulting image.
    type: str
  platform:
    description:
      - Platform in the format C(os[/arch[/variant]]).
    type: str
  shm_size:
    description:
      - "Size of C(/dev/shm) in format C(<number>[<unit>]). Number is positive integer.
        Unit can be V(B) (byte), V(K) (kibibyte, 1024B), V(M) (mebibyte), V(G) (gibibyte),
        V(T) (tebibyte), or V(P) (pebibyte)."
      - Omitting the unit defaults to bytes. If you omit the size entirely, Docker daemon uses V(64M).
    type: str
  labels:
    description:
      - Dictionary of key value pairs.
    type: dict
  rebuild:
    description:
      - Defines the behavior of the module if the image to build (as specified in O(name) and O(tag)) already exists.
    type: str
    choices:
      - never
      - always
    default: never

requirements:
  - "Docker CLI with Docker buildx plugin"

author:
  - Felix Fontein (@felixfontein)

seealso:
  - module: community.docker.docker_image_push
  - module: community.docker.docker_image_tag
'''

EXAMPLES = '''
- name: Build Python 3.12 image
  community.docker.docker_image_build:
    name: localhost/python/3.12:latest
    path: /home/user/images/python
    dockerfile: Dockerfile-3.12
'''

RETURN = '''
image:
    description: Image inspection results for the affected image.
    returned: success
    type: dict
    sample: {}
'''

import os
import traceback

from ansible.module_utils.common.text.converters import to_native
from ansible.module_utils.common.text.formatters import human_to_bytes

from ansible_collections.community.docker.plugins.module_utils.common_cli import (
    AnsibleModuleDockerClient,
    DockerException,
)

from ansible_collections.community.docker.plugins.module_utils.util import (
    DockerBaseClass,
    clean_dict_booleans_for_docker_api,
    is_image_name_id,
    is_valid_tag,
)

from ansible_collections.community.docker.plugins.module_utils._api.utils.utils import (
    parse_repository_tag,
)


def convert_to_bytes(value, module, name, unlimited_value=None):
    if value is None:
        return value
    try:
        if unlimited_value is not None and value in ('unlimited', str(unlimited_value)):
            return unlimited_value
        return human_to_bytes(value)
    except ValueError as exc:
        module.fail_json(msg='Failed to convert %s to bytes: %s' % (name, to_native(exc)))


def dict_to_list(dictionary, concat='='):
    return ['%s%s%s' % (k, concat, v) for k, v in sorted(dictionary.items())]


class ImageBuilder(DockerBaseClass):
    def __init__(self, client):
        super(ImageBuilder, self).__init__()
        self.client = client
        self.check_mode = self.client.check_mode
        parameters = self.client.module.params

        self.cache_from = parameters['cache_from']
        self.pull = parameters['pull']
        self.network = parameters['network']
        self.nocache = parameters['nocache']
        self.etc_hosts = clean_dict_booleans_for_docker_api(parameters['etc_hosts'])
        self.args = clean_dict_booleans_for_docker_api(parameters['args'])
        self.target = parameters['target']
        self.platform = parameters['platform']
        self.shm_size = convert_to_bytes(parameters['shm_size'], self.client.module, 'shm_size')
        self.labels = clean_dict_booleans_for_docker_api(parameters['labels'])
        self.rebuild = parameters['rebuild']

        buildx = self.client.get_client_plugin_info('buildx')
        if buildx is None:
            self.fail('Docker CLI {0} does not have the buildx plugin installed'.format(self.client.get_cli()))

        self.path = parameters['path']
        if not os.path.isdir(self.path):
            self.fail('"{0}" is not an existing directory'.format(self.path))
        self.dockerfile = parameters['dockerfile']
        if self.dockerfile and not os.path.isfile(os.path.join(self.path, self.dockerfile)):
            self.fail('"{0}" is not an existing file'.format(os.path.join(self.path, self.dockerfile)))

        self.name = parameters['name']
        self.tag = parameters['tag']
        if not is_valid_tag(self.tag, allow_empty=True):
            self.fail('"{0}" is not a valid docker tag'.format(self.tag))
        if is_image_name_id(self.name):
            self.fail('Image name must not be a digest')

        # If name contains a tag, it takes precedence over tag parameter.
        repo, repo_tag = parse_repository_tag(self.name)
        if repo_tag:
            self.name = repo
            self.tag = repo_tag

        if is_image_name_id(self.tag):
            self.fail('Image name must not contain a digest, but have a tag')

    def fail(self, msg, **kwargs):
        self.client.fail(msg, **kwargs)

    def add_list_arg(self, args, option, values):
        for value in values:
            args.extend([option, value])

    def add_args(self, args):
        args.extend(['--tag', '%s:%s' % (self.name, self.tag)])
        if self.dockerfile:
            args.extend(['--file', os.path.join(self.path, self.dockerfile)])
        if self.cache_from:
            self.add_list_arg(args, '--cache-from', self.cache_from)
        if self.pull:
            args.append('--pull')
        if self.network:
            args.extend(['--network', self.network])
        if self.nocache:
            args.append('--no-cache')
        if self.etc_hosts:
            self.add_list_arg(args, '--add-host', dict_to_list(self.etc_hosts, ':'))
        if self.args:
            self.add_list_arg(args, '--build-arg', dict_to_list(self.args))
        if self.target:
            args.extend(['--target', self.target])
        if self.platform:
            args.extend(['--platform', self.platform])
        if self.shm_size:
            args.extend(['--shm-size', str(self.shm_size)])
        if self.labels:
            self.add_list_arg(args, '--label', dict_to_list(self.labels))

    def build_image(self):
        image = self.client.find_image(self.name, self.tag)
        results = dict(
            changed=False,
            actions=[],
            image=image or {},
        )

        if image:
            if self.rebuild == 'never':
                return results

        results['changed'] = True
        if not self.check_mode:
            args = ['buildx', 'build', '--progress', 'plain']
            self.add_args(args)
            args.extend(['--', self.path])
            rc, stdout, stderr = self.client.call_cli(*args)
            if rc != 0:
                self.fail('Building %s:%s failed' % (self.name, self.tag), stdout=to_native(stdout), stderr=to_native(stderr))
            results['stdout'] = to_native(stdout)
            results['stderr'] = to_native(stderr)
            results['image'] = self.client.find_image(self.name, self.tag) or {}

        return results


def main():
    argument_spec = dict(
        name=dict(type='str', required=True),
        tag=dict(type='str', default='latest'),
        path=dict(type='path', required=True),
        dockerfile=dict(type='str'),
        cache_from=dict(type='list', elements='str'),
        pull=dict(type='bool', default=False),
        network=dict(type='str'),
        nocache=dict(type='bool', default=False),
        etc_hosts=dict(type='dict'),
        args=dict(type='dict'),
        target=dict(type='str'),
        platform=dict(type='str'),
        shm_size=dict(type='str'),
        labels=dict(type='dict'),
        rebuild=dict(type='str', choices=['never', 'always'], default='never'),
    )

    client = AnsibleModuleDockerClient(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    try:
        results = ImageBuilder(client).build_image()
        client.module.exit_json(**results)
    except DockerException as e:
        client.fail('An unexpected Docker error occurred: {0}'.format(to_native(e)), exception=traceback.format_exc())


if __name__ == '__main__':
    main()
