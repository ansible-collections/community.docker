=========================================
Docker Community Collection Release Notes
=========================================

.. contents:: Topics


v1.2.2
======

Release Summary
---------------

Security bugfix release to address CVE-2021-20191.

Security Fixes
--------------

- docker_swarm - enabled ``no_log`` for the option ``signing_ca_key`` to prevent accidental disclosure (CVE-2021-20191, https://github.com/ansible-collections/community.docker/pull/80).

v1.2.1
======

Release Summary
---------------

Bugfix release.

Bugfixes
--------

- docker connection plugin - fix Docker version parsing, as some docker versions have a leading ``v`` in the output of the command ``docker version --format "{{.Server.Version}}"`` (https://github.com/ansible-collections/community.docker/pull/76).

v1.2.0
======

Release Summary
---------------

Feature release with one new feature and two bugfixes.

Minor Changes
-------------

- docker_container - added ``default_host_ip`` option which allows to explicitly set the default IP string for published ports without explicitly specified IPs. When using IPv6 binds with Docker 20.10.2 or newer, this needs to be set to an empty string (``""``) (https://github.com/ansible-collections/community.docker/issues/70, https://github.com/ansible-collections/community.docker/pull/71).

Bugfixes
--------

- docker_container - allow IPv6 zones (RFC 4007) in bind IPs (https://github.com/ansible-collections/community.docker/pull/66).
- docker_image - fix crash on loading images with versions of Docker SDK for Python before 2.5.0 (https://github.com/ansible-collections/community.docker/issues/72, https://github.com/ansible-collections/community.docker/pull/73).

v1.1.0
======

Release Summary
---------------

Feature release with three new plugins and modules.

Minor Changes
-------------

- docker_container - support specifying ``cgroup_parent`` (https://github.com/ansible-collections/community.docker/issues/6, https://github.com/ansible-collections/community.docker/pull/59).
- docker_container - when a container is started with ``detached=false``, ``status`` is now also returned when it is 0 (https://github.com/ansible-collections/community.docker/issues/26, https://github.com/ansible-collections/community.docker/pull/58).
- docker_image - support ``platform`` when building images (https://github.com/ansible-collections/community.docker/issues/22, https://github.com/ansible-collections/community.docker/pull/54).

Deprecated Features
-------------------

- docker_container - currently ``published_ports`` can contain port mappings next to the special value ``all``, in which case the port mappings are ignored. This behavior is deprecated for community.docker 2.0.0, at which point it will either be forbidden, or this behavior will be properly implemented similar to how the Docker CLI tool handles this (https://github.com/ansible-collections/community.docker/issues/8, https://github.com/ansible-collections/community.docker/pull/60).

Bugfixes
--------

- docker_image - if ``push=true`` is used with ``repository``, and the image does not need to be tagged, still push. This can happen if ``repository`` and ``name`` are equal (https://github.com/ansible-collections/community.docker/issues/52, https://github.com/ansible-collections/community.docker/pull/53).
- docker_image - report error when loading a broken archive that contains no image (https://github.com/ansible-collections/community.docker/issues/46, https://github.com/ansible-collections/community.docker/pull/55).
- docker_image - report error when the loaded archive does not contain the specified image (https://github.com/ansible-collections/community.docker/issues/41, https://github.com/ansible-collections/community.docker/pull/55).

New Plugins
-----------

Connection
~~~~~~~~~~

- docker_api - Run tasks in docker containers

Inventory
~~~~~~~~~

- docker_containers - Ansible dynamic inventory plugin for Docker containers.

New Modules
-----------

- current_container_facts - Return facts about whether the module runs in a Docker container

v1.0.1
======

Release Summary
---------------

Maintenance release with a bugfix for ``docker_container``.

Bugfixes
--------

- docker_container - the validation for ``capabilities`` in ``device_requests`` was incorrect (https://github.com/ansible-collections/community.docker/issues/42, https://github.com/ansible-collections/community.docker/pull/43).

v1.0.0
======

Release Summary
---------------

This is the first production (non-prerelease) release of ``community.docker``.


Minor Changes
-------------

- Add collection-side support of the ``docker`` action group / module defaults group (https://github.com/ansible-collections/community.docker/pull/17).
- docker_image - return docker build output (https://github.com/ansible-collections/community.general/pull/805).
- docker_secret - add a warning when the secret does not have an ``ansible_key`` label but the ``force`` parameter is not set (https://github.com/ansible-collections/community.docker/issues/30, https://github.com/ansible-collections/community.docker/pull/31).

v0.1.0
======

Release Summary
---------------

The ``community.docker`` continues the work on the Ansible docker modules and plugins from their state in ``community.general`` 1.2.0. The changes listed here are thus relative to the modules and plugins ``community.general.docker*``.

All deprecation removals planned for ``community.general`` 2.0.0 have been applied. All deprecation removals scheduled for ``community.general`` 3.0.0 have been re-scheduled for ``community.docker`` 2.0.0.


Minor Changes
-------------

- docker_container - now supports the ``device_requests`` option, which allows to request additional resources such as GPUs (https://github.com/ansible/ansible/issues/65748, https://github.com/ansible-collections/community.general/pull/1119).

Removed Features (previously deprecated)
----------------------------------------

- docker_container - no longer returns ``ansible_facts`` (https://github.com/ansible-collections/community.docker/pull/1).
- docker_container - the default of ``networks_cli_compatible`` changed to ``true`` (https://github.com/ansible-collections/community.docker/pull/1).
- docker_container - the unused option ``trust_image_content`` has been removed (https://github.com/ansible-collections/community.docker/pull/1).
- docker_image - ``state=build`` has been removed. Use ``present`` instead (https://github.com/ansible-collections/community.docker/pull/1).
- docker_image - the ``container_limits``, ``dockerfile``, ``http_timeout``, ``nocache``, ``rm``, ``path``, ``buildargs``, ``pull`` have been removed. Use the corresponding suboptions of ``build`` instead (https://github.com/ansible-collections/community.docker/pull/1).
- docker_image - the ``force`` option has been removed. Use the more specific ``force_*`` options instead (https://github.com/ansible-collections/community.docker/pull/1).
- docker_image - the ``source`` option is now mandatory (https://github.com/ansible-collections/community.docker/pull/1).
- docker_image - the ``use_tls`` option has been removed. Use ``tls`` and ``validate_certs`` instead (https://github.com/ansible-collections/community.docker/pull/1).
- docker_image - the default of the ``build.pull`` option changed to ``false`` (https://github.com/ansible-collections/community.docker/pull/1).
- docker_image_facts - this alias is on longer availabe, use ``docker_image_info`` instead (https://github.com/ansible-collections/community.docker/pull/1).
- docker_network - no longer returns ``ansible_facts`` (https://github.com/ansible-collections/community.docker/pull/1).
- docker_network - the ``ipam_options`` option has been removed. Use ``ipam_config`` instead (https://github.com/ansible-collections/community.docker/pull/1).
- docker_service - no longer returns ``ansible_facts`` (https://github.com/ansible-collections/community.docker/pull/1).
- docker_swarm - ``state=inspect`` has been removed. Use ``docker_swarm_info`` instead (https://github.com/ansible-collections/community.docker/pull/1).
- docker_swarm_service - the ``constraints`` option has been removed. Use ``placement.constraints`` instead (https://github.com/ansible-collections/community.docker/pull/1).
- docker_swarm_service - the ``limit_cpu`` and ``limit_memory`` options has been removed. Use the corresponding suboptions in ``limits`` instead (https://github.com/ansible-collections/community.docker/pull/1).
- docker_swarm_service - the ``log_driver`` and ``log_driver_options`` options has been removed. Use the corresponding suboptions in ``logging`` instead (https://github.com/ansible-collections/community.docker/pull/1).
- docker_swarm_service - the ``reserve_cpu`` and ``reserve_memory`` options has been removed. Use the corresponding suboptions in ``reservations`` instead (https://github.com/ansible-collections/community.docker/pull/1).
- docker_swarm_service - the ``restart_policy``, ``restart_policy_attempts``, ``restart_policy_delay`` and ``restart_policy_window`` options has been removed. Use the corresponding suboptions in ``restart_config`` instead (https://github.com/ansible-collections/community.docker/pull/1).
- docker_swarm_service - the ``update_delay``, ``update_parallelism``, ``update_failure_action``, ``update_monitor``, ``update_max_failure_ratio`` and ``update_order`` options has been removed. Use the corresponding suboptions in ``update_config`` instead (https://github.com/ansible-collections/community.docker/pull/1).
- docker_volume - no longer returns ``ansible_facts`` (https://github.com/ansible-collections/community.docker/pull/1).
- docker_volume - the ``force`` option has been removed. Use ``recreate`` instead (https://github.com/ansible-collections/community.docker/pull/1).

Bugfixes
--------

- docker_login - fix internal config file storage to handle credentials for more than one registry (https://github.com/ansible-collections/community.general/issues/1117).
