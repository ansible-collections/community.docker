#!/usr/bin/env bash
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

if [ ! -e main.go ]; then
    echo "Must be run in a directory that contains main.go."
    exit 1
fi

PROGRAMS="main is-healthy make-healthy"

set -eux
IMAGE_NAME="${1:-localhost/$(basename "$(pwd)"):latest}"
podman manifest rm "${IMAGE_NAME}" || true
podman image rm "${IMAGE_NAME}" || true
buildah manifest create "${IMAGE_NAME}"
for ARCH in amd64 arm64 386; do
    for PROGRAM in ${PROGRAMS}; do
        rm -f "${PROGRAM}-${ARCH}"
        GOARCH="${ARCH}" go build -ldflags "-s -w" -o "${PROGRAM}-${ARCH}" "${PROGRAM}.go"
    done

    # Need format=docker for health checks to work
    WORKING_CONTAINER="$(buildah from --arch "${ARCH}" --format docker scratch)"
    for PROGRAM in ${PROGRAMS}; do
        buildah copy "${WORKING_CONTAINER}" "${PROGRAM}-${ARCH}" "/${PROGRAM}"
    done
    buildah config --entrypoint '["/main"]' "${WORKING_CONTAINER}"
    buildah config --healthcheck 'CMD /is-healthy' "${WORKING_CONTAINER}"
    buildah config --healthcheck-interval 1s "${WORKING_CONTAINER}"
    buildah config --healthcheck-retries 1 "${WORKING_CONTAINER}"
    buildah config --healthcheck-start-period 10s "${WORKING_CONTAINER}"
    buildah commit --format docker --manifest "${IMAGE_NAME}" "${WORKING_CONTAINER}"

    for PROGRAM in ${PROGRAMS}; do
        rm -f "${PROGRAM}-${ARCH}"
    done
done
