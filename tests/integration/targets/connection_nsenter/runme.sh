#!/usr/bin/env bash

set -euo pipefail

[[ -n "${DEBUG:-}" || -n "${ANSIBLE_DEBUG:-}" ]] && set -x

readonly IMAGE="quay.io/ansible/toolset:latest"
readonly PYTHON="$(command -v python3 python | head -n1)"

# Determine collection root
COLLECTION_ROOT=./
while true; do
    if [ -e ${COLLECTION_ROOT}galaxy.yml ] || [ -e ${COLLECTION_ROOT}MANIFEST.json ]; then
        break
    fi
    COLLECTION_ROOT="${COLLECTION_ROOT}../"
done
readonly COLLECTION_ROOT="$(cd ${COLLECTION_ROOT} ; pwd)"

# Setup phase
echo "Setup"
ANSIBLE_ROLES_PATH=.. ansible-playbook setup.yml

# If docker wasn't installed, don't run the tests
if [ "$(command -v docker)" == "" ]; then
    exit
fi

cleanup() {
    echo "Cleanup"
    echo "Shutdown"
    ANSIBLE_ROLES_PATH=.. ansible-playbook shutdown.yml
    echo "Done"
    exit 0
}

envs=(--env "HOME=${HOME:-}")
while IFS=$'\0' read -d '' -r line; do
    key="$(echo "$line" | cut -d= -f1)"
    value="$(echo "$line" | cut -d= -f2-)"
    if [[ "${key}" =~ ^(ANSIBLE_|JUNIT_OUTPUT_DIR$|OUTPUT_DIR$|PYTHONPATH$) ]]; then
        envs+=(--env "${key}=${value}")
    fi
done < <(printenv -0)

# Test phase
cat > test_connection.inventory << EOF
[nsenter]
nsenter-no-pipelining ansible_pipelining=false
nsenter-pipelining    ansible_pipelining=true

[nsenter:vars]
ansible_host=localhost
ansible_connection=community.docker.nsenter
ansible_host_volume_mount=/host
ansible_nsenter_pid=1
ansible_python_interpreter=${PYTHON}
EOF

echo "Run tests"
set -x
docker run \
    -i \
    --rm \
    --privileged \
    --pid host \
    "${envs[@]}" \
    --volume "${COLLECTION_ROOT}:${COLLECTION_ROOT}" \
    --workdir "$(pwd)" \
    "${IMAGE}" \
    ./runme-connection.sh "$@"
