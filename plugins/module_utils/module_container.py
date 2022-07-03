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


def _get_ansible_type(type):
    if type == 'set':
        return 'list'
    if type not in ('list', 'dict', 'int', 'float', 'str'):
        raise Exception('Invalid type "%s"' % (type, ))
    return type


class Option(object):
    def __init__(self, name, type, ansible_type=None, elements=None, ansible_elements=None, ansible_suboptions=None, ansible_aliases=None):
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
        if ansible_suboptions is None and needs_suboptions:
            raise Exception('suboptions required for Ansible lists with dicts, or Ansible dicts')
        self.ansible_suboptions = ansible_suboptions if needs_suboptions else None
        self.ansible_aliases = ansible_aliases


class OptionGroup(object):
    def __init__(self, preprocess=None):
        if preprocess is None:
            def preprocess(module, values):
                return values
        self.preprocess = preprocess
        self.options = []
        self.engines = {}

    def add_option(self, *args, **kwargs):
        self.options.append(Option(*args, **kwargs))
        return self

    def add_docker_api(self, docker_api):
        self.engines['docker_api'] = docker_api
        return self


_SENTRY = object()


def DockerAPIEngine(object):
    def __init__(self, get_value, preprocess_value, set_value=None, update_value=None, can_set_value=None, can_update_value=None, min_docker_api=None):
        self.min_docker_api = min_docker_api
        self.min_docker_api_obj = None if min_docker_api is None else LooseVersion(min_docker_api)
        self.get_value = get_value
        self.set_value = set_value
        self.preprocess_value = preprocess_value
        self.update_value = update_value
        self.can_set_value = can_set_value or (lambda api_version: set_value is not None)
        self.can_update_value = can_update_value or (lambda api_version: update_value is not None)

    @classmethod
    def config_value(cls, host_config_name, postprocess_for_get=None, preprocess_for_set=None, min_docker_api=None, preprocess_value=None):
        def preprocess_value_(module, api_version, options, values):
            if len(options) != 1:
                raise AssertionError('config_value can only be used for a single option')
            if preprocess_value is not None and options[0].name in values:
                values[options[0].name] = preprocess_value(module, api_version, values[options[0].name])
            return values

        def get_value(module, container, api_version, options):
            if len(options) != 1:
                raise AssertionError('config_value can only be used for a single option')
            value = container.get(host_config_name, _SENTRY)
            if postprocess_for_get:
                value = postprocess_for_get(module, api_version, value, _SENTRY)
            if value is _SENTRY:
                return {}
            return {options[0].name: value}

        def set_value(module, data, api_version, options, values):
            if len(options) != 1:
                raise AssertionError('config_value can only be used for a single option')
            if options[0].name not in values:
                return
            value = values[options[0].name]
            if preprocess_for_set:
                value = preprocess_for_set(module, api_version, value)
            data[host_config_name] = value

        return cls(get_value=get_value, preprocess_value=preprocess_value_, set_value=set_value, min_docker_api=min_docker_api)

    @classmethod
    def host_config_value(cls, host_config_name, postprocess_for_get=None, preprocess_for_set=None, min_docker_api=None, preprocess_value=None):
        def preprocess_value_(module, api_version, options, values):
            if len(options) != 1:
                raise AssertionError('host_config_value can only be used for a single option')
            if preprocess_value is not None and options[0].name in values:
                values[options[0].name] = preprocess_value(module, api_version, values[options[0].name])
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

        return cls(get_value=get_value, preprocess_value=preprocess_value_, set_value=set_value, min_docker_api=min_docker_api)


def _preprocess_command(module, api_version, value):
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


def _preprocess_cpus(module, api_version, value):
    if value is not None:
        value = int(round(value * 1E9))
    return value


def _preprocess_devices(module, api_version, value):
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


def _preprocess_rate_bps(module, api_version, value, name):
    if not value:
        return value
    devices = []
    for device in value:
        devices.append({
            'Path': device['path'],
            'Rate': human_to_bytes(device['rate']),
        })
    return devices


def _preprocess_rate_iops(module, api_version, value, name):
    if not value:
        return value
    devices = []
    for device in value:
        devices.append({
            'Path': device['path'],
            'Rate': device['rate'],
        })
    return devices


def _preprocess_device_requests(module, api_version, value):
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


def _preprocess_etc_hosts(module, api_version, value):
    if value is None:
        return value
    results = []
    for key, value in value.items():
        results.append("%s%s%s" % (key, ':', value))
    return results


def _preprocess_healthcheck(module, api_version, value):
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
        return
    try:
        value = values[name]
        if unlimited_value is not None and value == 'unlimited':
            value = unlimited_value
        else:
            value = human_to_bytes(value)
        values[name] = 
    except ValueError as exc:
        self.fail("Failed to convert %s to bytes: %s" % (name, to_native(exc)))


def _preprocess_links(module, api_version, value):
    if value is None:
        return None

    result = []
    for link in value:
        parsed_link = link.split(':', 1)
        if len(parsed_link) == 2:
            link, alias = parsed_link
        else:
            link, alias = parsed_link[0], parsed_link[0]
        result.append("/%s:/%s/%s" % (link, module.params['name'], alias))

    return result


OPTIONS = [
    OptionGroup()
    .add_option('auto_remove', type='bool')
    .add_docker_api(DockerAPIEngine.host_config_value('AutoRemove', min_docker_api='1.25')),

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
    .add_option('entrypoint', type='list', elements='str')
    .add_docker_api(DockerAPIEngine.config_value('Entrypoint', preprocess_value=_preprocess_command)),

    OptionGroup()
    .add_option('cpus', type='int', ansible_type='float')
    .add_docker_api(DockerAPIEngine.host_config_value('NanoCpus', min_docker_api='1.25', preprocess_value=_preprocess_cpus)),

    OptionGroup()
    .add_option('devices', type='set', elements='str')
    .add_docker_api(DockerAPIEngine.host_config_value('Devices', preprocess_value=_preprocess_devices)),

    OptionGroup()
    .add_option('device_read_bps', type='set', elements='dict', ansible_suboptions=dict(
        path=dict(required=True, type='str'),
        rate=dict(required=True, type='str'),
    ))
    .add_docker_api(DockerAPIEngine.host_config_value('BlkioDeviceReadBps', min_docker_api='1.22', preprocess_value=partial(_preprocess_rate_bps, name='device_read_bps'))),

    OptionGroup()
    .add_option('device_write_bps', type='set', elements='dict', ansible_suboptions=dict(
        path=dict(required=True, type='str'),
        rate=dict(required=True, type='str'),
    ))
    .add_docker_api(DockerAPIEngine.host_config_value('BlkioDeviceWriteBps', min_docker_api='1.22', preprocess_value=partial(_preprocess_rate_bps, name='device_write_bps'))),

    OptionGroup()
    .add_option('device_read_iops', type='set', elements='dict', ansible_suboptions=dict(
        path=dict(required=True, type='str'),
        rate=dict(required=True, type='int'),
    ))
    .add_docker_api(DockerAPIEngine.host_config_value('BlkioDeviceReadIOps', min_docker_api='1.22', preprocess_value=partial(_preprocess_rate_iops, name='device_read_iops'))),

    OptionGroup()
    .add_option('device_write_iops', type='set', elements='dict', ansible_suboptions=dict(
        path=dict(required=True, type='str'),
        rate=dict(required=True, type='int'),
    ))
    .add_docker_api(DockerAPIEngine.host_config_value('BlkioDeviceWriteIOps', min_docker_api='1.22', preprocess_value=partial(_preprocess_rate_iops, name='device_write_iops'))),

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
    .add_docker_api(DockerAPIEngine.host_config_value('DnsOptions', min_docker_api='1.21')),

    OptionGroup()
    .add_option('dns_search_domains', type='list', elements='str')
    .add_docker_api(DockerAPIEngine.host_config_value('DnsSearch')),

    OptionGroup()
    .add_option('domainname', type='str')
    .add_docker_api(DockerAPIEngine.config_value('Domainname')),

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
    .add_docker_api(DockerAPIEngine.config_value('GroupAdd', min_docker_api='1.24', preprocess_value=_preprocess_healthcheck, postprocess_for_get=_postprocess_healthcheck_get_value)),

    OptionGroup()
    .add_option('hostname', type='str')
    .add_docker_api(DockerAPIEngine.config_value('Hostname')),

    OptionGroup()
    .add_option('init', type='bool')
    .add_docker_api(DockerAPIEngine.host_config_value('Init', min_docker_api='1.25')),

    OptionGroup()
    .add_option('interactive', type='bool')
    .add_docker_api(DockerAPIEngine.config_value('OpenStdin')),

    OptionGroup()
    .add_option('links', type='set', elements='list', ansible_elements='str')
    .add_docker_api(DockerAPIEngine.config_value('Links', preprocess_values=_preprocess_links)),

    OptionGroup()
    .add_option('memory_swappiness', type='int')
    .add_docker_api(DockerAPIEngine.host_config_value('MemorySwappiness')),
]

# Regular module options:
#         cleanup=dict(type='bool', default=False),
#         comparisons=dict(type='dict'),
#         container_default_behavior=dict(type='str', default='no_defaults', choices=['compatibility', 'no_defaults']),
#         command_handling=dict(type='str', choices=['compatibility', 'correct']),
#         default_host_ip=dict(type='str'),
#         force_kill=dict(type='bool', default=False, aliases=['forcekill']),
#         ignore_image=dict(type='bool', default=False),
#         image=dict(type='str'),
#         image_label_mismatch=dict(type='str', choices=['ignore', 'fail'], default='ignore'),
#         keep_volumes=dict(type='bool', default=True),
#         kill_signal=dict(type='str'),
#         name=dict(type='str', required=True),

# Options that can be updated:
#         blkio_weight=dict(type='int'),
#         cpu_period=dict(type='int'),
#         cpu_quota=dict(type='int'),
#         cpuset_cpus=dict(type='str'),
#         cpuset_mems=dict(type='str'),
#         cpu_shares=dict(type='int'),

#    OptionGroup(preprocess=partial(_preprocess_convert_to_bytes, name='kernel_memory'))
#    .add_option('kernel_memory', type='int', ansible_type='str')
#    .add_docker_api(DockerAPIEngine.host_config_value('KernelMemory', min_docker_api='1.21')),


#    OptionGroup(preprocess=partial(_preprocess_convert_to_bytes, name='memory'))
#    .add_option('memory', type='int', ansible_type='str')
#    .add_docker_api(DockerAPIEngine.host_config_value('Memory')),

#    OptionGroup(preprocess=partial(_preprocess_convert_to_bytes, name='memory_reservation'))
#    .add_option('memory_reservation', type='int', ansible_type='str')
#    .add_docker_api(DockerAPIEngine.host_config_value('MemoryReservation', min_docker_api='1.21')),

#    OptionGroup(preprocess=partial(_preprocess_convert_to_bytes, name='memory_swap', unlimited_value=-1))
#    .add_option('memory_swap', type='int', ansible_type='str')
#    .add_docker_api(DockerAPIEngine.host_config_value('MemorySwap')),

# Options / option groups that are more complex:
#         detach=dict(type='bool'),
#         env=dict(type='dict'),
#         env_file=dict(type='path'),
#         exposed_ports=dict(type='list', elements='str', aliases=['exposed', 'expose']),
#         ipc_mode=dict(type='str'),
#         labels=dict(type='dict'),


#    OptionGroup()
#    .add_option('log_driver', type='str')
#    .add_option('log_options', type='dict', ansible_aliases=['log_opt'])
#    .add_docker_api(...)

#        if self.mac_address:
#            # Ensure the MAC address uses colons instead of hyphens for later comparison
#            self.mac_address = self.mac_address.replace('-', ':')
#
#        mac_address=config.get('MacAddress', network.get('MacAddress')),
#
#         mac_address=dict(type='str'),
#             mac_address=dict(docker_api_version='1.25'),

# REQUIRES_CONVERSION_TO_BYTES = [
#    'shm_size'
# ]

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
#         network_mode=dict(type='str'),
#         networks=dict(type='list', elements='dict', options=dict(
#             name=dict(type='str', required=True),
#             ipv4_address=dict(type='str'),
#             ipv6_address=dict(type='str'),
#             aliases=dict(type='list', elements='str'),
#             links=dict(type='list', elements='str'),
#         )),
#         networks_cli_compatible=dict(type='bool', default=True),
#         oom_killer=dict(type='bool'),
#         oom_score_adj=dict(type='int'),
#         output_logs=dict(type='bool', default=False),
#         paused=dict(type='bool'),
#         pid_mode=dict(type='str'),
#         pids_limit=dict(type='int'),
#         privileged=dict(type='bool'),
#         publish_all_ports=dict(type='bool'),
#         published_ports=dict(type='list', elements='str', aliases=['ports']),
#         pull=dict(type='bool', default=False),
#         purge_networks=dict(type='bool', default=False),
#         read_only=dict(type='bool'),
#         recreate=dict(type='bool', default=False),
#         removal_wait_timeout=dict(type='float'),
#         restart=dict(type='bool', default=False),
#         restart_policy=dict(type='str', choices=['no', 'on-failure', 'always', 'unless-stopped']),
#         restart_retries=dict(type='int'),
#         runtime=dict(type='str'),
#         security_opts=dict(type='list', elements='str'),
#         shm_size=dict(type='str'),
#         state=dict(type='str', default='started', choices=['absent', 'present', 'started', 'stopped']),
#         stop_signal=dict(type='str'),
#         stop_timeout=dict(type='int'),
#         storage_opts=dict(type='dict'),
#         sysctls=dict(type='dict'),
#         tmpfs=dict(type='list', elements='str'),
#         tty=dict(type='bool'),
#         ulimits=dict(type='list', elements='str'),
#         user=dict(type='str'),
#         userns_mode=dict(type='str'),
#         uts=dict(type='str'),
#         volume_driver=dict(type='str'),
#         volumes=dict(type='list', elements='str'),
#         volumes_from=dict(type='list', elements='str'),
#         working_dir=dict(type='str'),
#
#             # normal options
#             ipc_mode=dict(docker_api_version='1.25'),
#             oom_score_adj=dict(docker_api_version='1.22'),
#             shm_size=dict(docker_api_version='1.22'),
#             stop_signal=dict(docker_api_version='1.21'),
#             tmpfs=dict(docker_api_version='1.22'),
#             volume_driver=dict(docker_api_version='1.21'),
#             runtime=dict(docker_py_version='2.4.0', docker_api_version='1.25'),
#             sysctls=dict(docker_py_version='1.10.0', docker_api_version='1.24'),
#             userns_mode=dict(docker_py_version='1.10.0', docker_api_version='1.23'),
#             uts=dict(docker_py_version='3.5.0', docker_api_version='1.25'),
#             pids_limit=dict(docker_py_version='1.10.0', docker_api_version='1.23'),
#             mounts=dict(docker_py_version='2.6.0', docker_api_version='1.25'),
#             storage_opts=dict(docker_py_version='2.1.0', docker_api_version='1.24'),
#             # specials
#             ipvX_address_supported=dict(docker_py_version='1.9.0', docker_api_version='1.22',
#                                         detect_usage=detect_ipvX_address_usage,
#                                         usage_msg='ipv4_address or ipv6_address in networks'),
#         stop_timeout_supported = self.docker_api_version >= LooseVersion('1.25')
#         stop_timeout_needed_for_update = self.module.params.get("stop_timeout") is not None and self.module.params.get('state') != 'absent'
#         if not stop_timeout_supported:
#             if stop_timeout_needed_for_update and not stop_timeout_supported:
#                 # We warn (instead of fail) since in older versions, stop_timeout was not used
#                 # to update the container's configuration, but only when stopping a container.
#                 self.module.warn("Docker API version is %s. Minimum version required is 1.25 to set or "
#                                  "update the container's stop_timeout configuration." % (self.docker_api_version_str,))
#         self.option_minimal_versions['stop_timeout']['supported'] = stop_timeout_supported
#
#         explicit_types = dict(
#             env='set',
#             mounts='set(dict)',
#             networks='set(dict)',
#             ulimits='set(dict)',
#         )
#
#         default_values = dict(
#             stop_timeout='ignore',
#         }
