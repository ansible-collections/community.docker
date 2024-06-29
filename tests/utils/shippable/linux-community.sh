#!/usr/bin/env bash
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

set -o pipefail -eux

declare -a args
IFS='/:' read -ra args <<< "$1"

image="${args[1]}"
python="${args[2]}"

if [ "${#args[@]}" -gt 3 ]; then
    target="azp/${args[3]}/"
else
    target="azp/"
fi

if [[ "${python}" =~ -pypi-latest$ ]]; then
    python="${python/-pypi-latest}"
    echo 'force_docker_sdk_for_python_pypi: true' >> tests/integration/integration_config.yml
fi
if [[ "${python}" =~ -dev-latest$ ]]; then
    python="${python/-dev-latest}"
    echo 'force_docker_sdk_for_python_dev: true' >> tests/integration/integration_config.yml
fi

# shellcheck disable=SC2086
ansible-test integration --color -v --retry-on-error "${target}" ${COVERAGE:+"$COVERAGE"} ${CHANGED:+"$CHANGED"} ${UNSTABLE:+"$UNSTABLE"} \
    --docker "quay.io/ansible-community/test-image:${image}" --python "${python}"
