#!/usr/bin/env bash

# If you use another image, you possibly also need to adjust
# ansible_python_interpreter in test_connection.inventory.
IMAGE=python:3-alpine

# Setup phase

echo "Setup"
ANSIBLE_ROLES_PATH=.. ansible-playbook setup.yml

# If docker wasn't installed, don't run the tests
if [ "$(command -v docker)" == "" ]; then
    exit
fi


# Test phase


DOCKER_CONTAINERS="docker-connection-test-container"

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
    docker run --rm --name ${CONTAINER} --detach ${IMAGE} /bin/sh -c 'sleep 10m'
    docker exec ${CONTAINER} pip3 install coverage
    echo ${CONTAINER}
done

echo "Run tests"
./runme-connection.sh
