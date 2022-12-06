=========================================
Docker Community Collection Release Notes
=========================================

.. contents:: Topics


v2.7.3
======

Release Summary
---------------

Bugfix release.

Bugfixes
--------

- current_container_facts - make container detection work better in more cases (https://github.com/ansible-collections/community.docker/pull/522).

v2.7.2
======

Release Summary
---------------

Bugfix release.

Minor Changes
-------------

- current_container_facts - make work with current Docker version (https://github.com/ansible-collections/community.docker/pull/510, https://github.com/ansible-collections/community.docker/pull/512).

v2.7.1
======

Release Summary
---------------

Maintenance release with updated documentation.

Bugfixes
--------

- docker_stack - fix broken string formatting when reporting error in case ``compose`` was containing invalid values (https://github.com/ansible-collections/community.docker/pull/448).

v2.7.0
======

Release Summary
---------------

Bugfix and deprecation release. The next 2.x.y releases will only be bugfix releases, the next expect minor/major release will be 3.0.0 with some major changes.

Minor Changes
-------------

- Move common utility functions from the ``common`` module_util to a new module_util called ``util``. This should not have any user-visible effect (https://github.com/ansible-collections/community.docker/pull/390).

Deprecated Features
-------------------

- Support for Docker API version 1.20 to 1.24 has been deprecated and will be removed in community.docker 3.0.0. The first Docker version supporting API version 1.25 was Docker 1.13, released in January 2017. This affects the modules ``docker_container``, ``docker_container_exec``, ``docker_container_info``, ``docker_compose``, ``docker_login``, ``docker_image``, ``docker_image_info``, ``docker_image_load``, ``docker_host_info``, ``docker_network``, ``docker_network_info``, ``docker_node_info``, ``docker_swarm_info``, ``docker_swarm_service``, ``docker_swarm_service_info``, ``docker_volume_info``, and ``docker_volume``, whose minimally supported API version is between 1.20 and 1.24 (https://github.com/ansible-collections/community.docker/pull/396).
- Support for Python 2.6 is deprecated and will be removed in the next major release (community.docker 3.0.0). Some modules might still work with Python 2.6, but we will no longer try to ensure compatibility (https://github.com/ansible-collections/community.docker/pull/388).

Bugfixes
--------

- Docker SDK for Python based modules and plugins - if the API version is specified as an option, use that one to validate API version requirements of module/plugin options instead of the latest API version supported by the Docker daemon. This also avoids one unnecessary API call per module/plugin (https://github.com/ansible-collections/community.docker/pull/389).

v2.6.0
======

Release Summary
---------------

Bugfix and feature release.

Minor Changes
-------------

- docker_container - added ``image_label_mismatch`` parameter (https://github.com/ansible-collections/community.docker/issues/314, https://github.com/ansible-collections/community.docker/pull/370).

Deprecated Features
-------------------

- Support for Ansible 2.9 and ansible-base 2.10 is deprecated, and will be removed in the next major release (community.docker 3.0.0). Some modules might still work with these versions afterwards, but we will no longer keep compatibility code that was needed to support them (https://github.com/ansible-collections/community.docker/pull/361).
- The dependency on docker-compose for Execution Environments is deprecated and will be removed in community.docker 3.0.0. The `Python docker-compose library <https://pypi.org/project/docker-compose/>`__ is unmaintained and can cause dependency issues. You can manually still install it in an Execution Environment when needed (https://github.com/ansible-collections/community.docker/pull/373).
- Various modules - the default of ``tls_hostname`` that was supposed to be removed in community.docker 2.0.0 will now be removed in version 3.0.0 (https://github.com/ansible-collections/community.docker/pull/362).
- docker_stack - the return values ``out`` and ``err`` that were supposed to be removed in community.docker 2.0.0 will now be removed in version 3.0.0 (https://github.com/ansible-collections/community.docker/pull/362).

Bugfixes
--------

- docker_container - fail with a meaningful message instead of crashing if a port is specified with more than three colon-separated parts (https://github.com/ansible-collections/community.docker/pull/367, https://github.com/ansible-collections/community.docker/issues/365).
- docker_container - remove unused code that will cause problems with Python 3.13 (https://github.com/ansible-collections/community.docker/pull/354).

v2.5.1
======

Release Summary
---------------

Maintenance release.

Bugfixes
--------

- Include ``PSF-license.txt`` file for ``plugins/module_utils/_version.py``.

v2.5.0
======

Release Summary
---------------

Regular feature release.

Minor Changes
-------------

- docker_config - add support for ``template_driver`` with one option ``golang`` (https://github.com/ansible-collections/community.docker/issues/332, https://github.com/ansible-collections/community.docker/pull/345).
- docker_swarm - adds ``data_path_addr`` parameter during swarm initialization or when joining (https://github.com/ansible-collections/community.docker/issues/339).

v2.4.0
======

Release Summary
---------------

Regular feature and bugfix release.

Minor Changes
-------------

- Prepare collection for inclusion in an Execution Environment by declaring its dependencies. The ``docker_stack*`` modules are not supported (https://github.com/ansible-collections/community.docker/pull/336).
- current_container_facts - add detection for GitHub Actions (https://github.com/ansible-collections/community.docker/pull/336).
- docker_container - support returning Docker container log output when using Docker's ``local`` logging driver, an optimized local logging driver introduced in Docker 18.09 (https://github.com/ansible-collections/community.docker/pull/337).

Bugfixes
--------

- docker connection plugin - make sure that ``docker_extra_args`` is used for querying the Docker version. Also ensures that the Docker version is only queried when needed. This is currently the case if a remote user is specified (https://github.com/ansible-collections/community.docker/issues/325, https://github.com/ansible-collections/community.docker/pull/327).

v2.3.0
======

Release Summary
---------------

Regular feature and bugfix release.

Minor Changes
-------------

- docker connection plugin - implement connection reset by clearing internal container user cache (https://github.com/ansible-collections/community.docker/pull/312).
- docker connection plugin - simplify ``actual_user`` handling code (https://github.com/ansible-collections/community.docker/pull/311).
- docker connection plugin - the plugin supports new ways to define the timeout. These are the ``ANSIBLE_DOCKER_TIMEOUT`` environment variable, the ``timeout`` setting in the ``docker_connection`` section of ``ansible.cfg``, and the ``ansible_docker_timeout`` variable (https://github.com/ansible-collections/community.docker/pull/297).
- docker_api connection plugin - implement connection reset by clearing internal container user/group ID cache (https://github.com/ansible-collections/community.docker/pull/312).
- docker_api connection plugin - the plugin supports new ways to define the timeout. These are the ``ANSIBLE_DOCKER_TIMEOUT`` environment variable, the ``timeout`` setting in the ``docker_connection`` section of ``ansible.cfg``, and the ``ansible_docker_timeout`` variable (https://github.com/ansible-collections/community.docker/pull/308).

Bugfixes
--------

- docker connection plugin - fix option handling to be compatible with ansible-core 2.13 (https://github.com/ansible-collections/community.docker/pull/297, https://github.com/ansible-collections/community.docker/issues/307).
- docker_api connection plugin - fix option handling to be compatible with ansible-core 2.13 (https://github.com/ansible-collections/community.docker/pull/308).

v2.2.1
======

Release Summary
---------------

Regular bugfix release.

Bugfixes
--------

- docker_compose - fix Python 3 type error when extracting warnings or errors from docker-compose's output (https://github.com/ansible-collections/community.docker/pull/305).

v2.2.0
======

Release Summary
---------------

Regular feature and bugfix release.

Minor Changes
-------------

- docker_config - add support for rolling update, set ``rolling_versions`` to ``true`` to enable (https://github.com/ansible-collections/community.docker/pull/295, https://github.com/ansible-collections/community.docker/issues/109).
- docker_secret - add support for rolling update, set ``rolling_versions`` to ``true`` to enable (https://github.com/ansible-collections/community.docker/pull/293, https://github.com/ansible-collections/community.docker/issues/21).
- docker_swarm_service - add support for setting capabilities with the ``cap_add`` and ``cap_drop`` parameters. Usage is the same as with the ``capabilities`` and ``cap_drop`` parameters for ``docker_container`` (https://github.com/ansible-collections/community.docker/pull/294).

Bugfixes
--------

- docker_container, docker_image - adjust image finding code to pecularities of ``podman-docker``'s API emulation when Docker short names like ``redis`` are used (https://github.com/ansible-collections/community.docker/issues/292).

v2.1.1
======

Release Summary
---------------

Emergency release to amend breaking change in previous release.

Bugfixes
--------

- Fix unintended breaking change caused by `an earlier fix <https://github.com/ansible-collections/community.docker/pull/258>`_ by vendoring the deprecated Python standard library ``distutils.version`` until this collection stops supporting Ansible 2.9 and ansible-base 2.10 (https://github.com/ansible-collections/community.docker/issues/267, https://github.com/ansible-collections/community.docker/pull/269).

v2.1.0
======

Release Summary
---------------

Feature and bugfix release.

Minor Changes
-------------

- docker_container_exec - add ``detach`` parameter (https://github.com/ansible-collections/community.docker/issues/250, https://github.com/ansible-collections/community.docker/pull/255).
- docker_container_exec - add ``env`` option (https://github.com/ansible-collections/community.docker/issues/248, https://github.com/ansible-collections/community.docker/pull/254).

Bugfixes
--------

- Various modules and plugins - use vendored version of ``distutils.version`` included in ansible-core 2.12 if available. This avoids breakage when ``distutils`` is removed from the standard library of Python 3.12. Note that ansible-core 2.11, ansible-base 2.10 and Ansible 2.9 are right now not compatible with Python 3.12, hence this fix does not target these ansible-core/-base/2.9 versions (https://github.com/ansible-collections/community.docker/pull/258).
- docker connection plugin - replace deprecated ``distutils.spawn.find_executable`` with Ansible's ``get_bin_path`` to find the ``docker`` executable (https://github.com/ansible-collections/community.docker/pull/257).
- docker_container_exec - disallow using the ``chdir`` option for Docker API before 1.35 (https://github.com/ansible-collections/community.docker/pull/253).

v2.0.2
======

Release Summary
---------------

Bugfix release.

Bugfixes
--------

- docker_api connection plugin - avoid passing an unnecessary argument to a Docker SDK for Python call that is only supported by version 3.0.0 or later (https://github.com/ansible-collections/community.docker/pull/243).
- docker_container_exec - ``chdir`` is only supported since Docker SDK for Python 3.0.0. Make sure that this option can only use when 3.0.0 or later is installed, and prevent passing this parameter on when ``chdir`` is not provided to this module (https://github.com/ansible-collections/community.docker/pull/243, https://github.com/ansible-collections/community.docker/issues/242).
- nsenter connection plugin - ensure the ``nsenter_pid`` option is retrieved in ``_connect`` instead of ``__init__`` to prevent a crasher due to bad initialization order (https://github.com/ansible-collections/community.docker/pull/249).
- nsenter connection plugin - replace the use of ``--all-namespaces`` with specific namespaces to support compatibility with Busybox nsenter (used on, for example, Alpine containers) (https://github.com/ansible-collections/community.docker/pull/249).

v2.0.1
======

Release Summary
---------------

Maintenance release with some documentation fixes.

v2.0.0
======

Release Summary
---------------

New major release with some deprecations removed and a breaking change in the ``docker_compose`` module regarding the ``timeout`` parameter.

Breaking Changes / Porting Guide
--------------------------------

- docker_compose - fixed ``timeout`` defaulting behavior so that ``stop_grace_period``, if defined in the compose file, will be used if `timeout`` is not specified (https://github.com/ansible-collections/community.docker/pull/163).

Deprecated Features
-------------------

- docker_container - using the special value ``all`` in ``published_ports`` has been deprecated. Use ``publish_all_ports=true`` instead (https://github.com/ansible-collections/community.docker/pull/210).

Removed Features (previously deprecated)
----------------------------------------

- docker_container - the default value of ``container_default_behavior`` changed to ``no_defaults`` (https://github.com/ansible-collections/community.docker/pull/210).
- docker_container - the default value of ``network_mode`` is now the name of the first network specified in ``networks`` if such are specified and ``networks_cli_compatible=true`` (https://github.com/ansible-collections/community.docker/pull/210).
- docker_container - the special value ``all`` can no longer be used in ``published_ports`` next to other values. Please use ``publish_all_ports=true`` instead (https://github.com/ansible-collections/community.docker/pull/210).
- docker_login - removed the ``email`` option (https://github.com/ansible-collections/community.docker/pull/210).

v1.10.0
=======

Release Summary
---------------

Regular feature and bugfix release.

Minor Changes
-------------

- Add the modules docker_container_exec, docker_image_load and docker_plugin to the ``docker`` module defaults group (https://github.com/ansible-collections/community.docker/pull/209).
- docker_config - add option ``data_src`` to read configuration data from target (https://github.com/ansible-collections/community.docker/issues/64, https://github.com/ansible-collections/community.docker/pull/203).
- docker_secret - add option ``data_src`` to read secret data from target (https://github.com/ansible-collections/community.docker/issues/64, https://github.com/ansible-collections/community.docker/pull/203).

v1.9.1
======

Release Summary
---------------

Regular bugfix release.

Bugfixes
--------

- docker_compose - fixed incorrect ``changed`` status for services with ``profiles`` defined, but none enabled (https://github.com/ansible-collections/community.docker/pull/192).

v1.9.0
======

Release Summary
---------------

New bugfixes and features release.

Minor Changes
-------------

- docker_* modules - include ``ImportError`` traceback when reporting that Docker SDK for Python could not be found (https://github.com/ansible-collections/community.docker/pull/188).
- docker_compose - added ``env_file`` option for specifying custom environment files (https://github.com/ansible-collections/community.docker/pull/174).
- docker_container - added ``publish_all_ports`` option to publish all exposed ports to random ports except those explicitly bound with ``published_ports`` (this was already added in community.docker 1.8.0) (https://github.com/ansible-collections/community.docker/pull/162).
- docker_container - added new ``command_handling`` option with current deprecated default value ``compatibility`` which allows to control how the module handles shell quoting when interpreting lists, and how the module handles empty lists/strings. The default will switch to ``correct`` in community.docker 3.0.0 (https://github.com/ansible-collections/community.docker/pull/186).
- docker_container - lifted restriction preventing the creation of anonymous volumes with the ``mounts`` option (https://github.com/ansible-collections/community.docker/pull/181).

Deprecated Features
-------------------

- docker_container - the new ``command_handling``'s default value, ``compatibility``, is deprecated and will change to ``correct`` in community.docker 3.0.0. A deprecation warning is emitted by the module in cases where the behavior will change. Please note that ansible-core will output a deprecation warning only once, so if it is shown for an earlier task, there could be more tasks with this warning where it is not shown (https://github.com/ansible-collections/community.docker/pull/186).

Bugfixes
--------

- docker_compose - fixes task failures when bringing up services while using ``docker-compose <1.17.0`` (https://github.com/ansible-collections/community.docker/issues/180).
- docker_container - make sure to also return ``container`` on ``detached=false`` when status code is non-zero (https://github.com/ansible-collections/community.docker/pull/178).
- docker_stack_info - make sure that module isn't skipped in check mode (https://github.com/ansible-collections/community.docker/pull/183).
- docker_stack_task_info - make sure that module isn't skipped in check mode (https://github.com/ansible-collections/community.docker/pull/183).

New Plugins
-----------

Connection
~~~~~~~~~~

- nsenter - execute on host running controller container

v1.8.0
======

Release Summary
---------------

Regular bugfix and feature release.

Minor Changes
-------------

- Avoid internal ansible-core module_utils in favor of equivalent public API available since at least Ansible 2.9 (https://github.com/ansible-collections/community.docker/pull/164).
- docker_compose - added ``profiles`` option to specify service profiles when starting services (https://github.com/ansible-collections/community.docker/pull/167).
- docker_containers inventory plugin - when ``connection_type=docker-api``, now pass Docker daemon connection options from inventory plugin to connection plugin. This can be disabled by setting ``configure_docker_daemon=false`` (https://github.com/ansible-collections/community.docker/pull/157).
- docker_host_info - allow values for keys in ``containers_filters``, ``images_filters``, ``networks_filters``, and ``volumes_filters`` to be passed as YAML lists (https://github.com/ansible-collections/community.docker/pull/160).
- docker_plugin - added ``alias`` option to specify local names for docker plugins (https://github.com/ansible-collections/community.docker/pull/161).

Bugfixes
--------

- docker_compose - fix idempotence bug when using ``stopped: true`` (https://github.com/ansible-collections/community.docker/issues/142, https://github.com/ansible-collections/community.docker/pull/159).

v1.7.0
======

Release Summary
---------------

Small feature and bugfix release.

Minor Changes
-------------

- docker_image - allow to tag images by ID (https://github.com/ansible-collections/community.docker/pull/149).

v1.6.1
======

Release Summary
---------------

Bugfix release to reduce deprecation warning spam.

Bugfixes
--------

- docker_* modules and plugins, except ``docker_swarm`` connection plugin and ``docker_compose`` and ``docker_stack*` modules - only emit ``tls_hostname`` deprecation message if TLS is actually used (https://github.com/ansible-collections/community.docker/pull/143).

v1.6.0
======

Release Summary
---------------

Regular bugfix and feature release.

Minor Changes
-------------

- common module utils - correct error messages for guiding to install proper Docker SDK for Python module (https://github.com/ansible-collections/community.docker/pull/125).
- docker_container - allow ``memory_swap: -1`` to set memory swap limit to unlimited. This is useful when the user cannot set memory swap limits due to cgroup limitations or other reasons, as by default Docker will try to set swap usage to two times the value of ``memory`` (https://github.com/ansible-collections/community.docker/pull/138).

Deprecated Features
-------------------

- docker_* modules and plugins, except ``docker_swarm`` connection plugin and ``docker_compose`` and ``docker_stack*` modules - the current default ``localhost`` for ``tls_hostname`` is deprecated. In community.docker 2.0.0 it will be computed from ``docker_host`` instead (https://github.com/ansible-collections/community.docker/pull/134).

Bugfixes
--------

- docker-compose - fix not pulling when ``state: present`` and ``stopped: true`` (https://github.com/ansible-collections/community.docker/issues/12, https://github.com/ansible-collections/community.docker/pull/119).
- docker_plugin - also configure plugin after installing (https://github.com/ansible-collections/community.docker/issues/118, https://github.com/ansible-collections/community.docker/pull/135).
- docker_swarm_services - avoid crash during idempotence check if ``published_port`` is not specified (https://github.com/ansible-collections/community.docker/issues/107, https://github.com/ansible-collections/community.docker/pull/136).

v1.5.0
======

Release Summary
---------------

Regular feature release.

Minor Changes
-------------

- Add the ``use_ssh_client`` option to most docker modules and plugins (https://github.com/ansible-collections/community.docker/issues/108, https://github.com/ansible-collections/community.docker/pull/114).

Bugfixes
--------

- all modules - use ``to_native`` to convert exceptions to strings (https://github.com/ansible-collections/community.docker/pull/121).

New Modules
-----------

- docker_container_exec - Execute command in a docker container

v1.4.0
======

Release Summary
---------------

Security release to address another potential secret leak. Also includes regular bugfixes and features.

Minor Changes
-------------

- docker_swarm_service - change ``publish.published_port`` option from mandatory to optional. Docker will assign random high port if not specified (https://github.com/ansible-collections/community.docker/issues/99).

Breaking Changes / Porting Guide
--------------------------------

- docker_swarm - if ``join_token`` is specified, a returned join token with the same value will be replaced by ``VALUE_SPECIFIED_IN_NO_LOG_PARAMETER``. Make sure that you do not blindly use the join tokens from the return value of this module when the module is invoked with ``join_token`` specified! This breaking change appears in a minor release since it is necessary to fix a security issue (https://github.com/ansible-collections/community.docker/pull/103).

Security Fixes
--------------

- docker_swarm - the ``join_token`` option is now marked as ``no_log`` so it is no longer written into logs (https://github.com/ansible-collections/community.docker/pull/103).

Bugfixes
--------

- ``docker_swarm_service`` - fix KeyError on caused by reference to deprecated option ``update_failure_action`` (https://github.com/ansible-collections/community.docker/pull/100).
- docker_swarm_service - mark ``secrets`` module option with ``no_log=False`` since it does not leak secrets (https://github.com/ansible-collections/community.general/pull/2001).

v1.3.0
======

Release Summary
---------------

Regular feature and bugfix release.

Minor Changes
-------------

- docker_container - add ``storage_opts`` option to specify storage options (https://github.com/ansible-collections/community.docker/issues/91, https://github.com/ansible-collections/community.docker/pull/93).
- docker_image - allows to specify platform to pull for ``source=pull`` with new option ``pull_platform`` (https://github.com/ansible-collections/community.docker/issues/79, https://github.com/ansible-collections/community.docker/pull/89).
- docker_image - properly support image IDs (hashes) for loading and tagging images (https://github.com/ansible-collections/community.docker/issues/86, https://github.com/ansible-collections/community.docker/pull/87).
- docker_swarm_service - adding support for maximum number of tasks per node (``replicas_max_per_node``) when running swarm service in replicated mode. Introduced in API 1.40 (https://github.com/ansible-collections/community.docker/issues/7, https://github.com/ansible-collections/community.docker/pull/92).

Bugfixes
--------

- docker_container - fix healthcheck disabling idempotency issue with strict comparison (https://github.com/ansible-collections/community.docker/issues/85).
- docker_image - prevent module failure when removing image that is removed between inspection and removal (https://github.com/ansible-collections/community.docker/pull/87).
- docker_image - prevent module failure when removing non-existant image by ID (https://github.com/ansible-collections/community.docker/pull/87).
- docker_image_info - prevent module failure when image vanishes between listing and inspection (https://github.com/ansible-collections/community.docker/pull/87).
- docker_image_info - prevent module failure when querying non-existant image by ID (https://github.com/ansible-collections/community.docker/pull/87).

New Modules
-----------

- docker_image_load - Load docker image(s) from archives
- docker_plugin - Manage Docker plugins

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
