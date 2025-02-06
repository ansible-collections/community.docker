#!/usr/bin/python
#
# Copyright 2025 Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r"""
module: docker_context_info

short_description: Retrieve information on Docker contexts for the current user

description:
  - Essentially returns the output of C(docker context ls --format json).
extends_documentation_fragment:
  - community.docker.attributes
  - community.docker.attributes.info_module
  - community.docker.attributes.idempotent_not_modify_state

options:
  only_current:
    description:
      - If set to V(true), RV(contexts) will just contain the current context and none else.
      - If set to V(false), RV(contexts) will list all contexts.
    type: bool
    default: false
  cli_context:
    description:
      - The Docker CLI context to use.
      - If set, will ignore the E(DOCKER_HOST) and E(DOCKER_CONTEXT) environment variables and the user's Docker config.
      - If not set, the module will follow Docker CLI's precedence and uses E(DOCKER_HOST) if set;
        if not, uses E(DOCKER_CONTEXT) if set;
        if not, uses the current context from the Docker config;
        if not set, uses C(default).
    type: str

author:
  - "Felix Fontein (@felixfontein)"
"""

EXAMPLES = r"""
- name: Get infos on contexts
  community.docker.docker_context_info:
  register: result

- name: Show all contexts
  ansible.builtin.debug:
    msg: "{{ result.contexts }}"

- name: Get current context
  community.docker.docker_context_info:
    only_current: true
  register: docker_current_context

- name: Run community.docker modules with current context
  module_defaults:
    group/community.docker.docker: "{{ docker_current_context.contexts[0].config }}"
  block:
    - name: Task using the current context
      community.docker.docker_container:
        image: ubuntu:latest
        name: ubuntu
        state: running
"""

RETURN = r"""
contexts:
  description:
    - A list of all contexts (O(only_current=false)) or only the current context (O(only_current=true)).
  type: list
  elements: dict
  returned: success
  contains:
    current:
      description:
        - Whether this context is the current one.
      type: bool
      returned: success
      sample: true
    name:
      description:
        - The context's name.
      type: bool
      returned: success
      sample: default
    description:
      description:
        - The context's description, if available.
      type: bool
      returned: success
      sample: My context
    meta_path:
      description:
        - The path to the context's meta directory.
        - Not present for RV(contexts[].name=default).
      type: str
      returned: success
      sample: /home/felix/.docker/contexts/meta/0123456789abcdef01234567890abcdef0123456789abcdef0123456789abcde
    tls_path:
      description:
        - The path to the context's TLS config directory.
        - Not present for RV(contexts[].name=default).
      type: str
      returned: success
      sample: /home/user/.docker/contexts/tls/0123456789abcdef01234567890abcdef0123456789abcdef0123456789abcde/
    config:
      description:
        - In case the context is for Docker, contains option values to configure the community.docker modules to use this context.
      type: dict
      returned: success
      sample: {}
      contains:
        docker_host:
          description:
            - The Docker daemon to connect to.
          type: str
          returned: success and context is for Docker
          sample: unix:///var/run/docker.sock
        tls:
          description:
            - Whether the Docker context should use an unvalidated TLS connection.
          type: bool
          returned: success and context is for Docker
          sample: false
        ca_path:
          description:
            - The CA certificate used to validate the Docker daemon's certificate.
          type: bool
          returned: success, context is for Docker, TLS config is present, and CA cert is present
          sample: /path/to/ca-cert.pem
        client_cert:
          description:
            - The client certificate to authenticate with to the Docker daemon.
          type: bool
          returned: success, context is for Docker, TLS config is present, and client cert info is present
          sample: /path/to/client-cert.pem
        client_key:
          description:
            - The client certificate's key to authenticate with to the Docker daemon.
          type: bool
          returned: success, context is for Docker, TLS config is present, and client cert info is present
          sample: /path/to/client-key.pem
        validate_certs:
          description:
            - Whether the Docker context should use a validated TLS connection.
          type: bool
          returned: success, context is for Docker, and TLS config is present
          sample: true
"""

import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native, to_text
from ansible.module_utils.six import string_types

from ansible_collections.community.docker.plugins.module_utils._api.context.api import (
    ContextAPI,
)
from ansible_collections.community.docker.plugins.module_utils._api.context.config import (
    get_current_context_name,
)
from ansible_collections.community.docker.plugins.module_utils._api.context.context import (
    IN_MEMORY,
)
from ansible_collections.community.docker.plugins.module_utils._api.errors import DockerException


def tls_context_to_json(context):
    if context is None:
        return None
    return {
        'client_cert': context.cert[0] if context.cert else None,
        'client_key': context.cert[1] if context.cert else None,
        'ca_cert': context.ca_cert,
        'verify': context.verify,
        # 'ssl_version': context.ssl_version,  -- this isn't used anymore
    }


def to_bool(value):
    return True if value else False


def context_to_json(context, current):
    module_config = {}
    if 'docker' in context.endpoints:
        endpoint = context.endpoints['docker']
        if isinstance(endpoint.get('Host'), string_types):
            host_str = to_text(endpoint['Host'])

            # Adjust protocol name so that it works with the Docker CLI tool as well
            proto = None
            idx = host_str.find('://')
            if idx >= 0:
                proto = host_str[:idx]
                host_str = host_str[idx + 3:]
            if proto in ('http', 'https'):
                proto = 'tcp'
            if proto == 'http+unix':
                proto = 'unix'
            if proto:
                host_str = "{0}://{1}".format(proto, host_str)

            # Create config for the modules
            module_config['docker_host'] = host_str
            module_config['tls'] = not to_bool(endpoint.get('SkipTLSVerify'))
            if context.tls_cfg.get('docker'):
                tls_cfg = context.tls_cfg['docker']
                if tls_cfg.ca_cert:
                    module_config['ca_path'] = tls_cfg.ca_cert
                if tls_cfg.cert:
                    module_config['client_cert'] = tls_cfg.cert[0]
                    module_config['client_key'] = tls_cfg.cert[1]
                module_config['validate_certs'] = tls_cfg.verify
                module_config['tls'] = to_bool(tls_cfg.verify)
    return {
        'current': current,
        'name': context.name,
        'description': context.description,
        'meta_path': None if context.meta_path is IN_MEMORY else context.meta_path,
        'tls_path': None if context.tls_path is IN_MEMORY else context.tls_path,
        'config': module_config,
    }


def main():
    argument_spec = dict(
        only_current=dict(type='bool', default=False),
        cli_context=dict(type='str'),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    try:
        current_context_name = get_current_context_name()
        if module.params['only_current']:
            contexts = [context_to_json(ContextAPI.get_context(current_context_name), True)]
        else:
            contexts = [
                context_to_json(context, context.name == current_context_name)
                for context in ContextAPI.contexts()
            ]

        module.exit_json(
            changed=False,
            contexts=contexts,
        )
    except DockerException as e:
        module.fail_json(msg='An unexpected Docker error occurred: {0}'.format(to_native(e)), exception=traceback.format_exc())


if __name__ == '__main__':
    main()
