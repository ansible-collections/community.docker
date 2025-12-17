#!/usr/bin/env bash
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

set -o pipefail -e

declare -a SESSIONS
if [ "$1" != "" ]; then
    IFS=' ' read -ra SESSIONS <<< "$1"
    SESSIONS=('--sessions' "${SESSIONS[@]}")
fi

export FORCE_COLOR=1
export ANTSIBULL_NOX_IGNORE_INSTALLED_COLLECTIONS=true

# ANTSIBULL_CHANGE_DETECTION: "${{ inputs.change-detection }}"
# ANTSIBULL_BASE_BRANCH: "${{ inputs.change-detection-base-branch }}"
nox --verbose --reuse-existing-virtualenvs --no-install "${SESSIONS[@]}" 2>&1 | "$(dirname "$0")/time-command.py"
