#!/usr/bin/env bash
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

set -o pipefail -eux

declare -a args
IFS='/:' read -ra args <<< "$1"

ansible_version="${args[0]}"
script="${args[1]}"

function join {
    local IFS="$1";
    shift;
    echo "$*";
}

# Ensure we can write other collections to this dir
sudo chown -R "$(whoami)" "${PWD}/../../../"

test="$(join / "${args[@]:1}")"

docker images ansible/ansible
docker images quay.io/ansible/*
docker ps

for container in $(docker ps --format '{{.Image}} {{.ID}}' | grep -v -e '^drydock/' -e '^quay.io/ansible/azure-pipelines-test-container:' | sed 's/^.* //'); do
    docker rm -f "${container}" || true  # ignore errors
done

docker ps

if [ -d /home/shippable/cache/ ]; then
    ls -la /home/shippable/cache/
fi

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
if [ "${ansible_version}" == "devel" ]; then
    retry pip install https://github.com/ansible/ansible/archive/devel.tar.gz --disable-pip-version-check
else
    retry pip install "https://github.com/ansible/ansible/archive/stable-${ansible_version}.tar.gz" --disable-pip-version-check
fi

export ANSIBLE_COLLECTIONS_PATHS="${PWD}/../../../"

# START: HACK

retry git clone --depth=1 --single-branch --branch stable-1 https://github.com/ansible-collections/community.library_inventory_filtering.git "${ANSIBLE_COLLECTIONS_PATHS}/ansible_collections/community/library_inventory_filtering_v1"
# NOTE: we're installing with git to work around Galaxy being a huge PITA (https://github.com/ansible/galaxy/issues/2429)
# retry ansible-galaxy -vvv collection install community.library_inventory_filtering_v1

if [ "${test}" == "units/1" ]; then
    # Nothing further should be added to this list.
    # This is to prevent modules or plugins in this collection having a runtime dependency on other collections.
    retry git clone --depth=1 --single-branch https://github.com/ansible-collections/community.internal_test_tools.git "${ANSIBLE_COLLECTIONS_PATHS}/ansible_collections/community/internal_test_tools"
    # NOTE: we're installing with git to work around Galaxy being a huge PITA (https://github.com/ansible/galaxy/issues/2429)
    # retry ansible-galaxy -vvv collection install community.internal_test_tools
fi

if [ "${script}" != "sanity/1" ] && [ "${script}" != "units/1" ]; then
    # To prevent Python dependencies on other collections only install other collections for integration tests
    retry git clone --depth=1 --single-branch https://github.com/ansible-collections/ansible.posix.git "${ANSIBLE_COLLECTIONS_PATHS}/ansible_collections/ansible/posix"
    retry git clone --depth=1 --single-branch https://github.com/ansible-collections/community.crypto.git "${ANSIBLE_COLLECTIONS_PATHS}/ansible_collections/community/crypto"
    retry git clone --depth=1 --single-branch https://github.com/ansible-collections/community.general.git "${ANSIBLE_COLLECTIONS_PATHS}/ansible_collections/community/general"
    # NOTE: we're installing with git to work around Galaxy being a huge PITA (https://github.com/ansible/galaxy/issues/2429)
    # retry ansible-galaxy -vvv collection install ansible.posix
    # retry ansible-galaxy -vvv collection install community.crypto
    # retry ansible-galaxy -vvv collection install community.general
fi
# END: HACK


export PYTHONIOENCODING='utf-8'

if [ "${JOB_TRIGGERED_BY_NAME:-}" == "nightly-trigger" ]; then
    COVERAGE=yes
    COMPLETE=yes
fi

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
    export CHANGED=""
elif [[ "${COMMIT_MESSAGE}" =~ ci_complete ]]; then
    # disable change detection triggered by having 'ci_complete' in the latest commit message
    export CHANGED=""
else
    # enable change detection (default behavior)
    export CHANGED="--changed"
fi

if [ "${IS_PULL_REQUEST:-}" == "true" ]; then
    # run unstable tests which are targeted by focused changes on PRs
    export UNSTABLE="--allow-unstable-changed"
else
    # do not run unstable tests outside PRs
    export UNSTABLE=""
fi

# remove empty core/extras module directories from PRs created prior to the repo-merge
find plugins -type d -empty -print -delete

function cleanup
{
    # for complete on-demand coverage generate a report for all files with no coverage on the "sanity/5" job so we only have one copy
    if [ "${COVERAGE}" == "--coverage" ] && [ "${CHANGED}" == "" ] && [ "${test}" == "sanity/5" ]; then
        stub="--stub"
        # trigger coverage reporting for stubs even if no other coverage data exists
        mkdir -p tests/output/coverage/
    else
        stub=""
    fi

    if [ -d tests/output/coverage/ ]; then
        if find tests/output/coverage/ -mindepth 1 -name '.*' -prune -o -print -quit | grep -q .; then
            process_coverage='yes'  # process existing coverage files
        elif [ "${stub}" ]; then
            process_coverage='yes'  # process coverage when stubs are enabled
        else
            process_coverage=''
        fi

        if [ "${process_coverage}" ]; then
            # use python 3.7 for coverage to avoid running out of memory during coverage xml processing
            # only use it for coverage to avoid the additional overhead of setting up a virtual environment for a potential no-op job
            virtualenv --python /usr/bin/python3.7 ~/ansible-venv
            set +ux
            . ~/ansible-venv/bin/activate
            set -ux

            # shellcheck disable=SC2086
            ansible-test coverage xml --color -v --requirements --group-by command --group-by version ${stub:+"$stub"}
            cp -a tests/output/reports/coverage=*.xml "$SHIPPABLE_RESULT_DIR/codecoverage/"

            if [ "${ansible_version}" != "2.9" ]; then
                # analyze and capture code coverage aggregated by integration test target
                ansible-test coverage analyze targets generate -v "$SHIPPABLE_RESULT_DIR/testresults/coverage-analyze-targets.json"
            fi

            # upload coverage report to codecov.io only when using complete on-demand coverage
            if [ "${COVERAGE}" == "--coverage" ] && [ "${CHANGED}" == "" ]; then
                for file in tests/output/reports/coverage=*.xml; do
                    flags="${file##*/coverage=}"
                    flags="${flags%-powershell.xml}"
                    flags="${flags%.xml}"
                    # remove numbered component from stub files when converting to tags
                    flags="${flags//stub-[0-9]*/stub}"
                    flags="${flags//=/,}"
                    flags="${flags//[^a-zA-Z0-9_,]/_}"

                    bash <(curl -s https://ansible-ci-files.s3.us-east-1.amazonaws.com/codecov/codecov.sh) \
                        -f "${file}" \
                        -F "${flags}" \
                        -n "${test}" \
                        -t 8450ed26-4e94-4d07-8831-d2023d6d20a3 \
                        -X coveragepy \
                        -X gcov \
                        -X fix \
                        -X search \
                        -X xcode \
                    || echo "Failed to upload code coverage report to codecov.io: ${file}"
                done
            fi
        fi
    fi

    if [ -d  tests/output/junit/ ]; then
      cp -aT tests/output/junit/ "$SHIPPABLE_RESULT_DIR/testresults/"
    fi

    if [ -d tests/output/data/ ]; then
      cp -a tests/output/data/ "$SHIPPABLE_RESULT_DIR/testresults/"
    fi

    if [ -d  tests/output/bot/ ]; then
      cp -aT tests/output/bot/ "$SHIPPABLE_RESULT_DIR/testresults/"
    fi
}

if [ "${SHIPPABLE_BUILD_ID:-}" ]; then trap cleanup EXIT; fi

if [[ "${COVERAGE:-}" == "--coverage" ]]; then
    timeout=60
else
    timeout=50
fi

ansible-test env --dump --show --timeout "${timeout}" --color -v

if [ "${SHIPPABLE_BUILD_ID:-}" ]; then "tests/utils/shippable/check_matrix.py"; fi
"tests/utils/shippable/${script}.sh" "${test}"
