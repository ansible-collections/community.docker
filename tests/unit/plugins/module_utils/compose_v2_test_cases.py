# Copyright 2022 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.community.docker.plugins.module_utils.compose_v2 import (
    ResourceEvent,
)


EVENT_TEST_CASES = [
    # #######################################################################################################################
    # ## Docker Compose 2.18.1 ##############################################################################################
    # #######################################################################################################################
    # docker_compose_v2: "Absent" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-absent',
        '2.18.1',
        False,
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Stopping\n'
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Stopped\n'
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Removing\n'
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Removed\n'
        ' Network ansible-docker-test-dba91fb6-start-stop_default  Removing\n'
        ' Network ansible-docker-test-dba91fb6-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent (check)" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-absent-(check)',
        '2.18.1',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Stopped\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Removing\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Removed\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-dba91fb6-start-stop_default  Removing\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-dba91fb6-start-stop_default  Resource is still in use\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-start-stop_default',
                None,
                'Resource is still in use',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-cleanup',
        '2.18.1',
        False,
        ' Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Stopping\n'
        ' Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Stopped\n'
        ' Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Removing\n'
        ' Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Removed\n'
        ' Network ansible-docker-test-dba91fb6-pull_default  Removing\n'
        ' Network ansible-docker-test-dba91fb6-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-cleanup',
        '2.18.1',
        False,
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Stopping\n'
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Stopped\n'
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Removing\n'
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Removed\n'
        ' Network ansible-docker-test-dba91fb6-start-stop_default  Removing\n'
        ' Network ansible-docker-test-dba91fb6-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present',
        '2.18.1',
        False,
        ' ansible-docker-test-dba91fb6-container Pulling \n'
        ' ansible-docker-test-dba91fb6-container Pulled \n'
        ' Network ansible-docker-test-dba91fb6-start-stop_default  Creating\n'
        ' Network ansible-docker-test-dba91fb6-start-stop_default  Created\n'
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Creating\n'
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Created\n'
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Starting\n'
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-dba91fb6-container',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-dba91fb6-container',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
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
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 9121995872d_ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 9121995872d_ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                '9121995872d_ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                '9121995872d_ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed)" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-(changed)',
        '2.18.1',
        False,
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Recreate\n'
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Recreated\n'
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Starting\n'
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-dba91fb6-container Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-dba91fb6-container Pulled \n'
        ' DRY-RUN MODE -  Network ansible-docker-test-dba91fb6-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-dba91fb6-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-dba91fb6-container',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-dba91fb6-container',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-(idempotent-check)',
        '2.18.1',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent)" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-(idempotent)',
        '2.18.1',
        False,
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-stopped',
        '2.18.1',
        False,
        ' Network ansible-docker-test-dba91fb6-start-stop_default  Creating\n'
        ' Network ansible-docker-test-dba91fb6-start-stop_default  Created\n'
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Creating\n'
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped (check)" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-stopped-(check)',
        '2.18.1',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-dba91fb6-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-dba91fb6-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-with-pull=always',
        '2.18.1',
        False,
        ' ansible-docker-test-dba91fb6-cont Pulling \n'
        ' ansible-docker-test-dba91fb6-cont Pulled \n'
        ' Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Running\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-dba91fb6-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-dba91fb6-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-dba91fb6-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-dba91fb6-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container 002a15404ac_ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container 002a15404ac_ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-dba91fb6-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-dba91fb6-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                '002a15404ac_ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                '002a15404ac_ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-with-pull=missing',
        '2.18.1',
        False,
        ' ansible-docker-test-dba91fb6-cont Pulling \n'
        ' ansible-docker-test-dba91fb6-cont Pulled \n'
        ' Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Creating\n'
        ' Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Created\n'
        ' Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Starting\n'
        ' Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-dba91fb6-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-dba91fb6-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-dba91fb6-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-dba91fb6-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-dba91fb6-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-dba91fb6-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent)',
        '2.18.1',
        False,
        ' Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent,-check)',
        '2.18.1',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.18.1',
        False,
        ' Network ansible-docker-test-dba91fb6-pull_default  Creating\n'
        ' Network ansible-docker-test-dba91fb6-pull_default  Created\n'
        ' Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Creating\n'
        ' Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Created\n'
        ' Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Starting\n'
        ' Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.18.1',
        False,
        ' Network ansible-docker-test-dba91fb6-pull_default  Creating\n'
        ' Network ansible-docker-test-dba91fb6-pull_default  Created\n'
        ' Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Creating\n'
        'Error response from daemon: No such image: does-not-exist:latest\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'unknown',
                '',
                'Error',
                'Error response from daemon: No such image: does-not-exist:latest',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.18.1',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-dba91fb6-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-dba91fb6-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.18.1',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-dba91fb6-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-dba91fb6-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent)',
        '2.18.1',
        False,
        ' Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent,-check)',
        '2.18.1',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-without-explicit-pull',
        '2.18.1',
        False,
        ' ansible-docker-test-dba91fb6-cont Pulling \n'
        ' ansible-docker-test-dba91fb6-cont Error \n'
        "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied\n",  # noqa: E501
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-dba91fb6-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-dba91fb6-cont',
                'Error',
                "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied",  # noqa: E501
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-present-without-explicit-pull-(check)',
        '2.18.1',
        True,
        ' DRY-RUN MODE -  ansible-docker-test-dba91fb6-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-dba91fb6-cont Error \n'
        'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-dba91fb6-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-dba91fb6-cont',
                'Error',
                'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-restarted',
        '2.18.1',
        False,
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Restarting\n'
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-restarted',
        '2.18.1',
        False,
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Restarting\n'
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.18.1',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.18.1',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-started',
        '2.18.1',
        False,
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Starting\n'
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (check)" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-started-(check)',
        '2.18.1',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Starting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-started-(idempotent-check)',
        '2.18.1',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent)" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-started-(idempotent)',
        '2.18.1',
        False,
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-stopped',
        '2.18.1',
        False,
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Running\n'
        '\n'
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Stopping\n'
        ' Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped (check)" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-stopped-(check)',
        '2.18.1',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Running\n'
        '\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-start-stop-ansible-docker-test-dba91fb6-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopping service" on 2024-01-07 in 2.12-ubuntu1804
    (
        '2.18.1-2.12-ubuntu1804-2024-01-07-docker_compose_v2-stopping-service',
        '2.18.1',
        False,
        ' Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Stopping\n'
        ' Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Stopped\n'
        ' Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Removing\n'
        ' Container ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1  Removed\n'
        ' Network ansible-docker-test-dba91fb6-pull_default  Removing\n'
        ' Network ansible-docker-test-dba91fb6-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-dba91fb6-pull-ansible-docker-test-dba91fb6-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-dba91fb6-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # #######################################################################################################################
    # ## Docker Compose 2.21.0 ##############################################################################################
    # #######################################################################################################################
    # docker_compose_v2: "Absent" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-absent',
        '2.21.0',
        False,
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Stopping\n'
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Stopped\n'
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Removing\n'
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Removed\n'
        ' Network ansible-docker-test-19ffba88-start-stop_default  Removing\n'
        ' Network ansible-docker-test-19ffba88-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-absent',
        '2.21.0',
        False,
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Stopping\n'
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Stopped\n'
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Removing\n'
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Removed\n'
        ' Network ansible-docker-test-1f1d0d58-start-stop_default  Removing\n'
        ' Network ansible-docker-test-1f1d0d58-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-absent',
        '2.21.0',
        False,
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Stopping\n'
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Stopped\n'
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Removing\n'
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Removed\n'
        ' Network ansible-docker-test-2460e737-start-stop_default  Removing\n'
        ' Network ansible-docker-test-2460e737-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-absent',
        '2.21.0',
        False,
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Stopping\n'
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Stopped\n'
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Removing\n'
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Removed\n'
        ' Network ansible-docker-test-4baa7139-start-stop_default  Removing\n'
        ' Network ansible-docker-test-4baa7139-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-absent',
        '2.21.0',
        False,
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Stopping\n'
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Stopped\n'
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Removing\n'
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Removed\n'
        ' Network ansible-docker-test-5f3d2e16-start-stop_default  Removing\n'
        ' Network ansible-docker-test-5f3d2e16-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-absent',
        '2.21.0',
        False,
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Stopping\n'
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Stopped\n'
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Removing\n'
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Removed\n'
        ' Network ansible-docker-test-601188b1-start-stop_default  Removing\n'
        ' Network ansible-docker-test-601188b1-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-absent',
        '2.21.0',
        False,
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Stopping\n'
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Stopped\n'
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Removing\n'
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Removed\n'
        ' Network ansible-docker-test-64d917f4-start-stop_default  Removing\n'
        ' Network ansible-docker-test-64d917f4-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-absent',
        '2.21.0',
        False,
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Stopping\n'
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Stopped\n'
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Removing\n'
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Removed\n'
        ' Network ansible-docker-test-6aaaa304-start-stop_default  Removing\n'
        ' Network ansible-docker-test-6aaaa304-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-absent',
        '2.21.0',
        False,
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Stopping\n'
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Stopped\n'
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Removing\n'
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Removed\n'
        ' Network ansible-docker-test-ce1fa4d7-start-stop_default  Removing\n'
        ' Network ansible-docker-test-ce1fa4d7-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-absent',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Stopping\n'
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Stopped\n'
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Removing\n'
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Removed\n'
        ' Network ansible-docker-test-d1d30700-start-stop_default  Removing\n'
        ' Network ansible-docker-test-d1d30700-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-absent',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Stopping\n'
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Stopped\n'
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Removing\n'
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Removed\n'
        ' Network ansible-docker-test-d6ae094c-start-stop_default  Removing\n'
        ' Network ansible-docker-test-d6ae094c-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent (check)" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-absent-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Stopped\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Removing\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Removed\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-19ffba88-start-stop_default  Removing\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-19ffba88-start-stop_default  Resource is still in use\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-start-stop_default',
                None,
                'Resource is still in use',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent (check)" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-absent-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Stopped\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Removing\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Removed\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-1f1d0d58-start-stop_default  Removing\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-1f1d0d58-start-stop_default  Resource is still in use\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-start-stop_default',
                None,
                'Resource is still in use',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent (check)" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-absent-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Stopped\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Removing\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Removed\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-2460e737-start-stop_default  Removing\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-2460e737-start-stop_default  Resource is still in use\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-start-stop_default',
                None,
                'Resource is still in use',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent (check)" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-absent-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Stopped\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Removing\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Removed\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-4baa7139-start-stop_default  Removing\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-4baa7139-start-stop_default  Resource is still in use\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-start-stop_default',
                None,
                'Resource is still in use',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent (check)" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-absent-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Stopped\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Removing\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Removed\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-5f3d2e16-start-stop_default  Removing\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-5f3d2e16-start-stop_default  Resource is still in use\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-start-stop_default',
                None,
                'Resource is still in use',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent (check)" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-absent-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Stopped\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Removing\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Removed\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-601188b1-start-stop_default  Removing\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-601188b1-start-stop_default  Resource is still in use\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-start-stop_default',
                None,
                'Resource is still in use',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent (check)" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-absent-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Stopped\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Removing\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Removed\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-64d917f4-start-stop_default  Removing\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-64d917f4-start-stop_default  Resource is still in use\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-start-stop_default',
                None,
                'Resource is still in use',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent (check)" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-absent-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Stopped\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Removing\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Removed\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-6aaaa304-start-stop_default  Removing\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-6aaaa304-start-stop_default  Resource is still in use\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-start-stop_default',
                None,
                'Resource is still in use',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent (check)" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-absent-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Stopped\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Removing\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Removed\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-ce1fa4d7-start-stop_default  Removing\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-ce1fa4d7-start-stop_default  Resource is still in use\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-start-stop_default',
                None,
                'Resource is still in use',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent (check)" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-absent-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Stopped\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Removing\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Removed\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-d1d30700-start-stop_default  Removing\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-d1d30700-start-stop_default  Resource is still in use\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-start-stop_default',
                None,
                'Resource is still in use',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent (check)" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-absent-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Stopped\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Removing\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Removed\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-d6ae094c-start-stop_default  Removing\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-d6ae094c-start-stop_default  Resource is still in use\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-start-stop_default',
                None,
                'Resource is still in use',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-cleanup',
        '2.21.0',
        False,
        ' Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Stopping\n'
        ' Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Stopped\n'
        ' Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Removing\n'
        ' Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Removed\n'
        ' Network ansible-docker-test-19ffba88-pull_default  Removing\n'
        ' Network ansible-docker-test-19ffba88-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-cleanup',
        '2.21.0',
        False,
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Stopping\n'
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Stopped\n'
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Removing\n'
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Removed\n'
        ' Network ansible-docker-test-19ffba88-start-stop_default  Removing\n'
        ' Network ansible-docker-test-19ffba88-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-cleanup',
        '2.21.0',
        False,
        ' Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Stopping\n'
        ' Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Stopped\n'
        ' Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Removing\n'
        ' Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Removed\n'
        ' Network ansible-docker-test-1f1d0d58-pull_default  Removing\n'
        ' Network ansible-docker-test-1f1d0d58-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-cleanup',
        '2.21.0',
        False,
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Stopping\n'
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Stopped\n'
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Removing\n'
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Removed\n'
        ' Network ansible-docker-test-1f1d0d58-start-stop_default  Removing\n'
        ' Network ansible-docker-test-1f1d0d58-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-cleanup',
        '2.21.0',
        False,
        ' Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Stopping\n'
        ' Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Stopped\n'
        ' Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Removing\n'
        ' Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Removed\n'
        ' Network ansible-docker-test-2460e737-pull_default  Removing\n'
        ' Network ansible-docker-test-2460e737-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-cleanup',
        '2.21.0',
        False,
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Stopping\n'
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Stopped\n'
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Removing\n'
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Removed\n'
        ' Network ansible-docker-test-2460e737-start-stop_default  Removing\n'
        ' Network ansible-docker-test-2460e737-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-cleanup',
        '2.21.0',
        False,
        ' Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Stopping\n'
        ' Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Stopped\n'
        ' Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Removing\n'
        ' Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Removed\n'
        ' Network ansible-docker-test-4baa7139-pull_default  Removing\n'
        ' Network ansible-docker-test-4baa7139-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-cleanup',
        '2.21.0',
        False,
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Stopping\n'
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Stopped\n'
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Removing\n'
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Removed\n'
        ' Network ansible-docker-test-4baa7139-start-stop_default  Removing\n'
        ' Network ansible-docker-test-4baa7139-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-cleanup',
        '2.21.0',
        False,
        ' Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Stopping\n'
        ' Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Stopped\n'
        ' Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Removing\n'
        ' Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Removed\n'
        ' Network ansible-docker-test-5f3d2e16-pull_default  Removing\n'
        ' Network ansible-docker-test-5f3d2e16-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-cleanup',
        '2.21.0',
        False,
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Stopping\n'
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Stopped\n'
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Removing\n'
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Removed\n'
        ' Network ansible-docker-test-5f3d2e16-start-stop_default  Removing\n'
        ' Network ansible-docker-test-5f3d2e16-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-cleanup',
        '2.21.0',
        False,
        ' Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Stopping\n'
        ' Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Stopped\n'
        ' Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Removing\n'
        ' Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Removed\n'
        ' Network ansible-docker-test-601188b1-pull_default  Removing\n'
        ' Network ansible-docker-test-601188b1-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-cleanup',
        '2.21.0',
        False,
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Stopping\n'
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Stopped\n'
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Removing\n'
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Removed\n'
        ' Network ansible-docker-test-601188b1-start-stop_default  Removing\n'
        ' Network ansible-docker-test-601188b1-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-cleanup',
        '2.21.0',
        False,
        ' Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Stopping\n'
        ' Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Stopped\n'
        ' Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Removing\n'
        ' Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Removed\n'
        ' Network ansible-docker-test-64d917f4-pull_default  Removing\n'
        ' Network ansible-docker-test-64d917f4-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-cleanup',
        '2.21.0',
        False,
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Stopping\n'
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Stopped\n'
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Removing\n'
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Removed\n'
        ' Network ansible-docker-test-64d917f4-start-stop_default  Removing\n'
        ' Network ansible-docker-test-64d917f4-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-cleanup',
        '2.21.0',
        False,
        ' Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Stopping\n'
        ' Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Stopped\n'
        ' Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Removing\n'
        ' Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Removed\n'
        ' Network ansible-docker-test-6aaaa304-pull_default  Removing\n'
        ' Network ansible-docker-test-6aaaa304-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-cleanup',
        '2.21.0',
        False,
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Stopping\n'
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Stopped\n'
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Removing\n'
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Removed\n'
        ' Network ansible-docker-test-6aaaa304-start-stop_default  Removing\n'
        ' Network ansible-docker-test-6aaaa304-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-cleanup',
        '2.21.0',
        False,
        ' Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Stopping\n'
        ' Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Stopped\n'
        ' Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Removing\n'
        ' Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Removed\n'
        ' Network ansible-docker-test-ce1fa4d7-pull_default  Removing\n'
        ' Network ansible-docker-test-ce1fa4d7-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-cleanup',
        '2.21.0',
        False,
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Stopping\n'
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Stopped\n'
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Removing\n'
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Removed\n'
        ' Network ansible-docker-test-ce1fa4d7-start-stop_default  Removing\n'
        ' Network ansible-docker-test-ce1fa4d7-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-cleanup',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Stopping\n'
        ' Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Stopped\n'
        ' Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Removing\n'
        ' Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Removed\n'
        ' Network ansible-docker-test-d1d30700-pull_default  Removing\n'
        ' Network ansible-docker-test-d1d30700-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-cleanup',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Stopping\n'
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Stopped\n'
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Removing\n'
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Removed\n'
        ' Network ansible-docker-test-d1d30700-start-stop_default  Removing\n'
        ' Network ansible-docker-test-d1d30700-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-cleanup',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Stopping\n'
        ' Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Stopped\n'
        ' Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Removing\n'
        ' Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Removed\n'
        ' Network ansible-docker-test-d6ae094c-pull_default  Removing\n'
        ' Network ansible-docker-test-d6ae094c-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-cleanup',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Stopping\n'
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Stopped\n'
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Removing\n'
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Removed\n'
        ' Network ansible-docker-test-d6ae094c-start-stop_default  Removing\n'
        ' Network ansible-docker-test-d6ae094c-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-present',
        '2.21.0',
        False,
        ' Network ansible-docker-test-19ffba88-start-stop_default  Creating\n'
        ' Network ansible-docker-test-19ffba88-start-stop_default  Created\n'
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Creating\n'
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Created\n'
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Starting\n'
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-present',
        '2.21.0',
        False,
        ' Network ansible-docker-test-1f1d0d58-start-stop_default  Creating\n'
        ' Network ansible-docker-test-1f1d0d58-start-stop_default  Created\n'
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Creating\n'
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Created\n'
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Starting\n'
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-present',
        '2.21.0',
        False,
        ' Network ansible-docker-test-2460e737-start-stop_default  Creating\n'
        ' Network ansible-docker-test-2460e737-start-stop_default  Created\n'
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Creating\n'
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Created\n'
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Starting\n'
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present',
        '2.21.0',
        False,
        ' Network ansible-docker-test-4baa7139-start-stop_default  Creating\n'
        ' Network ansible-docker-test-4baa7139-start-stop_default  Created\n'
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Creating\n'
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Created\n'
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Starting\n'
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-present',
        '2.21.0',
        False,
        ' Network ansible-docker-test-5f3d2e16-start-stop_default  Creating\n'
        ' Network ansible-docker-test-5f3d2e16-start-stop_default  Created\n'
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Creating\n'
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Created\n'
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Starting\n'
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-present',
        '2.21.0',
        False,
        ' Network ansible-docker-test-601188b1-start-stop_default  Creating\n'
        ' Network ansible-docker-test-601188b1-start-stop_default  Created\n'
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Creating\n'
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Created\n'
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Starting\n'
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-present',
        '2.21.0',
        False,
        ' Network ansible-docker-test-64d917f4-start-stop_default  Creating\n'
        ' Network ansible-docker-test-64d917f4-start-stop_default  Created\n'
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Creating\n'
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Created\n'
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Starting\n'
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-present',
        '2.21.0',
        False,
        ' Network ansible-docker-test-6aaaa304-start-stop_default  Creating\n'
        ' Network ansible-docker-test-6aaaa304-start-stop_default  Created\n'
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Creating\n'
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Created\n'
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Starting\n'
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present',
        '2.21.0',
        False,
        ' Network ansible-docker-test-ce1fa4d7-start-stop_default  Creating\n'
        ' Network ansible-docker-test-ce1fa4d7-start-stop_default  Created\n'
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Creating\n'
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Created\n'
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Starting\n'
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-present',
        '2.21.0',
        False,
        ' Network ansible-docker-test-d1d30700-start-stop_default  Creating\n'
        ' Network ansible-docker-test-d1d30700-start-stop_default  Created\n'
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Creating\n'
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Created\n'
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Starting\n'
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-present',
        '2.21.0',
        False,
        ' Network ansible-docker-test-d6ae094c-start-stop_default  Creating\n'
        ' Network ansible-docker-test-d6ae094c-start-stop_default  Created\n'
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Creating\n'
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Created\n'
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Starting\n'
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
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
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 71e7a319c23_ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 71e7a319c23_ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                '71e7a319c23_ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                '71e7a319c23_ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
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
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 26bf8ff1675_ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 26bf8ff1675_ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                '26bf8ff1675_ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                '26bf8ff1675_ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
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
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 6dc8d091c94_ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 6dc8d091c94_ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                '6dc8d091c94_ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                '6dc8d091c94_ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
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
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 71b893893dc_ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 71b893893dc_ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                '71b893893dc_ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                '71b893893dc_ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
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
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container f6416652e13_ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Starting\n'
        ' DRY-RUN MODE -  Container f6416652e13_ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                'f6416652e13_ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'f6416652e13_ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
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
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container efe8857a191_ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Starting\n'
        ' DRY-RUN MODE -  Container efe8857a191_ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                'efe8857a191_ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'efe8857a191_ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
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
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 4b568108657_ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 4b568108657_ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                '4b568108657_ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                '4b568108657_ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
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
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 78e827e6673_ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 78e827e6673_ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                '78e827e6673_ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                '78e827e6673_ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
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
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container e508faa8323_ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Starting\n'
        ' DRY-RUN MODE -  Container e508faa8323_ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                'e508faa8323_ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'e508faa8323_ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
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
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container 0a77f424a61_ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Starting\n'
        ' DRY-RUN MODE -  Container 0a77f424a61_ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                '0a77f424a61_ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                '0a77f424a61_ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
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
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container dea4aafe907_ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Starting\n'
        ' DRY-RUN MODE -  Container dea4aafe907_ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                'dea4aafe907_ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'dea4aafe907_ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed)" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-present-(changed)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Recreate\n'
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Recreated\n'
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Starting\n'
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed)" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-present-(changed)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Recreate\n'
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Recreated\n'
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Starting\n'
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed)" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-present-(changed)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Recreate\n'
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Recreated\n'
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Starting\n'
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed)" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-(changed)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Recreate\n'
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Recreated\n'
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Starting\n'
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed)" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-present-(changed)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Recreate\n'
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Recreated\n'
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Starting\n'
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed)" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-present-(changed)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Recreate\n'
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Recreated\n'
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Starting\n'
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed)" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-present-(changed)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Recreate\n'
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Recreated\n'
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Starting\n'
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed)" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-present-(changed)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Recreate\n'
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Recreated\n'
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Starting\n'
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed)" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present-(changed)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Recreate\n'
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Recreated\n'
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Starting\n'
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed)" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-present-(changed)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Recreate\n'
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Recreated\n'
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Starting\n'
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed)" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-present-(changed)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Recreate\n'
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Recreated\n'
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Starting\n'
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
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
        ' DRY-RUN MODE -  Network ansible-docker-test-19ffba88-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-19ffba88-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
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
        ' DRY-RUN MODE -  Network ansible-docker-test-1f1d0d58-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-1f1d0d58-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
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
        ' DRY-RUN MODE -  Network ansible-docker-test-2460e737-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-2460e737-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
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
        ' DRY-RUN MODE -  Network ansible-docker-test-4baa7139-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-4baa7139-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
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
        ' DRY-RUN MODE -  Network ansible-docker-test-5f3d2e16-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-5f3d2e16-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
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
        ' DRY-RUN MODE -  Network ansible-docker-test-601188b1-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-601188b1-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
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
        ' DRY-RUN MODE -  Network ansible-docker-test-64d917f4-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-64d917f4-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
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
        ' DRY-RUN MODE -  Network ansible-docker-test-6aaaa304-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-6aaaa304-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
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
        ' DRY-RUN MODE -  Network ansible-docker-test-ce1fa4d7-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-ce1fa4d7-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
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
        ' DRY-RUN MODE -  Network ansible-docker-test-d1d30700-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-d1d30700-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
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
        ' DRY-RUN MODE -  Network ansible-docker-test-d6ae094c-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-d6ae094c-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-present-(idempotent-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-present-(idempotent-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-present-(idempotent-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-(idempotent-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-present-(idempotent-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-present-(idempotent-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-present-(idempotent-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-present-(idempotent-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present-(idempotent-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-present-(idempotent-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-present-(idempotent-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent)" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-present-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent)" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-present-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent)" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-present-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent)" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent)" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-present-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent)" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-present-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent)" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-present-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent)" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-present-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent)" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent)" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-present-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent)" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-present-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-present-stopped',
        '2.21.0',
        False,
        ' Network ansible-docker-test-19ffba88-start-stop_default  Creating\n'
        ' Network ansible-docker-test-19ffba88-start-stop_default  Created\n'
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Creating\n'
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-present-stopped',
        '2.21.0',
        False,
        ' Network ansible-docker-test-1f1d0d58-start-stop_default  Creating\n'
        ' Network ansible-docker-test-1f1d0d58-start-stop_default  Created\n'
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Creating\n'
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-present-stopped',
        '2.21.0',
        False,
        ' Network ansible-docker-test-2460e737-start-stop_default  Creating\n'
        ' Network ansible-docker-test-2460e737-start-stop_default  Created\n'
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Creating\n'
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-stopped',
        '2.21.0',
        False,
        ' Network ansible-docker-test-4baa7139-start-stop_default  Creating\n'
        ' Network ansible-docker-test-4baa7139-start-stop_default  Created\n'
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Creating\n'
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-present-stopped',
        '2.21.0',
        False,
        ' Network ansible-docker-test-5f3d2e16-start-stop_default  Creating\n'
        ' Network ansible-docker-test-5f3d2e16-start-stop_default  Created\n'
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Creating\n'
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-present-stopped',
        '2.21.0',
        False,
        ' Network ansible-docker-test-601188b1-start-stop_default  Creating\n'
        ' Network ansible-docker-test-601188b1-start-stop_default  Created\n'
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Creating\n'
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-present-stopped',
        '2.21.0',
        False,
        ' Network ansible-docker-test-64d917f4-start-stop_default  Creating\n'
        ' Network ansible-docker-test-64d917f4-start-stop_default  Created\n'
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Creating\n'
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-present-stopped',
        '2.21.0',
        False,
        ' Network ansible-docker-test-6aaaa304-start-stop_default  Creating\n'
        ' Network ansible-docker-test-6aaaa304-start-stop_default  Created\n'
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Creating\n'
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present-stopped',
        '2.21.0',
        False,
        ' Network ansible-docker-test-ce1fa4d7-start-stop_default  Creating\n'
        ' Network ansible-docker-test-ce1fa4d7-start-stop_default  Created\n'
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Creating\n'
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-present-stopped',
        '2.21.0',
        False,
        ' Network ansible-docker-test-d1d30700-start-stop_default  Creating\n'
        ' Network ansible-docker-test-d1d30700-start-stop_default  Created\n'
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Creating\n'
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-present-stopped',
        '2.21.0',
        False,
        ' Network ansible-docker-test-d6ae094c-start-stop_default  Creating\n'
        ' Network ansible-docker-test-d6ae094c-start-stop_default  Created\n'
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Creating\n'
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped (check)" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-present-stopped-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-19ffba88-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-19ffba88-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped (check)" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-present-stopped-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-1f1d0d58-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-1f1d0d58-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped (check)" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-present-stopped-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-2460e737-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-2460e737-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped (check)" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-stopped-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-4baa7139-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-4baa7139-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped (check)" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-present-stopped-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-5f3d2e16-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-5f3d2e16-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped (check)" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-present-stopped-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-601188b1-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-601188b1-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped (check)" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-present-stopped-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-64d917f4-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-64d917f4-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped (check)" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-present-stopped-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-6aaaa304-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-6aaaa304-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped (check)" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present-stopped-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-ce1fa4d7-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-ce1fa4d7-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped (check)" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-present-stopped-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-d1d30700-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-d1d30700-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped (check)" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-present-stopped-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-d6ae094c-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-d6ae094c-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-present-with-pull=always',
        '2.21.0',
        False,
        ' ansible-docker-test-19ffba88-cont Pulling \n'
        ' ansible-docker-test-19ffba88-cont Pulled \n'
        ' Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Running\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-19ffba88-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-19ffba88-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-present-with-pull=always',
        '2.21.0',
        False,
        ' ansible-docker-test-1f1d0d58-cont Pulling \n'
        ' ansible-docker-test-1f1d0d58-cont Pulled \n'
        ' Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Running\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-1f1d0d58-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-1f1d0d58-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-present-with-pull=always',
        '2.21.0',
        False,
        ' ansible-docker-test-2460e737-cont Pulling \n'
        ' ansible-docker-test-2460e737-cont Pulled \n'
        ' Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Running\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-2460e737-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-2460e737-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-with-pull=always',
        '2.21.0',
        False,
        ' ansible-docker-test-4baa7139-cont Pulling \n'
        ' ansible-docker-test-4baa7139-cont Pulled \n'
        ' Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Running\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-4baa7139-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-4baa7139-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-present-with-pull=always',
        '2.21.0',
        False,
        ' ansible-docker-test-5f3d2e16-cont Pulling \n'
        ' ansible-docker-test-5f3d2e16-cont Pulled \n'
        ' Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Running\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-5f3d2e16-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-5f3d2e16-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-present-with-pull=always',
        '2.21.0',
        False,
        ' ansible-docker-test-601188b1-cont Pulling \n'
        ' ansible-docker-test-601188b1-cont Pulled \n'
        ' Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Running\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-601188b1-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-601188b1-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-present-with-pull=always',
        '2.21.0',
        False,
        ' ansible-docker-test-64d917f4-cont Pulling \n'
        ' ansible-docker-test-64d917f4-cont Pulled \n'
        ' Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Running\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-64d917f4-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-64d917f4-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-present-with-pull=always',
        '2.21.0',
        False,
        ' ansible-docker-test-6aaaa304-cont Pulling \n'
        ' ansible-docker-test-6aaaa304-cont Pulled \n'
        ' Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Running\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-6aaaa304-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-6aaaa304-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present-with-pull=always',
        '2.21.0',
        False,
        ' ansible-docker-test-ce1fa4d7-cont Pulling \n'
        ' ansible-docker-test-ce1fa4d7-cont Pulled \n'
        ' Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Running\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-ce1fa4d7-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-ce1fa4d7-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-present-with-pull=always',
        '2.21.0',
        False,
        ' ansible-docker-test-d1d30700-cont Pulling \n'
        ' ansible-docker-test-d1d30700-cont Pulled \n'
        ' Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Running\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-d1d30700-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-d1d30700-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-present-with-pull=always',
        '2.21.0',
        False,
        ' ansible-docker-test-d6ae094c-cont Pulling \n'
        ' ansible-docker-test-d6ae094c-cont Pulled \n'
        ' Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Running\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-d6ae094c-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-d6ae094c-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Running',
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
        ' DRY-RUN MODE -  ansible-docker-test-19ffba88-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-19ffba88-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container fa8f62dfced_ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container fa8f62dfced_ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-19ffba88-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-19ffba88-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                'fa8f62dfced_ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'fa8f62dfced_ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-1f1d0d58-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-1f1d0d58-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container 0d5362bac93_ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container 0d5362bac93_ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-1f1d0d58-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-1f1d0d58-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                '0d5362bac93_ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                '0d5362bac93_ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-2460e737-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-2460e737-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container f48d54a75fb_ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container f48d54a75fb_ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-2460e737-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-2460e737-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                'f48d54a75fb_ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'f48d54a75fb_ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-4baa7139-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-4baa7139-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container ecd243ea972_ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container ecd243ea972_ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-4baa7139-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-4baa7139-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                'ecd243ea972_ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ecd243ea972_ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-5f3d2e16-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-5f3d2e16-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container c9d730c2613_ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container c9d730c2613_ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-5f3d2e16-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-5f3d2e16-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                'c9d730c2613_ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'c9d730c2613_ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-601188b1-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-601188b1-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container 611a044106b_ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container 611a044106b_ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-601188b1-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-601188b1-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                '611a044106b_ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                '611a044106b_ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-64d917f4-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-64d917f4-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container 8bec416e98d_ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container 8bec416e98d_ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-64d917f4-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-64d917f4-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                '8bec416e98d_ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                '8bec416e98d_ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-6aaaa304-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-6aaaa304-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container 5d30320650e_ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container 5d30320650e_ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-6aaaa304-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-6aaaa304-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                '5d30320650e_ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                '5d30320650e_ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-ce1fa4d7-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-ce1fa4d7-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container 61bd1b13d9c_ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container 61bd1b13d9c_ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-ce1fa4d7-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-ce1fa4d7-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                '61bd1b13d9c_ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                '61bd1b13d9c_ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-d1d30700-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-d1d30700-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container 3d7b7be6dbe_ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container 3d7b7be6dbe_ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-d1d30700-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-d1d30700-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                '3d7b7be6dbe_ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                '3d7b7be6dbe_ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-d6ae094c-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-d6ae094c-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container b78faf8a742_ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container b78faf8a742_ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-d6ae094c-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-d6ae094c-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                'b78faf8a742_ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'b78faf8a742_ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-present-with-pull=missing',
        '2.21.0',
        False,
        ' ansible-docker-test-19ffba88-cont Pulling \n'
        ' ansible-docker-test-19ffba88-cont Pulled \n'
        ' Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Creating\n'
        ' Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Created\n'
        ' Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Starting\n'
        ' Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-19ffba88-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-19ffba88-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-present-with-pull=missing',
        '2.21.0',
        False,
        ' ansible-docker-test-1f1d0d58-cont Pulling \n'
        ' ansible-docker-test-1f1d0d58-cont Pulled \n'
        ' Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Creating\n'
        ' Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Created\n'
        ' Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Starting\n'
        ' Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-1f1d0d58-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-1f1d0d58-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-present-with-pull=missing',
        '2.21.0',
        False,
        ' ansible-docker-test-2460e737-cont Pulling \n'
        ' ansible-docker-test-2460e737-cont Pulled \n'
        ' Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Creating\n'
        ' Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Created\n'
        ' Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Starting\n'
        ' Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-2460e737-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-2460e737-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-with-pull=missing',
        '2.21.0',
        False,
        ' ansible-docker-test-4baa7139-cont Pulling \n'
        ' ansible-docker-test-4baa7139-cont Pulled \n'
        ' Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Creating\n'
        ' Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Created\n'
        ' Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Starting\n'
        ' Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-4baa7139-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-4baa7139-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-present-with-pull=missing',
        '2.21.0',
        False,
        ' ansible-docker-test-5f3d2e16-cont Pulling \n'
        ' ansible-docker-test-5f3d2e16-cont Pulled \n'
        ' Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Creating\n'
        ' Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Created\n'
        ' Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Starting\n'
        ' Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-5f3d2e16-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-5f3d2e16-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-present-with-pull=missing',
        '2.21.0',
        False,
        ' ansible-docker-test-601188b1-cont Pulling \n'
        ' ansible-docker-test-601188b1-cont Pulled \n'
        ' Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Creating\n'
        ' Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Created\n'
        ' Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Starting\n'
        ' Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-601188b1-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-601188b1-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-present-with-pull=missing',
        '2.21.0',
        False,
        ' ansible-docker-test-64d917f4-cont Pulling \n'
        ' ansible-docker-test-64d917f4-cont Pulled \n'
        ' Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Creating\n'
        ' Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Created\n'
        ' Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Starting\n'
        ' Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-64d917f4-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-64d917f4-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-present-with-pull=missing',
        '2.21.0',
        False,
        ' ansible-docker-test-6aaaa304-cont Pulling \n'
        ' ansible-docker-test-6aaaa304-cont Pulled \n'
        ' Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Creating\n'
        ' Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Created\n'
        ' Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Starting\n'
        ' Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-6aaaa304-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-6aaaa304-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present-with-pull=missing',
        '2.21.0',
        False,
        ' ansible-docker-test-ce1fa4d7-cont Pulling \n'
        ' ansible-docker-test-ce1fa4d7-cont Pulled \n'
        ' Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Creating\n'
        ' Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Created\n'
        ' Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Starting\n'
        ' Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-ce1fa4d7-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-ce1fa4d7-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-present-with-pull=missing',
        '2.21.0',
        False,
        ' ansible-docker-test-d1d30700-cont Pulling \n'
        ' ansible-docker-test-d1d30700-cont Pulled \n'
        ' Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Creating\n'
        ' Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Created\n'
        ' Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Starting\n'
        ' Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-d1d30700-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-d1d30700-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-present-with-pull=missing',
        '2.21.0',
        False,
        ' ansible-docker-test-d6ae094c-cont Pulling \n'
        ' ansible-docker-test-d6ae094c-cont Pulled \n'
        ' Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Creating\n'
        ' Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Created\n'
        ' Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Starting\n'
        ' Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-d6ae094c-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-d6ae094c-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-19ffba88-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-19ffba88-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-19ffba88-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-19ffba88-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-1f1d0d58-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-1f1d0d58-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-1f1d0d58-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-1f1d0d58-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-2460e737-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-2460e737-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-2460e737-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-2460e737-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-4baa7139-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-4baa7139-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-4baa7139-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-4baa7139-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-5f3d2e16-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-5f3d2e16-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-5f3d2e16-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-5f3d2e16-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-601188b1-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-601188b1-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-601188b1-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-601188b1-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-64d917f4-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-64d917f4-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-64d917f4-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-64d917f4-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-6aaaa304-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-6aaaa304-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-6aaaa304-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-6aaaa304-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-ce1fa4d7-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-ce1fa4d7-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-ce1fa4d7-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-ce1fa4d7-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-d1d30700-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-d1d30700-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-d1d30700-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-d1d30700-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-d6ae094c-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-d6ae094c-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-d6ae094c-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-d6ae094c-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent,-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent,-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent,-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent,-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent,-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent,-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent,-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent,-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent,-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent,-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent,-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        ' Network ansible-docker-test-19ffba88-pull_default  Creating\n'
        ' Network ansible-docker-test-19ffba88-pull_default  Created\n'
        ' Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Creating\n'
        ' Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Created\n'
        ' Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Starting\n'
        ' Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        ' Network ansible-docker-test-19ffba88-pull_default  Creating\n'
        ' Network ansible-docker-test-19ffba88-pull_default  Created\n'
        ' Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Creating\n'
        'Error response from daemon: no such image: does-not-exist:latest: No such image: does-not-exist:latest\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'unknown',
                '',
                'Error',
                'Error response from daemon: no such image: does-not-exist:latest: No such image: does-not-exist:latest',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        ' Network ansible-docker-test-1f1d0d58-pull_default  Creating\n'
        ' Network ansible-docker-test-1f1d0d58-pull_default  Created\n'
        ' Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Creating\n'
        ' Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Created\n'
        ' Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Starting\n'
        ' Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        ' Network ansible-docker-test-1f1d0d58-pull_default  Creating\n'
        ' Network ansible-docker-test-1f1d0d58-pull_default  Created\n'
        ' Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Creating\n'
        'Error response from daemon: no such image: does-not-exist:latest: No such image: does-not-exist:latest\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'unknown',
                '',
                'Error',
                'Error response from daemon: no such image: does-not-exist:latest: No such image: does-not-exist:latest',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        ' Network ansible-docker-test-2460e737-pull_default  Creating\n'
        ' Network ansible-docker-test-2460e737-pull_default  Created\n'
        ' Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Creating\n'
        ' Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Created\n'
        ' Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Starting\n'
        ' Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        ' Network ansible-docker-test-2460e737-pull_default  Creating\n'
        ' Network ansible-docker-test-2460e737-pull_default  Created\n'
        ' Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Creating\n'
        'Error response from daemon: no such image: does-not-exist:latest: No such image: does-not-exist:latest\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'unknown',
                '',
                'Error',
                'Error response from daemon: no such image: does-not-exist:latest: No such image: does-not-exist:latest',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        ' Network ansible-docker-test-4baa7139-pull_default  Creating\n'
        ' Network ansible-docker-test-4baa7139-pull_default  Created\n'
        ' Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Creating\n'
        ' Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Created\n'
        ' Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Starting\n'
        ' Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        ' Network ansible-docker-test-4baa7139-pull_default  Creating\n'
        ' Network ansible-docker-test-4baa7139-pull_default  Created\n'
        ' Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Creating\n'
        'Error response from daemon: No such image: does-not-exist:latest\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'unknown',
                '',
                'Error',
                'Error response from daemon: No such image: does-not-exist:latest',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        ' Network ansible-docker-test-5f3d2e16-pull_default  Creating\n'
        ' Network ansible-docker-test-5f3d2e16-pull_default  Created\n'
        ' Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Creating\n'
        ' Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Created\n'
        ' Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Starting\n'
        ' Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        ' Network ansible-docker-test-5f3d2e16-pull_default  Creating\n'
        ' Network ansible-docker-test-5f3d2e16-pull_default  Created\n'
        ' Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Creating\n'
        'Error response from daemon: no such image: does-not-exist:latest: No such image: does-not-exist:latest\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'unknown',
                '',
                'Error',
                'Error response from daemon: no such image: does-not-exist:latest: No such image: does-not-exist:latest',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        ' Network ansible-docker-test-601188b1-pull_default  Creating\n'
        ' Network ansible-docker-test-601188b1-pull_default  Created\n'
        ' Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Creating\n'
        ' Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Created\n'
        ' Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Starting\n'
        ' Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        ' Network ansible-docker-test-601188b1-pull_default  Creating\n'
        ' Network ansible-docker-test-601188b1-pull_default  Created\n'
        ' Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Creating\n'
        'Error response from daemon: No such image: does-not-exist:latest\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'unknown',
                '',
                'Error',
                'Error response from daemon: No such image: does-not-exist:latest',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        ' Network ansible-docker-test-64d917f4-pull_default  Creating\n'
        ' Network ansible-docker-test-64d917f4-pull_default  Created\n'
        ' Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Creating\n'
        ' Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Created\n'
        ' Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Starting\n'
        ' Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        ' Network ansible-docker-test-64d917f4-pull_default  Creating\n'
        ' Network ansible-docker-test-64d917f4-pull_default  Created\n'
        ' Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Creating\n'
        'Error response from daemon: No such image: does-not-exist:latest\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'unknown',
                '',
                'Error',
                'Error response from daemon: No such image: does-not-exist:latest',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        ' Network ansible-docker-test-6aaaa304-pull_default  Creating\n'
        ' Network ansible-docker-test-6aaaa304-pull_default  Created\n'
        ' Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Creating\n'
        ' Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Created\n'
        ' Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Starting\n'
        ' Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        ' Network ansible-docker-test-6aaaa304-pull_default  Creating\n'
        ' Network ansible-docker-test-6aaaa304-pull_default  Created\n'
        ' Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Creating\n'
        'Error response from daemon: no such image: does-not-exist:latest: No such image: does-not-exist:latest\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'unknown',
                '',
                'Error',
                'Error response from daemon: no such image: does-not-exist:latest: No such image: does-not-exist:latest',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        ' Network ansible-docker-test-ce1fa4d7-pull_default  Creating\n'
        ' Network ansible-docker-test-ce1fa4d7-pull_default  Created\n'
        ' Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Creating\n'
        ' Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Created\n'
        ' Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Starting\n'
        ' Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        ' Network ansible-docker-test-ce1fa4d7-pull_default  Creating\n'
        ' Network ansible-docker-test-ce1fa4d7-pull_default  Created\n'
        ' Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Creating\n'
        'Error response from daemon: no such image: does-not-exist:latest: No such image: does-not-exist:latest\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'unknown',
                '',
                'Error',
                'Error response from daemon: no such image: does-not-exist:latest: No such image: does-not-exist:latest',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        ' Network ansible-docker-test-d1d30700-pull_default  Creating\n'
        ' Network ansible-docker-test-d1d30700-pull_default  Created\n'
        ' Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Creating\n'
        ' Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Created\n'
        ' Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Starting\n'
        ' Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        ' Network ansible-docker-test-d1d30700-pull_default  Creating\n'
        ' Network ansible-docker-test-d1d30700-pull_default  Created\n'
        ' Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Creating\n'
        'Error response from daemon: No such image: does-not-exist:latest\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'unknown',
                '',
                'Error',
                'Error response from daemon: No such image: does-not-exist:latest',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        ' Network ansible-docker-test-d6ae094c-pull_default  Creating\n'
        ' Network ansible-docker-test-d6ae094c-pull_default  Created\n'
        ' Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Creating\n'
        ' Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Created\n'
        ' Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Starting\n'
        ' Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.21.0',
        False,
        ' Network ansible-docker-test-d6ae094c-pull_default  Creating\n'
        ' Network ansible-docker-test-d6ae094c-pull_default  Created\n'
        ' Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Creating\n'
        'Error response from daemon: No such image: does-not-exist:latest\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'unknown',
                '',
                'Error',
                'Error response from daemon: No such image: does-not-exist:latest',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-19ffba88-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-19ffba88-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-19ffba88-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-19ffba88-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-1f1d0d58-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-1f1d0d58-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-1f1d0d58-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-1f1d0d58-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-2460e737-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-2460e737-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-2460e737-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-2460e737-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-4baa7139-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-4baa7139-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-4baa7139-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-4baa7139-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-5f3d2e16-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-5f3d2e16-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-5f3d2e16-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-5f3d2e16-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-601188b1-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-601188b1-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-601188b1-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-601188b1-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-64d917f4-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-64d917f4-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-64d917f4-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-64d917f4-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-6aaaa304-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-6aaaa304-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-6aaaa304-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-6aaaa304-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-ce1fa4d7-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-ce1fa4d7-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-ce1fa4d7-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-ce1fa4d7-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-d1d30700-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-d1d30700-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-d1d30700-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-d1d30700-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-d6ae094c-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-d6ae094c-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-d6ae094c-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-d6ae094c-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent,-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent,-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent,-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent,-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent,-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent,-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent,-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent,-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent,-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent,-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent,-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-present-without-explicit-pull',
        '2.21.0',
        False,
        ' ansible-docker-test-19ffba88-cont Pulling \n'
        ' ansible-docker-test-19ffba88-cont Error \n'
        "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied\n",  # noqa: E501
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-19ffba88-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-19ffba88-cont',
                'Error',
                "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied",  # noqa: E501
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-present-without-explicit-pull',
        '2.21.0',
        False,
        ' ansible-docker-test-1f1d0d58-cont Pulling \n'
        ' ansible-docker-test-1f1d0d58-cont Error \n'
        "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied\n",  # noqa: E501
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-1f1d0d58-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-1f1d0d58-cont',
                'Error',
                "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied",  # noqa: E501
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-present-without-explicit-pull',
        '2.21.0',
        False,
        ' ansible-docker-test-2460e737-cont Pulling \n'
        ' ansible-docker-test-2460e737-cont Error \n'
        "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied\n",  # noqa: E501
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-2460e737-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-2460e737-cont',
                'Error',
                "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied",  # noqa: E501
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-without-explicit-pull',
        '2.21.0',
        False,
        ' ansible-docker-test-4baa7139-cont Pulling \n'
        ' ansible-docker-test-4baa7139-cont Error \n'
        "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied\n",  # noqa: E501
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-4baa7139-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-4baa7139-cont',
                'Error',
                "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied",  # noqa: E501
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-present-without-explicit-pull',
        '2.21.0',
        False,
        ' ansible-docker-test-5f3d2e16-cont Pulling \n'
        ' ansible-docker-test-5f3d2e16-cont Error \n'
        "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied\n",  # noqa: E501
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-5f3d2e16-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-5f3d2e16-cont',
                'Error',
                "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied",  # noqa: E501
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-present-without-explicit-pull',
        '2.21.0',
        False,
        ' ansible-docker-test-601188b1-cont Pulling \n'
        ' ansible-docker-test-601188b1-cont Error \n'
        "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied\n",  # noqa: E501
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-601188b1-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-601188b1-cont',
                'Error',
                "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied",  # noqa: E501
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-present-without-explicit-pull',
        '2.21.0',
        False,
        ' ansible-docker-test-64d917f4-cont Pulling \n'
        ' ansible-docker-test-64d917f4-cont Error \n'
        "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied\n",  # noqa: E501
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-64d917f4-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-64d917f4-cont',
                'Error',
                "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied",  # noqa: E501
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-present-without-explicit-pull',
        '2.21.0',
        False,
        ' ansible-docker-test-6aaaa304-cont Pulling \n'
        ' ansible-docker-test-6aaaa304-cont Error \n'
        "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied\n",  # noqa: E501
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-6aaaa304-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-6aaaa304-cont',
                'Error',
                "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied",  # noqa: E501
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present-without-explicit-pull',
        '2.21.0',
        False,
        ' ansible-docker-test-ce1fa4d7-cont Pulling \n'
        ' ansible-docker-test-ce1fa4d7-cont Error \n'
        "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied\n",  # noqa: E501
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-ce1fa4d7-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-ce1fa4d7-cont',
                'Error',
                "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied",  # noqa: E501
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-present-without-explicit-pull',
        '2.21.0',
        False,
        ' ansible-docker-test-d1d30700-cont Pulling \n'
        ' ansible-docker-test-d1d30700-cont Error \n'
        "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied\n",  # noqa: E501
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-d1d30700-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-d1d30700-cont',
                'Error',
                "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied",  # noqa: E501
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-present-without-explicit-pull',
        '2.21.0',
        False,
        ' ansible-docker-test-d6ae094c-cont Pulling \n'
        ' ansible-docker-test-d6ae094c-cont Error \n'
        "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied\n",  # noqa: E501
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-d6ae094c-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-d6ae094c-cont',
                'Error',
                "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied",  # noqa: E501
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-present-without-explicit-pull-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  ansible-docker-test-19ffba88-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-19ffba88-cont Error \n'
        'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-19ffba88-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-19ffba88-cont',
                'Error',
                'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-present-without-explicit-pull-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  ansible-docker-test-1f1d0d58-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-1f1d0d58-cont Error \n'
        'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-1f1d0d58-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-1f1d0d58-cont',
                'Error',
                'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-present-without-explicit-pull-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  ansible-docker-test-2460e737-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-2460e737-cont Error \n'
        'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-2460e737-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-2460e737-cont',
                'Error',
                'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-present-without-explicit-pull-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  ansible-docker-test-4baa7139-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-4baa7139-cont Error \n'
        'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-4baa7139-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-4baa7139-cont',
                'Error',
                'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-present-without-explicit-pull-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  ansible-docker-test-5f3d2e16-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-5f3d2e16-cont Error \n'
        'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-5f3d2e16-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-5f3d2e16-cont',
                'Error',
                'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-present-without-explicit-pull-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  ansible-docker-test-601188b1-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-601188b1-cont Error \n'
        'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-601188b1-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-601188b1-cont',
                'Error',
                'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-present-without-explicit-pull-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  ansible-docker-test-64d917f4-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-64d917f4-cont Error \n'
        'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-64d917f4-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-64d917f4-cont',
                'Error',
                'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-present-without-explicit-pull-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  ansible-docker-test-6aaaa304-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-6aaaa304-cont Error \n'
        'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-6aaaa304-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-6aaaa304-cont',
                'Error',
                'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-present-without-explicit-pull-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  ansible-docker-test-ce1fa4d7-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-ce1fa4d7-cont Error \n'
        'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-ce1fa4d7-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-ce1fa4d7-cont',
                'Error',
                'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-present-without-explicit-pull-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  ansible-docker-test-d1d30700-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-d1d30700-cont Error \n'
        'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-d1d30700-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-d1d30700-cont',
                'Error',
                'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-present-without-explicit-pull-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  ansible-docker-test-d6ae094c-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-d6ae094c-cont Error \n'
        'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-d6ae094c-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-d6ae094c-cont',
                'Error',
                'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-restarted',
        '2.21.0',
        False,
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Restarting\n'
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-restarted',
        '2.21.0',
        False,
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Restarting\n'
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-restarted',
        '2.21.0',
        False,
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Restarting\n'
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-restarted',
        '2.21.0',
        False,
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Restarting\n'
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-restarted',
        '2.21.0',
        False,
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Restarting\n'
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-restarted',
        '2.21.0',
        False,
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Restarting\n'
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-restarted',
        '2.21.0',
        False,
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Restarting\n'
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-restarted',
        '2.21.0',
        False,
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Restarting\n'
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-restarted',
        '2.21.0',
        False,
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Restarting\n'
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-restarted',
        '2.21.0',
        False,
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Restarting\n'
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-restarted',
        '2.21.0',
        False,
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Restarting\n'
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-restarted',
        '2.21.0',
        False,
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Restarting\n'
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-restarted',
        '2.21.0',
        False,
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Restarting\n'
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-restarted',
        '2.21.0',
        False,
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Restarting\n'
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-restarted',
        '2.21.0',
        False,
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Restarting\n'
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-restarted',
        '2.21.0',
        False,
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Restarting\n'
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-restarted',
        '2.21.0',
        False,
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Restarting\n'
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-restarted',
        '2.21.0',
        False,
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Restarting\n'
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-restarted',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Restarting\n'
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-restarted',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Restarting\n'
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-restarted',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Restarting\n'
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-restarted',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Restarting\n'
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-started',
        '2.21.0',
        False,
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Starting\n'
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-started',
        '2.21.0',
        False,
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Starting\n'
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-started',
        '2.21.0',
        False,
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Starting\n'
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-started',
        '2.21.0',
        False,
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Starting\n'
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-started',
        '2.21.0',
        False,
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Starting\n'
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-started',
        '2.21.0',
        False,
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Starting\n'
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-started',
        '2.21.0',
        False,
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Starting\n'
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-started',
        '2.21.0',
        False,
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Starting\n'
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-started',
        '2.21.0',
        False,
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Starting\n'
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-started',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Starting\n'
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-started',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Starting\n'
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (check)" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-started-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Starting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (check)" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-started-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Starting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (check)" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-started-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Starting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (check)" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-started-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Starting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (check)" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-started-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Starting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (check)" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-started-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Starting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (check)" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-started-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Starting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (check)" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-started-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Starting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (check)" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-started-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Starting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (check)" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-started-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Starting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (check)" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-started-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Starting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-started-(idempotent-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-started-(idempotent-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-started-(idempotent-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-started-(idempotent-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-started-(idempotent-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-started-(idempotent-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-started-(idempotent-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-started-(idempotent-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-started-(idempotent-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-started-(idempotent-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-started-(idempotent-check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent)" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-started-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent)" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-started-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent)" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-started-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent)" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-started-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent)" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-started-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent)" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-started-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent)" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-started-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent)" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-started-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent)" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-started-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent)" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-started-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent)" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-started-(idempotent)',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-stopped',
        '2.21.0',
        False,
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Running\n'
        '\n'
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Stopping\n'
        ' Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-stopped',
        '2.21.0',
        False,
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Running\n'
        '\n'
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Stopping\n'
        ' Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-stopped',
        '2.21.0',
        False,
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Running\n'
        '\n'
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Stopping\n'
        ' Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-stopped',
        '2.21.0',
        False,
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Running\n'
        '\n'
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Stopping\n'
        ' Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-stopped',
        '2.21.0',
        False,
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Running\n'
        '\n'
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Stopping\n'
        ' Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-stopped',
        '2.21.0',
        False,
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Running\n'
        '\n'
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Stopping\n'
        ' Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-stopped',
        '2.21.0',
        False,
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Running\n'
        '\n'
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Stopping\n'
        ' Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-stopped',
        '2.21.0',
        False,
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Running\n'
        '\n'
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Stopping\n'
        ' Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-stopped',
        '2.21.0',
        False,
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Running\n'
        '\n'
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Stopping\n'
        ' Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-stopped',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Running\n'
        '\n'
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Stopping\n'
        ' Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-stopped',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Running\n'
        '\n'
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Stopping\n'
        ' Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped (check)" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-stopped-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Running\n'
        '\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-start-stop-ansible-docker-test-19ffba88-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped (check)" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-stopped-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Running\n'
        '\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-start-stop-ansible-docker-test-1f1d0d58-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped (check)" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-stopped-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Running\n'
        '\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-start-stop-ansible-docker-test-2460e737-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped (check)" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-stopped-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Running\n'
        '\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-start-stop-ansible-docker-test-4baa7139-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped (check)" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-stopped-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Running\n'
        '\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-start-stop-ansible-docker-test-5f3d2e16-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped (check)" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-stopped-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Running\n'
        '\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-start-stop-ansible-docker-test-601188b1-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped (check)" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-stopped-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Running\n'
        '\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-start-stop-ansible-docker-test-64d917f4-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped (check)" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-stopped-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Running\n'
        '\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-start-stop-ansible-docker-test-6aaaa304-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped (check)" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-stopped-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Running\n'
        '\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-start-stop-ansible-docker-test-ce1fa4d7-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped (check)" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-stopped-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Running\n'
        '\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-start-stop-ansible-docker-test-d1d30700-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped (check)" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-stopped-(check)',
        '2.21.0',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Running\n'
        '\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-start-stop-ansible-docker-test-d6ae094c-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopping service" on 2024-01-07 in devel-debian-bullseye
    (
        '2.21.0-devel-debian-bullseye-2024-01-07-docker_compose_v2-stopping-service',
        '2.21.0',
        False,
        ' Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Stopping\n'
        ' Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Stopped\n'
        ' Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Removing\n'
        ' Container ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1  Removed\n'
        ' Network ansible-docker-test-19ffba88-pull_default  Removing\n'
        ' Network ansible-docker-test-19ffba88-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-19ffba88-pull-ansible-docker-test-19ffba88-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-19ffba88-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopping service" on 2024-01-07 in devel-ubuntu2204
    (
        '2.21.0-devel-ubuntu2204-2024-01-07-docker_compose_v2-stopping-service',
        '2.21.0',
        False,
        ' Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Stopping\n'
        ' Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Stopped\n'
        ' Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Removing\n'
        ' Container ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1  Removed\n'
        ' Network ansible-docker-test-1f1d0d58-pull_default  Removing\n'
        ' Network ansible-docker-test-1f1d0d58-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-1f1d0d58-pull-ansible-docker-test-1f1d0d58-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-1f1d0d58-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopping service" on 2024-01-07 in devel-ubuntu2004
    (
        '2.21.0-devel-ubuntu2004-2024-01-07-docker_compose_v2-stopping-service',
        '2.21.0',
        False,
        ' Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Stopping\n'
        ' Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Stopped\n'
        ' Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Removing\n'
        ' Container ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1  Removed\n'
        ' Network ansible-docker-test-2460e737-pull_default  Removing\n'
        ' Network ansible-docker-test-2460e737-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-2460e737-pull-ansible-docker-test-2460e737-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-2460e737-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopping service" on 2024-01-07 in 2.14-rhel9.0
    (
        '2.21.0-2.14-rhel9.0-2024-01-07-docker_compose_v2-stopping-service',
        '2.21.0',
        False,
        ' Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Stopping\n'
        ' Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Stopped\n'
        ' Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Removing\n'
        ' Container ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1  Removed\n'
        ' Network ansible-docker-test-4baa7139-pull_default  Removing\n'
        ' Network ansible-docker-test-4baa7139-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-4baa7139-pull-ansible-docker-test-4baa7139-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-4baa7139-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopping service" on 2024-01-07 in devel-debian-bookworm
    (
        '2.21.0-devel-debian-bookworm-2024-01-07-docker_compose_v2-stopping-service',
        '2.21.0',
        False,
        ' Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Stopping\n'
        ' Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Stopped\n'
        ' Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Removing\n'
        ' Container ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1  Removed\n'
        ' Network ansible-docker-test-5f3d2e16-pull_default  Removing\n'
        ' Network ansible-docker-test-5f3d2e16-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-5f3d2e16-pull-ansible-docker-test-5f3d2e16-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-5f3d2e16-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopping service" on 2024-01-07 in 2.15-rhel7.9
    (
        '2.21.0-2.15-rhel7.9-2024-01-07-docker_compose_v2-stopping-service',
        '2.21.0',
        False,
        ' Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Stopping\n'
        ' Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Stopped\n'
        ' Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Removing\n'
        ' Container ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1  Removed\n'
        ' Network ansible-docker-test-601188b1-pull_default  Removing\n'
        ' Network ansible-docker-test-601188b1-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-601188b1-pull-ansible-docker-test-601188b1-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-601188b1-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopping service" on 2024-01-07 in devel-rhel9.3
    (
        '2.21.0-devel-rhel9.3-2024-01-07-docker_compose_v2-stopping-service',
        '2.21.0',
        False,
        ' Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Stopping\n'
        ' Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Stopped\n'
        ' Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Removing\n'
        ' Container ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1  Removed\n'
        ' Network ansible-docker-test-64d917f4-pull_default  Removing\n'
        ' Network ansible-docker-test-64d917f4-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-64d917f4-pull-ansible-docker-test-64d917f4-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-64d917f4-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopping service" on 2024-01-07 in 2.16-centos7
    (
        '2.21.0-2.16-centos7-2024-01-07-docker_compose_v2-stopping-service',
        '2.21.0',
        False,
        ' Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Stopping\n'
        ' Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Stopped\n'
        ' Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Removing\n'
        ' Container ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1  Removed\n'
        ' Network ansible-docker-test-6aaaa304-pull_default  Removing\n'
        ' Network ansible-docker-test-6aaaa304-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-6aaaa304-pull-ansible-docker-test-6aaaa304-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-6aaaa304-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopping service" on 2024-01-07 in 2.15-centos7
    (
        '2.21.0-2.15-centos7-2024-01-07-docker_compose_v2-stopping-service',
        '2.21.0',
        False,
        ' Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Stopping\n'
        ' Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Stopped\n'
        ' Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Removing\n'
        ' Container ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1  Removed\n'
        ' Network ansible-docker-test-ce1fa4d7-pull_default  Removing\n'
        ' Network ansible-docker-test-ce1fa4d7-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-ce1fa4d7-pull-ansible-docker-test-ce1fa4d7-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-ce1fa4d7-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopping service" on 2024-01-07 in 2.16-rhel9.2
    (
        '2.21.0-2.16-rhel9.2-2024-01-07-docker_compose_v2-stopping-service',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Stopping\n'
        ' Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Stopped\n'
        ' Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Removing\n'
        ' Container ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1  Removed\n'
        ' Network ansible-docker-test-d1d30700-pull_default  Removing\n'
        ' Network ansible-docker-test-d1d30700-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d1d30700-pull-ansible-docker-test-d1d30700-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d1d30700-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopping service" on 2024-01-07 in 2.15-rhel9.1
    (
        '2.21.0-2.15-rhel9.1-2024-01-07-docker_compose_v2-stopping-service',
        '2.21.0',
        False,
        ' Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Stopping\n'
        ' Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Stopped\n'
        ' Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Removing\n'
        ' Container ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1  Removed\n'
        ' Network ansible-docker-test-d6ae094c-pull_default  Removing\n'
        ' Network ansible-docker-test-d6ae094c-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-d6ae094c-pull-ansible-docker-test-d6ae094c-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-d6ae094c-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # #######################################################################################################################
    # ## Docker Compose 2.23.3 ##############################################################################################
    # #######################################################################################################################
    # docker_compose_v2: "Absent" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-absent',
        '2.23.3',
        False,
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Stopping\n'
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Stopped\n'
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Removing\n'
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Removed\n'
        ' Network ansible-docker-test-bc362ba-start-stop_default  Removing\n'
        ' Network ansible-docker-test-bc362ba-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Absent (check)" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-absent-(check)',
        '2.23.3',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Stopped\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Removing\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Removed\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-bc362ba-start-stop_default  Removing\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-bc362ba-start-stop_default  Resource is still in use\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-start-stop_default',
                None,
                'Resource is still in use',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-cleanup',
        '2.23.3',
        False,
        ' Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Stopping\n'
        ' Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Stopped\n'
        ' Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Removing\n'
        ' Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Removed\n'
        ' Network ansible-docker-test-bc362ba-pull_default  Removing\n'
        ' Network ansible-docker-test-bc362ba-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Cleanup" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-cleanup',
        '2.23.3',
        False,
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Stopping\n'
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Stopped\n'
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Removing\n'
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Removed\n'
        ' Network ansible-docker-test-bc362ba-start-stop_default  Removing\n'
        ' Network ansible-docker-test-bc362ba-start-stop_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-start-stop_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-start-stop_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present',
        '2.23.3',
        False,
        ' Network ansible-docker-test-bc362ba-start-stop_default  Creating\n'
        ' Network ansible-docker-test-bc362ba-start-stop_default  Created\n'
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Creating\n'
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Created\n'
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Starting\n'
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
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
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Recreated\n'
        ' DRY-RUN MODE -  Container df477f7889c_ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Starting\n'
        ' DRY-RUN MODE -  Container df477f7889c_ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                'df477f7889c_ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'df477f7889c_ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (changed)" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-(changed)',
        '2.23.3',
        False,
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Recreate\n'
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Recreated\n'
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Starting\n'
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
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
        ' DRY-RUN MODE -  Network ansible-docker-test-bc362ba-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-bc362ba-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent check)" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-(idempotent-check)',
        '2.23.3',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present (idempotent)" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-(idempotent)',
        '2.23.3',
        False,
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-stopped',
        '2.23.3',
        False,
        ' Network ansible-docker-test-bc362ba-start-stop_default  Creating\n'
        ' Network ansible-docker-test-bc362ba-start-stop_default  Created\n'
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Creating\n'
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present stopped (check)" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-stopped-(check)',
        '2.23.3',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-bc362ba-start-stop_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-bc362ba-start-stop_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Created\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-start-stop_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-start-stop_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Created',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=always" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-with-pull=always',
        '2.23.3',
        False,
        ' ansible-docker-test-bc362ba-cont Pulling \n'
        ' ansible-docker-test-bc362ba-cont Pulled \n'
        ' Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Running\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-bc362ba-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-bc362ba-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-bc362ba-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-bc362ba-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Recreate\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Recreated\n'
        ' DRY-RUN MODE -  Container 9f33f2ddb62_ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container 9f33f2ddb62_ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-bc362ba-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-bc362ba-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Recreate',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Recreated',
                None,
            ),
            ResourceEvent(
                'container',
                '9f33f2ddb62_ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                '9f33f2ddb62_ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-with-pull=missing',
        '2.23.3',
        False,
        ' ansible-docker-test-bc362ba-cont Pulling \n'
        ' ansible-docker-test-bc362ba-cont Pulled \n'
        ' Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Creating\n'
        ' Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Created\n'
        ' Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Starting\n'
        ' Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-bc362ba-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-bc362ba-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
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
        ' DRY-RUN MODE -  ansible-docker-test-bc362ba-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-bc362ba-cont Pulled \n'
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Started\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-bc362ba-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'service',
                'ansible-docker-test-bc362ba-cont',
                'Pulled',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent)" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent)',
        '2.23.3',
        False,
        ' Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=missing (idempotent, check)" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-with-pull=missing-(idempotent,-check)',
        '2.23.3',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.23.3',
        False,
        ' Network ansible-docker-test-bc362ba-pull_default  Creating\n'
        ' Network ansible-docker-test-bc362ba-pull_default  Created\n'
        ' Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Creating\n'
        ' Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Created\n'
        ' Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Starting\n'
        ' Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-with-pull=never',
        '2.23.3',
        False,
        ' Network ansible-docker-test-bc362ba-pull_default  Creating\n'
        ' Network ansible-docker-test-bc362ba-pull_default  Created\n'
        ' Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Creating\n'
        'Error response from daemon: no such image: does-not-exist:latest: No such image: does-not-exist:latest\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'unknown',
                '',
                'Error',
                'Error response from daemon: no such image: does-not-exist:latest: No such image: does-not-exist:latest',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.23.3',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-bc362ba-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-bc362ba-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (check)" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-with-pull=never-(check)',
        '2.23.3',
        True,
        ' DRY-RUN MODE -  Network ansible-docker-test-bc362ba-pull_default  Creating\n'
        ' DRY-RUN MODE -  Network ansible-docker-test-bc362ba-pull_default  Created\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Creating\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Created\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Starting\n'
        ' DRY-RUN MODE -  Container nsible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Started\n',
        [
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-pull_default',
                'Creating',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-pull_default',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Creating',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Created',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'nsible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent)" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent)',
        '2.23.3',
        False,
        ' Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present with pull=never (idempotent, check)" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-with-pull=never-(idempotent,-check)',
        '2.23.3',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-without-explicit-pull',
        '2.23.3',
        False,
        ' ansible-docker-test-bc362ba-cont Pulling \n'
        ' ansible-docker-test-bc362ba-cont Error \n'
        "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied\n",  # noqa: E501
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-bc362ba-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-bc362ba-cont',
                'Error',
                "Error response from daemon: pull access denied for does-not-exist, repository does not exist or may require 'docker login': denied: requested access to the resource is denied",  # noqa: E501
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Present without explicit pull (check)" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-present-without-explicit-pull-(check)',
        '2.23.3',
        True,
        ' DRY-RUN MODE -  ansible-docker-test-bc362ba-cont Pulling \n'
        ' DRY-RUN MODE -  ansible-docker-test-bc362ba-cont Error \n'
        'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed\n',
        [
            ResourceEvent(
                'service',
                'ansible-docker-test-bc362ba-cont',
                'Pulling',
                None,
            ),
            ResourceEvent(
                'unknown',
                'ansible-docker-test-bc362ba-cont',
                'Error',
                'pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed',
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-restarted',
        '2.23.3',
        False,
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Restarting\n'
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-restarted',
        '2.23.3',
        False,
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Restarting\n'
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.23.3',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Restarted (check)" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-restarted-(check)',
        '2.23.3',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Restarting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Restarting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-started',
        '2.23.3',
        False,
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Starting\n'
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (check)" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-started-(check)',
        '2.23.3',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Starting\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Started\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Starting',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Started',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent check)" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-started-(idempotent-check)',
        '2.23.3',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Started (idempotent)" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-started-(idempotent)',
        '2.23.3',
        False,
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Running\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Running',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-stopped',
        '2.23.3',
        False,
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Running\n'
        '\n'
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Stopping\n'
        ' Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopped (check)" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-stopped-(check)',
        '2.23.3',
        True,
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Running\n'
        '\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Stopping\n'
        ' DRY-RUN MODE -  Container ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1  Stopped\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Running',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-start-stop-ansible-docker-test-bc362ba-container-1',
                'Stopped',
                None,
            ),
        ],
        [],
    ),
    # docker_compose_v2: "Stopping service" on 2024-01-07 in devel-archlinux
    (
        '2.23.3-devel-archlinux-2024-01-07-docker_compose_v2-stopping-service',
        '2.23.3',
        False,
        ' Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Stopping\n'
        ' Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Stopped\n'
        ' Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Removing\n'
        ' Container ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1  Removed\n'
        ' Network ansible-docker-test-bc362ba-pull_default  Removing\n'
        ' Network ansible-docker-test-bc362ba-pull_default  Removed\n',
        [
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Stopping',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Stopped',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Removing',
                None,
            ),
            ResourceEvent(
                'container',
                'ansible-docker-test-bc362ba-pull-ansible-docker-test-bc362ba-cont-1',
                'Removed',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-pull_default',
                'Removing',
                None,
            ),
            ResourceEvent(
                'network',
                'ansible-docker-test-bc362ba-pull_default',
                'Removed',
                None,
            ),
        ],
        [],
    ),
]
