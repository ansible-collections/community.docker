#!/usr/bin/python
# coding: utf-8
#
# Copyright: (c) 2021 Red Hat | Ansible Sakar Mehra<@sakarmehra100@gmail.com | @sakar97>
# Copyright: (c) 2019, Vladimir Porshkevich (@porshkevich) <neosonic@mail.ru>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
module: docker_plugin
short_description: Manage Docker plugins
version_added: 1.3.0
description:
  - This module allows to install, delete, enable and disable Docker plugins.
  - Performs largely the same function as the C(docker plugin) CLI subcommand.
options:
  plugin_name:
    description:
      - Name of the plugin to operate on.
    required: true
    type: str

  state:
    description:
      - C(absent) remove the plugin.
      - C(present) install the plugin, if it does not already exist.
      - C(enable) enable the plugin.
      - C(disable) disable the plugin.
    default: present
    choices:
      - absent
      - present
      - enable
      - disable
    type: str

  plugin_options:
    description:
      - Dictionary of plugin settings.
    type: dict

  force_remove:
    description:
      - Remove even if the plugin is enabled.
    default: False
    type: bool

  enable_timeout:
    description:
      - Timeout in seconds.
    type: int
    default: 0

extends_documentation_fragment:
  - community.docker.docker
  - community.docker.docker.docker_py_2_documentation

author:
  - Sakar Mehra (@sakar97)
  - Vladimir Porshkevich (@porshkevich)

requirements:
  - "python >= 2.7"
  - "L(Docker SDK for Python,https://docker-py.readthedocs.io/en/stable/) >= 2.6.0"
  - "Docker API >= 1.25"
'''

EXAMPLES = '''
- name: Install a plugin
  community.docker.docker_plugin:
    plugin_name: plugin_one
    state: present

- name: Remove a plugin
  community.docker.docker_plugin:
    plugin_name: plugin_one
    state: absent

- name: Enable the plugin
  community.docker.docker_plugin:
    plugin_name: plugin_one
    state: enable

- name: Disable the plugin
  community.docker.docker_plugin:
    plugin_name: plugin_one
    state: disable

- name: Install a plugin with options
  community.docker.docker_plugin:
    name: weaveworks/net-plugin:latest_release
    plugin_options:
      IPALLOC_RANGE: "10.32.0.0/12"
      WEAVE_PASSWORD: "PASSWORD"
'''

RETURN = '''
plugin:
    description:
      - Plugin inspection results for the affected plugin.
    returned: success
    type: dict
    sample: {}
'''

import traceback

from ansible.module_utils._text import to_native

try:
    from docker.errors import APIError, NotFound, DockerException
    from docker import DockerClient
except ImportError:
    # missing docker-py handled in ansible.module_utils.docker_common
    pass

from ansible_collections.community.docker.plugins.module_utils.common import (
    DockerBaseClass,
    AnsibleDockerClient,
    DifferenceTracker,
    RequestException
)


class TaskParameters(DockerBaseClass):
    def __init__(self, client):
        super(TaskParameters, self).__init__()
        self.client = client
        self.plugin_name = None
        self.plugin_options = None
        self.debug = None
        self.force_remove = None
        self.enable_timeout = None

        for key, value in client.module.params.items():
            setattr(self, key, value)


def prepare_options(options):
    return ['%s=%s' % (k, v if v is not None else "") for k, v in options.items()] if options else []


def parse_options(options_list):
    return dict(x.split('=', 1) for x in options_list) if options_list else {}


class DockerPluginManager(object):

    def __init__(self, client):
        self.client = client

        self.dclient = DockerClient(**self.client._connect_params)
        self.dclient.api = client

        self.parameters = TaskParameters(client)
        self.check_mode = self.client.check_mode
        self.results = {
            u'changed': False,
            u'actions': []
        }
        self.diff = self.client.module._diff
        self.diff_tracker = DifferenceTracker()
        self.diff_result = dict()

        self.existing_plugin = self.get_existing_plugin()

        state = self.parameters.state
        if state == 'present':
            self.present()
        elif state == 'absent':
            self.absent()
        elif state == 'enable':
            self.enable()
        elif state == 'disable':
            self.disable()

        if self.diff or self.check_mode or self.parameters.debug:
            if self.diff:
                self.diff_result['before'], self.diff_result['after'] = self.diff_tracker.get_before_after()
            self.results['diff'] = self.diff_result

    def get_existing_plugin(self):
        name = self.parameters.plugin_name
        try:
            plugin = self.dclient.plugins.get(name)
        except NotFound:
            return None
        except APIError as e:
            self.client.fail(to_native(e))

        if plugin is None:
            return None
        else:
            return plugin

    def has_different_config(self):
        """
        Return the list of differences between the current parameters and the existing plugin.

        :return: list of options that differ
        """
        differences = DifferenceTracker()
        if self.parameters.plugin_options:
            if not self.existing_plugin.settings:
                differences.add('plugin_options', parameters=self.parameters.plugin_options, active=self.existing_plugin.settings['Env'])
            else:
                existing_options_list = self.existing_plugin.settings['Env']
                existing_options = parse_options(existing_options_list)

                for key, value in self.parameters.plugin_options.items():
                    options_count = 0
                    if ((not existing_options.get(key) and value) or
                            not value or
                            value != existing_options[key]):
                        differences.add('plugin_options.%s' % key,
                                        parameter=value,
                                        active=self.existing_plugin.settings['Env'][options_count])

        return differences

    def install_plugin(self):
        if not self.existing_plugin:
            if not self.check_mode:
                try:
                    self.existing_plugin = self.dclient.plugins.install(self.parameters.plugin_name, None)
                    if self.parameters.plugin_options:
                        self.existing_plugin.configure(prepare_options(self.parameters.plugin_options))
                except APIError as e:
                    self.client.fail(to_native(e))

            self.results['actions'].append("Installed plugin %s" % self.parameters.plugin_name)
            self.results['changed'] = True

    def remove_plugin(self):
        force = self.parameters.force_remove
        if self.existing_plugin:
            if not self.check_mode:
                try:
                    self.existing_plugin.remove(force)
                except APIError as e:
                    self.client.fail(to_native(e))

            self.results['actions'].append("Removed plugin %s" % self.parameters.plugin_name)
            self.results['changed'] = True

    def update_plugin(self):
        if self.existing_plugin:
            differences = self.has_different_config()
            if not differences.empty:
                if not self.check_mode:
                    try:
                        self.existing_plugin.configure(prepare_options(self.parameters.plugin_options))
                    except APIError as e:
                        self.client.fail(to_native(e))
                self.results['actions'].append("Updated plugin %s settings" % self.parameters.plugin_name)
                self.results['changed'] = True
        else:
            self.fail("Cannot update the plugin: Plugin does not exist")

    def present(self):
        differences = DifferenceTracker()
        if self.existing_plugin:
            differences = self.has_different_config()

        self.diff_tracker.add('exists', parameter=True, active=self.existing_plugin is not None)

        if self.existing_plugin:
            self.update_plugin()
        else:
            self.install_plugin()

        if self.diff or self.check_mode or self.parameters.debug:
            self.diff_tracker.merge(differences)

        if not self.check_mode and not self.parameters.debug:
            self.results.pop('actions')

    def absent(self):
        self.remove_plugin()

    def enable(self):
        timeout = self.parameters.enable_timeout
        if self.existing_plugin:
            if not self.existing_plugin.enabled:
                if not self.check_mode:
                    try:
                        self.existing_plugin.enable(timeout)
                    except APIError as e:
                        self.client.fail(to_native(e))
                self.results['actions'].append("Enabled plugin %s" % self.parameters.plugin_name)
                self.results['changed'] = True
        else:
            self.install_plugin()
            if not self.check_mode:
                try:
                    self.existing_plugin.enable(timeout)
                except APIError as e:
                    self.client.fail(to_native(e))
            self.results['actions'].append("Enabled plugin %s" % self.parameters.plugin_name)
            self.results['changed'] = True

    def disable(self):
        if self.existing_plugin:
            if self.existing_plugin.enabled:
                if not self.check_mode:
                    try:
                        self.existing_plugin.disable()
                    except APIError as e:
                        self.client.fail(to_native(e))
                self.results['actions'].append("Disable plugin %s" % self.parameters.plugin_name)
                self.results['changed'] = True
        else:
            self.fail("Plugin not found: Plugin does not exist.")


def main():
    argument_spec = dict(
        plugin_name=dict(type='str', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent', 'enable', 'disable']),
        plugin_options=dict(type='dict', default={}),
        debug=dict(type='bool', default=False),
        force_remove=dict(type='bool', default=False),
        enable_timeout=dict(type='int', default=0),
    )
    client = AnsibleDockerClient(
        argument_spec=argument_spec,
        supports_check_mode=True,
        min_docker_version='2.6.0',
        min_docker_api_version='1.25',
    )

    try:
        cm = DockerPluginManager(client)
        client.module.exit_json(**cm.results)
    except DockerException as e:
        client.fail('An unexpected docker error occurred: {0}'.format(to_native(e)), exception=traceback.format_exc())
    except RequestException as e:
        client.fail(
            'An unexpected requests error occurred when docker-py tried to talk to the docker daemon: {0}'.format(to_native(e)),
            exception=traceback.format_exc())


if __name__ == '__main__':
    main()
