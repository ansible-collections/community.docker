# Copyright (c) 2019-2020, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


from ansible.errors import AnsibleConnectionFailure


from ansible_collections.community.docker.plugins.module_utils.common import (
    AnsibleDockerClientBase,
    DOCKER_COMMON_ARGS,
)


class AnsibleDockerClient(AnsibleDockerClientBase):
    def __init__(self, plugin, min_docker_version=None, min_docker_api_version=None):
        self.plugin = plugin
        super(AnsibleDockerClient, self).__init__(
            min_docker_version=min_docker_version,
            min_docker_api_version=min_docker_api_version)

    def fail(self, msg, **kwargs):
        if kwargs:
            msg += '\nContext:\n' + '\n'.join('  {0} = {1!r}'.format(k, v) for (k, v) in kwargs.items())
        raise AnsibleConnectionFailure(msg)

    def _get_params(self):
        return dict([
            (option, self.plugin.get_option(option))
            for option in DOCKER_COMMON_ARGS
        ])
