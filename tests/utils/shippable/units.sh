#!/usr/bin/env bash
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

set -o pipefail -eux

declare -a args
IFS='/:' read -ra args <<< "$1"

group="${args[1]}"

if [[ "${COVERAGE:-}" == "--coverage" ]]; then
    timeout=90
else
    timeout=30
fi

group1=()

case "${group}" in
    1) options=("${group1[@]:+${group1[@]}}") ;;
esac

ansible-test env --timeout "${timeout}" --color -v

# shellcheck disable=SC2086
ansible-test units --color -v --docker default ${COVERAGE:+"$COVERAGE"} ${CHANGED:+"$CHANGED"} \
    "${options[@]:+${options[@]}}" \
