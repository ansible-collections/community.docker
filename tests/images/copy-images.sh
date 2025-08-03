#!/usr/bin/env bash
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

set -e

# Uncomment the container image to copy, and run this script to copy it.

DESTINATION_REPO=ansible-collections/community.docker

function convert_image {
  echo "========================================================================================================="
  local IMAGE_NAME="$1"
  local DEST_IMAGE="$2"
  echo "FROM ${IMAGE_NAME}" | podman build --annotation "org.opencontainers.image.source=https://github.com/${DESTINATION_REPO}" -t "ghcr.io/${DESTINATION_REPO}/${DEST_IMAGE}" -
  podman push "ghcr.io/${DESTINATION_REPO}/${DEST_IMAGE}"
  podman rmi "${IMAGE_NAME}"
  podman rmi "ghcr.io/${DESTINATION_REPO}/${DEST_IMAGE}"
}

# convert_image docker.io/library/registry:2.6.1 docker-distribution:2.6.1
# convert_image docker.io/library/registry:2.8.3 docker-distribution:2.8.3
# convert_image docker.io/library/registry:3.0.0 docker-distribution:3.0.0
convert_image docker.io/library/python:3-alpine docker-python:3-alpine
