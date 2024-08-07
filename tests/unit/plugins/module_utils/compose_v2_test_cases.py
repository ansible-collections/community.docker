# Copyright 2022 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.community.docker.plugins.module_utils.compose_v2 import (
    Event,
)


EVENT_TEST_CASES = [
    # #######################################################################################################################
    # ## Docker Compose 2.18.1 ##############################################################################################
    # #######################################################################################################################
    # docker_compose_v2: "Absent" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Absent" on 2024-01-13 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-absent',
        '2.18.1',
        False,
        False,
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopping\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopped\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Removing\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Removed\n'
        ' Network ansible-docker-test-01234567-start-stop_default  Removing\n'
        ' Network ansible-docker-test-01234567-start-stop_default  Removed\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopping',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopped',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Removing',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Removed',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Removing',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent (check)" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Absent (check)" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-absent-(check)',
        '2.18.1',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopped\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Removing\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Removed\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Removing\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Resource is still in use\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopping',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopped',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Removing',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Removed',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Removing',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                None,
                'Resource is still in use',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-cleanup',
        '2.18.1',
        False,
        False,
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Stopping\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Stopped\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Removing\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Removed\n'
        ' Network ansible-docker-test-01234567-pull_default  Removing\n'
        ' Network ansible-docker-test-01234567-pull_default  Removed\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Stopping',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Stopped',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Removing',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Removed',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Removing',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Present" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present',
        '2.18.1',
        False,
        False,
        ' ansible-docker-test-01234567-container Pulling \n'
        ' ansible-docker-test-01234567-container Pulled \n'
        ' Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-container',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-container',
                'Pulled',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-13-docker_compose_v2-present-(changed-check)',
        '2.18.1',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 80c52c26780_ansible-docker-test-7c5458ac-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 80c52c26780_ansible-docker-test-7c5458ac-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '80c52c26780_ansible-docker-test-7c5458ac-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '80c52c26780_ansible-docker-test-7c5458ac-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-(changed-check)',
        '2.18.1',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 9121995872d_ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 9121995872d_ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '9121995872d_ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '9121995872d_ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed)" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Present (changed)" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-(changed)',
        '2.18.1',
        False,
        False,
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-13-docker_compose_v2-present-(check)',
        '2.18.1',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-container Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-container Pulled \n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-7c5458ac-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-7c5458ac-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-container',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-container',
                'Pulled',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-7c5458ac-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-7c5458ac-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-(check)',
        '2.18.1',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-container Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-container Pulled \n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-dba91fb6-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-dba91fb6-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-container',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-container',
                'Pulled',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-dba91fb6-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-dba91fb6-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Present (idempotent check)" on 2024-01-13 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-(idempotent-check)',
        '2.18.1',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Running\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent)" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Present (idempotent)" on 2024-01-13 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-(idempotent)',
        '2.18.1',
        False,
        False,
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Running\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Present stopped" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-stopped',
        '2.18.1',
        False,
        False,
        ' Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped (check)" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Present stopped (check)" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-stopped-(check)',
        '2.18.1',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Present with pull=always" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-with-pull=always',
        '2.18.1',
        False,
        False,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' ansible-docker-test-01234567-cont Pulled \n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Running\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-with-pull=always-(check)',
        '2.18.1',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container 002a15404ac_ansible-docker-test-dba91fb6-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container 002a15404ac_ansible-docker-test-dba91fb6-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '002a15404ac_ansible-docker-test-dba91fb6-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '002a15404ac_ansible-docker-test-dba91fb6-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-13-docker_compose_v2-present-with-pull=always-(check)',
        '2.18.1',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container ec060c7b341_ansible-docker-test-7c5458ac-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container ec060c7b341_ansible-docker-test-7c5458ac-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'ec060c7b341_ansible-docker-test-7c5458ac-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'ec060c7b341_ansible-docker-test-7c5458ac-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Present with pull=missing" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-with-pull=missing',
        '2.18.1',
        False,
        False,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' ansible-docker-test-01234567-cont Pulled \n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-13-docker_compose_v2-present-with-pull=missing-(check)',
        '2.18.1',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-7c5458ac-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-7c5458ac-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-7c5458ac-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-7c5458ac-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-with-pull=missing-(check)',
        '2.18.1',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-dba91fb6-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-dba91fb6-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-dba91fb6-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-dba91fb6-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-13 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent)',
        '2.18.1',
        False,
        False,
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Running\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-13 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent,-check)',
        '2.18.1',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Running\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.18.1',
        False,
        False,
        ' Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' Network ansible-docker-test-01234567-pull_default  Created\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.18.1',
        False,
        True,
        ' Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' Network ansible-docker-test-01234567-pull_default  Created\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        'Error response from daemon: No such image: does-not-exist:latest\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'unknown',
                '',
                'Error',
                'Error response from daemon: No such image: does-not-exist:latest',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-13-docker_compose_v2-present-with-pull=never-(check)',
        '2.18.1',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-7c5458ac-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-7c5458ac-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-7c5458ac-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-7c5458ac-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.18.1',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-dba91fb6-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-dba91fb6-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-dba91fb6-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-dba91fb6-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Present without explicit pull" on 2024-01-13 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2_pull: "Pull" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-without-explicit-pull',
        '2.18.1',
        False,
        True,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' ansible-docker-test-01234567-cont Error \n'
        "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied\n",  # noqa: E501
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'unknown',
                'ansible-docker-test-01234567-cont',
                'Error',
                "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied",  # noqa: E501
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Present without explicit pull (check)" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-without-explicit-pull-(check)',
        '2.18.1',
        True,
        True,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Error \n'
        'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'unknown',
                'ansible-docker-test-01234567-cont',
                'Error',
                'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-restarted',
        '2.18.1',
        False,
        False,
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Restarting\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Restarting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.18.1',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Restarting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Started" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-started',
        '2.18.1',
        False,
        False,
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (check)" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Started (check)" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-started-(check)',
        '2.18.1',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Stopped" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-stopped',
        '2.18.1',
        False,
        False,
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Running\n'
        '\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopping\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopped\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Running',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopping',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped (check)" on 2024-01-07 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2: "Stopped (check)" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-stopped-(check)',
        '2.18.1',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Running\n'
        '\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopped\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Running',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopping',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2_pull: "Pull (check)" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-13-docker_compose_v2_pull-pull-(check)',
        '2.18.1',
        True,
        True,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Error \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont  - Pull error for image: does-not-exist:latest \n'
        'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'unknown',
                'ansible-docker-test-01234567-cont',
                'Error',
                'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed',
            ),
        ],
        [],
    ),
    # docker_compose_v2_pull: "Pull with policy=always" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-13-docker_compose_v2_pull-pull-with-policy=always',
        '2.18.1',
        False,
        False,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' 486039affc0a Pulling fs layer \n'
        ' 486039affc0a Downloading [>                                                  ]  32.16kB/2.207MB\n'
        ' 486039affc0a Verifying Checksum \n'
        ' 486039affc0a Download complete \n'
        ' 486039affc0a Extracting [>                                                  ]  32.77kB/2.207MB\n'
        ' 486039affc0a Extracting [==================================================>]  2.207MB/2.207MB\n'
        ' 486039affc0a Pull complete \n'
        ' ansible-docker-test-01234567-cont Pulled \n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pulling fs layer',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Downloading',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Verifying Checksum',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Download complete',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pull complete',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2_pull: "Pull with policy=always (again)" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-13-docker_compose_v2_pull-pull-with-policy=always-(again)',
        '2.18.1',
        False,
        False,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' ansible-docker-test-01234567-cont Pulled \n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2_pull: "Pull with policy=always (again, check)" on 2024-01-13 in 2.12-ubuntu1804
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (check)" on 2024-01-13 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-13-docker_compose_v2_pull-pull-with-policy=always-(again,-check)',
        '2.18.1',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
        ],
        [],
    ),
    # #######################################################################################################################
    # ## Docker Compose 2.21.0 ##############################################################################################
    # #######################################################################################################################
    # docker_compose_v2: "Absent" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Absent" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Absent" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Absent" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Absent" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Absent" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Absent" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Absent" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Absent" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Absent" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Absent" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Absent" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Absent" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Absent" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Absent" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Absent" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Absent" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Absent" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Absent" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Absent" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Absent" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Absent" on 2024-01-13 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-absent',
        '2.21.0',
        False,
        False,
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopping\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopped\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Removing\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Removed\n'
        ' Network ansible-docker-test-01234567-start-stop_default  Removing\n'
        ' Network ansible-docker-test-01234567-start-stop_default  Removed\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopping',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopped',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Removing',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Removed',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Removing',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent (check)" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Absent (check)" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Absent (check)" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Absent (check)" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Absent (check)" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Absent (check)" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Absent (check)" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Absent (check)" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Absent (check)" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Absent (check)" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Absent (check)" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Absent (check)" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Absent (check)" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Absent (check)" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Absent (check)" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Absent (check)" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Absent (check)" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Absent (check)" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Absent (check)" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Absent (check)" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Absent (check)" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Absent (check)" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-absent-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopped\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Removing\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Removed\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Removing\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Resource is still in use\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopping',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopped',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Removing',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Removed',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Removing',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                None,
                'Resource is still in use',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-cleanup',
        '2.21.0',
        False,
        False,
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Stopping\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Stopped\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Removing\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Removed\n'
        ' Network ansible-docker-test-01234567-pull_default  Removing\n'
        ' Network ansible-docker-test-01234567-pull_default  Removed\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Stopping',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Stopped',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Removing',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Removed',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Removing',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Present" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present',
        '2.21.0',
        False,
        False,
        ' Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-13 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-13-docker_compose_v2-present-(changed-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 054e03eb5ea_ansible-docker-test-b2745d99-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 054e03eb5ea_ansible-docker-test-b2745d99-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '054e03eb5ea_ansible-docker-test-b2745d99-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '054e03eb5ea_ansible-docker-test-b2745d99-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-present-(changed-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 0a77f424a61_ansible-docker-test-d1d30700-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 0a77f424a61_ansible-docker-test-d1d30700-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '0a77f424a61_ansible-docker-test-d1d30700-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '0a77f424a61_ansible-docker-test-d1d30700-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-13 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-13-docker_compose_v2-present-(changed-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 0e165a36533_ansible-docker-test-e700ac20-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 0e165a36533_ansible-docker-test-e700ac20-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '0e165a36533_ansible-docker-test-e700ac20-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '0e165a36533_ansible-docker-test-e700ac20-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-present-(changed-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 26bf8ff1675_ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 26bf8ff1675_ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '26bf8ff1675_ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '26bf8ff1675_ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-13 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-13-docker_compose_v2-present-(changed-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 27c209a84a5_ansible-docker-test-d616c3a5-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 27c209a84a5_ansible-docker-test-d616c3a5-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '27c209a84a5_ansible-docker-test-d616c3a5-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '27c209a84a5_ansible-docker-test-d616c3a5-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-present-(changed-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 4b568108657_ansible-docker-test-64d917f4-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 4b568108657_ansible-docker-test-64d917f4-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '4b568108657_ansible-docker-test-64d917f4-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '4b568108657_ansible-docker-test-64d917f4-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-present-(changed-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 6dc8d091c94_ansible-docker-test-2460e737-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 6dc8d091c94_ansible-docker-test-2460e737-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '6dc8d091c94_ansible-docker-test-2460e737-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '6dc8d091c94_ansible-docker-test-2460e737-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-(changed-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 71b893893dc_ansible-docker-test-4baa7139-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 71b893893dc_ansible-docker-test-4baa7139-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '71b893893dc_ansible-docker-test-4baa7139-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '71b893893dc_ansible-docker-test-4baa7139-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-present-(changed-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 71e7a319c23_ansible-docker-test-19ffba88-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 71e7a319c23_ansible-docker-test-19ffba88-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '71e7a319c23_ansible-docker-test-19ffba88-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '71e7a319c23_ansible-docker-test-19ffba88-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-present-(changed-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 78e827e6673_ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 78e827e6673_ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '78e827e6673_ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '78e827e6673_ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-13 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-13-docker_compose_v2-present-(changed-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 7971b0c189d_ansible-docker-test-51914faa-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 7971b0c189d_ansible-docker-test-51914faa-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '7971b0c189d_ansible-docker-test-51914faa-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '7971b0c189d_ansible-docker-test-51914faa-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-13 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-13-docker_compose_v2-present-(changed-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 7b8d91093c9_ansible-docker-test-d2caf0c9-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 7b8d91093c9_ansible-docker-test-d2caf0c9-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '7b8d91093c9_ansible-docker-test-d2caf0c9-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '7b8d91093c9_ansible-docker-test-d2caf0c9-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-13 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-13-docker_compose_v2-present-(changed-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 7bedd9b4513_ansible-docker-test-1ba2643a-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 7bedd9b4513_ansible-docker-test-1ba2643a-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '7bedd9b4513_ansible-docker-test-1ba2643a-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '7bedd9b4513_ansible-docker-test-1ba2643a-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-13 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-13-docker_compose_v2-present-(changed-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 87873e68934_ansible-docker-test-ad622acd-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 87873e68934_ansible-docker-test-ad622acd-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '87873e68934_ansible-docker-test-ad622acd-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '87873e68934_ansible-docker-test-ad622acd-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-13 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-13-docker_compose_v2-present-(changed-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container a81dce9774b_ansible-docker-test-4fcbaf1e-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container a81dce9774b_ansible-docker-test-4fcbaf1e-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'a81dce9774b_ansible-docker-test-4fcbaf1e-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'a81dce9774b_ansible-docker-test-4fcbaf1e-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-13 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-13-docker_compose_v2-present-(changed-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container d28b7978587_ansible-docker-test-971ad57c-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container d28b7978587_ansible-docker-test-971ad57c-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'd28b7978587_ansible-docker-test-971ad57c-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'd28b7978587_ansible-docker-test-971ad57c-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-present-(changed-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container dea4aafe907_ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container dea4aafe907_ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'dea4aafe907_ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'dea4aafe907_ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present-(changed-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container e508faa8323_ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container e508faa8323_ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'e508faa8323_ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'e508faa8323_ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-13-docker_compose_v2-present-(changed-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container ef57cb7913f_ansible-docker-test-ede01681-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container ef57cb7913f_ansible-docker-test-ede01681-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'ef57cb7913f_ansible-docker-test-ede01681-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'ef57cb7913f_ansible-docker-test-ede01681-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-present-(changed-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container efe8857a191_ansible-docker-test-601188b1-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container efe8857a191_ansible-docker-test-601188b1-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'efe8857a191_ansible-docker-test-601188b1-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'efe8857a191_ansible-docker-test-601188b1-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-13 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-13-docker_compose_v2-present-(changed-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container f0de40ba686_ansible-docker-test-834c1a9b-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container f0de40ba686_ansible-docker-test-834c1a9b-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'f0de40ba686_ansible-docker-test-834c1a9b-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'f0de40ba686_ansible-docker-test-834c1a9b-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-present-(changed-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container f6416652e13_ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container f6416652e13_ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'f6416652e13_ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'f6416652e13_ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed)" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present (changed)" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present (changed)" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present (changed)" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present (changed)" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present (changed)" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present (changed)" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present (changed)" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present (changed)" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present (changed)" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present (changed)" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present (changed)" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present (changed)" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present (changed)" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present (changed)" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present (changed)" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present (changed)" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present (changed)" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present (changed)" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present (changed)" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present (changed)" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Present (changed)" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-(changed)',
        '2.21.0',
        False,
        False,
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-present-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-19ffba88-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-19ffba88-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-19ffba88-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-19ffba88-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-13 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-13-docker_compose_v2-present-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-1ba2643a-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-1ba2643a-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-1ba2643a-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-1ba2643a-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-present-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-1f1d0d58-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-1f1d0d58-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-1f1d0d58-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-1f1d0d58-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-present-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-2460e737-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-2460e737-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-2460e737-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-2460e737-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-4baa7139-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-4baa7139-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-4baa7139-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-4baa7139-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-13 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-13-docker_compose_v2-present-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-4fcbaf1e-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-4fcbaf1e-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-4fcbaf1e-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-4fcbaf1e-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-13 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-13-docker_compose_v2-present-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-51914faa-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-51914faa-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-51914faa-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-51914faa-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-present-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-5f3d2e16-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-5f3d2e16-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-5f3d2e16-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-5f3d2e16-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-present-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-601188b1-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-601188b1-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-601188b1-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-601188b1-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-present-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-64d917f4-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-64d917f4-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-64d917f4-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-64d917f4-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-present-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-6aaaa304-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-6aaaa304-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-6aaaa304-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-6aaaa304-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-13 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-13-docker_compose_v2-present-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-834c1a9b-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-834c1a9b-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-834c1a9b-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-834c1a9b-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-13 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-13-docker_compose_v2-present-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-971ad57c-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-971ad57c-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-971ad57c-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-971ad57c-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-13 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-13-docker_compose_v2-present-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ad622acd-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ad622acd-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-ad622acd-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-ad622acd-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-13 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-13-docker_compose_v2-present-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-b2745d99-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-b2745d99-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-b2745d99-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-b2745d99-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-present-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d1d30700-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d1d30700-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d1d30700-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d1d30700-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-13 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-13-docker_compose_v2-present-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d2caf0c9-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d2caf0c9-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d2caf0c9-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d2caf0c9-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-13 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-13-docker_compose_v2-present-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d616c3a5-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d616c3a5-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d616c3a5-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d616c3a5-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-present-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d6ae094c-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d6ae094c-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d6ae094c-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d6ae094c-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-13 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-13-docker_compose_v2-present-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-e700ac20-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-e700ac20-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-e700ac20-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-e700ac20-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-13-docker_compose_v2-present-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ede01681-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ede01681-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-ede01681-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-ede01681-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present (idempotent check)" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present (idempotent check)" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present (idempotent check)" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present (idempotent check)" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present (idempotent check)" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present (idempotent check)" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present (idempotent check)" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present (idempotent check)" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present (idempotent check)" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present (idempotent check)" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Present (idempotent check)" on 2024-01-13 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-(idempotent-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Running\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent)" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present (idempotent)" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present (idempotent)" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present (idempotent)" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present (idempotent)" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present (idempotent)" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present (idempotent)" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present (idempotent)" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present (idempotent)" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present (idempotent)" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present (idempotent)" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present (idempotent)" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present (idempotent)" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present (idempotent)" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present (idempotent)" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present (idempotent)" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present (idempotent)" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present (idempotent)" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present (idempotent)" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present (idempotent)" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present (idempotent)" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Present (idempotent)" on 2024-01-13 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-(idempotent)',
        '2.21.0',
        False,
        False,
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Running\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present stopped" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present stopped" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present stopped" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present stopped" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present stopped" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present stopped" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present stopped" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present stopped" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present stopped" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present stopped" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present stopped" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present stopped" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present stopped" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present stopped" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present stopped" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present stopped" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present stopped" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present stopped" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present stopped" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present stopped" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Present stopped" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-stopped',
        '2.21.0',
        False,
        False,
        ' Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped (check)" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present stopped (check)" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present stopped (check)" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present stopped (check)" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present stopped (check)" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present stopped (check)" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present stopped (check)" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present stopped (check)" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present stopped (check)" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present stopped (check)" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present stopped (check)" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present stopped (check)" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present stopped (check)" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present stopped (check)" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present stopped (check)" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present stopped (check)" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present stopped (check)" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present stopped (check)" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present stopped (check)" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present stopped (check)" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present stopped (check)" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Present stopped (check)" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-stopped-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present with pull=always" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present with pull=always" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=always" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=always" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present with pull=always" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present with pull=always" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present with pull=always" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present with pull=always" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=always" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=always" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present with pull=always" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present with pull=always" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present with pull=always" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present with pull=always" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present with pull=always" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present with pull=always" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present with pull=always" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present with pull=always" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present with pull=always" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present with pull=always" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Present with pull=always" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-with-pull=always',
        '2.21.0',
        False,
        False,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' ansible-docker-test-01234567-cont Pulled \n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Running\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-13 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-13-docker_compose_v2-present-with-pull=always-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container 0b4286904e0_ansible-docker-test-51914faa-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container 0b4286904e0_ansible-docker-test-51914faa-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '0b4286904e0_ansible-docker-test-51914faa-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '0b4286904e0_ansible-docker-test-51914faa-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-present-with-pull=always-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container 0d5362bac93_ansible-docker-test-1f1d0d58-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container 0d5362bac93_ansible-docker-test-1f1d0d58-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '0d5362bac93_ansible-docker-test-1f1d0d58-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '0d5362bac93_ansible-docker-test-1f1d0d58-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-present-with-pull=always-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container 3d7b7be6dbe_ansible-docker-test-d1d30700-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container 3d7b7be6dbe_ansible-docker-test-d1d30700-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '3d7b7be6dbe_ansible-docker-test-d1d30700-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '3d7b7be6dbe_ansible-docker-test-d1d30700-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-13 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-13-docker_compose_v2-present-with-pull=always-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container 49ff7fef052_ansible-docker-test-1ba2643a-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container 49ff7fef052_ansible-docker-test-1ba2643a-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '49ff7fef052_ansible-docker-test-1ba2643a-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '49ff7fef052_ansible-docker-test-1ba2643a-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-present-with-pull=always-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container 5d30320650e_ansible-docker-test-6aaaa304-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container 5d30320650e_ansible-docker-test-6aaaa304-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '5d30320650e_ansible-docker-test-6aaaa304-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '5d30320650e_ansible-docker-test-6aaaa304-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-present-with-pull=always-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container 611a044106b_ansible-docker-test-601188b1-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container 611a044106b_ansible-docker-test-601188b1-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '611a044106b_ansible-docker-test-601188b1-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '611a044106b_ansible-docker-test-601188b1-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-13 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-13-docker_compose_v2-present-with-pull=always-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container 61802a08aa6_ansible-docker-test-e700ac20-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container 61802a08aa6_ansible-docker-test-e700ac20-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '61802a08aa6_ansible-docker-test-e700ac20-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '61802a08aa6_ansible-docker-test-e700ac20-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present-with-pull=always-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container 61bd1b13d9c_ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container 61bd1b13d9c_ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '61bd1b13d9c_ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '61bd1b13d9c_ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-13 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-13-docker_compose_v2-present-with-pull=always-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container 769aec9cd4d_ansible-docker-test-d2caf0c9-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container 769aec9cd4d_ansible-docker-test-d2caf0c9-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '769aec9cd4d_ansible-docker-test-d2caf0c9-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '769aec9cd4d_ansible-docker-test-d2caf0c9-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-13-docker_compose_v2-present-with-pull=always-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container 813ca227a6f_ansible-docker-test-ede01681-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container 813ca227a6f_ansible-docker-test-ede01681-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '813ca227a6f_ansible-docker-test-ede01681-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '813ca227a6f_ansible-docker-test-ede01681-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-13 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-13-docker_compose_v2-present-with-pull=always-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container 8a586ed91d6_ansible-docker-test-834c1a9b-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container 8a586ed91d6_ansible-docker-test-834c1a9b-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '8a586ed91d6_ansible-docker-test-834c1a9b-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '8a586ed91d6_ansible-docker-test-834c1a9b-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-present-with-pull=always-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container 8bec416e98d_ansible-docker-test-64d917f4-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container 8bec416e98d_ansible-docker-test-64d917f4-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '8bec416e98d_ansible-docker-test-64d917f4-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '8bec416e98d_ansible-docker-test-64d917f4-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-13 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-13-docker_compose_v2-present-with-pull=always-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container 906450ba6e7_ansible-docker-test-b2745d99-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container 906450ba6e7_ansible-docker-test-b2745d99-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '906450ba6e7_ansible-docker-test-b2745d99-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '906450ba6e7_ansible-docker-test-b2745d99-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-13 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-13-docker_compose_v2-present-with-pull=always-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container a99ed30c7d6_ansible-docker-test-d616c3a5-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container a99ed30c7d6_ansible-docker-test-d616c3a5-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'a99ed30c7d6_ansible-docker-test-d616c3a5-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'a99ed30c7d6_ansible-docker-test-d616c3a5-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-present-with-pull=always-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container b78faf8a742_ansible-docker-test-d6ae094c-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container b78faf8a742_ansible-docker-test-d6ae094c-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'b78faf8a742_ansible-docker-test-d6ae094c-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'b78faf8a742_ansible-docker-test-d6ae094c-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-13 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-13-docker_compose_v2-present-with-pull=always-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container be1b2a9ca28_ansible-docker-test-971ad57c-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container be1b2a9ca28_ansible-docker-test-971ad57c-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'be1b2a9ca28_ansible-docker-test-971ad57c-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'be1b2a9ca28_ansible-docker-test-971ad57c-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-present-with-pull=always-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container c9d730c2613_ansible-docker-test-5f3d2e16-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container c9d730c2613_ansible-docker-test-5f3d2e16-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'c9d730c2613_ansible-docker-test-5f3d2e16-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'c9d730c2613_ansible-docker-test-5f3d2e16-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-13 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-13-docker_compose_v2-present-with-pull=always-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container da16aa68f6f_ansible-docker-test-ad622acd-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container da16aa68f6f_ansible-docker-test-ad622acd-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'da16aa68f6f_ansible-docker-test-ad622acd-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'da16aa68f6f_ansible-docker-test-ad622acd-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-13 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-13-docker_compose_v2-present-with-pull=always-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container dff4b309c58_ansible-docker-test-4fcbaf1e-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container dff4b309c58_ansible-docker-test-4fcbaf1e-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'dff4b309c58_ansible-docker-test-4fcbaf1e-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'dff4b309c58_ansible-docker-test-4fcbaf1e-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-with-pull=always-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container ecd243ea972_ansible-docker-test-4baa7139-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container ecd243ea972_ansible-docker-test-4baa7139-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'ecd243ea972_ansible-docker-test-4baa7139-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'ecd243ea972_ansible-docker-test-4baa7139-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-present-with-pull=always-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container f48d54a75fb_ansible-docker-test-2460e737-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container f48d54a75fb_ansible-docker-test-2460e737-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'f48d54a75fb_ansible-docker-test-2460e737-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'f48d54a75fb_ansible-docker-test-2460e737-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-present-with-pull=always-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container fa8f62dfced_ansible-docker-test-19ffba88-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container fa8f62dfced_ansible-docker-test-19ffba88-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'fa8f62dfced_ansible-docker-test-19ffba88-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'fa8f62dfced_ansible-docker-test-19ffba88-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present with pull=missing" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present with pull=missing" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=missing" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=missing" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present with pull=missing" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present with pull=missing" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present with pull=missing" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present with pull=missing" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=missing" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=missing" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present with pull=missing" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present with pull=missing" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present with pull=missing" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present with pull=missing" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present with pull=missing" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present with pull=missing" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present with pull=missing" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present with pull=missing" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present with pull=missing" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present with pull=missing" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Present with pull=missing" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-with-pull=missing',
        '2.21.0',
        False,
        False,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' ansible-docker-test-01234567-cont Pulled \n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-present-with-pull=missing-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-19ffba88-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-19ffba88-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-19ffba88-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-19ffba88-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-13 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-13-docker_compose_v2-present-with-pull=missing-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-1ba2643a-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-1ba2643a-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-1ba2643a-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-1ba2643a-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-present-with-pull=missing-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-1f1d0d58-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-1f1d0d58-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-1f1d0d58-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-1f1d0d58-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-present-with-pull=missing-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-2460e737-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-2460e737-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-2460e737-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-2460e737-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-with-pull=missing-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-4baa7139-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-4baa7139-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-4baa7139-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-4baa7139-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-13 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-13-docker_compose_v2-present-with-pull=missing-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-4fcbaf1e-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-4fcbaf1e-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-4fcbaf1e-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-4fcbaf1e-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-13 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-13-docker_compose_v2-present-with-pull=missing-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-51914faa-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-51914faa-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-51914faa-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-51914faa-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-present-with-pull=missing-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-5f3d2e16-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-5f3d2e16-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-5f3d2e16-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-5f3d2e16-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-present-with-pull=missing-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-601188b1-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-601188b1-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-601188b1-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-601188b1-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-present-with-pull=missing-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-64d917f4-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-64d917f4-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-64d917f4-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-64d917f4-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-present-with-pull=missing-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-6aaaa304-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-6aaaa304-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-6aaaa304-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-6aaaa304-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-13 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-13-docker_compose_v2-present-with-pull=missing-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-834c1a9b-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-834c1a9b-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-834c1a9b-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-834c1a9b-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-13 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-13-docker_compose_v2-present-with-pull=missing-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-971ad57c-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-971ad57c-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-971ad57c-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-971ad57c-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-13 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-13-docker_compose_v2-present-with-pull=missing-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ad622acd-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ad622acd-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-ad622acd-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-ad622acd-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-13 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-13-docker_compose_v2-present-with-pull=missing-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-b2745d99-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-b2745d99-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-b2745d99-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-b2745d99-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present-with-pull=missing-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ce1fa4d7-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ce1fa4d7-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-ce1fa4d7-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-ce1fa4d7-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-present-with-pull=missing-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d1d30700-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d1d30700-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d1d30700-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d1d30700-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-13 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-13-docker_compose_v2-present-with-pull=missing-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d2caf0c9-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d2caf0c9-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d2caf0c9-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d2caf0c9-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-13 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-13-docker_compose_v2-present-with-pull=missing-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d616c3a5-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d616c3a5-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d616c3a5-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d616c3a5-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-present-with-pull=missing-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d6ae094c-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d6ae094c-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d6ae094c-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d6ae094c-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-13 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-13-docker_compose_v2-present-with-pull=missing-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-e700ac20-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-e700ac20-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-e700ac20-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-e700ac20-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-13-docker_compose_v2-present-with-pull=missing-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ede01681-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ede01681-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-ede01681-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-ede01681-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-13 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent)',
        '2.21.0',
        False,
        False,
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Running\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-13 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent,-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Running\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        False,
        ' Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' Network ansible-docker-test-01234567-pull_default  Created\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in devel-rhel9.3
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        True,
        ' Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' Network ansible-docker-test-01234567-pull_default  Created\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        'Error response from daemon: No such image: does-not-exist:latest\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'unknown',
                '',
                'Error',
                'Error response from daemon: No such image: does-not-exist:latest',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        True,
        ' Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' Network ansible-docker-test-01234567-pull_default  Created\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        'Error response from daemon: no such image: does-not-exist:latest: No such image: does-not-exist:latest\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'unknown',
                '',
                'Error',
                'Error response from daemon: no such image: does-not-exist:latest: No such image: does-not-exist:latest',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-19ffba88-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-19ffba88-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-19ffba88-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-19ffba88-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-13-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-1ba2643a-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-1ba2643a-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-1ba2643a-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-1ba2643a-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-1f1d0d58-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-1f1d0d58-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-1f1d0d58-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-1f1d0d58-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-2460e737-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-2460e737-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-2460e737-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-2460e737-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-4baa7139-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-4baa7139-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-4baa7139-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-4baa7139-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-13-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-4fcbaf1e-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-4fcbaf1e-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-4fcbaf1e-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-4fcbaf1e-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-13-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-51914faa-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-51914faa-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-51914faa-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-51914faa-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-5f3d2e16-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-5f3d2e16-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-5f3d2e16-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-5f3d2e16-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-601188b1-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-601188b1-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-601188b1-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-601188b1-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-64d917f4-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-64d917f4-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-64d917f4-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-64d917f4-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-6aaaa304-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-6aaaa304-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-6aaaa304-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-6aaaa304-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-13-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-834c1a9b-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-834c1a9b-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-834c1a9b-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-834c1a9b-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-13-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-971ad57c-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-971ad57c-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-971ad57c-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-971ad57c-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-13-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ad622acd-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ad622acd-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-ad622acd-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-ad622acd-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-13-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-b2745d99-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-b2745d99-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-b2745d99-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-b2745d99-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ce1fa4d7-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ce1fa4d7-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-ce1fa4d7-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-ce1fa4d7-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d1d30700-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d1d30700-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d1d30700-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d1d30700-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-13-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d2caf0c9-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d2caf0c9-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d2caf0c9-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d2caf0c9-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-13-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d616c3a5-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d616c3a5-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d616c3a5-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d616c3a5-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d6ae094c-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d6ae094c-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d6ae094c-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-d6ae094c-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-13-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-e700ac20-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-e700ac20-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-e700ac20-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-e700ac20-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-13-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ede01681-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ede01681-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-ede01681-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-ede01681-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present without explicit pull" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present without explicit pull" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present without explicit pull" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present without explicit pull" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present without explicit pull" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present without explicit pull" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present without explicit pull" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present without explicit pull" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present without explicit pull" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present without explicit pull" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present without explicit pull" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present without explicit pull" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present without explicit pull" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present without explicit pull" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present without explicit pull" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present without explicit pull" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present without explicit pull" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present without explicit pull" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present without explicit pull" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present without explicit pull" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Present without explicit pull" on 2024-01-13 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2_pull: "Pull" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2_pull: "Pull" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2_pull: "Pull" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2_pull: "Pull" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2_pull: "Pull" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2_pull: "Pull" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2_pull: "Pull" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2_pull: "Pull" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2_pull: "Pull" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2_pull: "Pull" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2_pull: "Pull" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-without-explicit-pull',
        '2.21.0',
        False,
        True,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' ansible-docker-test-01234567-cont Error \n'
        "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied\n",  # noqa: E501
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'unknown',
                'ansible-docker-test-01234567-cont',
                'Error',
                "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied",  # noqa: E501
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present without explicit pull (check)" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present without explicit pull (check)" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present without explicit pull (check)" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present without explicit pull (check)" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present without explicit pull (check)" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present without explicit pull (check)" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present without explicit pull (check)" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present without explicit pull (check)" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present without explicit pull (check)" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present without explicit pull (check)" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Present without explicit pull (check)" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-without-explicit-pull-(check)',
        '2.21.0',
        True,
        True,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Error \n'
        'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'unknown',
                'ansible-docker-test-01234567-cont',
                'Error',
                'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-restarted',
        '2.21.0',
        False,
        False,
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Restarting\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Restarting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Restarting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Started" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Started" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Started" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Started" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Started" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Started" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Started" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Started" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Started" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Started" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Started" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Started" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Started" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Started" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Started" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Started" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Started" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Started" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Started" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Started" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Started" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-started',
        '2.21.0',
        False,
        False,
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (check)" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Started (check)" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Started (check)" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Started (check)" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Started (check)" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Started (check)" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Started (check)" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Started (check)" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Started (check)" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Started (check)" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Started (check)" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Started (check)" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Started (check)" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Started (check)" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Started (check)" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Started (check)" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Started (check)" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Started (check)" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Started (check)" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Started (check)" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Started (check)" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Started (check)" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-started-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Stopped" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Stopped" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Stopped" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Stopped" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Stopped" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Stopped" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Stopped" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Stopped" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Stopped" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Stopped" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Stopped" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Stopped" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Stopped" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Stopped" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Stopped" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Stopped" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Stopped" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Stopped" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Stopped" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Stopped" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Stopped" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-stopped',
        '2.21.0',
        False,
        False,
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Running\n'
        '\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopping\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopped\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Running',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopping',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped (check)" on 2024-01-07 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Stopped (check)" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2: "Stopped (check)" on 2024-01-07 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Stopped (check)" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2: "Stopped (check)" on 2024-01-07 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Stopped (check)" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2: "Stopped (check)" on 2024-01-07 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Stopped (check)" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2: "Stopped (check)" on 2024-01-07 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Stopped (check)" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2: "Stopped (check)" on 2024-01-07 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Stopped (check)" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2: "Stopped (check)" on 2024-01-07 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Stopped (check)" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2: "Stopped (check)" on 2024-01-07 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Stopped (check)" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2: "Stopped (check)" on 2024-01-07 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Stopped (check)" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2: "Stopped (check)" on 2024-01-07 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Stopped (check)" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2: "Stopped (check)" on 2024-01-07 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2: "Stopped (check)" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-stopped-(check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Running\n'
        '\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopped\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Running',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopping',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2_pull: "Pull (check)" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2_pull: "Pull (check)" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2_pull: "Pull (check)" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2_pull: "Pull (check)" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2_pull: "Pull (check)" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2_pull: "Pull (check)" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2_pull: "Pull (check)" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2_pull: "Pull (check)" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2_pull: "Pull (check)" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2_pull: "Pull (check)" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2_pull: "Pull (check)" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-13-docker_compose_v2_pull-pull-(check)',
        '2.21.0',
        True,
        True,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Error \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont  - Pull error for image: does-not-exist:latest \n'
        'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'unknown',
                'ansible-docker-test-01234567-cont',
                'Error',
                'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed',
            ),
        ],
        [],
    ),
    # docker_compose_v2_pull: "Pull with policy=always" on 2024-01-13 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-13-docker_compose_v2_pull-pull-with-policy=always',
        '2.21.0',
        False,
        False,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' 486039affc0a Pulling fs layer \n'
        ' 486039affc0a Downloading [>                                                  ]   34.2kB/2.207MB\n'
        ' 486039affc0a Verifying Checksum \n'
        ' 486039affc0a Download complete \n'
        ' 486039affc0a Extracting [>                                                  ]  32.77kB/2.207MB\n'
        ' 486039affc0a Extracting [==================================================>]  2.207MB/2.207MB\n'
        ' 486039affc0a Pull complete \n'
        ' ansible-docker-test-01234567-cont Pulled \n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pulling fs layer',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Downloading',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Verifying Checksum',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Download complete',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pull complete',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2_pull: "Pull with policy=always" on 2024-01-13 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-13-docker_compose_v2_pull-pull-with-policy=always',
        '2.21.0',
        False,
        False,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' 486039affc0a Pulling fs layer \n'
        ' 486039affc0a Downloading [>                                                  ]  32.12kB/2.207MB\n'
        ' 486039affc0a Download complete \n'
        ' 486039affc0a Extracting [>                                                  ]  32.77kB/2.207MB\n'
        ' 486039affc0a Extracting [==================================================>]  2.207MB/2.207MB\n'
        ' 486039affc0a Pull complete \n'
        ' ansible-docker-test-01234567-cont Pulled \n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pulling fs layer',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Downloading',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Download complete',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pull complete',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2_pull: "Pull with policy=always" on 2024-01-13 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-13-docker_compose_v2_pull-pull-with-policy=always',
        '2.21.0',
        False,
        False,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' 486039affc0a Pulling fs layer \n'
        ' 486039affc0a Downloading [>                                                  ]  32.12kB/2.207MB\n'
        ' 486039affc0a Downloading [==================================================>]  2.207MB/2.207MB\n'
        ' 486039affc0a Download complete \n'
        ' 486039affc0a Extracting [>                                                  ]  32.77kB/2.207MB\n'
        ' 486039affc0a Extracting [==================================================>]  2.207MB/2.207MB\n'
        ' 486039affc0a Pull complete \n'
        ' ansible-docker-test-01234567-cont Pulled \n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pulling fs layer',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Downloading',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Downloading',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Download complete',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pull complete',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2_pull: "Pull with policy=always" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always" on 2024-01-13 in devel-rhel9.3
    (
        '2.21.0-2.14-rhel9.0-2024-01-13-docker_compose_v2_pull-pull-with-policy=always',
        '2.21.0',
        False,
        False,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' 486039affc0a Pulling fs layer \n'
        ' 486039affc0a Downloading [>                                                  ]  32.16kB/2.207MB\n'
        ' 486039affc0a Verifying Checksum \n'
        ' 486039affc0a Download complete \n'
        ' 486039affc0a Extracting [>                                                  ]  32.77kB/2.207MB\n'
        ' 486039affc0a Extracting [==================================================>]  2.207MB/2.207MB\n'
        ' 486039affc0a Pull complete \n'
        ' ansible-docker-test-01234567-cont Pulled \n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pulling fs layer',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Downloading',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Verifying Checksum',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Download complete',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pull complete',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2_pull: "Pull with policy=always" on 2024-01-13 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-13-docker_compose_v2_pull-pull-with-policy=always',
        '2.21.0',
        False,
        False,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' 486039affc0a Pulling fs layer \n'
        ' 486039affc0a Downloading [>                                                  ]  32.16kB/2.207MB\n'
        ' 486039affc0a Verifying Checksum \n'
        ' 486039affc0a Download complete \n'
        ' 486039affc0a Extracting [>                                                  ]  32.77kB/2.207MB\n'
        ' 486039affc0a Extracting [================================================>  ]   2.13MB/2.207MB\n'
        ' 486039affc0a Extracting [==================================================>]  2.207MB/2.207MB\n'
        ' 486039affc0a Pull complete \n'
        ' ansible-docker-test-01234567-cont Pulled \n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pulling fs layer',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Downloading',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Verifying Checksum',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Download complete',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pull complete',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2_pull: "Pull with policy=always" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-13-docker_compose_v2_pull-pull-with-policy=always',
        '2.21.0',
        False,
        False,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' 486039affc0a Pulling fs layer \n'
        ' 486039affc0a Downloading [>                                                  ]  32.16kB/2.207MB\n'
        ' 486039affc0a Verifying Checksum \n'
        ' 486039affc0a Download complete \n'
        ' 486039affc0a Extracting [>                                                  ]  32.77kB/2.207MB\n'
        ' 486039affc0a Extracting [===============================================>   ]  2.097MB/2.207MB\n'
        ' 486039affc0a Extracting [==================================================>]  2.207MB/2.207MB\n'
        ' 486039affc0a Pull complete \n'
        ' ansible-docker-test-01234567-cont Pulled \n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pulling fs layer',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Downloading',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Verifying Checksum',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Download complete',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pull complete',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2_pull: "Pull with policy=always" on 2024-01-13 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-13-docker_compose_v2_pull-pull-with-policy=always',
        '2.21.0',
        False,
        False,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' 486039affc0a Pulling fs layer \n'
        ' 486039affc0a Downloading [>                                                  ]  32.16kB/2.207MB\n'
        ' 486039affc0a Verifying Checksum \n'
        ' 486039affc0a Download complete \n'
        ' 486039affc0a Extracting [>                                                  ]  32.77kB/2.207MB\n'
        ' 486039affc0a Extracting [==============================================>    ]  2.032MB/2.207MB\n'
        ' 486039affc0a Extracting [==================================================>]  2.207MB/2.207MB\n'
        ' 486039affc0a Pull complete \n'
        ' ansible-docker-test-01234567-cont Pulled \n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pulling fs layer',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Downloading',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Verifying Checksum',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Download complete',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pull complete',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2_pull: "Pull with policy=always" on 2024-01-13 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-13-docker_compose_v2_pull-pull-with-policy=always',
        '2.21.0',
        False,
        False,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' 486039affc0a Pulling fs layer \n'
        ' 486039affc0a Downloading [>                                                  ]  32.16kB/2.207MB\n'
        ' 486039affc0a Verifying Checksum \n'
        ' 486039affc0a Download complete \n'
        ' 486039affc0a Extracting [>                                                  ]  32.77kB/2.207MB\n'
        ' 486039affc0a Extracting [============================================>      ]  1.966MB/2.207MB\n'
        ' 486039affc0a Extracting [==================================================>]  2.207MB/2.207MB\n'
        ' 486039affc0a Pull complete \n'
        ' ansible-docker-test-01234567-cont Pulled \n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pulling fs layer',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Downloading',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Verifying Checksum',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Download complete',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pull complete',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2_pull: "Pull with policy=always" on 2024-01-13 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-13-docker_compose_v2_pull-pull-with-policy=always',
        '2.21.0',
        False,
        False,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' 486039affc0a Pulling fs layer \n'
        ' 486039affc0a Downloading [>                                                  ]  32.16kB/2.207MB\n'
        ' 486039affc0a Verifying Checksum \n'
        ' 486039affc0a Download complete \n'
        ' 486039affc0a Extracting [>                                                  ]  32.77kB/2.207MB\n'
        ' 486039affc0a Extracting [=======================================>           ]  1.737MB/2.207MB\n'
        ' 486039affc0a Extracting [==================================================>]  2.207MB/2.207MB\n'
        ' 486039affc0a Pull complete \n'
        ' ansible-docker-test-01234567-cont Pulled \n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pulling fs layer',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Downloading',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Verifying Checksum',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Download complete',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pull complete',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2_pull: "Pull with policy=always" on 2024-01-13 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-13-docker_compose_v2_pull-pull-with-policy=always',
        '2.21.0',
        False,
        False,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' 486039affc0a Pulling fs layer \n'
        ' 486039affc0a Downloading [>                                                  ]  32.16kB/2.207MB\n'
        ' 486039affc0a Verifying Checksum \n'
        ' 486039affc0a Download complete \n'
        ' 486039affc0a Extracting [>                                                  ]  32.77kB/2.207MB\n'
        ' 486039affc0a Extracting [=====================================>             ]  1.638MB/2.207MB\n'
        ' 486039affc0a Extracting [==================================================>]  2.207MB/2.207MB\n'
        ' 486039affc0a Pull complete \n'
        ' ansible-docker-test-01234567-cont Pulled \n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pulling fs layer',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Downloading',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Verifying Checksum',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Download complete',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pull complete',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2_pull: "Pull with policy=always (again)" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (again)" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (again)" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (again)" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (again)" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (again)" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (again)" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (again)" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (again)" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (again)" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (again)" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-13-docker_compose_v2_pull-pull-with-policy=always-(again)',
        '2.21.0',
        False,
        False,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' ansible-docker-test-01234567-cont Pulled \n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2_pull: "Pull with policy=always (again, check)" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (again, check)" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (again, check)" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (again, check)" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (again, check)" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (again, check)" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (again, check)" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (again, check)" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (again, check)" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (again, check)" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (again, check)" on 2024-01-13 in devel-ubuntu2204
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (check)" on 2024-01-13 in 2.14-rhel9.0
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (check)" on 2024-01-13 in 2.15-centos7
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (check)" on 2024-01-13 in 2.15-rhel7.9
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (check)" on 2024-01-13 in 2.15-rhel9.1
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (check)" on 2024-01-13 in 2.16-centos7
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (check)" on 2024-01-13 in 2.16-rhel9.2
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (check)" on 2024-01-13 in devel-debian-bookworm
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (check)" on 2024-01-13 in devel-debian-bullseye
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (check)" on 2024-01-13 in devel-rhel9.3
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (check)" on 2024-01-13 in devel-ubuntu2004
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=always (check)" on 2024-01-13 in devel-ubuntu2204
    (
        '2.21.0-2.14-rhel9.0-2024-01-13-docker_compose_v2_pull-pull-with-policy=always-(again,-check)',
        '2.21.0',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
        ],
        [],
    ),
    # #######################################################################################################################
    # ## Docker Compose 2.23.3 ##############################################################################################
    # #######################################################################################################################
    # docker_compose_v2: "Absent" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Absent" on 2024-01-13 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-absent',
        '2.23.3',
        False,
        False,
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopping\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopped\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Removing\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Removed\n'
        ' Network ansible-docker-test-01234567-start-stop_default  Removing\n'
        ' Network ansible-docker-test-01234567-start-stop_default  Removed\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopping',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopped',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Removing',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Removed',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Removing',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent (check)" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Absent (check)" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-absent-(check)',
        '2.23.3',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopped\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Removing\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Removed\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Removing\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Resource is still in use\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopping',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopped',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Removing',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Removed',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Removing',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                None,
                'Resource is still in use',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Cleanup" on 2024-01-13 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Stopping service" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-cleanup',
        '2.23.3',
        False,
        False,
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Stopping\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Stopped\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Removing\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Removed\n'
        ' Network ansible-docker-test-01234567-pull_default  Removing\n'
        ' Network ansible-docker-test-01234567-pull_default  Removed\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Stopping',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Stopped',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Removing',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Removed',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Removing',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Present" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present',
        '2.23.3',
        False,
        False,
        ' Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-(changed-check)',
        '2.23.3',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container df477f7889c_ansible-docker-test-bc362ba-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container df477f7889c_ansible-docker-test-bc362ba-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'df477f7889c_ansible-docker-test-bc362ba-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'df477f7889c_ansible-docker-test-bc362ba-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed check)" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-13-docker_compose_v2-present-(changed-check)',
        '2.23.3',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container e3161c3ca1e_ansible-docker-test-26fefc5c-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container e3161c3ca1e_ansible-docker-test-26fefc5c-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'e3161c3ca1e_ansible-docker-test-26fefc5c-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'e3161c3ca1e_ansible-docker-test-26fefc5c-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed)" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Present (changed)" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-(changed)',
        '2.23.3',
        False,
        False,
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreate\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Recreated\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-13-docker_compose_v2-present-(check)',
        '2.23.3',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-26fefc5c-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-26fefc5c-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-26fefc5c-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-26fefc5c-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (check)" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-(check)',
        '2.23.3',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-bc362ba-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-bc362ba-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-bc362ba-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-bc362ba-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Present (idempotent check)" on 2024-01-13 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Started (idempotent check)" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-(idempotent-check)',
        '2.23.3',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Running\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent)" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Present (idempotent)" on 2024-01-13 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Started (idempotent)" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-(idempotent)',
        '2.23.3',
        False,
        False,
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Running\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Present stopped" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-stopped',
        '2.23.3',
        False,
        False,
        ' Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped (check)" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Present stopped (check)" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-stopped-(check)',
        '2.23.3',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Created\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-start-stop_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Present with pull=always" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-with-pull=always',
        '2.23.3',
        False,
        False,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' ansible-docker-test-01234567-cont Pulled \n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Running\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-with-pull=always-(check)',
        '2.23.3',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container 9f33f2ddb62_ansible-docker-test-bc362ba-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container 9f33f2ddb62_ansible-docker-test-bc362ba-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                '9f33f2ddb62_ansible-docker-test-bc362ba-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                '9f33f2ddb62_ansible-docker-test-bc362ba-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always (check)" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-13-docker_compose_v2-present-with-pull=always-(check)',
        '2.23.3',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container e6dd7e14964_ansible-docker-test-26fefc5c-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container e6dd7e14964_ansible-docker-test-26fefc5c-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreate',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Recreated',
                None,
            ),
            Event(
                'container',
                'e6dd7e14964_ansible-docker-test-26fefc5c-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'e6dd7e14964_ansible-docker-test-26fefc5c-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Present with pull=missing" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-with-pull=missing',
        '2.23.3',
        False,
        False,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' ansible-docker-test-01234567-cont Pulled \n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-13-docker_compose_v2-present-with-pull=missing-(check)',
        '2.23.3',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-26fefc5c-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-26fefc5c-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-26fefc5c-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-26fefc5c-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (check)" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-with-pull=missing-(check)',
        '2.23.3',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-bc362ba-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-bc362ba-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-bc362ba-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-bc362ba-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-13 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent)',
        '2.23.3',
        False,
        False,
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Running\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-13 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent,-check)',
        '2.23.3',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Running\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.23.3',
        False,
        False,
        ' Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' Network ansible-docker-test-01234567-pull_default  Created\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Present with pull=never" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.23.3',
        False,
        True,
        ' Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' Network ansible-docker-test-01234567-pull_default  Created\n'
        ' Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        'Error response from daemon: no such image: does-not-exist:latest: No such image: does-not-exist:latest\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'unknown',
                '',
                'Error',
                'Error response from daemon: no such image: does-not-exist:latest: No such image: does-not-exist:latest',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-13-docker_compose_v2-present-with-pull=never-(check)',
        '2.23.3',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-26fefc5c-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-26fefc5c-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-26fefc5c-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-26fefc5c-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.23.3',
        True,
        False,
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-01234567-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-bc362ba-pull-ansible-docker-test-01234567-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-bc362ba-pull-ansible-docker-test-01234567-cont-1  Started\n',
        [
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Creating',
                None,
            ),
            Event(
                'network',
                'ansible-docker-test-01234567-pull_default',
                'Created',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Creating',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-pull-ansible-docker-test-01234567-cont-1',
                'Created',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-bc362ba-pull-ansible-docker-test-01234567-cont-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'nsible-docker-test-bc362ba-pull-ansible-docker-test-01234567-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Present without explicit pull" on 2024-01-13 in devel-archlinux
    # Duplicated in: docker_compose_v2_pull: "Pull" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-without-explicit-pull',
        '2.23.3',
        False,
        True,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' ansible-docker-test-01234567-cont Error \n'
        "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied\n",  # noqa: E501
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'unknown',
                'ansible-docker-test-01234567-cont',
                'Error',
                "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied",  # noqa: E501
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Present without explicit pull (check)" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-without-explicit-pull-(check)',
        '2.23.3',
        True,
        True,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Error \n'
        'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'unknown',
                'ansible-docker-test-01234567-cont',
                'Error',
                'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Restarted" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-restarted',
        '2.23.3',
        False,
        False,
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Restarting\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Restarting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Restarted (check)" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.23.3',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Restarting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Started" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-started',
        '2.23.3',
        False,
        False,
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (check)" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Started (check)" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-started-(check)',
        '2.23.3',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Starting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Started\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Starting',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Stopped" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-stopped',
        '2.23.3',
        False,
        False,
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Running\n'
        '\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopping\n'
        ' Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopped\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Running',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopping',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped (check)" on 2024-01-07 in devel-archlinux
    # Duplicated in: docker_compose_v2: "Stopped (check)" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-stopped-(check)',
        '2.23.3',
        True,
        False,
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Running\n'
        '\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1  Stopped\n',
        [
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Running',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopping',
                None,
            ),
            Event(
                'container',
                'ansible-docker-test-01234567-start-stop-ansible-docker-test-01234567-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2_pull: "Pull (check)" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-13-docker_compose_v2_pull-pull-(check)',
        '2.23.3',
        True,
        True,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Error \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont  - Pull error for image: does-not-exist:latest \n'
        'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed\n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'unknown',
                'ansible-docker-test-01234567-cont',
                'Error',
                'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed',
            ),
        ],
        [],
    ),
    # docker_compose_v2_pull: "Pull with policy=always" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-13-docker_compose_v2_pull-pull-with-policy=always',
        '2.23.3',
        False,
        False,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' ansible-docker-test-01234567-cont Pulled \n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2_pull: "Pull with policy=always (check)" on 2024-01-13 in devel-archlinux
    # Duplicated in: docker_compose_v2_pull: "Pull with policy=missing (check)" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-13-docker_compose_v2_pull-pull-with-policy=always-(check)',
        '2.23.3',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Pulled \n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2_pull: "Pull with policy=missing" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-13-docker_compose_v2_pull-pull-with-policy=missing',
        '2.23.3',
        False,
        False,
        ' ansible-docker-test-01234567-cont Pulling \n'
        ' 486039affc0a Pulling fs layer \n'
        ' 486039affc0a Downloading [>                                                  ]  32.16kB/2.207MB\n'
        ' 486039affc0a Verifying Checksum \n'
        ' 486039affc0a Download complete \n'
        ' 486039affc0a Extracting [>                                                  ]  32.77kB/2.207MB\n'
        ' 486039affc0a Extracting [==========================================>        ]  1.868MB/2.207MB\n'
        ' 486039affc0a Extracting [==================================================>]  2.207MB/2.207MB\n'
        ' 486039affc0a Pull complete \n'
        ' ansible-docker-test-01234567-cont Pulled \n',
        [
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulling',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pulling fs layer',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Downloading',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Verifying Checksum',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Download complete',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Extracting',
                None,
            ),
            Event(
                'image-layer',
                '486039affc0a',
                'Pull complete',
                None,
            ),
            Event(
                'service',
                'ansible-docker-test-01234567-cont',
                'Pulled',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2_pull: "Pull with policy=missing (idempotent)" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-13-docker_compose_v2_pull-pull-with-policy=missing-(idempotent)',
        '2.23.3',
        False,
        False,
        ' ansible-docker-test-01234567-cont Skipped - Image is already present locally \n',
        [
            Event(
                'unknown',
                'ansible-docker-test-01234567-cont',
                'Skipped',
                'Image is already present locally',
            ),
        ],
        [],
    ),
    # docker_compose_v2_pull: "Pull with policy=missing (idempotent, check)" on 2024-01-13 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-13-docker_compose_v2_pull-pull-with-policy=missing-(idempotent,-check)',
        '2.23.3',
        True,
        False,
        ' DRY-RUN MODE -  ansible-docker-test-01234567-cont Skipped - Image is already present locally \n',
        [
            Event(
                'unknown',
                'ansible-docker-test-01234567-cont',
                'Skipped',
                'Image is already present locally',
            ),
        ],
        [],
    ),
]
