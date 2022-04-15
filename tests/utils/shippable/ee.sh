#!/usr/bin/env bash

set -o pipefail -eux

declare -a args
IFS='/:' read -ra args <<< "$1"

ansible_runner_tag="${args[1]}"

# Install ansible-builder and ansible-navigator
pip install ansible-builder ansible-navigator

# Verify requirements
( cd ../../../ ; ansible-builder introspect --sanitize . )

# Build collection
ansible-galaxy collection build --output-path ../../../

# Create files for building execution environment
cd ../../../
COLLECTION_FILENAME="$(ls community-*-*.tar.gz)"

# EE config
cat > execution-environment.yml <<EOF
---
version: 1
build_arg_defaults:
  EE_BASE_IMAGE: 'quay.io/ansible/ansible-runner:${ansible_runner_tag}'
dependencies:
  galaxy: requirements.yml
EOF
echo "=========================================== execution-environment.yml ========"
cat execution-environment.yml
echo "=============================================================================="

# Requirements
cat > requirements.yml <<EOF
---
collections:
- name: ${COLLECTION_FILENAME}
  type: file
EOF
echo "=========================================== requirements.yml ================="
cat requirements.yml
echo "=============================================================================="

# Build image
mkdir -p context/_build/
cp community-*-*.tar.gz context/_build/
ansible-builder build -v 3 -t test-ee:latest --container-runtime=docker

# shellcheck disable=SC2103
cd -

# Run basic tests
cd tests/ee
ls -la
set +e
ansible-navigator run -vvv \
    --mode stdout \
    --pull-policy never \
    --set-environment-variable ANSIBLE_PRIVATE_ROLE_VARS=true \
    --container-options=-v --container-options=/var/lib/docker:/var/lib/docker \
    --execution-environment-image test-ee:latest \
    all.yml
result=$?
set -e
if [ ${result} != 0 ]; then
    cat ansible-navigator.log
    exit ${result}
fi
