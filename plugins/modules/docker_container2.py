#!/usr/bin/python
#
# Copyright 2016 Red Hat | Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: docker_container2

short_description: manage Docker containers

description:
  - Manage the life cycle of Docker containers.
  - Supports check mode. Run with C(--check) and C(--diff) to view config difference and list of actions to be taken.


notes:
  - For most config changes, the container needs to be recreated. This means that the existing container has to be destroyed and
    a new one created. This can cause unexpected data loss and downtime. You can use the I(comparisons) option to
    prevent this.
  - If the module needs to recreate the container, it will only use the options provided to the module to create the
    new container (except I(image)). Therefore, always specify B(all) options relevant to the container.
  - When I(restart) is set to C(true), the module will only restart the container if no config changes are detected.

options:
  auto_remove:
    description:
      - Enable auto-removal of the container on daemon side when the container's process exits.
      - If I(container_default_behavior) is set to C(compatibility), this option has a default of C(false).
    type: bool
  blkio_weight:
    description:
      - Block IO (relative weight), between 10 and 1000.
    type: int
  capabilities:
    description:
      - List of capabilities to add to the container.
      - This is equivalent to C(docker run --cap-add), or the docker-compose option C(cap_add).
    type: list
    elements: str
  cap_drop:
    description:
      - List of capabilities to drop from the container.
    type: list
    elements: str
  cgroup_parent:
    description:
      - Specify the parent cgroup for the container.
    type: str
    version_added: 1.1.0
  cleanup:
    description:
      - Use with I(detach=false) to remove the container after successful execution.
    type: bool
    default: no
  command:
    description:
      - Command to execute when the container starts. A command may be either a string or a list.
      - Prior to version 2.4, strings were split on commas.
      - See I(command_handling) for differences in how strings and lists are handled.
    type: raw
  comparisons:
    description:
      - Allows to specify how properties of existing containers are compared with
        module options to decide whether the container should be recreated / updated
        or not.
      - Only options which correspond to the state of a container as handled by the
        Docker daemon can be specified, as well as C(networks).
      - Must be a dictionary specifying for an option one of the keys C(strict), C(ignore)
        and C(allow_more_present).
      - If C(strict) is specified, values are tested for equality, and changes always
        result in updating or restarting. If C(ignore) is specified, changes are ignored.
      - C(allow_more_present) is allowed only for lists, sets and dicts. If it is
        specified for lists or sets, the container will only be updated or restarted if
        the module option contains a value which is not present in the container's
        options. If the option is specified for a dict, the container will only be updated
        or restarted if the module option contains a key which is not present in the
        container's option, or if the value of a key present differs.
      - The wildcard option C(*) can be used to set one of the default values C(strict)
        or C(ignore) to I(all) comparisons which are not explicitly set to other values.
      - See the examples for details.
    type: dict
  container_default_behavior:
    description:
      - In older versions of this module, various module options used to have default values.
        This caused problems with containers which use different values for these options.
      - The default value is now C(no_defaults). To restore the old behavior, set it to
        C(compatibility), which will ensure that the default values are used when the values
        are not explicitly specified by the user.
      - This affects the I(auto_remove), I(detach), I(init), I(interactive), I(memory),
        I(paused), I(privileged), I(read_only) and I(tty) options.
    type: str
    choices:
      - compatibility
      - no_defaults
    default: no_defaults
  command_handling:
    description:
      - The default behavior for I(command) (when provided as a list) and I(entrypoint) is to
        convert them to strings without considering shell quoting rules. (For comparing idempotency,
        the resulting string is split considering shell quoting rules.)
      - Also, setting I(command) to an empty list of string, and setting I(entrypoint) to an empty
        list will be handled as if these options are not specified. This is different from idempotency
        handling for other container-config related options.
      - When this is set to C(compatibility), which was the default until community.docker 3.0.0, the
        current behavior will be kept.
      - When this is set to C(correct), these options are kept as lists, and an empty value or empty
        list will be handled correctly for idempotency checks. This has been the default since
        community.docker 3.0.0.
    type: str
    choices:
      - compatibility
      - correct
    version_added: 1.9.0
    default: correct
  cpu_period:
    description:
      - Limit CPU CFS (Completely Fair Scheduler) period.
      - See I(cpus) for an easier to use alternative.
    type: int
  cpu_quota:
    description:
      - Limit CPU CFS (Completely Fair Scheduler) quota.
      - See I(cpus) for an easier to use alternative.
    type: int
  cpus:
    description:
      - Specify how much of the available CPU resources a container can use.
      - A value of C(1.5) means that at most one and a half CPU (core) will be used.
    type: float
  cpuset_cpus:
    description:
      - CPUs in which to allow execution C(1,3) or C(1-3).
    type: str
  cpuset_mems:
    description:
      - Memory nodes (MEMs) in which to allow execution C(0-3) or C(0,1).
    type: str
  cpu_shares:
    description:
      - CPU shares (relative weight).
    type: int
  default_host_ip:
    description:
      - Define the default host IP to use.
      - Must be an empty string, an IPv4 address, or an IPv6 address.
      - With Docker 20.10.2 or newer, this should be set to an empty string (C("")) to avoid the
        port bindings without an explicit IP address to only bind to IPv4.
        See U(https://github.com/ansible-collections/community.docker/issues/70) for details.
      - By default, the module will try to auto-detect this value from the C(bridge) network's
        C(com.docker.network.bridge.host_binding_ipv4) option. If it cannot auto-detect it, it
        will fall back to C(0.0.0.0).
    type: str
    version_added: 1.2.0
  detach:
    description:
      - Enable detached mode to leave the container running in background.
      - If disabled, the task will reflect the status of the container run (failed if the command failed).
      - If I(container_default_behavior) is set to C(compatibility), this option has a default of C(true).
    type: bool
  devices:
    description:
      - List of host device bindings to add to the container.
      - "Each binding is a mapping expressed in the format C(<path_on_host>:<path_in_container>:<cgroup_permissions>)."
    type: list
    elements: str
  device_read_bps:
    description:
      - "List of device path and read rate (bytes per second) from device."
    type: list
    elements: dict
    suboptions:
      path:
        description:
        - Device path in the container.
        type: str
        required: yes
      rate:
        description:
        - "Device read limit in format C(<number>[<unit>])."
        - "Number is a positive integer. Unit can be one of C(B) (byte), C(K) (kibibyte, 1024B), C(M) (mebibyte), C(G) (gibibyte),
          C(T) (tebibyte), or C(P) (pebibyte)."
        - "Omitting the unit defaults to bytes."
        type: str
        required: yes
  device_write_bps:
    description:
      - "List of device and write rate (bytes per second) to device."
    type: list
    elements: dict
    suboptions:
      path:
        description:
        - Device path in the container.
        type: str
        required: yes
      rate:
        description:
        - "Device read limit in format C(<number>[<unit>])."
        - "Number is a positive integer. Unit can be one of C(B) (byte), C(K) (kibibyte, 1024B), C(M) (mebibyte), C(G) (gibibyte),
          C(T) (tebibyte), or C(P) (pebibyte)."
        - "Omitting the unit defaults to bytes."
        type: str
        required: yes
  device_read_iops:
    description:
      - "List of device and read rate (IO per second) from device."
    type: list
    elements: dict
    suboptions:
      path:
        description:
        - Device path in the container.
        type: str
        required: yes
      rate:
        description:
        - "Device read limit."
        - "Must be a positive integer."
        type: int
        required: yes
  device_write_iops:
    description:
      - "List of device and write rate (IO per second) to device."
    type: list
    elements: dict
    suboptions:
      path:
        description:
        - Device path in the container.
        type: str
        required: yes
      rate:
        description:
        - "Device read limit."
        - "Must be a positive integer."
        type: int
        required: yes
  device_requests:
    description:
      - Allows to request additional resources, such as GPUs.
    type: list
    elements: dict
    suboptions:
      capabilities:
        description:
          - List of lists of strings to request capabilities.
          - The top-level list entries are combined by OR, and for every list entry,
            the entries in the list it contains are combined by AND.
          - The driver tries to satisfy one of the sub-lists.
          - Available capabilities for the C(nvidia) driver can be found at
            U(https://github.com/NVIDIA/nvidia-container-runtime).
        type: list
        elements: list
      count:
        description:
          - Number or devices to request.
          - Set to C(-1) to request all available devices.
        type: int
      device_ids:
        description:
          - List of device IDs.
        type: list
        elements: str
      driver:
        description:
          - Which driver to use for this device.
        type: str
      options:
        description:
          - Driver-specific options.
        type: dict
    version_added: 0.1.0
  dns_opts:
    description:
      - List of DNS options.
    type: list
    elements: str
  dns_servers:
    description:
      - List of custom DNS servers.
    type: list
    elements: str
  dns_search_domains:
    description:
      - List of custom DNS search domains.
    type: list
    elements: str
  domainname:
    description:
      - Container domainname.
    type: str
  env:
    description:
      - Dictionary of key,value pairs.
      - Values which might be parsed as numbers, booleans or other types by the YAML parser must be quoted (for example C("true")) in order to avoid data loss.
      - Please note that if you are passing values in with Jinja2 templates, like C("{{ value }}"), you need to add C(| string) to prevent Ansible to
        convert strings such as C("true") back to booleans. The correct way is to use C("{{ value | string }}").
    type: dict
  env_file:
    description:
      - Path to a file, present on the target, containing environment variables I(FOO=BAR).
      - If variable also present in I(env), then the I(env) value will override.
    type: path
  entrypoint:
    description:
      - Command that overwrites the default C(ENTRYPOINT) of the image.
      - See I(command_handling) for differences in how strings and lists are handled.
    type: list
    elements: str
  etc_hosts:
    description:
      - Dict of host-to-IP mappings, where each host name is a key in the dictionary.
        Each host name will be added to the container's C(/etc/hosts) file.
    type: dict
  exposed_ports:
    description:
      - List of additional container ports which informs Docker that the container
        listens on the specified network ports at runtime.
      - If the port is already exposed using C(EXPOSE) in a Dockerfile, it does not
        need to be exposed again.
    type: list
    elements: str
    aliases:
      - exposed
      - expose
  force_kill:
    description:
      - Use the kill command when stopping a running container.
    type: bool
    default: no
    aliases:
      - forcekill
  groups:
    description:
      - List of additional group names and/or IDs that the container process will run as.
    type: list
    elements: str
  healthcheck:
    description:
      - Configure a check that is run to determine whether or not containers for this service are "healthy".
      - "See the docs for the L(HEALTHCHECK Dockerfile instruction,https://docs.docker.com/engine/reference/builder/#healthcheck)
        for details on how healthchecks work."
      - "I(interval), I(timeout) and I(start_period) are specified as durations. They accept duration as a string in a format
        that look like: C(5h34m56s), C(1m30s) etc. The supported units are C(us), C(ms), C(s), C(m) and C(h)."
    type: dict
    suboptions:
      test:
        description:
          - Command to run to check health.
          - Must be either a string or a list. If it is a list, the first item must be one of C(NONE), C(CMD) or C(CMD-SHELL).
        type: raw
      interval:
        description:
          - Time between running the check.
          - The default used by the Docker daemon is C(30s).
        type: str
      timeout:
        description:
          - Maximum time to allow one check to run.
          - The default used by the Docker daemon is C(30s).
        type: str
      retries:
        description:
          - Consecutive number of failures needed to report unhealthy.
          - The default used by the Docker daemon is C(3).
        type: int
      start_period:
        description:
          - Start period for the container to initialize before starting health-retries countdown.
          - The default used by the Docker daemon is C(0s).
        type: str
  hostname:
    description:
      - The container's hostname.
    type: str
  ignore_image:
    description:
      - When I(state) is C(present) or C(started), the module compares the configuration of an existing
        container to requested configuration. The evaluation includes the image version. If the image
        version in the registry does not match the container, the container will be recreated. You can
        stop this behavior by setting I(ignore_image) to C(True).
      - "B(Warning:) This option is ignored if C(image: ignore) or C(*: ignore) is specified in the
        I(comparisons) option."
    type: bool
    default: no
  image:
    description:
      - Repository path and tag used to create the container. If an image is not found or pull is true, the image
        will be pulled from the registry. If no tag is included, C(latest) will be used.
      - Can also be an image ID. If this is the case, the image is assumed to be available locally.
        The I(pull) option is ignored for this case.
    type: str
  image_label_mismatch:
    description:
      - How to handle labels inherited from the image that are not set explicitly.
      - When C(ignore), labels that are present in the image but not specified in I(labels) will be
        ignored. This is useful to avoid having to specify the image labels in I(labels) while keeping
        labels I(comparisons) C(strict).
      - When C(fail), if there are labels present in the image which are not set from I(labels), the
        module will fail. This prevents introducing unexpected labels from the base image.
      - "B(Warning:) This option is ignored unless C(labels: strict) or C(*: strict) is specified in
        the I(comparisons) option."
    type: str
    choices:
      - 'ignore'
      - 'fail'
    default: ignore
    version_added: 2.6.0
  init:
    description:
      - Run an init inside the container that forwards signals and reaps processes.
      - If I(container_default_behavior) is set to C(compatibility), this option has a default of C(false).
    type: bool
  interactive:
    description:
      - Keep stdin open after a container is launched, even if not attached.
      - If I(container_default_behavior) is set to C(compatibility), this option has a default of C(false).
    type: bool
  ipc_mode:
    description:
      - Set the IPC mode for the container.
      - Can be one of C(container:<name|id>) to reuse another container's IPC namespace or C(host) to use
        the host's IPC namespace within the container.
    type: str
  keep_volumes:
    description:
      - Retain anonymous volumes associated with a removed container.
    type: bool
    default: yes
  kill_signal:
    description:
      - Override default signal used to kill a running container.
    type: str
  kernel_memory:
    description:
      - "Kernel memory limit in format C(<number>[<unit>]). Number is a positive integer.
        Unit can be C(B) (byte), C(K) (kibibyte, 1024B), C(M) (mebibyte), C(G) (gibibyte),
        C(T) (tebibyte), or C(P) (pebibyte). Minimum is C(4M)."
      - Omitting the unit defaults to bytes.
    type: str
  labels:
    description:
      - Dictionary of key value pairs.
    type: dict
  links:
    description:
      - List of name aliases for linked containers in the format C(container_name:alias).
      - Setting this will force container to be restarted.
    type: list
    elements: str
  log_driver:
    description:
      - Specify the logging driver. Docker uses C(json-file) by default.
      - See L(here,https://docs.docker.com/config/containers/logging/configure/) for possible choices.
    type: str
  log_options:
    description:
      - Dictionary of options specific to the chosen I(log_driver).
      - See U(https://docs.docker.com/engine/admin/logging/overview/) for details.
      - I(log_driver) needs to be specified for I(log_options) to take effect, even if using the default C(json-file) driver.
    type: dict
    aliases:
      - log_opt
  mac_address:
    description:
      - Container MAC address (for example, C(92:d0:c6:0a:29:33)).
    type: str
  memory:
    description:
      - "Memory limit in format C(<number>[<unit>]). Number is a positive integer.
        Unit can be C(B) (byte), C(K) (kibibyte, 1024B), C(M) (mebibyte), C(G) (gibibyte),
        C(T) (tebibyte), or C(P) (pebibyte)."
      - Omitting the unit defaults to bytes.
      - If I(container_default_behavior) is set to C(compatibility), this option has a default of C("0").
    type: str
  memory_reservation:
    description:
      - "Memory soft limit in format C(<number>[<unit>]). Number is a positive integer.
        Unit can be C(B) (byte), C(K) (kibibyte, 1024B), C(M) (mebibyte), C(G) (gibibyte),
        C(T) (tebibyte), or C(P) (pebibyte)."
      - Omitting the unit defaults to bytes.
    type: str
  memory_swap:
    description:
      - "Total memory limit (memory + swap) in format C(<number>[<unit>]), or
        the special values C(unlimited) or C(-1) for unlimited swap usage.
        Number is a positive integer. Unit can be C(B) (byte), C(K) (kibibyte, 1024B),
        C(M) (mebibyte), C(G) (gibibyte), C(T) (tebibyte), or C(P) (pebibyte)."
      - Omitting the unit defaults to bytes.
    type: str
  memory_swappiness:
    description:
        - Tune a container's memory swappiness behavior. Accepts an integer between 0 and 100.
        - If not set, the value will be remain the same if container exists and will be inherited
          from the host machine if it is (re-)created.
    type: int
  mounts:
    type: list
    elements: dict
    description:
      - Specification for mounts to be added to the container. More powerful alternative to I(volumes).
    suboptions:
      target:
        description:
          - Path inside the container.
        type: str
        required: true
      source:
        description:
          - Mount source.
          - For example, this can be a volume name or a host path.
          - If not supplied when I(type=volume) an anonymous volume will be created.
        type: str
      type:
        description:
          - The mount type.
          - Note that C(npipe) is only supported by Docker for Windows.
        type: str
        choices:
          - bind
          - npipe
          - tmpfs
          - volume
        default: volume
      read_only:
        description:
          - Whether the mount should be read-only.
        type: bool
      consistency:
        description:
          - The consistency requirement for the mount.
        type: str
        choices:
          - cached
          - consistent
          - default
          - delegated
      propagation:
        description:
          - Propagation mode. Only valid for the C(bind) type.
        type: str
        choices:
          - private
          - rprivate
          - shared
          - rshared
          - slave
          - rslave
      no_copy:
        description:
          - False if the volume should be populated with the data from the target. Only valid for the C(volume) type.
          - The default value is C(false).
        type: bool
      labels:
        description:
          - User-defined name and labels for the volume. Only valid for the C(volume) type.
        type: dict
      volume_driver:
        description:
          - Specify the volume driver. Only valid for the C(volume) type.
          - See L(here,https://docs.docker.com/storage/volumes/#use-a-volume-driver) for details.
        type: str
      volume_options:
        description:
          - Dictionary of options specific to the chosen volume_driver. See
            L(here,https://docs.docker.com/storage/volumes/#use-a-volume-driver) for details.
        type: dict
      tmpfs_size:
        description:
          - "The size for the tmpfs mount in bytes in format <number>[<unit>]."
          - "Number is a positive integer. Unit can be one of C(B) (byte), C(K) (kibibyte, 1024B), C(M) (mebibyte), C(G) (gibibyte),
             C(T) (tebibyte), or C(P) (pebibyte)."
          - "Omitting the unit defaults to bytes."
        type: str
      tmpfs_mode:
        description:
          - The permission mode for the tmpfs mount.
        type: str
  name:
    description:
      - Assign a name to a new container or match an existing container.
      - When identifying an existing container name may be a name or a long or short container ID.
    type: str
    required: yes
  network_mode:
    description:
      - Connect the container to a network. Choices are C(bridge), C(host), C(none), C(container:<name|id>), C(<network_name>) or C(default).
      - "Since community.docker 2.0.0, if I(networks_cli_compatible) is C(true) and I(networks) contains at least one network,
         the default value for I(network_mode) is the name of the first network in the I(networks) list. You can prevent this
         by explicitly specifying a value for I(network_mode), like the default value C(default) which will be used by Docker if
         I(network_mode) is not specified."
    type: str
  userns_mode:
    description:
      - Set the user namespace mode for the container. Currently, the only valid value are C(host) and the empty string.
    type: str
  networks:
    description:
      - List of networks the container belongs to.
      - For examples of the data structure and usage see EXAMPLES below.
      - To remove a container from one or more networks, use the I(purge_networks) option.
      - If I(networks_cli_compatible) is set to C(false), this will not remove the default network if I(networks) is specified.
        This is different from the behavior of C(docker run ...). You need to explicitly use I(purge_networks) to enforce
        the removal of the default network (and all other networks not explicitly mentioned in I(networks)) in that case.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - The network's name.
        type: str
        required: yes
      ipv4_address:
        description:
          - The container's IPv4 address in this network.
        type: str
      ipv6_address:
        description:
          - The container's IPv6 address in this network.
        type: str
      links:
        description:
          - A list of containers to link to.
        type: list
        elements: str
      aliases:
        description:
          - List of aliases for this container in this network. These names
            can be used in the network to reach this container.
        type: list
        elements: str
  networks_cli_compatible:
    description:
      - "If I(networks_cli_compatible) is set to C(yes) (default), this module will behave as
         C(docker run --network) and will B(not) add the default network if I(networks) is
         specified. If I(networks) is not specified, the default network will be attached."
      - "When I(networks_cli_compatible) is set to C(no) and networks are provided to the module
         via the I(networks) option, the module behaves differently than C(docker run --network):
         C(docker run --network other) will create a container with network C(other) attached,
         but the default network not attached. This module with I(networks: {name: other}) will
         create a container with both C(default) and C(other) attached. If I(purge_networks) is
         set to C(yes), the C(default) network will be removed afterwards."
    type: bool
    default: true
  oom_killer:
    description:
      - Whether or not to disable OOM Killer for the container.
    type: bool
  oom_score_adj:
    description:
      - An integer value containing the score given to the container in order to tune
        OOM killer preferences.
    type: int
  output_logs:
    description:
      - If set to true, output of the container command will be printed.
      - Only effective when I(log_driver) is set to C(json-file), C(journald), or C(local).
    type: bool
    default: no
  paused:
    description:
      - Use with the started state to pause running processes inside the container.
      - If I(container_default_behavior) is set to C(compatibility), this option has a default of C(false).
    type: bool
  pid_mode:
    description:
      - Set the PID namespace mode for the container.
    type: str
  pids_limit:
    description:
      - Set PIDs limit for the container. It accepts an integer value.
      - Set C(-1) for unlimited PIDs.
    type: int
  privileged:
    description:
      - Give extended privileges to the container.
      - If I(container_default_behavior) is set to C(compatibility), this option has a default of C(false).
    type: bool
  publish_all_ports:
    description:
      - Publish all ports to the host.
      - Any specified port bindings from I(published_ports) will remain intact when C(true).
    type: bool
    version_added: 1.8.0
  published_ports:
    description:
      - List of ports to publish from the container to the host.
      - "Use docker CLI syntax: C(8000), C(9000:8000), or C(0.0.0.0:9000:8000), where 8000 is a
        container port, 9000 is a host port, and 0.0.0.0 is a host interface."
      - Port ranges can be used for source and destination ports. If two ranges with
        different lengths are specified, the shorter range will be used.
        Since community.general 0.2.0, if the source port range has length 1, the port will not be assigned
        to the first port of the destination range, but to a free port in that range. This is the
        same behavior as for C(docker) command line utility.
      - "Bind addresses must be either IPv4 or IPv6 addresses. Hostnames are B(not) allowed. This
        is different from the C(docker) command line utility. Use the R(dig lookup,ansible_collections.community.general.dig_lookup)
        to resolve hostnames."
      - If I(networks) parameter is provided, will inspect each network to see if there exists
        a bridge network with optional parameter C(com.docker.network.bridge.host_binding_ipv4).
        If such a network is found, then published ports where no host IP address is specified
        will be bound to the host IP pointed to by C(com.docker.network.bridge.host_binding_ipv4).
        Note that the first bridge network with a C(com.docker.network.bridge.host_binding_ipv4)
        value encountered in the list of I(networks) is the one that will be used.
      - The value C(all) was allowed in earlier versions of this module. Support for it was removed in
        community.docker 3.0.0. Use the I(publish_all_ports) option instead.
    type: list
    elements: str
    aliases:
      - ports
  pull:
    description:
       - If true, always pull the latest version of an image. Otherwise, will only pull an image
         when missing.
       - "B(Note:) images are only pulled when specified by name. If the image is specified
         as a image ID (hash), it cannot be pulled."
    type: bool
    default: no
  purge_networks:
    description:
       - Remove the container from ALL networks not included in I(networks) parameter.
       - Any default networks such as C(bridge), if not found in I(networks), will be removed as well.
    type: bool
    default: no
  read_only:
    description:
      - Mount the container's root file system as read-only.
      - If I(container_default_behavior) is set to C(compatibility), this option has a default of C(false).
    type: bool
  recreate:
    description:
      - Use with present and started states to force the re-creation of an existing container.
    type: bool
    default: no
  removal_wait_timeout:
    description:
      - When removing an existing container, the docker daemon API call exists after the container
        is scheduled for removal. Removal usually is very fast, but it can happen that during high I/O
        load, removal can take longer. By default, the module will wait until the container has been
        removed before trying to (re-)create it, however long this takes.
      - By setting this option, the module will wait at most this many seconds for the container to be
        removed. If the container is still in the removal phase after this many seconds, the module will
        fail.
    type: float
  restart:
    description:
      - Use with started state to force a matching container to be stopped and restarted.
    type: bool
    default: no
  restart_policy:
    description:
      - Container restart policy.
      - Place quotes around C(no) option.
    type: str
    choices:
      - 'no'
      - 'on-failure'
      - 'always'
      - 'unless-stopped'
  restart_retries:
    description:
      - Use with restart policy to control maximum number of restart attempts.
    type: int
  runtime:
    description:
      - Runtime to use for the container.
    type: str
  shm_size:
    description:
      - "Size of C(/dev/shm) in format C(<number>[<unit>]). Number is positive integer.
        Unit can be C(B) (byte), C(K) (kibibyte, 1024B), C(M) (mebibyte), C(G) (gibibyte),
        C(T) (tebibyte), or C(P) (pebibyte)."
      - Omitting the unit defaults to bytes. If you omit the size entirely, Docker daemon uses C(64M).
    type: str
  security_opts:
    description:
      - List of security options in the form of C("label:user:User").
    type: list
    elements: str
  state:
    description:
      - 'C(absent) - A container matching the specified name will be stopped and removed. Use I(force_kill) to kill the container
         rather than stopping it. Use I(keep_volumes) to retain anonymous volumes associated with the removed container.'
      - 'C(present) - Asserts the existence of a container matching the name and any provided configuration parameters. If no
        container matches the name, a container will be created. If a container matches the name but the provided configuration
        does not match, the container will be updated, if it can be. If it cannot be updated, it will be removed and re-created
        with the requested config.'
      - 'C(started) - Asserts that the container is first C(present), and then if the container is not running moves it to a running
        state. Use I(restart) to force a matching container to be stopped and restarted.'
      - 'C(stopped) - Asserts that the container is first C(present), and then if the container is running moves it to a stopped
        state.'
      - To control what will be taken into account when comparing configuration, see the I(comparisons) option. To avoid that the
        image version will be taken into account, you can also use the I(ignore_image) option.
      - Use the I(recreate) option to always force re-creation of a matching container, even if it is running.
      - If the container should be killed instead of stopped in case it needs to be stopped for recreation, or because I(state) is
        C(stopped), please use the I(force_kill) option. Use I(keep_volumes) to retain anonymous volumes associated with a removed container.
      - Use I(keep_volumes) to retain anonymous volumes associated with a removed container.
    type: str
    default: started
    choices:
      - absent
      - present
      - stopped
      - started
  stop_signal:
    description:
      - Override default signal used to stop the container.
    type: str
  stop_timeout:
    description:
      - Number of seconds to wait for the container to stop before sending C(SIGKILL).
        When the container is created by this module, its C(StopTimeout) configuration
        will be set to this value.
      - When the container is stopped, will be used as a timeout for stopping the
        container. In case the container has a custom C(StopTimeout) configuration,
        the behavior depends on the version of the docker daemon. New versions of
        the docker daemon will always use the container's configured C(StopTimeout)
        value if it has been configured.
    type: int
  storage_opts:
    description:
      - Storage driver options for this container as a key-value mapping.
    type: dict
    version_added: 1.3.0
  tmpfs:
    description:
      - Mount a tmpfs directory.
    type: list
    elements: str
  tty:
    description:
      - Allocate a pseudo-TTY.
      - If I(container_default_behavior) is set to C(compatibility), this option has a default of C(false).
    type: bool
  ulimits:
    description:
      - "List of ulimit options. A ulimit is specified as C(nofile:262144:262144)."
    type: list
    elements: str
  sysctls:
    description:
      - Dictionary of key,value pairs.
    type: dict
  user:
    description:
      - Sets the username or UID used and optionally the groupname or GID for the specified command.
      - "Can be of the forms C(user), C(user:group), C(uid), C(uid:gid), C(user:gid) or C(uid:group)."
    type: str
  uts:
    description:
      - Set the UTS namespace mode for the container.
    type: str
  volumes:
    description:
      - List of volumes to mount within the container.
      - "Use docker CLI-style syntax: C(/host:/container[:mode])"
      - "Mount modes can be a comma-separated list of various modes such as C(ro), C(rw), C(consistent),
        C(delegated), C(cached), C(rprivate), C(private), C(rshared), C(shared), C(rslave), C(slave), and
        C(nocopy). Note that the docker daemon might not support all modes and combinations of such modes."
      - SELinux hosts can additionally use C(z) or C(Z) to use a shared or private label for the volume.
      - "Note that Ansible 2.7 and earlier only supported one mode, which had to be one of C(ro), C(rw),
        C(z), and C(Z)."
    type: list
    elements: str
  volume_driver:
    description:
      - The container volume driver.
    type: str
  volumes_from:
    description:
      - List of container names or IDs to get volumes from.
    type: list
    elements: str
  working_dir:
    description:
      - Path to the working directory.
    type: str
extends_documentation_fragment:
- community.docker.docker
- community.docker.docker.docker_py_1_documentation


author:
  - "Cove Schneider (@cove)"
  - "Joshua Conner (@joshuaconner)"
  - "Pavel Antonov (@softzilla)"
  - "Thomas Steinbach (@ThomasSteinbach)"
  - "Philippe Jandot (@zfil)"
  - "Daan Oosterveld (@dusdanig)"
  - "Chris Houseknecht (@chouseknecht)"
  - "Kassian Sun (@kassiansun)"
  - "Felix Fontein (@felixfontein)"

requirements:
  - "Docker API >= 1.25"
'''

EXAMPLES = '''
- name: Create a data container
  community.docker.docker_container:
    name: mydata
    image: busybox
    volumes:
      - /data

- name: Re-create a redis container
  community.docker.docker_container:
    name: myredis
    image: redis
    command: redis-server --appendonly yes
    state: present
    recreate: yes
    exposed_ports:
      - 6379
    volumes_from:
      - mydata

- name: Restart a container
  community.docker.docker_container:
    name: myapplication
    image: someuser/appimage
    state: started
    restart: yes
    links:
     - "myredis:aliasedredis"
    devices:
     - "/dev/sda:/dev/xvda:rwm"
    ports:
     # Publish container port 9000 as host port 8080
     - "8080:9000"
     # Publish container UDP port 9001 as host port 8081 on interface 127.0.0.1
     - "127.0.0.1:8081:9001/udp"
     # Publish container port 9002 as a random host port
     - "9002"
     # Publish container port 9003 as a free host port in range 8000-8100
     # (the host port will be selected by the Docker daemon)
     - "8000-8100:9003"
     # Publish container ports 9010-9020 to host ports 7000-7010
     - "7000-7010:9010-9020"
    env:
        SECRET_KEY: "ssssh"
        # Values which might be parsed as numbers, booleans or other types by the YAML parser need to be quoted
        BOOLEAN_KEY: "yes"

- name: Container present
  community.docker.docker_container:
    name: mycontainer
    state: present
    image: ubuntu:14.04
    command: sleep infinity

- name: Stop a container
  community.docker.docker_container:
    name: mycontainer
    state: stopped

- name: Start 4 load-balanced containers
  community.docker.docker_container:
    name: "container{{ item }}"
    recreate: yes
    image: someuser/anotherappimage
    command: sleep 1d
  with_sequence: count=4

- name: Remove container
  community.docker.docker_container:
    name: ohno
    state: absent

- name: Syslogging output
  community.docker.docker_container:
    name: myservice
    image: busybox
    log_driver: syslog
    log_options:
      syslog-address: tcp://my-syslog-server:514
      syslog-facility: daemon
      # NOTE: in Docker 1.13+ the "syslog-tag" option was renamed to "tag" for
      # older docker installs, use "syslog-tag" instead
      tag: myservice

- name: Create db container and connect to network
  community.docker.docker_container:
    name: db_test
    image: "postgres:latest"
    networks:
      - name: "{{ docker_network_name }}"

- name: Start container, connect to network and link
  community.docker.docker_container:
    name: sleeper
    image: ubuntu:14.04
    networks:
      - name: TestingNet
        ipv4_address: "172.16.1.100"
        aliases:
          - sleepyzz
        links:
          - db_test:db
      - name: TestingNet2

- name: Start a container with a command
  community.docker.docker_container:
    name: sleepy
    image: ubuntu:14.04
    command: ["sleep", "infinity"]

- name: Add container to networks
  community.docker.docker_container:
    name: sleepy
    networks:
      - name: TestingNet
        ipv4_address: 172.16.1.18
        links:
          - sleeper
      - name: TestingNet2
        ipv4_address: 172.16.10.20

- name: Update network with aliases
  community.docker.docker_container:
    name: sleepy
    networks:
      - name: TestingNet
        aliases:
          - sleepyz
          - zzzz

- name: Remove container from one network
  community.docker.docker_container:
    name: sleepy
    networks:
      - name: TestingNet2
    purge_networks: yes

- name: Remove container from all networks
  community.docker.docker_container:
    name: sleepy
    purge_networks: yes

- name: Start a container and use an env file
  community.docker.docker_container:
    name: agent
    image: jenkinsci/ssh-slave
    env_file: /var/tmp/jenkins/agent.env

- name: Create a container with limited capabilities
  community.docker.docker_container:
    name: sleepy
    image: ubuntu:16.04
    command: sleep infinity
    capabilities:
      - sys_time
    cap_drop:
      - all

- name: Finer container restart/update control
  community.docker.docker_container:
    name: test
    image: ubuntu:18.04
    env:
      arg1: "true"
      arg2: "whatever"
    volumes:
      - /tmp:/tmp
    comparisons:
      image: ignore   # do not restart containers with older versions of the image
      env: strict   # we want precisely this environment
      volumes: allow_more_present   # if there are more volumes, that's ok, as long as `/tmp:/tmp` is there

- name: Finer container restart/update control II
  community.docker.docker_container:
    name: test
    image: ubuntu:18.04
    env:
      arg1: "true"
      arg2: "whatever"
    comparisons:
      '*': ignore  # by default, ignore *all* options (including image)
      env: strict   # except for environment variables; there, we want to be strict

- name: Start container with healthstatus
  community.docker.docker_container:
    name: nginx-proxy
    image: nginx:1.13
    state: started
    healthcheck:
      # Check if nginx server is healthy by curl'ing the server.
      # If this fails or timeouts, the healthcheck fails.
      test: ["CMD", "curl", "--fail", "http://nginx.host.com"]
      interval: 1m30s
      timeout: 10s
      retries: 3
      start_period: 30s

- name: Remove healthcheck from container
  community.docker.docker_container:
    name: nginx-proxy
    image: nginx:1.13
    state: started
    healthcheck:
      # The "NONE" check needs to be specified
      test: ["NONE"]

- name: Start container with block device read limit
  community.docker.docker_container:
    name: test
    image: ubuntu:18.04
    state: started
    device_read_bps:
      # Limit read rate for /dev/sda to 20 mebibytes per second
      - path: /dev/sda
        rate: 20M
    device_read_iops:
      # Limit read rate for /dev/sdb to 300 IO per second
      - path: /dev/sdb
        rate: 300

- name: Start container with GPUs
  community.docker.docker_container:
    name: test
    image: ubuntu:18.04
    state: started
    device_requests:
      - # Add some specific devices to this container
        device_ids:
          - '0'
          - 'GPU-3a23c669-1f69-c64e-cf85-44e9b07e7a2a'
      - # Add nVidia GPUs to this container
        driver: nvidia
        count: -1  # this means we want all
        capabilities:
          # We have one OR condition: 'gpu' AND 'utility'
          - - gpu
            - utility
          # See https://github.com/NVIDIA/nvidia-container-runtime#supported-driver-capabilities
          # for a list of capabilities supported by the nvidia driver

- name: Start container with storage options
  community.docker.docker_container:
    name: test
    image: ubuntu:18.04
    state: started
    storage_opts:
      # Limit root filesystem to 12 MB - note that this requires special storage backends
      # (https://fabianlee.org/2020/01/15/docker-use-overlay2-with-an-xfs-backing-filesystem-to-limit-rootfs-size/)
      size: 12m
'''

RETURN = '''
container:
    description:
      - Facts representing the current state of the container. Matches the docker inspection output.
      - Empty if I(state) is C(absent).
      - If I(detach=false), will include C(Output) attribute containing any output from container run.
    returned: success; or when I(state=started) and I(detach=false), and when waiting for the container result did not fail
    type: dict
    sample: '{
        "AppArmorProfile": "",
        "Args": [],
        "Config": {
            "AttachStderr": false,
            "AttachStdin": false,
            "AttachStdout": false,
            "Cmd": [
                "/usr/bin/supervisord"
            ],
            "Domainname": "",
            "Entrypoint": null,
            "Env": [
                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
            ],
            "ExposedPorts": {
                "443/tcp": {},
                "80/tcp": {}
            },
            "Hostname": "8e47bf643eb9",
            "Image": "lnmp_nginx:v1",
            "Labels": {},
            "OnBuild": null,
            "OpenStdin": false,
            "StdinOnce": false,
            "Tty": false,
            "User": "",
            "Volumes": {
                "/tmp/lnmp/nginx-sites/logs/": {}
            },
            ...
    }'
status:
    description:
      - In case a container is started without detaching, this contains the exit code of the process in the container.
      - Before community.docker 1.1.0, this was only returned when non-zero.
    returned: when I(state=started) and I(detach=false), and when waiting for the container result did not fail
    type: int
    sample: 0
'''

import os
import re
import shlex
import traceback
from time import sleep

from ansible.module_utils.common.text.formatters import human_to_bytes
from ansible.module_utils.common.text.converters import to_native, to_text
from ansible.module_utils.six import string_types

from ansible_collections.community.docker.plugins.module_utils.version import LooseVersion

from ansible_collections.community.docker.plugins.module_utils.common_api import (
    AnsibleDockerClient,
    RequestException,
)
from ansible_collections.community.docker.plugins.module_utils.module_container import (
    DockerAPIEngineDriver,
    OPTIONS,
    Option,
)
from ansible_collections.community.docker.plugins.module_utils.util import (
    DifferenceTracker,
    DockerBaseClass,
    compare_generic,
    is_image_name_id,
    sanitize_result,
    clean_dict_booleans_for_docker_api,
    omit_none_from_dict,
    parse_healthcheck,
    DOCKER_COMMON_ARGS,
)

from ansible_collections.community.docker.plugins.module_utils._api.errors import APIError, DockerException, NotFound

from ansible_collections.community.docker.plugins.module_utils._api.utils.utils import parse_repository_tag, normalize_links


class Container(DockerBaseClass):
    def __init__(self, container):
        super(Container, self).__init__()
        self.raw = container
        self.Id = None
        self.Image = None
        self.container = container
        if container:
            self.Id = container['Id']
            self.Image = container['Image']
        self.log(self.container, pretty_print=True)

    @property
    def exists(self):
        return True if self.container else False

    @property
    def removing(self):
        if self.container and self.container.get('State'):
            return self.container['State'].get('Status') == 'removing'
        return False

    @property
    def running(self):
        if self.container and self.container.get('State'):
            if self.container['State'].get('Running') and not self.container['State'].get('Ghost', False):
                return True
        return False

    @property
    def paused(self):
        if self.container and self.container.get('State'):
            return self.container['State'].get('Paused', False)
        return False


class ContainerManager(DockerBaseClass):
    def __init__(self, module, client, active_options):
        self.client = client
        self.options = active_options
        self.all_options = self._collect_all_options(active_options)
        self.module = module
        self.check_mode = self.module.check_mode
        self.param_cleanup = self.module.params['cleanup']
        self.param_container_default_behavior = self.module.params['container_default_behavior']
        self.param_debug = self.module.params['debug']
        self.param_force_kill = self.module.params['force_kill']
        self.param_image = self.module.params['image']
        self.param_image_label_mismatch = self.module.params['image_label_mismatch']
        self.param_keep_volumes = self.module.params['keep_volumes']
        self.param_kill_signal = self.module.params['kill_signal']
        self.param_name = self.module.params['name']
        self.param_networks_cli_compatible = self.module.params['networks_cli_compatible']
        self.param_output_logs = self.module.params['output_logs']
        self.param_paused = self.module.params['paused']
        self.param_pull = self.module.params['pull']
        self.param_purge_networks = self.module.params['purge_networks']
        self.param_recreate = self.module.params['recreate']
        self.param_removal_wait_timeout = self.module.params['removal_wait_timeout']
        self.param_restart = self.module.params['restart']
        self.param_state = self.module.params['state']
        self._parse_comparisons()
        self._update_params()
        self.parameters = self._collect_params(active_options)
        self.results = {'changed': False, 'actions': []}
        self.diff = {}
        self.diff_tracker = DifferenceTracker()
        self.facts = {}

    def _collect_all_options(self, active_options):
        all_options = {}
        for options in active_options:
            for option in options.options:
                all_options[option.name] = option
        for option in [
            Option('image', 'str', None),
            Option('networks', 'set', None, elements='dict', ansible_suboptions={}),
        ]:
            all_options[option.name] = option
        return all_options

    def _collect_all_module_params(self):
        all_module_options = set()
        for option, data in self.module.argument_spec.items():
            all_module_options.add(option)
            if 'aliases' in data:
                for alias in data['aliases']:
                    all_module_options.add(alias)
        return all_module_options

    def _parse_comparisons(self):
        # Keep track of all module params and all option aliases
        all_module_options = self._collect_all_module_params()
        comp_aliases = {}
        for option_name, option in self.all_options.items():
            comp_aliases[option_name] = option_name
            for alias in option.ansible_aliases:
                comp_aliases[alias] = option_name
        # Process legacy ignore options
        if self.module.params['ignore_image']:
            self.all_options['image'].comparison = 'ignore'
        if self.param_purge_networks:
            self.all_options['networks'].comparison = 'strict'
        # Process comparsions specified by user
        if self.module.params.get('comparisons'):
            # If '*' appears in comparisons, process it first
            if '*' in self.module.params['comparisons']:
                value = self.module.params['comparisons']['*']
                if value not in ('strict', 'ignore'):
                    self.fail("The wildcard can only be used with comparison modes 'strict' and 'ignore'!")
                for option in self.all_options.values():
                    if option.name == 'networks':
                        # `networks` is special: only update if
                        # some value is actually specified
                        if self.module.params['networks'] is None:
                            continue
                    option.comparison = value
            # Now process all other comparisons.
            comp_aliases_used = {}
            for key, value in self.module.params['comparisons'].items():
                if key == '*':
                    continue
                # Find main key
                key_main = comp_aliases.get(key)
                if key_main is None:
                    if key_main in all_module_options:
                        self.fail("The module option '%s' cannot be specified in the comparisons dict, "
                                  "since it does not correspond to container's state!" % key)
                    if key not in self.all_options:
                        self.fail("Unknown module option '%s' in comparisons dict!" % key)
                    key_main = key
                if key_main in comp_aliases_used:
                    self.fail("Both '%s' and '%s' (aliases of %s) are specified in comparisons dict!" % (key, comp_aliases_used[key_main], key_main))
                comp_aliases_used[key_main] = key
                # Check value and update accordingly
                if value in ('strict', 'ignore'):
                    self.all_options[key_main].comparison = value
                elif value == 'allow_more_present':
                    if self.all_options[key_main].comparison_type == 'value':
                        self.fail("Option '%s' is a value and not a set/list/dict, so its comparison cannot be %s" % (key, value))
                    self.all_options[key_main].comparison = value
                else:
                    self.fail("Unknown comparison mode '%s'!" % value)
        # Check legacy values
        if self.module.params['ignore_image'] and self.all_options['image'].comparison != 'ignore':
            self.module.warn('The ignore_image option has been overridden by the comparisons option!')
        if self.param_purge_networks and self.all_options['networks'].comparison != 'strict':
            self.module.warn('The purge_networks option has been overridden by the comparisons option!')

    def _update_params(self):
        if self.param_networks_cli_compatible is True and self.module.params['networks'] and self.module.params['network_mode'] is None:
            # Same behavior as Docker CLI: if networks are specified, use the name of the first network as the value for network_mode
            # (assuming no explicit value is specified for network_mode)
            self.module.params['network_mode'] = self.module.params['networks'][0]['name']
        if self.param_container_default_behavior == 'compatibility':
            old_default_values = dict(
                auto_remove=False,
                detach=True,
                init=False,
                interactive=False,
                memory='0',
                paused=False,
                privileged=False,
                read_only=False,
                tty=False,
            )
            for param, value in old_default_values.items():
                if self.module.params[param] is None:
                    self.module.params[param] = value

    def _collect_params(self, active_options):
        parameters = []
        for options in active_options:
            values = {}
            engine = options.get_engine('docker_api')
            for option in options.options:
                if self.module.params[option.name] is not None:
                    values[option.name] = self.module.params[option.name]
            values = options.preprocess(self.module, values)
            engine.preprocess_value(self.module, self.client, self.client.docker_api_version, options.options, values)
            parameters.append((options, values))
        return parameters

    def fail(self, *args, **kwargs):
        self.client.fail(*args, **kwargs)

    def run(self):
        if self.param_state in ('stopped', 'started', 'present'):
            self.present(self.param_state)
        elif self.param_state == 'absent':
            self.absent()

        if not self.check_mode and not self.param_debug:
            self.results.pop('actions')

        if self.module._diff or self.param_debug:
            self.diff['before'], self.diff['after'] = self.diff_tracker.get_before_after()
            self.results['diff'] = self.diff

        if self.facts:
            self.results['container'] = self.facts

    def wait_for_state(self, container_id, complete_states=None, wait_states=None, accept_removal=False, max_wait=None):
        delay = 1.0
        total_wait = 0
        while True:
            # Inspect container
            result = self.client.get_container_by_id(container_id)
            if result is None:
                if accept_removal:
                    return
                msg = 'Encontered vanished container while waiting for container "{0}"'
                self.fail(msg.format(container_id))
            # Check container state
            state = result.get('State', {}).get('Status')
            if complete_states is not None and state in complete_states:
                return
            if wait_states is not None and state not in wait_states:
                msg = 'Encontered unexpected state "{1}" while waiting for container "{0}"'
                self.fail(msg.format(container_id, state))
            # Wait
            if max_wait is not None:
                if total_wait > max_wait:
                    msg = 'Timeout of {1} seconds exceeded while waiting for container "{0}"'
                    self.fail(msg.format(container_id, max_wait))
                if total_wait + delay > max_wait:
                    delay = max_wait - total_wait
            sleep(delay)
            total_wait += delay
            # Exponential backoff, but never wait longer than 10 seconds
            # (1.1**24 < 10, 1.1**25 > 10, so it will take 25 iterations
            #  until the maximal 10 seconds delay is reached. By then, the
            #  code will have slept for ~1.5 minutes.)
            delay = min(delay * 1.1, 10)

    def present(self, state):
        container = self._get_container(self.param_name)
        was_running = container.running
        was_paused = container.paused
        container_created = False

        # If the image parameter was passed then we need to deal with the image
        # version comparison. Otherwise we handle this depending on whether
        # the container already runs or not; in the former case, in case the
        # container needs to be restarted, we use the existing container's
        # image ID.
        image = self._get_image()
        self.log(image, pretty_print=True)
        if not container.exists or container.removing:
            # New container
            if container.removing:
                self.log('Found container in removal phase')
            else:
                self.log('No container found')
            if not self.param_image:
                self.fail('Cannot create container when image is not specified!')
            self.diff_tracker.add('exists', parameter=True, active=False)
            if container.removing and not self.check_mode:
                # Wait for container to be removed before trying to create it
                self.wait_for_state(
                    container.Id, wait_states=['removing'], accept_removal=True, max_wait=self.param_removal_wait_timeout)
            new_container = self.container_create(self.param_image)
            if new_container:
                container = new_container
            container_created = True
        else:
            # Existing container
            different, differences = self.has_different_configuration(container, image)
            image_different = False
            if self.all_options['image'].comparison == 'strict':
                image_different = self._image_is_different(image, container)
            if image_different or different or self.param_recreate:
                self.diff_tracker.merge(differences)
                self.diff['differences'] = differences.get_legacy_docker_container_diffs()
                if image_different:
                    self.diff['image_different'] = True
                self.log("differences")
                self.log(differences.get_legacy_docker_container_diffs(), pretty_print=True)
                image_to_use = self.param_image
                if not image_to_use and container and container.Image:
                    image_to_use = container.Image
                if not image_to_use:
                    self.fail('Cannot recreate container when image is not specified or cannot be extracted from current container!')
                if container.running:
                    self.container_stop(container.Id)
                self.container_remove(container.Id)
                if not self.check_mode:
                    self.wait_for_state(
                        container.Id, wait_states=['removing'], accept_removal=True, max_wait=self.param_removal_wait_timeout)
                new_container = self.container_create(image_to_use)
                if new_container:
                    container = new_container
                container_created = True

        if container and container.exists:
            container = self.update_limits(container, image)
            container = self.update_networks(container, container_created)

            if state == 'started' and not container.running:
                self.diff_tracker.add('running', parameter=True, active=was_running)
                container = self.container_start(container.Id)
            elif state == 'started' and self.param_restart:
                self.diff_tracker.add('running', parameter=True, active=was_running)
                self.diff_tracker.add('restarted', parameter=True, active=False)
                container = self.container_restart(container.Id)
            elif state == 'stopped' and container.running:
                self.diff_tracker.add('running', parameter=False, active=was_running)
                self.container_stop(container.Id)
                container = self._get_container(container.Id)

            if state == 'started' and self.param_paused is not None and container.paused != self.param_paused:
                self.diff_tracker.add('paused', parameter=self.param_paused, active=was_paused)
                if not self.check_mode:
                    try:
                        if self.param_paused:
                            self.client.post_call('/containers/{0}/pause', container.Id)
                        else:
                            self.client.post_call('/containers/{0}/unpause', container.Id)
                    except Exception as exc:
                        self.fail("Error %s container %s: %s" % (
                            "pausing" if self.param_paused else "unpausing", container.Id, to_native(exc)
                        ))
                    container = self._get_container(container.Id)
                self.results['changed'] = True
                self.results['actions'].append(dict(set_paused=self.param_paused))

        self.facts = container.raw

    def absent(self):
        container = self._get_container(self.param_name)
        if container.exists:
            if container.running:
                self.diff_tracker.add('running', parameter=False, active=True)
                self.container_stop(container.Id)
            self.diff_tracker.add('exists', parameter=False, active=True)
            self.container_remove(container.Id)

    def _output_logs(self, msg):
        self.module.log(msg=msg)

    def _get_container(self, container):
        '''
        Expects container ID or Name. Returns a container object
        '''
        return Container(self.client.get_container(container))

    def _get_image(self):
        image_parameter = self.param_image
        if not image_parameter:
            self.log('No image specified')
            return None
        if is_image_name_id(image_parameter):
            image = self.client.find_image_by_id(image_parameter)
        else:
            repository, tag = parse_repository_tag(image_parameter)
            if not tag:
                tag = "latest"
            image = self.client.find_image(repository, tag)
            if not image or self.param_pull:
                if not self.check_mode:
                    self.log("Pull the image.")
                    image, alreadyToLatest = self.client.pull_image(repository, tag)
                    if alreadyToLatest:
                        self.results['changed'] = False
                    else:
                        self.results['changed'] = True
                        self.results['actions'].append(dict(pulled_image="%s:%s" % (repository, tag)))
                elif not image:
                    # If the image isn't there, claim we'll pull.
                    # (Implicitly: if the image is there, claim it already was latest.)
                    self.results['changed'] = True
                    self.results['actions'].append(dict(pulled_image="%s:%s" % (repository, tag)))

        self.log("image")
        self.log(image, pretty_print=True)
        return image

    def _image_is_different(self, image, container):
        if image and image.get('Id'):
            if container and container.Image:
                if image.get('Id') != container.Image:
                    self.diff_tracker.add('image', parameter=image.get('Id'), active=container.Image)
                    return True
        return False

    def _compose_create_parameters(self, image):
        params = {
            'Image': image,
        }
        for options, values in self.parameters:
            engine = options.get_engine('docker_api')
            if engine.can_set_value(self.client.docker_api_version):
                engine.set_value(self.module, params, self.client.docker_api_version, options.options, values)
        return params

    def has_different_configuration(self, container, image):
        differences = DifferenceTracker()
        for options, param_values in self.parameters:
            engine = options.get_engine('docker_api')
            container_values = engine.get_value(self.module, container.raw, self.client.docker_api_version, options.options)
            expected_values = engine.get_expected_values(self.module, self.client, self.client.docker_api_version, options.options, image, param_values.copy())
            for option in options.options:
                if option.name in expected_values:
                    param_value = expected_values[option.name]
                    container_value = container_values.get(option.name)
                    match = compare_generic(param_value, container_value, option.comparison, option.comparison_type)

                    if not match:
                        if engine.ignore_mismatching_result(self.module, self.client, self.client.docker_api_version, option, image, container_value, param_value):
                            continue
                        # TODO
                        # if option.name == 'healthcheck' and config_mapping['disable_healthcheck'] and self.parameters.disable_healthcheck:
                        #     # If the healthcheck is disabled (both in parameters and for the current container), and the user
                        #     # requested strict comparison for healthcheck, the comparison will fail. That's why we ignore the
                        #     # expected_healthcheck comparison in this case.
                        #     continue

                        # no match. record the differences
                        p = param_value
                        c = container_value
                        if option.comparison_type == 'set':
                            # Since the order does not matter, sort so that the diff output is better.
                            if p is not None:
                                p = sorted(p)
                            if c is not None:
                                c = sorted(c)
                        elif option.comparison_type == 'set(dict)':
                            # Since the order does not matter, sort so that the diff output is better.
                            if option.name == 'expected_mounts':
                                # For selected values, use one entry as key
                                def sort_key_fn(x):
                                    return x['target']
                            else:
                                # We sort the list of dictionaries by using the sorted items of a dict as its key.
                                def sort_key_fn(x):
                                    return sorted((a, to_text(b, errors='surrogate_or_strict')) for a, b in x.items())
                            if p is not None:
                                p = sorted(p, key=sort_key_fn)
                            if c is not None:
                                c = sorted(c, key=sort_key_fn)
                        differences.add(option.name, parameter=p, active=c)

        has_differences = not differences.empty
        return has_differences, differences

    def has_different_resource_limits(self, container, image):
        '''
        Diff parameters and container resource limits
        '''
        differences = DifferenceTracker()
        for options, param_values in self.parameters:
            engine = options.get_engine('docker_api')
            if not engine.can_update_value(self.client.docker_api_version):
                continue
            container_values = engine.get_value(self.module, container.raw, self.client.docker_api_version, options.options)
            expected_values = engine.get_expected_values(self.module, self.client, self.client.docker_api_version, options.options, image, param_values.copy())
            for option in options.options:
                if option.name in expected_values:
                    param_value = expected_values[option.name]
                    container_value = container_values.get(option.name)
                    match = compare_generic(param_value, container_value, option.comparison, option.comparison_type)

                    if not match:
                        # no match. record the differences
                        differences.add(option.name, parameter=param_value, active=container_value)
        different = not differences.empty
        return different, differences

    def _compose_update_parameters(self):
        result = {}
        for options, values in self.parameters:
            engine = options.get_engine('docker_api')
            if not engine.can_update_value(self.client.docker_api_version):
                continue
            engine.update_value(self.module, result, self.client.docker_api_version, options.options, values)
        return result

    def update_limits(self, container, image):
        limits_differ, different_limits = self.has_different_resource_limits(container, image)
        if limits_differ:
            self.log("limit differences:")
            self.log(different_limits.get_legacy_docker_container_diffs(), pretty_print=True)
            self.diff_tracker.merge(different_limits)
        if limits_differ and not self.check_mode:
            self.container_update(container.Id, self._compose_update_parameters())
            return self._get_container(container.Id)
        return container

    def has_network_differences(self, container):
        '''
        Check if the container is connected to requested networks with expected options: links, aliases, ipv4, ipv6
        '''
        different = False
        differences = []

        if not self.module.params['networks']:
            return different, differences

        if not container.container.get('NetworkSettings'):
            self.fail("has_missing_networks: Error parsing container properties. NetworkSettings missing.")

        connected_networks = container.container['NetworkSettings']['Networks']
        for network in self.module.params['networks']:
            network_info = connected_networks.get(network['name'])
            if network_info is None:
                different = True
                differences.append(dict(
                    parameter=network,
                    container=None
                ))
            else:
                diff = False
                network_info_ipam = network_info.get('IPAMConfig') or {}
                if network.get('ipv4_address') and network['ipv4_address'] != network_info_ipam.get('IPv4Address'):
                    diff = True
                if network.get('ipv6_address') and network['ipv6_address'] != network_info_ipam.get('IPv6Address'):
                    diff = True
                if network.get('aliases'):
                    if not compare_generic(network['aliases'], network_info.get('Aliases'), 'allow_more_present', 'set'):
                        diff = True
                if network.get('links'):
                    expected_links = []
                    for link, alias in network['links']:
                        expected_links.append("%s:%s" % (link, alias))
                    if not compare_generic(expected_links, network_info.get('Links'), 'allow_more_present', 'set'):
                        diff = True
                if diff:
                    different = True
                    differences.append(dict(
                        parameter=network,
                        container=dict(
                            name=network['name'],
                            ipv4_address=network_info_ipam.get('IPv4Address'),
                            ipv6_address=network_info_ipam.get('IPv6Address'),
                            aliases=network_info.get('Aliases'),
                            links=network_info.get('Links')
                        )
                    ))
        return different, differences

    def has_extra_networks(self, container):
        '''
        Check if the container is connected to non-requested networks
        '''
        extra_networks = []
        extra = False

        if not container.container.get('NetworkSettings'):
            self.fail("has_extra_networks: Error parsing container properties. NetworkSettings missing.")

        connected_networks = container.container['NetworkSettings'].get('Networks')
        if connected_networks:
            for network, network_config in connected_networks.items():
                keep = False
                if self.module.params['networks']:
                    for expected_network in self.module.params['networks']:
                        if expected_network['name'] == network:
                            keep = True
                if not keep:
                    extra = True
                    extra_networks.append(dict(name=network, id=network_config['NetworkID']))
        return extra, extra_networks

    def update_networks(self, container, container_created):
        updated_container = container
        if self.all_options['networks'].comparison != 'ignore' or container_created:
            has_network_differences, network_differences = self.has_network_differences(container)
            if has_network_differences:
                if self.diff.get('differences'):
                    self.diff['differences'].append(dict(network_differences=network_differences))
                else:
                    self.diff['differences'] = [dict(network_differences=network_differences)]
                for netdiff in network_differences:
                    self.diff_tracker.add(
                        'network.{0}'.format(netdiff['parameter']['name']),
                        parameter=netdiff['parameter'],
                        active=netdiff['container']
                    )
                self.results['changed'] = True
                updated_container = self._add_networks(container, network_differences)

        if (self.all_options['networks'].comparison == 'strict' and self.module.params['networks'] is not None) or self.param_purge_networks:
            has_extra_networks, extra_networks = self.has_extra_networks(container)
            if has_extra_networks:
                if self.diff.get('differences'):
                    self.diff['differences'].append(dict(purge_networks=extra_networks))
                else:
                    self.diff['differences'] = [dict(purge_networks=extra_networks)]
                for extra_network in extra_networks:
                    self.diff_tracker.add(
                        'network.{0}'.format(extra_network['name']),
                        active=extra_network
                    )
                self.results['changed'] = True
                updated_container = self._purge_networks(container, extra_networks)
        return updated_container

    def _add_networks(self, container, differences):
        for diff in differences:
            # remove the container from the network, if connected
            if diff.get('container'):
                self.results['actions'].append(dict(removed_from_network=diff['parameter']['name']))
                if not self.check_mode:
                    try:
                        self.client.post_json('/networks/{0}/disconnect', diff['parameter']['id'], data={'Container': container.Id})
                    except Exception as exc:
                        self.fail("Error disconnecting container from network %s - %s" % (diff['parameter']['name'],
                                                                                          to_native(exc)))
            # connect to the network
            params = dict()
            for para, dest_para in {'ipv4_address': 'IPv4Address', 'ipv6_address': 'IPv6Address', 'links': 'Links', 'aliases': 'Aliases'}.items():
                if diff['parameter'].get(para):
                    value = diff['parameter'][para]
                    if para == 'links':
                        value = normalize_links(value)
                    params[dest_para] = value
            self.results['actions'].append(dict(added_to_network=diff['parameter']['name'], network_parameters=params))
            if not self.check_mode:
                try:
                    self.log("Connecting container to network %s" % diff['parameter']['id'])
                    self.log(params, pretty_print=True)
                    data = {
                        'Container': container.Id,
                        'EndpointConfig': params,
                    }
                    self.client.post_json('/networks/{0}/connect', diff['parameter']['id'], data=data)
                except Exception as exc:
                    self.fail("Error connecting container to network %s - %s" % (diff['parameter']['name'], to_native(exc)))
        return self._get_container(container.Id)

    def _purge_networks(self, container, networks):
        for network in networks:
            self.results['actions'].append(dict(removed_from_network=network['name']))
            if not self.check_mode:
                try:
                    self.client.post_json('/networks/{0}/disconnect', network['name'], data={'Container': container.Id})
                except Exception as exc:
                    self.fail("Error disconnecting container from network %s - %s" % (network['name'],
                                                                                      to_native(exc)))
        return self._get_container(container.Id)

    def container_create(self, image):
        create_parameters = self._compose_create_parameters(image)
        self.log("create container")
        self.log("image: %s parameters:" % image)
        self.log(create_parameters, pretty_print=True)
        self.results['actions'].append(dict(created="Created container", create_parameters=create_parameters))
        self.results['changed'] = True
        new_container = None
        if not self.check_mode:
            try:
                params = {'name': self.param_name}
                new_container = self.client.post_json_to_json('/containers/create', data=create_parameters, params=params)
                self.client.report_warnings(new_container)
            except Exception as exc:
                self.fail("Error creating container: %s" % to_native(exc))
            return self._get_container(new_container['Id'])
        return new_container

    def container_start(self, container_id):
        self.log("start container %s" % (container_id))
        self.results['actions'].append(dict(started=container_id))
        self.results['changed'] = True
        if not self.check_mode:
            try:
                self.client.post_json('/containers/{0}/start', container_id)
            except Exception as exc:
                self.fail("Error starting container %s: %s" % (container_id, to_native(exc)))

            if self.module.params['detach'] is False:
                status = self.client.post_json_as_json('/containers/{0}/wait', container_id)['StatusCode']
                self.client.fail_results['status'] = status
                self.results['status'] = status

                if self.module.params['auto_remove']:
                    output = "Cannot retrieve result as auto_remove is enabled"
                    if self.param_output_logs:
                        self.module.warn('Cannot output_logs if auto_remove is enabled!')
                else:
                    config = self.client.get_json('/containers/{0}/json', container_id)
                    logging_driver = config['HostConfig']['LogConfig']['Type']

                    if logging_driver in ('json-file', 'journald', 'local'):
                        params = {
                            'stderr': 1,
                            'stdout': 1,
                            'timestamps': 0,
                            'follow': 0,
                            'tail': 'all',
                        }
                        res = self.client._get(self.client._url('/containers/{0}/logs', container_id), params=params)
                        output = self.client._get_result_tty(False, res, config['Config']['Tty'])
                        if self.param_output_logs:
                            self._output_logs(msg=output)
                    else:
                        output = "Result logged using `%s` driver" % logging_driver

                if self.param_cleanup:
                    self.container_remove(container_id, force=True)
                insp = self._get_container(container_id)
                if insp.raw:
                    insp.raw['Output'] = output
                else:
                    insp.raw = dict(Output=output)
                if status != 0:
                    # Set `failed` to True and return output as msg
                    self.results['failed'] = True
                    self.results['msg'] = output
                return insp
        return self._get_container(container_id)

    def container_remove(self, container_id, link=False, force=False):
        volume_state = (not self.param_keep_volumes)
        self.log("remove container container:%s v:%s link:%s force%s" % (container_id, volume_state, link, force))
        self.results['actions'].append(dict(removed=container_id, volume_state=volume_state, link=link, force=force))
        self.results['changed'] = True
        if not self.check_mode:
            count = 0
            while True:
                try:
                    params = {'v': volume_state, 'link': link, 'force': force}
                    self.client.delete_call('/containers/{0}', container_id, params=params)
                except NotFound as dummy:
                    pass
                except APIError as exc:
                    if 'Unpause the container before stopping or killing' in exc.explanation:
                        # New docker daemon versions do not allow containers to be removed
                        # if they are paused. Make sure we don't end up in an infinite loop.
                        if count == 3:
                            self.fail("Error removing container %s (tried to unpause three times): %s" % (container_id, to_native(exc)))
                        count += 1
                        # Unpause
                        try:
                            self.client.post_call('/containers/{0}/unpause', container_id)
                        except Exception as exc2:
                            self.fail("Error unpausing container %s for removal: %s" % (container_id, to_native(exc2)))
                        # Now try again
                        continue
                    if 'removal of container ' in exc.explanation and ' is already in progress' in exc.explanation:
                        pass
                    else:
                        self.fail("Error removing container %s: %s" % (container_id, to_native(exc)))
                except Exception as exc:
                    self.fail("Error removing container %s: %s" % (container_id, to_native(exc)))
                # We only loop when explicitly requested by 'continue'
                break

    def container_update(self, container_id, update_parameters):
        if update_parameters:
            self.log("update container %s" % (container_id))
            self.log(update_parameters, pretty_print=True)
            self.results['actions'].append(dict(updated=container_id, update_parameters=update_parameters))
            self.results['changed'] = True
            if not self.check_mode and callable(getattr(self.client, 'update_container')):
                try:
                    result = self.client.post_json_to_json('/containers/{0}/update', container_id, data=update_parameters)
                    self.client.report_warnings(result)
                except Exception as exc:
                    self.fail("Error updating container %s: %s" % (container_id, to_native(exc)))
        return self._get_container(container_id)

    def container_kill(self, container_id):
        self.results['actions'].append(dict(killed=container_id, signal=self.param_kill_signal))
        self.results['changed'] = True
        if not self.check_mode:
            try:
                params = {}
                if self.param_kill_signal is not None:
                    params['signal'] = int(self.param_kill_signal)
                self.client.post_call('/containers/{0}/kill', container_id, params=params)
            except Exception as exc:
                self.fail("Error killing container %s: %s" % (container_id, to_native(exc)))

    def container_restart(self, container_id):
        self.results['actions'].append(dict(restarted=container_id, timeout=self.module.params['stop_timeout']))
        self.results['changed'] = True
        if not self.check_mode:
            try:
                timeout = self.module.params['stop_timeout'] or 10
                client_timeout = self.client.timeout
                if client_timeout is not None:
                    client_timeout += timeout
                self.client.post_call('/containers/{0}/restart', container_id, params={'t': timeout}, timeout=client_timeout)
            except Exception as exc:
                self.fail("Error restarting container %s: %s" % (container_id, to_native(exc)))
        return self._get_container(container_id)

    def container_stop(self, container_id):
        if self.param_force_kill:
            self.container_kill(container_id)
            return
        self.results['actions'].append(dict(stopped=container_id, timeout=self.module.params['stop_timeout']))
        self.results['changed'] = True
        if not self.check_mode:
            count = 0
            while True:
                try:
                    timeout = self.module.params['stop_timeout']
                    if timeout:
                        params = {'t': timeout}
                    else:
                        params = {}
                        timeout = 10
                    client_timeout = self.client.timeout
                    if client_timeout is not None:
                        client_timeout += timeout
                    self.client.post_call('/containers/{0}/stop', container_id, params=params, timeout=client_timeout)
                except APIError as exc:
                    if 'Unpause the container before stopping or killing' in exc.explanation:
                        # New docker daemon versions do not allow containers to be removed
                        # if they are paused. Make sure we don't end up in an infinite loop.
                        if count == 3:
                            self.fail("Error removing container %s (tried to unpause three times): %s" % (container_id, to_native(exc)))
                        count += 1
                        # Unpause
                        try:
                            self.client.post_call('/containers/{0}/unpause', container_id)
                        except Exception as exc2:
                            self.fail("Error unpausing container %s for removal: %s" % (container_id, to_native(exc2)))
                        # Now try again
                        continue
                    self.fail("Error stopping container %s: %s" % (container_id, to_native(exc)))
                except Exception as exc:
                    self.fail("Error stopping container %s: %s" % (container_id, to_native(exc)))
                # We only loop when explicitly requested by 'continue'
                break


def main():
    argument_spec = dict(
        cleanup=dict(type='bool', default=False),
        comparisons=dict(type='dict'),
        container_default_behavior=dict(type='str', default='no_defaults', choices=['compatibility', 'no_defaults']),
        command_handling=dict(type='str', choices=['compatibility', 'correct']),
        default_host_ip=dict(type='str'),
        force_kill=dict(type='bool', default=False, aliases=['forcekill']),
        ignore_image=dict(type='bool', default=False),
        image=dict(type='str'),
        image_label_mismatch=dict(type='str', choices=['ignore', 'fail'], default='ignore'),
        keep_volumes=dict(type='bool', default=True),
        kill_signal=dict(type='str'),
        name=dict(type='str', required=True),
        networks=dict(type='list', elements='dict', options=dict(
            name=dict(type='str', required=True),
            ipv4_address=dict(type='str'),
            ipv6_address=dict(type='str'),
            aliases=dict(type='list', elements='str'),
            links=dict(type='list', elements='str'),
        )),
        networks_cli_compatible=dict(type='bool', default=True),
        output_logs=dict(type='bool', default=False),
        paused=dict(type='bool'),
        pull=dict(type='bool', default=False),
        purge_networks=dict(type='bool', default=False),
        recreate=dict(type='bool', default=False),
        removal_wait_timeout=dict(type='float'),
        restart=dict(type='bool', default=False),
        state=dict(type='str', default='started', choices=['absent', 'present', 'started', 'stopped']),
        stop_signal=dict(type='str'),
    )

    mutually_exclusive = []
    required_together = []
    required_one_of = []
    required_if = [
        ('state', 'present', ['image'])
    ]
    required_by = {}

    option_minimal_versions = {}

    active_options = []
    for options in OPTIONS:
        if not options.supports_engine('docker_api'):
            continue

        mutually_exclusive.extend(options.ansible_mutually_exclusive)
        required_together.extend(options.ansible_required_together)
        required_one_of.extend(options.ansible_required_one_of)
        required_if.extend(options.ansible_required_if)
        required_by.update(options.ansible_required_by)
        argument_spec.update(options.argument_spec)

        engine = options.get_engine('docker_api')
        if engine.min_docker_api is not None:
            for option in options.options:
                option_minimal_versions[option.name] = {'docker_api_version': engine.min_docker_api}

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

    try:
        cm = ContainerManager(client.module, client, active_options)
        cm.run()
        client.module.exit_json(**sanitize_result(cm.results))
    except DockerException as e:
        client.fail('An unexpected Docker error occurred: {0}'.format(to_native(e)), exception=traceback.format_exc())
    except RequestException as e:
        client.fail(
            'An unexpected requests error occurred when trying to talk to the Docker daemon: {0}'.format(to_native(e)),
            exception=traceback.format_exc())


if __name__ == '__main__':
    main()
