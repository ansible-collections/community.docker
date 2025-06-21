..
  Copyright (c) Ansible Project
  GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
  SPDX-License-Identifier: GPL-3.0-or-later

.. _ansible_collections.community.docker.docsite.scenario_guide:

Docker Guide
============

The `community.docker collection <https://galaxy.ansible.com/ui/repo/published/community/docker/>`_ offers several modules and plugins for orchestrating Docker containers and Docker Swarm.

.. contents::
   :local:
   :depth: 1


Requirements
------------

Most of the modules and plugins in community.docker require the `Docker SDK for Python <https://docker-py.readthedocs.io/en/stable/>`_. The SDK needs to be installed on the machines where the modules and plugins are executed, and for the Python version(s) with which the modules and plugins are executed. You can use the :ansplugin:`community.general.python_requirements_info module <community.general.python_requirements_info#module>` to make sure that the Docker SDK for Python is installed on the correct machine and for the Python version used by Ansible.

Note that plugins (inventory plugins and connection plugins) are always executed in the context of Ansible itself. If you use a plugin that requires the Docker SDK for Python, you need to install it on the machine running ``ansible`` or ``ansible-playbook`` and for the same Python interpreter used by Ansible. To see which Python is used, run ``ansible --version``.

You can install the Docker SDK for Python for Python 3.6 or later as follows:

.. code-block:: console

    $ pip install docker

For Python 2.7, you need to use a version between 2.0.0 and 4.4.4 since the Python package for Docker removed support for Python 2.7 on 5.0.0. You can install the specific version of the Docker SDK for Python as follows:

.. code-block:: console

    $ pip install 'docker==4.4.4'

Note that the Docker SDK for Python was called ``docker-py`` on PyPi before version 2.0.0. Please avoid installing this really old version, and make sure to not install both ``docker`` and ``docker-py``. Installing both will result in a broken installation. If this happens, Ansible will detect it and inform you about it. If that happens, you must uninstall both and reinstall the correct version. If in doubt, always install ``docker`` and never ``docker-py``.


Connecting to the Docker API
----------------------------

You can connect to a local or remote API using parameters passed to each task or by setting environment variables. The order of precedence is command line parameters and then environment variables. If neither a command line option nor an environment variable is found, Ansible uses the default value  provided under `Parameters`_.


Parameters
..........

Most plugins and modules can be configured by the following parameters:

    docker_host
        The URL or Unix socket path used to connect to the Docker API. Defaults to ``unix:///var/run/docker.sock``. To connect to a remote host, provide the TCP connection string (for example: ``tcp://192.0.2.23:2376``). If TLS is used to encrypt the connection to the API, then the module will automatically replace ``tcp`` in the connection URL with ``https``.

    api_version
        The version of the Docker API running on the Docker Host. Defaults to the latest version of the API supported by the Docker SDK for Python installed.

    timeout
        The maximum amount of time in seconds to wait on a response from the API. Defaults to 60 seconds.

    tls
        Secure the connection to the API by using TLS without verifying the authenticity of the Docker host server. Defaults to ``false``.

    validate_certs
        Secure the connection to the API by using TLS and verifying the authenticity of the Docker host server. Default is ``false``.

    ca_path
        Use a CA certificate when performing server verification by providing the path to a CA certificate file.

    cert_path
        Path to the client's TLS certificate file.

    key_path
        Path to the client's TLS key file.

    tls_hostname
        When verifying the authenticity of the Docker Host server, provide the expected name of the server. Defaults to ``localhost``.

    ssl_version
        Provide a valid SSL version number. The default value is determined by the Docker SDK for Python.

        This option is not available for the CLI based plugins. It is mainly needed for legacy systems and should be avoided.


Module default group
....................

To avoid having to specify common parameters for all the modules in every task, you can use the ``community.docker.docker`` :ref:`module defaults group <module_defaults_groups>`, or its short name ``docker``.

.. note::

  Module default groups only work for modules, not for plugins (connection and inventory plugins).

The following example shows how the module default group can be used in a playbook:

.. code-block:: yaml+jinja

    ---
    - name: Pull and image and start the container
      hosts: localhost
      gather_facts: false
      module_defaults:
        group/community.docker.docker:
          # Select Docker Daemon on other host
          docker_host: tcp://192.0.2.23:2376
          # Configure TLS
          tls: true
          validate_certs: true
          tls_hostname: docker.example.com
          ca_path: /path/to/cacert.pem
          # Increase timeout
          timeout: 120
      tasks:
        - name: Pull image
          community.docker.docker_image_pull:
            name: python
            tag: 3.12

        - name: Start container
          community.docker.docker_container:
            cleanup: true
            command: python --version
            detach: false
            image: python:3.12
            name: my-python-container
            output_logs: true

        - name: Show output
          ansible.builtin.debug:
            msg: "{{ output.container.Output }}"

Here the two ``community.docker`` tasks will use the options set for the module defaults group.


Environment variables
.....................

You can also control how the plugins and modules connect to the Docker API by setting the following environment variables.

For plugins, they have to be set for the environment Ansible itself runs in. For modules, they have to be set for the environment the modules are executed in. For modules running on remote machines, the environment variables have to be set on that machine for the user used to execute the modules with.

.. envvar:: DOCKER_HOST

    The URL or Unix socket path used to connect to the Docker API.

.. envvar:: DOCKER_API_VERSION

    The version of the Docker API running on the Docker Host. Defaults to the latest version of the API supported
    by Docker SDK for Python.

.. envvar:: DOCKER_TIMEOUT

    The maximum amount of time in seconds to wait on a response from the API.

.. envvar:: DOCKER_CERT_PATH

    Path to the directory containing the client certificate, client key and CA certificate.

.. envvar:: DOCKER_SSL_VERSION

    Provide a valid SSL version number.

.. envvar:: DOCKER_TLS

    Secure the connection to the API by using TLS without verifying the authenticity of the Docker Host.

.. envvar:: DOCKER_TLS_HOSTNAME

    When verifying the authenticity of the Docker Host, uses this hostname to compare to the host's certificate.

.. envvar:: DOCKER_TLS_VERIFY

    Secure the connection to the API by using TLS and verify the authenticity of the Docker Host.


Plain Docker daemon: images, networks, volumes, and containers
--------------------------------------------------------------

For working with a plain Docker daemon, that is without Swarm, there are connection plugins, an inventory plugin, and several modules available:

    docker connection plugin
        The :ansplugin:`community.docker.docker connection plugin <community.docker.docker#connection>` uses the Docker CLI utility to connect to Docker containers and execute modules in them. It essentially wraps ``docker exec`` and ``docker cp``. This connection plugin is supported by the :ansplugin:`ansible.posix.synchronize module <ansible.posix.synchronize#module>`.

    docker_api connection plugin
        The :ansplugin:`community.docker.docker_api connection plugin <community.docker.docker_api#connection>` talks directly to the Docker daemon to connect to Docker containers and execute modules in them.

    docker_containers inventory plugin
        The :ansplugin:`community.docker.docker_containers inventory plugin <community.docker.docker_containers#inventory>` allows you to dynamically add Docker containers from a Docker Daemon to your Ansible inventory. See :ref:`dynamic_inventory` for details on dynamic inventories.

        The `docker inventory script <https://github.com/ansible-community/contrib-scripts/blob/main/inventory/docker.py>`_ is deprecated. Please use the inventory plugin instead. The inventory plugin has several compatibility options. If you need to collect Docker containers from multiple Docker daemons, you need to add every Docker daemon as an individual inventory source.

    docker_host_info module
        The :ansplugin:`community.docker.docker_host_info module <community.docker.docker_host_info#module>` allows you to retrieve information on a Docker daemon, such as all containers, images, volumes, networks and so on.

    docker_login module
        The :ansplugin:`community.docker.docker_login module <community.docker.docker_login#module>` allows you to log in and out of a remote registry, such as Docker Hub or a private registry. It provides similar functionality to the ``docker login`` and ``docker logout`` CLI commands.

    docker_prune module
        The :ansplugin:`community.docker.docker_prune module <community.docker.docker_prune#module>` allows  you to prune no longer needed containers, images, volumes and so on. It provides similar functionality to the ``docker prune`` CLI command.

    docker_image module
        The :ansplugin:`community.docker.docker_image module <community.docker.docker_image#module>` provides full control over images, including: build, pull, push, tag and remove.

    docker_image_build
        The :ansplugin:`community.docker.docker_image_build module <community.docker.docker_image_build#module>` allows you to build a Docker image using Docker buildx.

    docker_image_export module
        The :ansplugin:`community.docker.docker_image_export module <community.docker.docker_image_export#module>` allows you to export (archive) images.

    docker_image_info module
        The :ansplugin:`community.docker.docker_image_info module <community.docker.docker_image_info#module>` allows you to list and inspect images.

    docker_image_load
        The :ansplugin:`community.docker.docker_image_load module <community.docker.docker_image_load#module>` allows you to import one or multiple images from tarballs.

    docker_image_pull
        The :ansplugin:`community.docker.docker_image_pull module <community.docker.docker_image_pull#module>` allows you to pull a Docker image from a registry.

    docker_image_push
        The :ansplugin:`community.docker.docker_image_push module <community.docker.docker_image_push#module>` allows you to push a Docker image to a registry.

    docker_image_remove
        The :ansplugin:`community.docker.docker_image_remove module <community.docker.docker_image_remove#module>` allows you to remove and/or untag a Docker image from the Docker daemon.

    docker_image_tag
        The :ansplugin:`community.docker.docker_image_tag module <community.docker.docker_image_tag#module>` allows you to tag a Docker image with additional names and/or tags.

    docker_network module
        The :ansplugin:`community.docker.docker_network module <community.docker.docker_network#module>` provides full control over Docker networks.

    docker_network_info module
        The :ansplugin:`community.docker.docker_network_info module <community.docker.docker_network_info#module>` allows you to inspect Docker networks.

    docker_volume_info module
        The :ansplugin:`community.docker.docker_volume_info module <community.docker.docker_volume_info#module>` provides full control over Docker volumes.

    docker_volume module
        The :ansplugin:`community.docker.docker_volume module <community.docker.docker_volume#module>` allows you to inspect Docker volumes.

    docker_container module
        The :ansplugin:`community.docker.docker_container module <community.docker.docker_container#module>` manages the container lifecycle by providing the ability to create, update, stop, start and destroy a Docker container.

    docker_container_copy_into
        The :ansplugin:`community.docker.docker_container_copy_into module <community.docker.docker_container_copy_into#module>` allows you to copy files from the control node into a container.

    docker_container_exec
        The :ansplugin:`community.docker.docker_container_exec module <community.docker.docker_container_exec#module>` allows you to execute commands in a running container.

    docker_container_info module
        The :ansplugin:`community.docker.docker_container_info module <community.docker.docker_container_info#module>` allows you to inspect a Docker container.

    docker_plugin
        The :ansplugin:`community.docker.docker_plugin module <community.docker.docker_plugin#module>` allows you to manage Docker plugins.


Docker Compose
--------------

Docker Compose v2
.................

There are several modules for working with Docker Compose projects:

    community.docker.docker_compose_v2
        The :ansplugin:`community.docker.docker_compose_v2 module <community.docker.docker_compose_v2#module>` allows you to use your existing Docker Compose files to orchestrate containers on a single Docker daemon or on Swarm.

    community.docker.docker_compose_v2_exec
        The :ansplugin:`community.docker.docker_compose_v2_exec module <community.docker.docker_compose_v2_exec#module>` allows you to run a command in a container of Docker Compose projects.

    community.docker.docker_compose_v2_pull
        The :ansplugin:`community.docker.docker_compose_v2_pull module <community.docker.docker_compose_v2_pull#module>` allows you to pull Docker Compose projects.

    community.docker.docker_compose_v2_run
        The :ansplugin:`community.docker.docker_compose_v2_run module <community.docker.docker_compose_v2_run#module>` allows you to run a command in a new container of a Docker Compose project.

These modules use the Docker CLI "compose" plugin (``docker compose``), and thus needs access to the Docker CLI tool.
No further requirements next to to the CLI tool and its Docker Compose plugin are needed.


Docker Machine
--------------

The :ansplugin:`community.docker.docker_machine inventory plugin <community.docker.docker_machine#inventory>` allows you to dynamically add Docker Machine hosts to your Ansible inventory.


Docker Swarm stack
------------------

The :ansplugin:`community.docker.docker_stack module <community.docker.docker_stack#module>` module allows you to control Docker Swarm stacks. Information on Swarm stacks can be retrieved by the :ansplugin:`community.docker.docker_stack_info module <community.docker.docker_stack_info#module>`, and information on Swarm stack tasks can be retrieved by the :ansplugin:`community.docker.docker_stack_task_info module <community.docker.docker_stack_task_info#module>`.


Docker Swarm
------------

The community.docker collection provides multiple plugins and modules for managing Docker Swarms.

Swarm management
................

One inventory plugin and several modules are provided to manage Docker Swarms:

    docker_swarm inventory plugin
        The :ansplugin:`community.docker.docker_swarm inventory plugin <community.docker.docker_swarm#inventory>` allows  you to dynamically add all Docker Swarm nodes to your Ansible inventory.

    docker_swarm module
        The :ansplugin:`community.docker.docker_swarm module <community.docker.docker_swarm#module>` allows you to globally configure Docker Swarm manager nodes to join and leave swarms, and to change the Docker Swarm configuration.

    docker_swarm_info module
        The :ansplugin:`community.docker.docker_swarm_info module <community.docker.docker_swarm_info#module>` allows  you to retrieve information on Docker Swarm.

    docker_node module
        The :ansplugin:`community.docker.docker_node module <community.docker.docker_node#module>` allows you to manage Docker Swarm nodes.

    docker_node_info module
        The :ansplugin:`community.docker.docker_node_info module <community.docker.docker_node_info#module>` allows you to retrieve information on Docker Swarm nodes.

Configuration management
........................

The community.docker collection offers modules to manage Docker Swarm configurations and secrets:

    docker_config module
        The :ansplugin:`community.docker.docker_config module <community.docker.docker_config#module>` allows you to create and modify Docker Swarm configs.

    docker_secret module
        The :ansplugin:`community.docker.docker_secret module <community.docker.docker_secret#module>` allows you to create and modify Docker Swarm secrets.

Swarm services
..............

Docker Swarm services can be created and updated with the :ansplugin:`community.docker.docker_swarm_service module <community.docker.docker_swarm_service#module>`, and information on them can be queried by the :ansplugin:`community.docker.docker_swarm_service_info module <community.docker.docker_swarm_service_info#module>`.
