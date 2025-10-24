#!/usr/bin/python
#
# Copyright (c) 2019 Hannes Ljungberg <hannes.ljungberg@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations


DOCUMENTATION = r"""
module: docker_swarm_service_info

short_description: Retrieves information about docker services from a Swarm Manager

description:
  - Retrieves information about a docker service.
  - Essentially returns the output of C(docker service inspect <name>).
  - Must be executed on a host running as Swarm Manager, otherwise the module will fail.
extends_documentation_fragment:
  - community.docker._docker
  - community.docker._docker.docker_py_2_documentation
  - community.docker._attributes
  - community.docker._attributes.actiongroup_docker
  - community.docker._attributes.info_module
  - community.docker._attributes.idempotent_not_modify_state

options:
  name:
    description:
      - The name of the service to inspect.
    type: str
    required: true

author:
  - Hannes Ljungberg (@hannseman)

requirements:
  - "L(Docker SDK for Python,https://docker-py.readthedocs.io/en/stable/) >= 2.0.0"
  - "Docker API >= 1.25"
"""

EXAMPLES = r"""
---
- name: Get info from a service
  community.docker.docker_swarm_service_info:
    name: myservice
  register: result
"""

RETURN = r"""
exists:
  description:
    - Returns whether the service exists.
  type: bool
  returned: always
  sample: true
service:
  description:
    - A dictionary representing the current state of the service. Matches the C(docker service inspect) output.
    - Will be V(none) if service does not exist.
  returned: always
  type: dict
"""

import traceback
import typing as t


try:
    from docker.errors import DockerException
except ImportError:
    # missing Docker SDK for Python handled in ansible.module_utils.docker.common
    pass

from ansible_collections.community.docker.plugins.module_utils._common import (
    RequestException,
)
from ansible_collections.community.docker.plugins.module_utils._swarm import (
    AnsibleDockerSwarmClient,
)


def get_service_info(client: AnsibleDockerSwarmClient) -> dict[str, t.Any] | None:
    service = client.module.params["name"]
    return client.get_service_inspect(service_id=service, skip_missing=True)


def main() -> None:
    argument_spec = {
        "name": {"type": "str", "required": True},
    }

    client = AnsibleDockerSwarmClient(
        argument_spec=argument_spec,
        supports_check_mode=True,
        min_docker_version="2.0.0",
    )

    client.fail_task_if_not_swarm_manager()

    try:
        service = get_service_info(client)

        client.module.exit_json(changed=False, service=service, exists=bool(service))
    except DockerException as e:
        client.fail(
            f"An unexpected Docker error occurred: {e}",
            exception=traceback.format_exc(),
        )
    except RequestException as e:
        client.fail(
            f"An unexpected requests error occurred when Docker SDK for Python tried to talk to the docker daemon: {e}",
            exception=traceback.format_exc(),
        )


if __name__ == "__main__":
    main()
