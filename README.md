# Docker Community Collection

[![Doc](https://img.shields.io/badge/docs-brightgreen.svg)](https://docs.ansible.com/ansible/latest/collections/community/docker/)
[![Build Status](https://dev.azure.com/ansible/community.docker/_apis/build/status/CI?branchName=main)](https://dev.azure.com/ansible/community.docker/_build?definitionId=25)
[![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/community.docker)](https://codecov.io/gh/ansible-collections/community.docker)

This repo contains the `community.docker` Ansible Collection. The collection includes many modules and plugins to work with Docker.

Please note that this collection does **not** support Windows targets. The connection plugins included in this collection support Windows targets on a best-effort basis, but we are not testing this in CI.

## Tested with Ansible

Tested with the current Ansible 2.9, ansible-base 2.10, ansible-core 2.11 and ansible-core 2.12 releases and the current development version of ansible-core. Ansible versions before 2.9.10 are not supported.

## External requirements

Most modules and plugins require the [Docker SDK for Python](https://pypi.org/project/docker/). For Python 2.6 support, use [the deprecated docker-py library](https://pypi.org/project/docker-py/) instead.

Both libraries cannot be installed at the same time. If you accidentally did install them simultaneously, you have to uninstall *both* before re-installing one of them.

## Included content

* Connection plugins:
  - community.docker.docker: use Docker containers as remotes
* Inventory plugins:
  - community.docker.docker_machine: collect Docker machines as inventory
  - community.docker.docker_swarm: collect Docker Swarm nodes as inventory
* Modules:
  * Docker:
    - community.docker.docker_container: manage Docker containers
    - community.docker.docker_container_exec: run commands in Docker containers
    - community.docker.docker_container_info: retrieve information on Docker containers
    - community.docker.docker_host_info: retrieve information on the Docker daemon
    - community.docker.docker_image: manage Docker images
    - community.docker.docker_image_info: retrieve information on Docker images
    - community.docker.docker_image_load: load Docker images from archives
    - community.docker.docker_login: log in and out to/from registries
    - community.docker.docker_network: manage Docker networks
    - community.docker.docker_network_info: retrieve information on Docker networks
    - community.docker.docker_plugin: manage Docker plugins
    - community.docker.docker_prune: prune Docker containers, images, networks, volumes, and build data
    - community.docker.docker_volume: manage Docker volumes
    - community.docker.docker_volume_info: retrieve information on Docker volumes
  * Docker Compose:
    - community.docker.docker_compose: manage Docker Compose files
  * Docker Swarm:
    - community.docker.docker_config: manage configurations
    - community.docker.docker_node: manage Docker Swarm nodes
    - community.docker.docker_node_info: retrieve information on Docker Swarm nodes
    - community.docker.docker_secret: manage secrets
    - community.docker.docker_swarm: manage Docker Swarm
    - community.docker.docker_swarm_info: retrieve information on Docker Swarm
    - community.docker.docker_swarm_service: manage Docker Swarm services
    - community.docker.docker_swarm_service_info: retrieve information on Docker Swarm services
  * Docker Stack:
    - community.docker.docker_stack: manage Docker Stacks
    - community.docker.docker_stack_info: retrieve information on Docker Stacks
    - community.docker.docker_stack_task_info: retrieve information on tasks in Docker Stacks
  * Other:
    - current_container_facts: return facts about whether the module runs in a Docker container

## Using this collection

Before using the General community collection, you need to install the collection with the `ansible-galaxy` CLI:

    ansible-galaxy collection install community.docker

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml` using the format:

```yaml
collections:
- name: community.docker
```

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Contributing to this collection

If you want to develop new content for this collection or improve what is already here, the easiest way to work on the collection is to clone it into one of the configured [`COLLECTIONS_PATH`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#collections-paths), and work on it there.

You can find more information in the [developer guide for collections](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections), and in the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html).

## Release notes

See the [changelog](https://github.com/ansible-collections/community.docker/tree/main/CHANGELOG.rst).

## More information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Collections Checklist](https://github.com/ansible-collections/overview/blob/master/collection_requirements.rst)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)
- [The Bullhorn (the Ansible Contributor newsletter)](https://us19.campaign-archive.com/home/?u=56d874e027110e35dea0e03c1&id=d6635f5420)
- [Changes impacting Contributors](https://github.com/ansible-collections/overview/issues/45)

## Licensing

GNU General Public License v3.0 or later.

See [COPYING](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
