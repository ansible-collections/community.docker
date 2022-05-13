#!/usr/bin/env bash

set -o pipefail -eux

declare -a args
IFS='/:' read -ra args <<< "$1"

platform="${args[0]}"
version="${args[1]}"
target="shippable/posix/"

if [ "${#args[@]}" -gt 3 ]; then
    if [ "${args[2]}" == "pypi-latest" ]; then
        echo 'force_docker_sdk_for_python_pypi: true' >> tests/integration/interation_config.yml
    else
        echo "Invalid Docker SDK for Python version: '${args[2]}'"
        exit 254
    fi
    target="shippable/posix/group${args[3]}/"
elif [ "${#args[@]}" -gt 2 ]; then
    target="shippable/posix/group${args[2]}/"
fi

stage="${S:-prod}"
provider="${P:-default}"

if [ "${platform}" == "rhel" ] && [[ "${version}" =~ ^8 ]]; then
    echo "pynacl >= 1.4.0, < 1.5.0; python_version == '3.6'" >> tests/utils/constraints.txt
fi

# shellcheck disable=SC2086
ansible-test integration --color -v --retry-on-error "${target}" ${COVERAGE:+"$COVERAGE"} ${CHANGED:+"$CHANGED"} ${UNSTABLE:+"$UNSTABLE"} \
    --remote "${platform}/${version}" --remote-terminate always --remote-stage "${stage}" --remote-provider "${provider}"
