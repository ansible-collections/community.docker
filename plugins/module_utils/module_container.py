# Copyright (c) 2022 Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import shlex

from functools import partial

from ansible.module_utils.common.text.converters import to_native, to_text
from ansible.module_utils.common.text.formatters import human_to_bytes

from ansible_collections.community.docker.plugins.module_utils.version import LooseVersion

from ansible_collections.community.docker.plugins.module_utils.util import (
    parse_healthcheck,
)

from ansible_collections.community.docker.plugins.module_utils._api.utils.utils import parse_env_file


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
        needs_suboptions = (self.type in ('list', 'set') and elements == 'dict') or (self.type == 'dict')
        if ansible_suboptions is not None and not needs_suboptions:
            raise Exception('suboptions only allowed for Ansible lists with dicts, or Ansible dicts')
        if ansible_suboptions is None and needs_suboptions and not needs_no_suboptions:
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


class DockerAPIEngineDriver(object):
    pass


class DockerAPIEngine(object):
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
        min_docker_api=None,
    ):
        self.min_docker_api = min_docker_api
        self.min_docker_api_obj = None if min_docker_api is None else LooseVersion(min_docker_api)
        self.get_value = get_value
        self.set_value = set_value
        self.get_expected_values = get_expected_values or (lambda module, client, api_version, options, image, values: values)
        self.ignore_mismatching_result = ignore_mismatching_result or (lambda module, client, api_version, option, image, container_value, expected_value: False)
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
        min_docker_api=None,
        preprocess_value=None,
        update_parameter=None,
    ):
        def preprocess_value_(module, client, api_version, options, values):
            if len(options) != 1:
                raise AssertionError('config_value can only be used for a single option')
            if preprocess_value is not None and options[0].name in values:
                values[options[0].name] = preprocess_value(module, client, api_version, values[options[0].name])
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
            min_docker_api=min_docker_api,
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
        min_docker_api=None,
        preprocess_value=None,
        update_parameter=None,
    ):
        def preprocess_value_(module, client, api_version, options, values):
            if len(options) != 1:
                raise AssertionError('host_config_value can only be used for a single option')
            if preprocess_value is not None and options[0].name in values:
                values[options[0].name] = preprocess_value(module, client, api_version, values[options[0].name])
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
            min_docker_api=min_docker_api,
            update_value=update_value,
        )


def _get_value_detach_interactive(module, container, api_version, options):
    attach_stdin = container.get('AttachStdin')
    attach_stderr = container.get('AttachStderr')
    attach_stdout = container.get('AttachStdout')
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
    if not detach:
        data['AttachStdout'] = True
        data['AttachStderr'] = True
        if interactive:
            data['AttachStdin'] = True
            data['StdinOnce'] = True


def _preprocess_command(module, client, api_version, value):
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
    return value


def _preprocess_entrypoint(module, api_version, value):
    if module.params['command_handling'] == 'correct':
        if value is not None:
            value = [to_text(x, errors='surrogate_or_strict') for x in value]
    elif value:
        # convert from list to str.
        value = shlex.split(' '.join([to_text(x, errors='surrogate_or_strict') for x in value]))
        value = [to_text(x, errors='surrogate_or_strict') for x in value]
    return value


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
    for key, value in final_env:
        formatted_env.append('%s=%s' % (key, value))
    return formatted_env


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
    return {
        'Test': healthcheck.get('test'),
        'Interval': healthcheck.get('interval'),
        'Timeout': healthcheck.get('timeout'),
        'StartPeriod': healthcheck.get('start_period'),
        'Retries': healthcheck.get('retries'),
    }


def _postprocess_healthcheck_get_value(module, api_version, value, sentry):
    if value is None or value is sentry or value.get('Test') == ['NONE']:
        return {'Test': ['NONE']}
    return value


def _preprocess_convert_to_bytes(module, values, name, unlimited_value=None):
    if name not in values:
        return values
    try:
        value = values[name]
        if unlimited_value is not None and value == 'unlimited':
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
        for label in image_labels:
            if label not in module.params['labels'] or {}:
                # Format label for error message
                would_remove_labels.append('"%s"' % (label, ))
        if would_remove_labels:
            msg = ("Some labels should be removed but are present in the base image. You can set image_label_mismatch to 'ignore' to ignore"
                   " this error. Labels: {0}")
            module.fail_json(msg=msg.format(', '.join(would_remove_labels)))
    return False


def _preprocess_mac_address(module, values):
    if 'mac_address' not in values:
        return values
    return {
        'mac_address': values['mac_address'].replace('-', ':'),
    }


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
    .add_docker_api(DockerAPIEngine.config_value('BlkioWeight', update_parameter='BlkioWeight')),

    OptionGroup()
    .add_option('capabilities', type='set', elements='str')
    .add_docker_api(DockerAPIEngine.host_config_value('CapAdd')),

    OptionGroup()
    .add_option('cap_drop', type='set', elements='str')
    .add_docker_api(DockerAPIEngine.host_config_value('CapDrop')),

    OptionGroup()
    .add_option('cgroup_parent', type='str')
    .add_docker_api(DockerAPIEngine.host_config_value('CgroupParent')),

    OptionGroup()
    .add_option('command', type='list', elements='str', ansible_type='raw')
    .add_docker_api(DockerAPIEngine.config_value('Cmd', preprocess_value=_preprocess_command)),

    OptionGroup()
    .add_option('cpu_period', type='int')
    .add_docker_api(DockerAPIEngine.config_value('CpuPeriod', update_parameter='CpuPeriod')),

    OptionGroup()
    .add_option('cpu_quota', type='int')
    .add_docker_api(DockerAPIEngine.config_value('CpuQuota', update_parameter='CpuQuota')),

    OptionGroup()
    .add_option('cpuset_cpus', type='str')
    .add_docker_api(DockerAPIEngine.config_value('CpuShares', update_parameter='CpuShares')),

    OptionGroup()
    .add_option('cpuset_mems', type='str')
    .add_docker_api(DockerAPIEngine.config_value('CpusetCpus', update_parameter='CpusetCpus')),

    OptionGroup()
    .add_option('cpu_shares', type='int')
    .add_docker_api(DockerAPIEngine.config_value('CpusetMems', update_parameter='CpusetMems')),

    OptionGroup()
    .add_option('entrypoint', type='list', elements='str')
    .add_docker_api(DockerAPIEngine.config_value('Entrypoint', preprocess_value=_preprocess_command)),

    OptionGroup()
    .add_option('cpus', type='int', ansible_type='float')
    .add_docker_api(DockerAPIEngine.host_config_value('NanoCpus', preprocess_value=_preprocess_cpus)),

    OptionGroup()
    .add_option('detach', type='bool')
    .add_option('interactive', type='bool')
    .add_docker_api(DockerAPIEngine(get_value=_get_value_detach_interactive, set_value=_set_value_detach_interactive)),

    OptionGroup()
    .add_option('devices', type='set', elements='str')
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
    .add_docker_api(DockerAPIEngine.host_config_value('DeviceRequests', min_docker_api='1.40', preprocess_value=_preprocess_device_requests)),

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
    .add_option('env', type='set', ansible_type='dict', elements='str')
    .add_option('env_file', type='set', ansible_type='path', elements='str', not_a_container_option=True)
    .add_docker_api(DockerAPIEngine.config_value('Env', get_expected_value=_get_expected_env_value)),

    OptionGroup()
    .add_option('etc_hosts', type='set', ansible_type='dict', elements='str')
    .add_docker_api(DockerAPIEngine.host_config_value('ExtraHosts', preprocess_value=_preprocess_etc_hosts)),

    OptionGroup()
    .add_option('groups', type='set', elements='str')
    .add_docker_api(DockerAPIEngine.config_value('GroupAdd')),

    OptionGroup()
    .add_option('healthcheck', type='dict', ansible_suboptions=dict(
        test=dict(type='raw'),
        interval=dict(type='str'),
        timeout=dict(type='str'),
        start_period=dict(type='str'),
        retries=dict(type='int'),
    ))
    .add_docker_api(DockerAPIEngine.config_value('GroupAdd', preprocess_value=_preprocess_healthcheck, postprocess_for_get=_postprocess_healthcheck_get_value)),

    OptionGroup()
    .add_option('hostname', type='str')
    .add_docker_api(DockerAPIEngine.config_value('Hostname')),

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
    .add_docker_api(DockerAPIEngine.config_value('Labels', get_expected_value=_get_expected_labels_value, ignore_mismatching_result=_ignore_mismatching_label_result)),

    OptionGroup()
    .add_option('links', type='set', elements='list', ansible_elements='str')
    .add_docker_api(DockerAPIEngine.config_value('Links', preprocess_value=_preprocess_links)),

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

    OptionGroup()
    .add_option('network_mode', type='str')
    .add_docker_api(DockerAPIEngine.host_config_value('NetworkMode', preprocess_value=_preprocess_container_names)),

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
    .add_option('storage_opts', type='dict', needs_no_suboptions=True)
    .add_docker_api(DockerAPIEngine.host_config_value('StorageOpt')),

    OptionGroup()
    .add_option('tty', type='bool')
    .add_docker_api(DockerAPIEngine.config_value('Tty')),

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
]

# Options / option groups that are more complex:
#         exposed_ports=dict(type='list', elements='str', aliases=['exposed', 'expose']),
#         publish_all_ports=dict(type='bool'),
#         published_ports=dict(type='list', elements='str', aliases=['ports']),

#    OptionGroup(ansible_required_by={'log_options': ['log_driver']})
#    .add_option('log_driver', type='str')
#    .add_option('log_options', type='dict', ansible_aliases=['log_opt'])
#    .add_docker_api(...)

#    OptionGroup(ansible_required_by={'restart_retries': ['restart_policy']})
#    .add_option('restart_policy', type='str', ansible_choices=['no', 'on-failure', 'always', 'unless-stopped'])
#    .add_option('restart_retries', type='int')
#    .add_docker_api(..., )
#   ---------------- only for policy: update_parameter='RestartPolicy'

# Options to convert / triage:
#         mounts=dict(type='list', elements='dict', options=dict(
#             target=dict(type='str', required=True),
#             source=dict(type='str'),
#             type=dict(type='str', choices=['bind', 'volume', 'tmpfs', 'npipe'], default='volume'),
#             read_only=dict(type='bool'),
#             consistency=dict(type='str', choices=['default', 'consistent', 'cached', 'delegated']),
#             propagation=dict(type='str', choices=['private', 'rprivate', 'shared', 'rshared', 'slave', 'rslave']),
#             no_copy=dict(type='bool'),
#             labels=dict(type='dict'),
#             volume_driver=dict(type='str'),
#             volume_options=dict(type='dict'),
#             tmpfs_size=dict(type='str'),
#             tmpfs_mode=dict(type='str'),
#         )),
#         sysctls=dict(type='dict'),
#         tmpfs=dict(type='list', elements='str'),
#         ulimits=dict(type='list', elements='str'),
#         volumes=dict(type='list', elements='str'),
#
#         explicit_types = dict(
#             mounts='set(dict)',
#             ulimits='set(dict)',
#         )
