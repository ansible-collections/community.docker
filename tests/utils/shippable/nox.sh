#!/usr/bin/env bash
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

set -o pipefail -eux

nox_session="$1"

docker images ansible/ansible
docker images quay.io/ansible/*
docker ps

for container in $(docker ps --format '{{.Image}} {{.ID}}' | grep -v -e '^drydock/' -e '^quay.io/ansible/azure-pipelines-test-container:' | sed 's/^.* //'); do
    docker rm -f "${container}" || true  # ignore errors
done

docker ps
command -v python
python -V

function retry
{
    # shellcheck disable=SC2034
    for repetition in 1 2 3; do
        set +e
        "$@"
        result=$?
        set -e
        if [ ${result} == 0 ]; then
            return ${result}
        fi
        echo "@* -> ${result}"
    done
    echo "Command '@*' failed 3 times!"
    exit 255
}

command -v pip
pip --version
pip list --disable-pip-version-check
retry pip install https://github.com/ansible-community/antsibull-nox/archive/main.tar.gz --disable-pip-version-check

export PYTHONIOENCODING='utf-8'

if [ -n "${COVERAGE:-}" ]; then
    # on-demand coverage reporting triggered by setting the COVERAGE environment variable to a non-empty value
    export COVERAGE="--coverage"
elif [[ "${COMMIT_MESSAGE}" =~ ci_coverage ]]; then
    # on-demand coverage reporting triggered by having 'ci_coverage' in the latest commit message
    export COVERAGE="--coverage"
else
    # on-demand coverage reporting disabled (default behavior, always-on coverage reporting remains enabled)
    export COVERAGE="--coverage-check"
fi

if [ -n "${COMPLETE:-}" ]; then
    # disable change detection triggered by setting the COMPLETE environment variable to a non-empty value
    export ANTSIBULL_CHANGE_DETECTION=""
elif [[ "${COMMIT_MESSAGE}" =~ ci_complete ]]; then
    # disable change detection triggered by having 'ci_complete' in the latest commit message
    export ANTSIBULL_CHANGE_DETECTION=""
elif [ "${IS_PULL_REQUEST:-}" == "true" ]; then
    # enable change detection for PRs (default behavior)
    export ANTSIBULL_CHANGE_DETECTION="true"
    export ANTSIBULL_BASE_BRANCH="${SYSTEM_PULLREQUEST_TARGETBRANCH}"
    # Create a branch for the current HEAD, which happens to be a merge commit
    git checkout -b "pull-request-branch"
    # Name the target branch
    git branch "${SYSTEM_PULLREQUEST_TARGETBRANCH}" --track "origin/${SYSTEM_PULLREQUEST_TARGETBRANCH}"
    # Show branches
    git branch -vv
else
    # disable change detection for pushes and scheduled runs
    export ANTSIBULL_CHANGE_DETECTION=""
fi

if [[ "${COVERAGE:-}" == "--coverage" ]]; then
    export ANTSIBULL_NOX_TIMEOUT=60
else
    export ANTSIBULL_NOX_TIMEOUT=50
fi

if [ "${IS_PULL_REQUEST:-}" == "true" ]; then
    export ANTSIBULL_NOX_INTEGRATION_ALLOW_UNSTABLE_CHANGED="true"
fi

export FORCE_COLOR=1
export ANTSIBULL_NOX_IGNORE_INSTALLED_COLLECTIONS="true"
export ANTSIBULL_NOX_COVERAGE_DESTINATION="${COVERAGE_DESTINATION_DIRECTORY}"
export ANTSIBULL_NOX_COVERAGE_ANALYSIS_FILE="${COVERAGE_DESTINATION_DIRECTORY}/coverage-analyze-targets.json"
export ANTSIBULL_NOX_COVERAGE_NO_XML="true"

nox -e "${nox_session}" -- ${COVERAGE}
