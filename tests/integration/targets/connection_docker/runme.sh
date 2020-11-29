#!/usr/bin/env bash

# If you use another image, you possibly also need to adjust
# ansible_python_interpreter in test_connection.inventory.
source ../setup_docker/vars/main.env
IMAGE="${DOCKER_TEST_IMAGE_PYTHON3}"

# Setup phase

echo "Setup"
ANSIBLE_ROLES_PATH=.. ansible-playbook setup.yml

# If docker wasn't installed, don't run the tests
if [ "$(command -v docker)" == "" ]; then
    exit
fi


# Test phase

CONTAINER_SUFFIX=-${RANDOM}

DOCKER_CONTAINERS="docker-connection-test-container${CONTAINER_SUFFIX}"

[[ -n "$DEBUG" || -n "$ANSIBLE_DEBUG" ]] && set -x

set -euo pipefail

cleanup() {
    echo "Cleanup"
    docker rm -f ${DOCKER_CONTAINERS}
    echo "Shutdown"
    ANSIBLE_ROLES_PATH=.. ansible-playbook shutdown.yml
    echo "Done"
    exit 0
}

trap cleanup INT TERM EXIT

echo "Start containers"
for CONTAINER in ${DOCKER_CONTAINERS}; do
    if [ "${ANSIBLE_TEST_COVERAGE:-}" == "" ]; then
        docker run --rm --name ${CONTAINER} --detach "${IMAGE}" /bin/sh -c 'sleep 10m'
    else
        docker run --rm --name ${CONTAINER} --detach -v /tmp:/tmp "${IMAGE}" /bin/sh -c 'sleep 10m'
        docker exec ${CONTAINER} pip3 install coverage
    fi
    echo ${CONTAINER}
done

cat > test_connection.inventory << EOF
[docker]
docker-no-pipelining ansible_pipelining=false
docker-pipelining    ansible_pipelining=true

[docker:vars]
ansible_host=docker-connection-test-container${CONTAINER_SUFFIX}
ansible_connection=community.docker.docker
ansible_python_interpreter=/usr/local/bin/python3
EOF

echo "Run tests"
./runme-connection.sh "$@"
