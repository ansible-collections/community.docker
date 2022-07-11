# Copyright (c) 2022 Felix Fontein <felix@fontein.de>
# Copyright 2016 Red Hat | Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import abc
import json
import os
import re
import shlex
import traceback

from functools import partial

from ansible.module_utils.common.text.converters import to_native, to_text
from ansible.module_utils.common.text.formatters import human_to_bytes
from ansible.module_utils.six import string_types

from ansible_collections.community.docker.plugins.module_utils.common_api import (
    AnsibleDockerClient,
    RequestException,
)

from ansible_collections.community.docker.plugins.module_utils.util import (
    clean_dict_booleans_for_docker_api,
    omit_none_from_dict,
    parse_healthcheck,
)

from ansible_collections.community.docker.plugins.module_utils.version import LooseVersion

from ansible_collections.community.docker.plugins.module_utils._api.errors import (
    APIError,
    DockerException,
    NotFound,
)

from ansible_collections.community.docker.plugins.module_utils._api.utils.utils import (
    convert_port_bindings,
    normalize_links,
    parse_env_file,
    parse_repository_tag,
)


_DEFAULT_IP_REPLACEMENT_STRING = '[[DEFAULT_IP:iewahhaeB4Sae6Aen8IeShairoh4zeph7xaekoh8Geingunaesaeweiy3ooleiwi]]'


_MOUNT_OPTION_TYPES = dict(
    volume_driver='volume',
    volume_options='volume',
    propagation='bind',
    no_copy='volume',
    labels='volume',
    tmpfs_size='tmpfs',
    tmpfs_mode='tmpfs',
)


def _get_ansible_type(type):
    if type == 'set':
        return 'list'
    if type not in ('list', 'dict', 'bool', 'int', 'float', 'str'):
        raise Exception('Invalid type "%s"' % (type, ))
    return type


class Option(object):
    def __init__(
        self,
        name,
        type,
        owner,
        ansible_type=None,
        elements=None,
        ansible_elements=None,
        ansible_suboptions=None,
        ansible_aliases=None,
        ansible_choices=None,
        needs_no_suboptions=False,
        default_comparison=None,
        not_a_container_option=False,
        not_an_ansible_option=False,
        copy_comparison_from=None,
    ):
        self.name = name
        self.type = type
        self.ansible_type = ansible_type or _get_ansible_type(type)
        needs_elements = self.type in ('list', 'set')
        needs_ansible_elements = self.ansible_type in ('list', )
        if elements is not None and not needs_elements:
            raise Exception('elements only allowed for lists/sets')
        if elements is None and needs_elements:
            raise Exception('elements required for lists/sets')
        if ansible_elements is not None and not needs_ansible_elements:
            raise Exception('Ansible elements only allowed for Ansible lists')
        if (elements is None and ansible_elements is None) and needs_ansible_elements:
            raise Exception('Ansible elements required for Ansible lists')
        self.elements = elements if needs_elements else None
        self.ansible_elements = (ansible_elements or _get_ansible_type(elements)) if needs_ansible_elements else None
        needs_suboptions = (self.ansible_type == 'list' and self.ansible_elements == 'dict') or (self.ansible_type == 'dict')
        if ansible_suboptions is not None and not needs_suboptions:
            raise Exception('suboptions only allowed for Ansible lists with dicts, or Ansible dicts')
        if ansible_suboptions is None and needs_suboptions and not needs_no_suboptions and not not_an_ansible_option:
            raise Exception('suboptions required for Ansible lists with dicts, or Ansible dicts')
        self.ansible_suboptions = ansible_suboptions if needs_suboptions else None
        self.ansible_aliases = ansible_aliases or []
        self.ansible_choices = ansible_choices
        comparison_type = self.type
        if comparison_type == 'set' and self.elements == 'dict':
            comparison_type = 'set(dict)'
        elif comparison_type not in ('set', 'list', 'dict'):
            comparison_type = 'value'
        self.comparison_type = comparison_type
        if default_comparison is not None:
            self.comparison = default_comparison
        elif comparison_type in ('list', 'value'):
            self.comparison = 'strict'
        else:
            self.comparison = 'allow_more_present'
        self.not_a_container_option = not_a_container_option
        self.not_an_ansible_option = not_an_ansible_option
        self.copy_comparison_from = copy_comparison_from


class OptionGroup(object):
    def __init__(
        self,
        preprocess=None,
        ansible_mutually_exclusive=None,
        ansible_required_together=None,
        ansible_required_one_of=None,
        ansible_required_if=None,
        ansible_required_by=None,
    ):
        if preprocess is None:
            def preprocess(module, values):
                return values
        self.preprocess = preprocess
        self.options = []
        self.engines = {}
        self.ansible_mutually_exclusive = ansible_mutually_exclusive or []
        self.ansible_required_together = ansible_required_together or []
        self.ansible_required_one_of = ansible_required_one_of or []
        self.ansible_required_if = ansible_required_if or []
        self.ansible_required_by = ansible_required_by or {}
        self.argument_spec = {}

    def add_option(self, *args, **kwargs):
        option = Option(*args, owner=self, **kwargs)
        if not option.not_a_container_option:
            self.options.append(option)
        if not option.not_an_ansible_option:
            ansible_option = {
                'type': option.ansible_type,
            }
            if option.ansible_elements is not None:
                ansible_option['elements'] = option.ansible_elements
            if option.ansible_suboptions is not None:
                ansible_option['options'] = option.ansible_suboptions
            if option.ansible_aliases:
                ansible_option['aliases'] = option.ansible_aliases
            if option.ansible_choices is not None:
                ansible_option['choices'] = option.ansible_choices
            self.argument_spec[option.name] = ansible_option
        return self

    def supports_engine(self, engine_name):
        return engine_name in self.engines

    def get_engine(self, engine_name):
        return self.engines[engine_name]

    def add_docker_api(self, docker_api):
        self.engines['docker_api'] = docker_api
        return self


_SENTRY = object()


class Engine(object):
    min_api_version = None  # string or None
    min_api_version_obj = None  # LooseVersion object or None

    @abc.abstractmethod
    def get_value(self, module, container, api_version, options):
        pass

    @abc.abstractmethod
    def set_value(self, module, data, api_version, options, values):
        pass

    @abc.abstractmethod
    def get_expected_values(self, module, client, api_version, options, image, values):
        pass

    @abc.abstractmethod
    def ignore_mismatching_result(self, module, client, api_version, option, image, container_value, expected_value):
        pass

    @abc.abstractmethod
    def preprocess_value(self, module, client, api_version, options, values):
        pass

    @abc.abstractmethod
    def update_value(self, module, data, api_version, options, values):
        pass

    @abc.abstractmethod
    def can_set_value(self, api_version):
        pass

    @abc.abstractmethod
    def can_update_value(self, api_version):
        pass


class EngineDriver(object):
    name = None  # string

    @abc.abstractmethod
    def setup(self, argument_spec, mutually_exclusive=None, required_together=None, required_one_of=None, required_if=None, required_by=None):
        # Return (module, active_options, client)
        pass

    @abc.abstractmethod
    def get_api_version(self, client):
        pass

    @abc.abstractmethod
    def get_container_id(self, container):
        pass

    @abc.abstractmethod
    def get_image_from_container(self, container):
        pass

    @abc.abstractmethod
    def is_container_removing(self, container):
        pass

    @abc.abstractmethod
    def is_container_running(self, container):
        pass

    @abc.abstractmethod
    def is_container_paused(self, container):
        pass

    @abc.abstractmethod
    def inspect_container_by_name(self, client, container_name):
        pass

    @abc.abstractmethod
    def inspect_container_by_id(self, client, container_id):
        pass

    @abc.abstractmethod
    def inspect_image_by_id(self, client, image_id):
        pass

    @abc.abstractmethod
    def inspect_image_by_name(self, client, repository, tag):
        pass

    @abc.abstractmethod
    def pull_image(self, client, repository, tag):
        pass

    @abc.abstractmethod
    def pause_container(self, client, container_id):
        pass

    @abc.abstractmethod
    def unpause_container(self, client, container_id):
        pass

    @abc.abstractmethod
    def disconnect_container_from_network(self, client, container_id, network_id):
        pass

    @abc.abstractmethod
    def connect_container_to_network(self, client, container_id, network_id, parameters=None):
        pass

    @abc.abstractmethod
    def create_container(self, client, container_name, create_parameters):
        pass

    @abc.abstractmethod
    def start_container(self, client, container_id):
        pass

    @abc.abstractmethod
    def wait_for_container(self, client, container_id):
        pass

    @abc.abstractmethod
    def get_container_output(self, client, container_id):
        pass

    @abc.abstractmethod
    def update_container(self, client, container_id, update_parameters):
        pass

    @abc.abstractmethod
    def restart_container(self, client, container_id, timeout=None):
        pass

    @abc.abstractmethod
    def kill_container(self, client, container_id, kill_signal=None):
        pass

    @abc.abstractmethod
    def stop_container(self, client, container_id, timeout=None):
        pass

    @abc.abstractmethod
    def remove_container(self, client, container_id, remove_volumes=False, link=False, force=False):
        pass

    @abc.abstractmethod
    def run(self, runner, client):
        pass


class DockerAPIEngineDriver(EngineDriver):
    name = 'docker_api'

    def setup(self, argument_spec, mutually_exclusive=None, required_together=None, required_one_of=None, required_if=None, required_by=None):
        argument_spec = argument_spec or {}
        mutually_exclusive = mutually_exclusive or []
        required_together = required_together or []
        required_one_of = required_one_of or []
        required_if = required_if or []
        required_by = required_by or {}

        active_options = []
        option_minimal_versions = {}
        for options in OPTIONS:
            if not options.supports_engine(self.name):
                continue

            mutually_exclusive.extend(options.ansible_mutually_exclusive)
            required_together.extend(options.ansible_required_together)
            required_one_of.extend(options.ansible_required_one_of)
            required_if.extend(options.ansible_required_if)
            required_by.update(options.ansible_required_by)
            argument_spec.update(options.argument_spec)

            engine = options.get_engine(self.name)
            if engine.min_api_version is not None:
                for option in options.options:
                    if not option.not_an_ansible_option:
                        option_minimal_versions[option.name] = {'docker_api_version': engine.min_api_version}

            active_options.append(options)

        client = AnsibleDockerClient(
            argument_spec=argument_spec,
            mutually_exclusive=mutually_exclusive,
            required_together=required_together,
            required_one_of=required_one_of,
            required_if=required_if,
            required_by=required_by,
            option_minimal_versions=option_minimal_versions,
            supports_check_mode=True,
        )

        return client.module, active_options, client

    def get_api_version(self, client):
        return client.docker_api_version

    def get_container_id(self, container):
        return container['Id']

    def get_image_from_container(self, container):
        return container['Image']

    def is_container_removing(self, container):
        if container.get('State'):
            return container['State'].get('Status') == 'removing'
        return False

    def is_container_running(self, container):
        if container.get('State'):
            if container['State'].get('Running') and not container['State'].get('Ghost', False):
                return True
        return False

    def is_container_paused(self, container):
        if container.get('State'):
            return container['State'].get('Paused', False)
        return False

    def inspect_container_by_name(self, client, container_name):
        return client.get_container(container_name)

    def inspect_container_by_id(self, client, container_id):
        return client.get_container_by_id(container_id)

    def inspect_image_by_id(self, client, image_id):
        return client.find_image_by_id(image_id)

    def inspect_image_by_name(self, client, repository, tag):
        return client.find_image(repository, tag)

    def pull_image(self, client, repository, tag):
        return client.pull_image(repository, tag)

    def pause_container(self, client, container_id):
        client.post_call('/containers/{0}/pause', container_id)

    def unpause_container(self, client, container_id):
        client.post_call('/containers/{0}/unpause', container_id)

    def disconnect_container_from_network(self, client, container_id, network_id):
        client.post_json('/networks/{0}/disconnect', network_id, data={'Container': container_id})

    def connect_container_to_network(self, client, container_id, network_id, parameters=None):
        parameters = (parameters or {}).copy()
        params = {}
        for para, dest_para in {'ipv4_address': 'IPv4Address', 'ipv6_address': 'IPv6Address', 'links': 'Links', 'aliases': 'Aliases'}.items():
            value = parameters.pop(para, None)
            if value:
                if para == 'links':
                    value = normalize_links(value)
                params[dest_para] = value
        if parameters:
            raise Exception(
                'Unknown parameter(s) for connect_container_to_network for Docker API driver: %s' % (', '.join(['"%s"' % p for p in sorted(parameters)])))
        ipam_config = {}
        for param in ('IPv4Address', 'IPv6Address'):
            if param in params:
                ipam_config[param] = params.pop(param)
        if ipam_config:
            params['IPAMConfig'] = ipam_config
        data = {
            'Container': container_id,
            'EndpointConfig': params,
        }
        client.post_json('/networks/{0}/connect', network_id, data=data)

    def create_container(self, client, container_name, create_parameters):
        params = {'name': container_name}
        new_container = client.post_json_to_json('/containers/create', data=create_parameters, params=params)
        client.report_warnings(new_container)
        return new_container['Id']

    def start_container(self, client, container_id):
        client.post_json('/containers/{0}/start', container_id)

    def wait_for_container(self, client, container_id):
        return client.post_json_to_json('/containers/{0}/wait', container_id)['StatusCode']

    def get_container_output(self, client, container_id):
        config = client.get_json('/containers/{0}/json', container_id)
        logging_driver = config['HostConfig']['LogConfig']['Type']
        if logging_driver in ('json-file', 'journald', 'local'):
            params = {
                'stderr': 1,
                'stdout': 1,
                'timestamps': 0,
                'follow': 0,
                'tail': 'all',
            }
            res = client._get(client._url('/containers/{0}/logs', container_id), params=params)
            output = client._get_result_tty(False, res, config['Config']['Tty'])
            return output, True
        else:
            return "Result logged using `%s` driver" % logging_driver, False

    def update_container(self, client, container_id, update_parameters):
        result = client.post_json_to_json('/containers/{0}/update', container_id, data=update_parameters)
        client.report_warnings(result)

    def restart_container(self, client, container_id, timeout=None):
        client_timeout = client.timeout
        if client_timeout is not None:
            client_timeout += timeout or 10
        client.post_call('/containers/{0}/restart', container_id, params={'t': timeout}, timeout=client_timeout)

    def kill_container(self, client, container_id, kill_signal=None):
        params = {}
        if kill_signal is not None:
            params['signal'] = int(kill_signal)
        client.post_call('/containers/{0}/kill', container_id, params=params)

    def stop_container(self, client, container_id, timeout=None):
        if timeout:
            params = {'t': timeout}
        else:
            params = {}
            timeout = 10
        client_timeout = client.timeout
        if client_timeout is not None:
            client_timeout += timeout
        count = 0
        while True:
            try:
                client.post_call('/containers/{0}/stop', container_id, params=params, timeout=client_timeout)
            except APIError as exc:
                if 'Unpause the container before stopping or killing' in exc.explanation:
                    # New docker daemon versions do not allow containers to be removed
                    # if they are paused. Make sure we don't end up in an infinite loop.
                    if count == 3:
                        raise Exception('%s [tried to unpause three times]' % to_native(exc))
                    count += 1
                    # Unpause
                    try:
                        self.unpause_container(client, container_id)
                    except Exception as exc2:
                        raise Exception('%s [while unpausing]' % to_native(exc2))
                    # Now try again
                    continue
                raise
            # We only loop when explicitly requested by 'continue'
            break

    def remove_container(self, client, container_id, remove_volumes=False, link=False, force=False):
        params = {'v': remove_volumes, 'link': link, 'force': force}
        count = 0
        while True:
            try:
                client.delete_call('/containers/{0}', container_id, params=params)
            except NotFound as dummy:
                pass
            except APIError as exc:
                if 'Unpause the container before stopping or killing' in exc.explanation:
                    # New docker daemon versions do not allow containers to be removed
                    # if they are paused. Make sure we don't end up in an infinite loop.
                    if count == 3:
                        raise Exception('%s [tried to unpause three times]' % to_native(exc))
                    count += 1
                    # Unpause
                    try:
                        self.unpause_container(client, container_id)
                    except Exception as exc2:
                        raise Exception('%s [while unpausing]' % to_native(exc2))
                    # Now try again
                    continue
                if 'removal of container ' in exc.explanation and ' is already in progress' in exc.explanation:
                    pass
                raise
            # We only loop when explicitly requested by 'continue'
            break

    def run(self, runner, client):
        try:
            runner()
        except DockerException as e:
            client.fail('An unexpected Docker error occurred: {0}'.format(to_native(e)), exception=traceback.format_exc())
        except RequestException as e:
            client.fail(
                'An unexpected requests error occurred when trying to talk to the Docker daemon: {0}'.format(to_native(e)),
                exception=traceback.format_exc())


class DockerAPIEngine(Engine):
    def __init__(
        self,
        get_value,
        preprocess_value=None,
        get_expected_values=None,
        ignore_mismatching_result=None,
        set_value=None,
        update_value=None,
        can_set_value=None,
        can_update_value=None,
        min_api_version=None,
    ):
        self.min_api_version = min_api_version
        self.min_api_version_obj = None if min_api_version is None else LooseVersion(min_api_version)
        self.get_value = get_value
        self.set_value = set_value
        self.get_expected_values = get_expected_values or (lambda module, client, api_version, options, image, values: values)
        self.ignore_mismatching_result = ignore_mismatching_result or \
            (lambda module, client, api_version, option, image, container_value, expected_value: False)
        self.preprocess_value = preprocess_value or (lambda module, client, api_version, options, values: values)
        self.update_value = update_value
        self.can_set_value = can_set_value or (lambda api_version: set_value is not None)
        self.can_update_value = can_update_value or (lambda api_version: update_value is not None)

    @classmethod
    def config_value(
        cls,
        config_name,
        postprocess_for_get=None,
        preprocess_for_set=None,
        get_expected_value=None,
        ignore_mismatching_result=None,
        min_api_version=None,
        preprocess_value=None,
        update_parameter=None,
    ):
        def preprocess_value_(module, client, api_version, options, values):
            if len(options) != 1:
                raise AssertionError('config_value can only be used for a single option')
            if preprocess_value is not None and options[0].name in values:
                value = preprocess_value(module, client, api_version, values[options[0].name])
                if value is None:
                    del values[options[0].name]
                else:
                    values[options[0].name] = value
            return values

        def get_value(module, container, api_version, options):
            if len(options) != 1:
                raise AssertionError('config_value can only be used for a single option')
            value = container['Config'].get(config_name, _SENTRY)
            if postprocess_for_get:
                value = postprocess_for_get(module, api_version, value, _SENTRY)
            if value is _SENTRY:
                return {}
            return {options[0].name: value}

        get_expected_values_ = None
        if get_expected_value:
            def get_expected_values_(module, client, api_version, options, image, values):
                if len(options) != 1:
                    raise AssertionError('host_config_value can only be used for a single option')
                value = values.get(options[0].name, _SENTRY)
                value = get_expected_value(module, client, api_version, image, value, _SENTRY)
                if value is _SENTRY:
                    return values
                return {options[0].name: value}

        def set_value(module, data, api_version, options, values):
            if len(options) != 1:
                raise AssertionError('config_value can only be used for a single option')
            if options[0].name not in values:
                return
            value = values[options[0].name]
            if preprocess_for_set:
                value = preprocess_for_set(module, api_version, value)
            data[config_name] = value

        update_value = None
        if update_parameter:
            def update_value(module, data, api_version, options, values):
                if len(options) != 1:
                    raise AssertionError('update_parameter can only be used for a single option')
                if options[0].name not in values:
                    return
                value = values[options[0].name]
                if preprocess_for_set:
                    value = preprocess_for_set(module, api_version, value)
                data[update_parameter] = value

        return cls(
            get_value=get_value,
            preprocess_value=preprocess_value_,
            get_expected_values=get_expected_values_,
            ignore_mismatching_result=ignore_mismatching_result,
            set_value=set_value,
            min_api_version=min_api_version,
            update_value=update_value,
        )

    @classmethod
    def host_config_value(
        cls,
        host_config_name,
        postprocess_for_get=None,
        preprocess_for_set=None,
        get_expected_value=None,
        ignore_mismatching_result=None,
        min_api_version=None,
        preprocess_value=None,
        update_parameter=None,
    ):
        def preprocess_value_(module, client, api_version, options, values):
            if len(options) != 1:
                raise AssertionError('host_config_value can only be used for a single option')
            if preprocess_value is not None and options[0].name in values:
                value = preprocess_value(module, client, api_version, values[options[0].name])
                if value is None:
                    del values[options[0].name]
                else:
                    values[options[0].name] = value
            return values

        def get_value(module, container, api_version, options):
            if len(options) != 1:
                raise AssertionError('host_config_value can only be used for a single option')
            value = container['HostConfig'].get(host_config_name, _SENTRY)
            if postprocess_for_get:
                value = postprocess_for_get(module, api_version, value, _SENTRY)
            if value is _SENTRY:
                return {}
            return {options[0].name: value}

        get_expected_values_ = None
        if get_expected_value:
            def get_expected_values_(module, client, api_version, options, image, values):
                if len(options) != 1:
                    raise AssertionError('host_config_value can only be used for a single option')
                value = values.get(options[0].name, _SENTRY)
                value = get_expected_value(module, client, api_version, image, value, _SENTRY)
                if value is _SENTRY:
                    return values
                return {options[0].name: value}

        def set_value(module, data, api_version, options, values):
            if len(options) != 1:
                raise AssertionError('host_config_value can only be used for a single option')
            if options[0].name not in values:
                return
            if 'HostConfig' not in data:
                data['HostConfig'] = {}
            value = values[options[0].name]
            if preprocess_for_set:
                value = preprocess_for_set(module, api_version, value)
            data['HostConfig'][host_config_name] = value

        update_value = None
        if update_parameter:
            def update_value(module, data, api_version, options, values):
                if len(options) != 1:
                    raise AssertionError('update_parameter can only be used for a single option')
                if options[0].name not in values:
                    return
                value = values[options[0].name]
                if preprocess_for_set:
                    value = preprocess_for_set(module, api_version, value)
                data[update_parameter] = value

        return cls(
            get_value=get_value,
            preprocess_value=preprocess_value_,
            get_expected_values=get_expected_values_,
            ignore_mismatching_result=ignore_mismatching_result,
            set_value=set_value,
            min_api_version=min_api_version,
            update_value=update_value,
        )


def _is_volume_permissions(mode):
    for part in mode.split(','):
        if part not in ('rw', 'ro', 'z', 'Z', 'consistent', 'delegated', 'cached', 'rprivate', 'private', 'rshared', 'shared', 'rslave', 'slave', 'nocopy'):
            return False
    return True


def _parse_port_range(range_or_port, module):
    '''
    Parses a string containing either a single port or a range of ports.

    Returns a list of integers for each port in the list.
    '''
    if '-' in range_or_port:
        try:
            start, end = [int(port) for port in range_or_port.split('-')]
        except Exception:
            module.fail_json(msg='Invalid port range: "{0}"'.format(range_or_port))
        if end < start:
            module.fail_json(msg='Invalid port range: "{0}"'.format(range_or_port))
        return list(range(start, end + 1))
    else:
        try:
            return [int(range_or_port)]
        except Exception:
            module.fail_json(msg='Invalid port: "{0}"'.format(range_or_port))


def _split_colon_ipv6(text, module):
    '''
    Split string by ':', while keeping IPv6 addresses in square brackets in one component.
    '''
    if '[' not in text:
        return text.split(':')
    start = 0
    result = []
    while start < len(text):
        i = text.find('[', start)
        if i < 0:
            result.extend(text[start:].split(':'))
            break
        j = text.find(']', i)
        if j < 0:
            module.fail_json(msg='Cannot find closing "]" in input "{0}" for opening "[" at index {1}!'.format(text, i + 1))
        result.extend(text[start:i].split(':'))
        k = text.find(':', j)
        if k < 0:
            result[-1] += text[i:]
            start = len(text)
        else:
            result[-1] += text[i:k]
            if k == len(text):
                result.append('')
                break
            start = k + 1
    return result


def _normalize_port(port):
    if '/' not in port:
        return port + '/tcp'
    return port


def _get_default_host_ip(module, client):
    if module.params['default_host_ip'] is not None:
        return module.params['default_host_ip']
    ip = '0.0.0.0'
    for network_data in module.params['networks'] or []:
        if network_data.get('name'):
            network = client.get_network(network_data['name'])
            if network is None:
                client.fail(
                    "Cannot inspect the network '{0}' to determine the default IP".format(network_data['name']),
                )
            if network.get('Driver') == 'bridge' and network.get('Options', {}).get('com.docker.network.bridge.host_binding_ipv4'):
                ip = network['Options']['com.docker.network.bridge.host_binding_ipv4']
                break
    return ip


def _get_value_detach_interactive(module, container, api_version, options):
    attach_stdin = container['Config'].get('OpenStdin')
    attach_stderr = container['Config'].get('AttachStderr')
    attach_stdout = container['Config'].get('AttachStdout')
    return {
        'interactive': bool(attach_stdin),
        'detach': not (attach_stderr and attach_stdout),
    }


def _set_value_detach_interactive(module, data, api_version, options, values):
    interactive = values.get('interactive')
    detach = values.get('detach')

    data['AttachStdout'] = False
    data['AttachStderr'] = False
    data['AttachStdin'] = False
    data['StdinOnce'] = False
    data['OpenStdin'] = interactive
    if not detach:
        data['AttachStdout'] = True
        data['AttachStderr'] = True
        if interactive:
            data['AttachStdin'] = True
            data['StdinOnce'] = True


def _preprocess_command(module, values):
    if 'command' not in values:
        return values
    value = values['command']
    if module.params['command_handling'] == 'correct':
        if value is not None:
            if not isinstance(value, list):
                # convert from str to list
                value = shlex.split(to_text(value, errors='surrogate_or_strict'))
            value = [to_text(x, errors='surrogate_or_strict') for x in value]
    elif value:
        # convert from list to str
        if isinstance(value, list):
            value = shlex.split(' '.join([to_text(x, errors='surrogate_or_strict') for x in value]))
            value = [to_text(x, errors='surrogate_or_strict') for x in value]
        else:
            value = shlex.split(to_text(value, errors='surrogate_or_strict'))
            value = [to_text(x, errors='surrogate_or_strict') for x in value]
    else:
        return {}
    return {
        'command': value,
    }


def _preprocess_entrypoint(module, values):
    if 'entrypoint' not in values:
        return values
    value = values['entrypoint']
    if module.params['command_handling'] == 'correct':
        if value is not None:
            value = [to_text(x, errors='surrogate_or_strict') for x in value]
    elif value:
        # convert from list to str.
        value = shlex.split(' '.join([to_text(x, errors='surrogate_or_strict') for x in value]))
        value = [to_text(x, errors='surrogate_or_strict') for x in value]
    else:
        return {}
    return {
        'entrypoint': value,
    }


def _preprocess_env(module, values):
    if not values:
        return {}
    final_env = {}
    if 'env_file' in values:
        parsed_env_file = parse_env_file(values['env_file'])
        for name, value in parsed_env_file.items():
            final_env[name] = to_text(value, errors='surrogate_or_strict')
    if 'env' in values:
        for name, value in values['env'].items():
            if not isinstance(value, string_types):
                module.fail_json(msg='Non-string value found for env option. Ambiguous env options must be '
                                     'wrapped in quotes to avoid them being interpreted. Key: %s' % (name, ))
            final_env[name] = to_text(value, errors='surrogate_or_strict')
    formatted_env = []
    for key, value in final_env.items():
        formatted_env.append('%s=%s' % (key, value))
    return {
        'env': formatted_env,
    }


def _get_expected_env_value(module, client, api_version, image, value, sentry):
    expected_env = {}
    if image and image['Config'].get('Env'):
        for env_var in image['Config']['Env']:
            parts = env_var.split('=', 1)
            expected_env[parts[0]] = parts[1]
    if value and value is not sentry:
        for env_var in value:
            parts = env_var.split('=', 1)
            expected_env[parts[0]] = parts[1]
    param_env = []
    for key, env_value in expected_env.items():
        param_env.append("%s=%s" % (key, env_value))
    return param_env


def _preprocess_cpus(module, client, api_version, value):
    if value is not None:
        value = int(round(value * 1E9))
    return value


def _preprocess_devices(module, client, api_version, value):
    if not value:
        return value
    expected_devices = []
    for device in value:
        parts = device.split(':')
        if len(parts) == 1:
            expected_devices.append(
                dict(
                    CgroupPermissions='rwm',
                    PathInContainer=parts[0],
                    PathOnHost=parts[0]
                ))
        elif len(parts) == 2:
            parts = device.split(':')
            expected_devices.append(
                dict(
                    CgroupPermissions='rwm',
                    PathInContainer=parts[1],
                    PathOnHost=parts[0]
                )
            )
        else:
            expected_devices.append(
                dict(
                    CgroupPermissions=parts[2],
                    PathInContainer=parts[1],
                    PathOnHost=parts[0]
                ))
    return expected_devices


def _preprocess_rate_bps(module, client, api_version, value):
    if not value:
        return value
    devices = []
    for device in value:
        devices.append({
            'Path': device['path'],
            'Rate': human_to_bytes(device['rate']),
        })
    return devices


def _preprocess_rate_iops(module, client, api_version, value):
    if not value:
        return value
    devices = []
    for device in value:
        devices.append({
            'Path': device['path'],
            'Rate': device['rate'],
        })
    return devices


def _preprocess_device_requests(module, client, api_version, value):
    if not value:
        return value
    device_requests = []
    for dr in value:
        device_requests.append({
            'Driver': dr['driver'],
            'Count': dr['count'],
            'DeviceIDs': dr['device_ids'],
            'Capabilities': dr['capabilities'],
            'Options': dr['options'],
        })
    return device_requests


def _preprocess_etc_hosts(module, client, api_version, value):
    if value is None:
        return value
    results = []
    for key, value in value.items():
        results.append('%s%s%s' % (key, ':', value))
    return results


def _preprocess_healthcheck(module, client, api_version, value):
    if value is None:
        return value
    healthcheck, disable_healthcheck = parse_healthcheck(value)
    if disable_healthcheck:
        healthcheck = {'test': ['NONE']}
    if not healthcheck:
        return None
    return omit_none_from_dict({
        'Test': healthcheck.get('test'),
        'Interval': healthcheck.get('interval'),
        'Timeout': healthcheck.get('timeout'),
        'StartPeriod': healthcheck.get('start_period'),
        'Retries': healthcheck.get('retries'),
    })


def _postprocess_healthcheck_get_value(module, api_version, value, sentry):
    if value is None or value is sentry or value.get('Test') == ['NONE']:
        return {'Test': ['NONE']}
    return value


def _preprocess_convert_to_bytes(module, values, name, unlimited_value=None):
    if name not in values:
        return values
    try:
        value = values[name]
        if unlimited_value is not None and value in ('unlimited', str(unlimited_value)):
            value = unlimited_value
        else:
            value = human_to_bytes(value)
        values[name] = value
        return values
    except ValueError as exc:
        module.fail_json(msg='Failed to convert %s to bytes: %s' % (name, to_native(exc)))


def _get_image_labels(image):
    if not image:
        return {}

    # Can't use get('Labels', {}) because 'Labels' may be present and be None
    return image['Config'].get('Labels') or {}


def _get_expected_labels_value(module, client, api_version, image, value, sentry):
    if value is sentry:
        return sentry
    expected_labels = {}
    if module.params['image_label_mismatch'] == 'ignore':
        expected_labels.update(dict(_get_image_labels(image)))
    expected_labels.update(value)
    return expected_labels


def _preprocess_links(module, client, api_version, value):
    if value is None:
        return None

    result = []
    for link in value:
        parsed_link = link.split(':', 1)
        if len(parsed_link) == 2:
            link, alias = parsed_link
        else:
            link, alias = parsed_link[0], parsed_link[0]
        result.append('/%s:/%s/%s' % (link, module.params['name'], alias))

    return result


def _ignore_mismatching_label_result(module, client, api_version, option, image, container_value, expected_value):
    if option.comparison == 'strict' and module.params['image_label_mismatch'] == 'fail':
        # If there are labels from the base image that should be removed and
        # base_image_mismatch is fail we want raise an error.
        image_labels = _get_image_labels(image)
        would_remove_labels = []
        labels_param = module.params['labels'] or {}
        for label in image_labels:
            if label not in labels_param:
                # Format label for error message
                would_remove_labels.append('"%s"' % (label, ))
        if would_remove_labels:
            msg = ("Some labels should be removed but are present in the base image. You can set image_label_mismatch to 'ignore' to ignore"
                   " this error. Labels: {0}")
            client.fail(msg.format(', '.join(would_remove_labels)))
    return False


def _preprocess_mac_address(module, values):
    if 'mac_address' not in values:
        return values
    return {
        'mac_address': values['mac_address'].replace('-', ':'),
    }


def _preprocess_networks(module, values):
    if module.params['networks_cli_compatible'] is True and values.get('networks') and 'network_mode' not in values:
        # Same behavior as Docker CLI: if networks are specified, use the name of the first network as the value for network_mode
        # (assuming no explicit value is specified for network_mode)
        values['network_mode'] = values['networks'][0]['name']

    if 'networks' in values:
        for network in values['networks']:
            if network['links']:
                parsed_links = []
                for link in network['links']:
                    parsed_link = link.split(':', 1)
                    if len(parsed_link) == 1:
                        parsed_link = (link, link)
                    parsed_links.append(tuple(parsed_link))
                network['links'] = parsed_links

    return values


def _ignore_mismatching_network_result(module, client, api_version, option, image, container_value, expected_value):
    # 'networks' is handled out-of-band
    if option.name == 'networks':
        return True
    return False


def _preprocess_network_values(module, client, api_version, options, values):
    if 'networks' in values:
        for network in values['networks']:
            network['id'] = _get_network_id(module, client, network['name'])
            if not network['id']:
                client.fail("Parameter error: network named %s could not be found. Does it exist?" % (network['name'], ))

    if 'network_mode' in values:
        values['network_mode'] = _preprocess_container_names(module, client, api_version, values['network_mode'])

    return values


def _get_network_id(module, client, network_name):
    try:
        network_id = None
        params = {'filters': json.dumps({'name': [network_name]})}
        for network in client.get_json('/networks', params=params):
            if network['Name'] == network_name:
                network_id = network['Id']
                break
        return network_id
    except Exception as exc:
        client.fail("Error getting network id for %s - %s" % (network_name, to_native(exc)))


def _get_values_network(module, container, api_version, options):
    value = container['HostConfig'].get('NetworkMode', _SENTRY)
    if value is _SENTRY:
        return {}
    return {'network_mode': value}


def _set_values_network(module, data, api_version, options, values):
    if 'network_mode' not in values:
        return
    if 'HostConfig' not in data:
        data['HostConfig'] = {}
    value = values['network_mode']
    data['HostConfig']['NetworkMode'] = value


def _preprocess_sysctls(module, values):
    if 'sysctls' in values:
        for key, value in values['sysctls'].items():
            values['sysctls'][key] = to_text(value, errors='surrogate_or_strict')
    return values


def _preprocess_tmpfs(module, values):
    if 'tmpfs' not in values:
        return values
    result = {}
    for tmpfs_spec in values['tmpfs']:
        split_spec = tmpfs_spec.split(":", 1)
        if len(split_spec) > 1:
            result[split_spec[0]] = split_spec[1]
        else:
            result[split_spec[0]] = ""
    return {
        'tmpfs': result
    }


def _preprocess_ulimits(module, values):
    if 'ulimits' not in values:
        return values
    result = []
    for limit in values['ulimits']:
        limits = dict()
        pieces = limit.split(':')
        if len(pieces) >= 2:
            limits['Name'] = pieces[0]
            limits['Soft'] = int(pieces[1])
            limits['Hard'] = int(pieces[1])
        if len(pieces) == 3:
            limits['Hard'] = int(pieces[2])
        result.append(limits)
    return {
        'ulimits': result,
    }


def _preprocess_mounts(module, values):
    last = dict()

    def check_collision(t, name):
        if t in last:
            if name == last[t]:
                module.fail_json(msg='The mount point "{0}" appears twice in the {1} option'.format(t, name))
            else:
                module.fail_json(msg='The mount point "{0}" appears both in the {1} and {2} option'.format(t, name, last[t]))
        last[t] = name

    if 'mounts' in values:
        mounts = []
        for mount in values['mounts']:
            target = mount['target']
            mount_type = mount['type']

            check_collision(target, 'mounts')

            mount_dict = dict(mount)

            # Sanity checks
            if mount['source'] is None and mount_type not in ('tmpfs', 'volume'):
                module.fail_json(msg='source must be specified for mount "{0}" of type "{1}"'.format(target, mount_type))
            for option, req_mount_type in _MOUNT_OPTION_TYPES.items():
                if mount[option] is not None and mount_type != req_mount_type:
                    module.fail_json(
                        msg='{0} cannot be specified for mount "{1}" of type "{2}" (needs type "{3}")'.format(option, target, mount_type, req_mount_type)
                    )

            # Streamline options
            volume_options = mount_dict.pop('volume_options')
            if mount_dict['volume_driver'] and volume_options:
                mount_dict['volume_options'] = clean_dict_booleans_for_docker_api(volume_options)
            if mount_dict['labels']:
                mount_dict['labels'] = clean_dict_booleans_for_docker_api(mount_dict['labels'])
            if mount_dict['tmpfs_size'] is not None:
                try:
                    mount_dict['tmpfs_size'] = human_to_bytes(mount_dict['tmpfs_size'])
                except ValueError as exc:
                    module.fail_json(msg='Failed to convert tmpfs_size of mount "{0}" to bytes: {1}'.format(target, to_native(exc)))
            if mount_dict['tmpfs_mode'] is not None:
                try:
                    mount_dict['tmpfs_mode'] = int(mount_dict['tmpfs_mode'], 8)
                except Exception as dummy:
                    module.fail_json(msg='tmp_fs mode of mount "{0}" is not an octal string!'.format(target))

            # Add result to list
            mounts.append(omit_none_from_dict(mount_dict))
        values['mounts'] = mounts
    if 'volumes' in values:
        new_vols = []
        for vol in values['volumes']:
            parts = vol.split(':')
            if ':' in vol:
                if len(parts) == 3:
                    host, container, mode = parts
                    if not _is_volume_permissions(mode):
                        module.fail_json(msg='Found invalid volumes mode: {0}'.format(mode))
                    if re.match(r'[.~]', host):
                        host = os.path.abspath(os.path.expanduser(host))
                    check_collision(container, 'volumes')
                    new_vols.append("%s:%s:%s" % (host, container, mode))
                    continue
                elif len(parts) == 2:
                    if not _is_volume_permissions(parts[1]) and re.match(r'[.~]', parts[0]):
                        host = os.path.abspath(os.path.expanduser(parts[0]))
                        check_collision(parts[1], 'volumes')
                        new_vols.append("%s:%s:rw" % (host, parts[1]))
                        continue
            check_collision(parts[min(1, len(parts) - 1)], 'volumes')
            new_vols.append(vol)
        values['volumes'] = new_vols
        new_binds = []
        for vol in new_vols:
            host = None
            if ':' in vol:
                parts = vol.split(':')
                if len(parts) == 3:
                    host, container, mode = parts
                    if not _is_volume_permissions(mode):
                        module.fail_json(msg='Found invalid volumes mode: {0}'.format(mode))
                elif len(parts) == 2:
                    if not _is_volume_permissions(parts[1]):
                        host, container, mode = (parts + ['rw'])
            if host is not None:
                new_binds.append('%s:%s:%s' % (host, container, mode))
        values['volume_binds'] = new_binds
    return values


def _get_values_mounts(module, container, api_version, options):
    volumes = container['Config'].get('Volumes')
    binds = container['HostConfig'].get('Binds')
    # According to https://github.com/moby/moby/, support for HostConfig.Mounts
    # has been included at least since v17.03.0-ce, which has API version 1.26.
    # The previous tag, v1.9.1, has API version 1.21 and does not have
    # HostConfig.Mounts. I have no idea what about API 1.25...
    mounts = container['HostConfig'].get('Mounts')
    if mounts is not None:
        result = []
        empty_dict = {}
        for mount in mounts:
            result.append({
                'type': mount.get('Type'),
                'source': mount.get('Source'),
                'target': mount.get('Target'),
                'read_only': mount.get('ReadOnly', False),  # golang's omitempty for bool returns None for False
                'consistency': mount.get('Consistency'),
                'propagation': mount.get('BindOptions', empty_dict).get('Propagation'),
                'no_copy': mount.get('VolumeOptions', empty_dict).get('NoCopy', False),
                'labels': mount.get('VolumeOptions', empty_dict).get('Labels', empty_dict),
                'volume_driver': mount.get('VolumeOptions', empty_dict).get('DriverConfig', empty_dict).get('Name'),
                'volume_options': mount.get('VolumeOptions', empty_dict).get('DriverConfig', empty_dict).get('Options', empty_dict),
                'tmpfs_size': mount.get('TmpfsOptions', empty_dict).get('SizeBytes'),
                'tmpfs_mode': mount.get('TmpfsOptions', empty_dict).get('Mode'),
            })
        mounts = result
    result = {}
    if volumes is not None:
        result['volumes'] = volumes
    if binds is not None:
        result['volume_binds'] = binds
    if mounts is not None:
        result['mounts'] = mounts
    return result


def _get_bind_from_dict(volume_dict):
    results = []
    if volume_dict:
        for host_path, config in volume_dict.items():
            if isinstance(config, dict) and config.get('bind'):
                container_path = config.get('bind')
                mode = config.get('mode', 'rw')
                results.append("%s:%s:%s" % (host_path, container_path, mode))
    return results


def _get_image_binds(volumes):
    '''
    Convert array of binds to array of strings with format host_path:container_path:mode

    :param volumes: array of bind dicts
    :return: array of strings
    '''
    results = []
    if isinstance(volumes, dict):
        results += _get_bind_from_dict(volumes)
    elif isinstance(volumes, list):
        for vol in volumes:
            results += _get_bind_from_dict(vol)
    return results


def _get_expected_values_mounts(module, client, api_version, options, image, values):
    expected_values = {}

    # binds
    if 'mounts' in values:
        expected_values['mounts'] = values['mounts']

    # volumes
    expected_vols = dict()
    if image and image['Config'].get('Volumes'):
        expected_vols.update(image['Config'].get('Volumes'))
    if 'volumes' in values:
        for vol in values['volumes']:
            # We only expect anonymous volumes to show up in the list
            if ':' in vol:
                parts = vol.split(':')
                if len(parts) == 3:
                    continue
                if len(parts) == 2:
                    if not _is_volume_permissions(parts[1]):
                        continue
            expected_vols[vol] = {}
    if expected_vols:
        expected_values['volumes'] = expected_vols

    # binds
    image_vols = []
    if image:
        image_vols = _get_image_binds(image['Config'].get('Volumes'))
    param_vols = []
    if 'volume_binds' in values:
        param_vols = values['volume_binds']
    expected_values['volume_binds'] = list(set(image_vols + param_vols))

    return expected_values


def _set_values_mounts(module, data, api_version, options, values):
    if 'mounts' in values:
        if 'HostConfig' not in data:
            data['HostConfig'] = {}
        mounts = []
        for mount in values['mounts']:
            mount_type = mount.get('type')
            mount_res = {
                'Target': mount.get('target'),
                'Source': mount.get('source'),
                'Type': mount_type,
                'ReadOnly': mount.get('read_only'),
            }
            if 'consistency' in mount:
                mount_res['Consistency'] = mount['consistency']
            if mount_type == 'bind':
                if 'propagation' in mount:
                    mount_res['BindOptions'] = {
                        'Propagation': mount['propagation'],
                    }
            if mount_type == 'volume':
                volume_opts = {}
                if mount.get('no_copy'):
                    volume_opts['NoCopy'] = True
                if mount.get('labels'):
                    volume_opts['Labels'] = mount.get('labels')
                if mount.get('volume_driver'):
                    driver_config = {
                        'Name': mount.get('volume_driver'),
                    }
                    if mount.get('volume_options'):
                        driver_config['Options'] = mount.get('volume_options')
                    volume_opts['DriverConfig'] = driver_config
                if volume_opts:
                    mount_res['VolumeOptions'] = volume_opts
            if mount_type == 'tmpfs':
                tmpfs_opts = {}
                if mount.get('tmpfs_mode'):
                    tmpfs_opts['Mode'] = mount.get('tmpfs_mode')
                if mount.get('tmpfs_size'):
                    tmpfs_opts['SizeBytes'] = mount.get('tmpfs_size')
                if mount.get('tmpfs_opts'):
                    mount_res['TmpfsOptions'] = mount.get('tmpfs_opts')
            mounts.append(mount_res)
        data['HostConfig']['Mounts'] = mounts
    if 'volumes' in values:
        volumes = {}
        for volume in values['volumes']:
            # Only pass anonymous volumes to create container
            if ':' in volume:
                parts = volume.split(':')
                if len(parts) == 3:
                    continue
                if len(parts) == 2:
                    if not _is_volume_permissions(parts[1]):
                        continue
            volumes[volume] = {}
        data['Volumes'] = volumes
    if 'volume_binds' in values:
        if 'HostConfig' not in data:
            data['HostConfig'] = {}
        data['HostConfig']['Binds'] = values['volume_binds']


def _preprocess_log(module, values):
    result = {}
    if 'log_driver' not in values:
        return result
    result['log_driver'] = values['log_driver']
    if 'log_options' in values:
        options = {}
        for k, v in values['log_options'].items():
            if not isinstance(v, string_types):
                module.warn(
                    "Non-string value found for log_options option '%s'. The value is automatically converted to '%s'. "
                    "If this is not correct, or you want to avoid such warnings, please quote the value." % (
                        k, to_text(v, errors='surrogate_or_strict'))
                )
            v = to_text(v, errors='surrogate_or_strict')
            options[k] = v
        result['log_options'] = options
    return result


def _get_values_log(module, container, api_version, options):
    log_config = container['HostConfig'].get('LogConfig') or {}
    return {
        'log_driver': log_config.get('Type'),
        'log_options': log_config.get('Config'),
    }


def _set_values_log(module, data, api_version, options, values):
    if 'log_driver' not in values:
        return
    log_config = {
        'Type': values['log_driver'],
        'Config': values.get('log_options') or {},
    }
    if 'HostConfig' not in data:
        data['HostConfig'] = {}
    data['HostConfig']['LogConfig'] = log_config


def _get_values_restart(module, container, api_version, options):
    restart_policy = container['HostConfig'].get('RestartPolicy') or {}
    return {
        'restart_policy': restart_policy.get('Name'),
        'restart_retries': restart_policy.get('MaximumRetryCount'),
    }


def _set_values_restart(module, data, api_version, options, values):
    if 'restart_policy' not in values:
        return
    restart_policy = {
        'Name': values['restart_policy'],
        'MaximumRetryCount': values.get('restart_retries'),
    }
    if 'HostConfig' not in data:
        data['HostConfig'] = {}
    data['HostConfig']['RestartPolicy'] = restart_policy


def _update_value_restart(module, data, api_version, options, values):
    if 'restart_policy' not in values:
        return
    data['RestartPolicy'] = {
        'Name': values['restart_policy'],
        'MaximumRetryCount': values.get('restart_retries'),
    }


def _preprocess_ports(module, values):
    if 'published_ports' in values:
        if 'all' in values['published_ports']:
            module.fail_json(
                msg='Specifying "all" in published_ports is no longer allowed. Set publish_all_ports to "true" instead '
                    'to randomly assign port mappings for those not specified by published_ports.')

        binds = {}
        for port in values['published_ports']:
            parts = _split_colon_ipv6(to_text(port, errors='surrogate_or_strict'), module)
            container_port = parts[-1]
            protocol = ''
            if '/' in container_port:
                container_port, protocol = parts[-1].split('/')
            container_ports = _parse_port_range(container_port, module)

            p_len = len(parts)
            if p_len == 1:
                port_binds = len(container_ports) * [(_DEFAULT_IP_REPLACEMENT_STRING, )]
            elif p_len == 2:
                if len(container_ports) == 1:
                    port_binds = [(_DEFAULT_IP_REPLACEMENT_STRING, parts[0])]
                else:
                    port_binds = [(_DEFAULT_IP_REPLACEMENT_STRING, port) for port in _parse_port_range(parts[0], module)]
            elif p_len == 3:
                # We only allow IPv4 and IPv6 addresses for the bind address
                ipaddr = parts[0]
                if not re.match(r'^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$', parts[0]) and not re.match(r'^\[[0-9a-fA-F:]+(?:|%[^\]/]+)\]$', ipaddr):
                    module.fail_json(
                        msg='Bind addresses for published ports must be IPv4 or IPv6 addresses, not hostnames. '
                            'Use the dig lookup to resolve hostnames. (Found hostname: {0})'.format(ipaddr)
                    )
                if re.match(r'^\[[0-9a-fA-F:]+\]$', ipaddr):
                    ipaddr = ipaddr[1:-1]
                if parts[1]:
                    if len(container_ports) == 1:
                        port_binds = [(ipaddr, parts[1])]
                    else:
                        port_binds = [(ipaddr, port) for port in _parse_port_range(parts[1], module)]
                else:
                    port_binds = len(container_ports) * [(ipaddr,)]
            else:
                module.fail_json(
                    msg='Invalid port description "%s" - expected 1 to 3 colon-separated parts, but got %d. '
                        'Maybe you forgot to use square brackets ([...]) around an IPv6 address?' % (port, p_len)
                )

            for bind, container_port in zip(port_binds, container_ports):
                idx = '{0}/{1}'.format(container_port, protocol) if protocol else container_port
                if idx in binds:
                    old_bind = binds[idx]
                    if isinstance(old_bind, list):
                        old_bind.append(bind)
                    else:
                        binds[idx] = [old_bind, bind]
                else:
                    binds[idx] = bind
        values['published_ports'] = binds

    exposed = []
    if 'exposed_ports' in values:
        for port in values['exposed_ports']:
            port = to_text(port, errors='surrogate_or_strict').strip()
            protocol = 'tcp'
            match = re.search(r'(/.+$)', port)
            if match:
                protocol = match.group(1).replace('/', '')
                port = re.sub(r'/.+$', '', port)
            exposed.append((port, protocol))
    if 'published_ports' in values:
        # Any published port should also be exposed
        for publish_port in values['published_ports']:
            match = False
            if isinstance(publish_port, string_types) and '/' in publish_port:
                port, protocol = publish_port.split('/')
                port = int(port)
            else:
                protocol = 'tcp'
                port = int(publish_port)
            for exposed_port in exposed:
                if exposed_port[1] != protocol:
                    continue
                if isinstance(exposed_port[0], string_types) and '-' in exposed_port[0]:
                    start_port, end_port = exposed_port[0].split('-')
                    if int(start_port) <= port <= int(end_port):
                        match = True
                elif exposed_port[0] == port:
                    match = True
            if not match:
                exposed.append((port, protocol))
    values['ports'] = exposed
    return values


def _get_values_ports(module, container, api_version, options):
    host_config = container['HostConfig']
    config = container['Config']

    # "ExposedPorts": null returns None type & causes AttributeError - PR #5517
    if config.get('ExposedPorts') is not None:
        expected_exposed = [_normalize_port(p) for p in config.get('ExposedPorts', dict()).keys()]
    else:
        expected_exposed = []

    return {
        'published_ports': host_config.get('PortBindings'),
        'exposed_ports': expected_exposed,
        'publish_all_ports': host_config.get('PublishAllPorts'),
    }


def _get_expected_values_ports(module, client, api_version, options, image, values):
    expected_values = {}

    if 'published_ports' in values:
        expected_bound_ports = {}
        for container_port, config in values['published_ports'].items():
            if isinstance(container_port, int):
                container_port = "%s/tcp" % container_port
            if len(config) == 1:
                if isinstance(config[0], int):
                    expected_bound_ports[container_port] = [{'HostIp': "0.0.0.0", 'HostPort': config[0]}]
                else:
                    expected_bound_ports[container_port] = [{'HostIp': config[0], 'HostPort': ""}]
            elif isinstance(config[0], tuple):
                expected_bound_ports[container_port] = []
                for host_ip, host_port in config:
                    expected_bound_ports[container_port].append({'HostIp': host_ip, 'HostPort': to_text(host_port, errors='surrogate_or_strict')})
            else:
                expected_bound_ports[container_port] = [{'HostIp': config[0], 'HostPort': to_text(config[1], errors='surrogate_or_strict')}]
        expected_values['published_ports'] = expected_bound_ports

    image_ports = []
    if image:
        image_exposed_ports = image['Config'].get('ExposedPorts') or {}
        image_ports = [_normalize_port(p) for p in image_exposed_ports]
    param_ports = []
    if 'ports' in values:
        param_ports = [to_text(p[0], errors='surrogate_or_strict') + '/' + p[1] for p in values['ports']]
    result = list(set(image_ports + param_ports))
    expected_values['exposed_ports'] = result

    if 'publish_all_ports' in values:
        expected_values['publish_all_ports'] = values['publish_all_ports']

    return expected_values


def _set_values_ports(module, data, api_version, options, values):
    if 'ports' in values:
        exposed_ports = {}
        for port_definition in values['ports']:
            port = port_definition
            proto = 'tcp'
            if isinstance(port_definition, tuple):
                if len(port_definition) == 2:
                    proto = port_definition[1]
                port = port_definition[0]
            exposed_ports['%s/%s' % (port, proto)] = {}
        data['ExposedPorts'] = exposed_ports
    if 'published_ports' in values:
        if 'HostConfig' not in data:
            data['HostConfig'] = {}
        data['HostConfig']['PortBindings'] = convert_port_bindings(values['published_ports'])
    if 'publish_all_ports' in values and values['publish_all_ports']:
        if 'HostConfig' not in data:
            data['HostConfig'] = {}
        data['HostConfig']['PublishAllPorts'] = values['publish_all_ports']


def _preprocess_value_ports(module, client, api_version, options, values):
    if 'published_ports' not in values:
        return values
    found = False
    for port_spec in values['published_ports'].values():
        if port_spec[0] == _DEFAULT_IP_REPLACEMENT_STRING:
            found = True
            break
    if not found:
        return values
    default_ip = _get_default_host_ip(module, client)
    for port, port_spec in values['published_ports'].items():
        if port_spec[0] == _DEFAULT_IP_REPLACEMENT_STRING:
            values['published_ports'][port] = tuple([default_ip] + list(port_spec[1:]))
    return values


def _preprocess_container_names(module, client, api_version, value):
    if value is None or not value.startswith('container:'):
        return value
    container_name = value[len('container:'):]
    # Try to inspect container to see whether this is an ID or a
    # name (and in the latter case, retrieve it's ID)
    container = client.get_container(container_name)
    if container is None:
        # If we can't find the container, issue a warning and continue with
        # what the user specified.
        module.warn('Cannot find a container with name or ID "{0}"'.format(container_name))
        return value
    return 'container:{0}'.format(container['Id'])


OPTIONS = [
    OptionGroup()
    .add_option('auto_remove', type='bool')
    .add_docker_api(DockerAPIEngine.host_config_value('AutoRemove')),

    OptionGroup()
    .add_option('blkio_weight', type='int')
    .add_docker_api(DockerAPIEngine.host_config_value('BlkioWeight', update_parameter='BlkioWeight')),

    OptionGroup()
    .add_option('capabilities', type='set', elements='str')
    .add_docker_api(DockerAPIEngine.host_config_value('CapAdd')),

    OptionGroup()
    .add_option('cap_drop', type='set', elements='str')
    .add_docker_api(DockerAPIEngine.host_config_value('CapDrop')),

    OptionGroup()
    .add_option('cgroup_parent', type='str')
    .add_docker_api(DockerAPIEngine.host_config_value('CgroupParent')),

    OptionGroup(preprocess=_preprocess_command)
    .add_option('command', type='list', elements='str', ansible_type='raw')
    .add_docker_api(DockerAPIEngine.config_value('Cmd')),

    OptionGroup()
    .add_option('cpu_period', type='int')
    .add_docker_api(DockerAPIEngine.host_config_value('CpuPeriod', update_parameter='CpuPeriod')),

    OptionGroup()
    .add_option('cpu_quota', type='int')
    .add_docker_api(DockerAPIEngine.host_config_value('CpuQuota', update_parameter='CpuQuota')),

    OptionGroup()
    .add_option('cpuset_cpus', type='str')
    .add_docker_api(DockerAPIEngine.host_config_value('CpusetCpus', update_parameter='CpusetCpus')),

    OptionGroup()
    .add_option('cpuset_mems', type='str')
    .add_docker_api(DockerAPIEngine.host_config_value('CpusetMems', update_parameter='CpusetMems')),

    OptionGroup()
    .add_option('cpu_shares', type='int')
    .add_docker_api(DockerAPIEngine.host_config_value('CpuShares', update_parameter='CpuShares')),

    OptionGroup(preprocess=_preprocess_entrypoint)
    .add_option('entrypoint', type='list', elements='str')
    .add_docker_api(DockerAPIEngine.config_value('Entrypoint')),

    OptionGroup()
    .add_option('cpus', type='int', ansible_type='float')
    .add_docker_api(DockerAPIEngine.host_config_value('NanoCpus', preprocess_value=_preprocess_cpus)),

    OptionGroup()
    .add_option('detach', type='bool')
    .add_option('interactive', type='bool')
    .add_docker_api(DockerAPIEngine(get_value=_get_value_detach_interactive, set_value=_set_value_detach_interactive)),

    OptionGroup()
    .add_option('devices', type='set', elements='dict', ansible_elements='str')
    .add_docker_api(DockerAPIEngine.host_config_value('Devices', preprocess_value=_preprocess_devices)),

    OptionGroup()
    .add_option('device_read_bps', type='set', elements='dict', ansible_suboptions=dict(
        path=dict(required=True, type='str'),
        rate=dict(required=True, type='str'),
    ))
    .add_docker_api(DockerAPIEngine.host_config_value('BlkioDeviceReadBps', preprocess_value=_preprocess_rate_bps)),

    OptionGroup()
    .add_option('device_write_bps', type='set', elements='dict', ansible_suboptions=dict(
        path=dict(required=True, type='str'),
        rate=dict(required=True, type='str'),
    ))
    .add_docker_api(DockerAPIEngine.host_config_value('BlkioDeviceWriteBps', preprocess_value=_preprocess_rate_bps)),

    OptionGroup()
    .add_option('device_read_iops', type='set', elements='dict', ansible_suboptions=dict(
        path=dict(required=True, type='str'),
        rate=dict(required=True, type='int'),
    ))
    .add_docker_api(DockerAPIEngine.host_config_value('BlkioDeviceReadIOps', preprocess_value=_preprocess_rate_iops)),

    OptionGroup()
    .add_option('device_write_iops', type='set', elements='dict', ansible_suboptions=dict(
        path=dict(required=True, type='str'),
        rate=dict(required=True, type='int'),
    ))
    .add_docker_api(DockerAPIEngine.host_config_value('BlkioDeviceWriteIOps', preprocess_value=_preprocess_rate_iops)),

    OptionGroup()
    .add_option('device_requests', type='set', elements='dict', ansible_suboptions=dict(
        capabilities=dict(type='list', elements='list'),
        count=dict(type='int'),
        device_ids=dict(type='list', elements='str'),
        driver=dict(type='str'),
        options=dict(type='dict'),
    ))
    .add_docker_api(DockerAPIEngine.host_config_value('DeviceRequests', min_api_version='1.40', preprocess_value=_preprocess_device_requests)),

    OptionGroup()
    .add_option('dns_servers', type='list', elements='str')
    .add_docker_api(DockerAPIEngine.host_config_value('Dns')),

    OptionGroup()
    .add_option('dns_opts', type='set', elements='str')
    .add_docker_api(DockerAPIEngine.host_config_value('DnsOptions')),

    OptionGroup()
    .add_option('dns_search_domains', type='list', elements='str')
    .add_docker_api(DockerAPIEngine.host_config_value('DnsSearch')),

    OptionGroup()
    .add_option('domainname', type='str')
    .add_docker_api(DockerAPIEngine.config_value('Domainname')),

    OptionGroup(preprocess=_preprocess_env)
    .add_option('env', type='set', ansible_type='dict', elements='str', needs_no_suboptions=True)
    .add_option('env_file', type='set', ansible_type='path', elements='str', not_a_container_option=True)
    .add_docker_api(DockerAPIEngine.config_value('Env', get_expected_value=_get_expected_env_value)),

    OptionGroup()
    .add_option('etc_hosts', type='set', ansible_type='dict', elements='str', needs_no_suboptions=True)
    .add_docker_api(DockerAPIEngine.host_config_value('ExtraHosts', preprocess_value=_preprocess_etc_hosts)),

    OptionGroup()
    .add_option('groups', type='set', elements='str')
    .add_docker_api(DockerAPIEngine.host_config_value('GroupAdd')),

    OptionGroup()
    .add_option('healthcheck', type='dict', ansible_suboptions=dict(
        test=dict(type='raw'),
        interval=dict(type='str'),
        timeout=dict(type='str'),
        start_period=dict(type='str'),
        retries=dict(type='int'),
    ))
    .add_docker_api(DockerAPIEngine.config_value(
        'Healthcheck', preprocess_value=_preprocess_healthcheck, postprocess_for_get=_postprocess_healthcheck_get_value)),

    OptionGroup()
    .add_option('hostname', type='str')
    .add_docker_api(DockerAPIEngine.config_value('Hostname')),

    OptionGroup(preprocess=_preprocess_networks)
    .add_option('image', type='str')
    .add_docker_api(DockerAPIEngine.config_value(
        'Image', ignore_mismatching_result=lambda module, client, api_version, option, image, container_value, expected_value: True)),

    OptionGroup()
    .add_option('init', type='bool')
    .add_docker_api(DockerAPIEngine.host_config_value('Init')),

    OptionGroup()
    .add_option('ipc_mode', type='str')
    .add_docker_api(DockerAPIEngine.host_config_value('IpcMode', preprocess_value=_preprocess_container_names)),

    OptionGroup(preprocess=partial(_preprocess_convert_to_bytes, name='kernel_memory'))
    .add_option('kernel_memory', type='int', ansible_type='str')
    .add_docker_api(DockerAPIEngine.host_config_value('KernelMemory', update_parameter='KernelMemory')),

    OptionGroup()
    .add_option('labels', type='dict', needs_no_suboptions=True)
    .add_docker_api(DockerAPIEngine.config_value(
        'Labels', get_expected_value=_get_expected_labels_value, ignore_mismatching_result=_ignore_mismatching_label_result)),

    OptionGroup()
    .add_option('links', type='set', elements='list', ansible_elements='str')
    .add_docker_api(DockerAPIEngine.host_config_value('Links', preprocess_value=_preprocess_links)),

    OptionGroup(preprocess=_preprocess_log, ansible_required_by={'log_options': ['log_driver']})
    .add_option('log_driver', type='str')
    .add_option('log_options', type='dict', ansible_aliases=['log_opt'], needs_no_suboptions=True)
    .add_docker_api(DockerAPIEngine(
        get_value=_get_values_log,
        set_value=_set_values_log,
    )),

    OptionGroup(preprocess=_preprocess_mac_address)
    .add_option('mac_address', type='str')
    .add_docker_api(DockerAPIEngine.config_value('MacAddress')),

    OptionGroup(preprocess=partial(_preprocess_convert_to_bytes, name='memory'))
    .add_option('memory', type='int', ansible_type='str')
    .add_docker_api(DockerAPIEngine.host_config_value('Memory', update_parameter='Memory')),

    OptionGroup(preprocess=partial(_preprocess_convert_to_bytes, name='memory_reservation'))
    .add_option('memory_reservation', type='int', ansible_type='str')
    .add_docker_api(DockerAPIEngine.host_config_value('MemoryReservation', update_parameter='MemoryReservation')),

    OptionGroup(preprocess=partial(_preprocess_convert_to_bytes, name='memory_swap', unlimited_value=-1))
    .add_option('memory_swap', type='int', ansible_type='str')
    .add_docker_api(DockerAPIEngine.host_config_value('MemorySwap', update_parameter='MemorySwap')),

    OptionGroup()
    .add_option('memory_swappiness', type='int')
    .add_docker_api(DockerAPIEngine.host_config_value('MemorySwappiness')),

    OptionGroup()
    .add_option('stop_timeout', type='int', default_comparison='ignore')
    .add_docker_api(DockerAPIEngine.config_value('StopTimeout')),

    OptionGroup(preprocess=_preprocess_networks)
    .add_option('network_mode', type='str')
    .add_option('networks', type='set', elements='dict', ansible_suboptions=dict(
        name=dict(type='str', required=True),
        ipv4_address=dict(type='str'),
        ipv6_address=dict(type='str'),
        aliases=dict(type='list', elements='str'),
        links=dict(type='list', elements='str'),
    ))
    .add_docker_api(DockerAPIEngine(
        preprocess_value=_preprocess_network_values,
        get_value=_get_values_network,
        set_value=_set_values_network,
        ignore_mismatching_result=_ignore_mismatching_network_result,
    )),

    OptionGroup()
    .add_option('oom_killer', type='bool')
    .add_docker_api(DockerAPIEngine.host_config_value('OomKillDisable')),

    OptionGroup()
    .add_option('oom_score_adj', type='int')
    .add_docker_api(DockerAPIEngine.host_config_value('OomScoreAdj')),

    OptionGroup()
    .add_option('pid_mode', type='str')
    .add_docker_api(DockerAPIEngine.host_config_value('PidMode', preprocess_value=_preprocess_container_names)),

    OptionGroup()
    .add_option('pids_limit', type='int')
    .add_docker_api(DockerAPIEngine.host_config_value('PidsLimit')),

    OptionGroup()
    .add_option('privileged', type='bool')
    .add_docker_api(DockerAPIEngine.host_config_value('Privileged')),

    OptionGroup()
    .add_option('read_only', type='bool')
    .add_docker_api(DockerAPIEngine.host_config_value('ReadonlyRootfs')),

    OptionGroup(ansible_required_by={'restart_retries': ['restart_policy']})
    .add_option('restart_policy', type='str', ansible_choices=['no', 'on-failure', 'always', 'unless-stopped'])
    .add_option('restart_retries', type='int')
    .add_docker_api(DockerAPIEngine(
        get_value=_get_values_restart,
        set_value=_set_values_restart,
        update_value=_update_value_restart,
    )),

    OptionGroup()
    .add_option('runtime', type='str')
    .add_docker_api(DockerAPIEngine.host_config_value('Runtime')),

    OptionGroup()
    .add_option('security_opts', type='set', elements='str')
    .add_docker_api(DockerAPIEngine.host_config_value('SecurityOpt')),

    OptionGroup(preprocess=partial(_preprocess_convert_to_bytes, name='shm_size'))
    .add_option('shm_size', type='int', ansible_type='str')
    .add_docker_api(DockerAPIEngine.host_config_value('ShmSize')),

    OptionGroup()
    .add_option('stop_signal', type='str')
    .add_docker_api(DockerAPIEngine.config_value('StopSignal')),

    OptionGroup()
    .add_option('storage_opts', type='dict', needs_no_suboptions=True)
    .add_docker_api(DockerAPIEngine.host_config_value('StorageOpt')),

    OptionGroup(preprocess=_preprocess_sysctls)
    .add_option('sysctls', type='dict', needs_no_suboptions=True)
    .add_docker_api(DockerAPIEngine.host_config_value('Sysctls')),

    OptionGroup(preprocess=_preprocess_tmpfs)
    .add_option('tmpfs', type='dict', ansible_type='list', ansible_elements='str')
    .add_docker_api(DockerAPIEngine.host_config_value('Tmpfs')),

    OptionGroup()
    .add_option('tty', type='bool')
    .add_docker_api(DockerAPIEngine.config_value('Tty')),

    OptionGroup(preprocess=_preprocess_ulimits)
    .add_option('ulimits', type='set', elements='dict', ansible_elements='str')
    .add_docker_api(DockerAPIEngine.host_config_value('Ulimits')),

    OptionGroup()
    .add_option('user', type='str')
    .add_docker_api(DockerAPIEngine.config_value('User')),

    OptionGroup()
    .add_option('userns_mode', type='str')
    .add_docker_api(DockerAPIEngine.host_config_value('UsernsMode')),

    OptionGroup()
    .add_option('uts', type='str')
    .add_docker_api(DockerAPIEngine.host_config_value('UTSMode')),

    OptionGroup()
    .add_option('volume_driver', type='str')
    .add_docker_api(DockerAPIEngine.host_config_value('VolumeDriver')),

    OptionGroup()
    .add_option('volumes_from', type='set', elements='str')
    .add_docker_api(DockerAPIEngine.host_config_value('VolumesFrom')),

    OptionGroup()
    .add_option('working_dir', type='str')
    .add_docker_api(DockerAPIEngine.config_value('WorkingDir')),

    OptionGroup(preprocess=_preprocess_mounts)
    .add_option('mounts', type='set', elements='dict', ansible_suboptions=dict(
        target=dict(type='str', required=True),
        source=dict(type='str'),
        type=dict(type='str', choices=['bind', 'volume', 'tmpfs', 'npipe'], default='volume'),
        read_only=dict(type='bool'),
        consistency=dict(type='str', choices=['default', 'consistent', 'cached', 'delegated']),
        propagation=dict(type='str', choices=['private', 'rprivate', 'shared', 'rshared', 'slave', 'rslave']),
        no_copy=dict(type='bool'),
        labels=dict(type='dict'),
        volume_driver=dict(type='str'),
        volume_options=dict(type='dict'),
        tmpfs_size=dict(type='str'),
        tmpfs_mode=dict(type='str'),
    ))
    .add_option('volumes', type='set', elements='str')
    .add_option('volume_binds', type='set', elements='str', not_an_ansible_option=True, copy_comparison_from='volumes')
    .add_docker_api(DockerAPIEngine(
        get_value=_get_values_mounts,
        get_expected_values=_get_expected_values_mounts,
        set_value=_set_values_mounts,
    )),

    OptionGroup(preprocess=_preprocess_ports)
    .add_option('exposed_ports', type='set', elements='str', ansible_aliases=['exposed', 'expose'])
    .add_option('publish_all_ports', type='bool')
    .add_option('published_ports', type='dict', ansible_type='list', ansible_elements='str', ansible_aliases=['ports'])
    .add_option('ports', type='set', elements='str', not_an_ansible_option=True, default_comparison='ignore')
    .add_docker_api(DockerAPIEngine(
        get_value=_get_values_ports,
        get_expected_values=_get_expected_values_ports,
        set_value=_set_values_ports,
        preprocess_value=_preprocess_value_ports,
    )),
]
