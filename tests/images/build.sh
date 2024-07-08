#!/usr/bin/env bash
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

if [ ! -e main.go ]; then
    echo "Must be run in a directory that contains main.go."
    exit 1
fi

set -eux
IMAGE_NAME="${1:-localhost/$(basename "$(pwd)"):latest}"
podman manifest rm "${IMAGE_NAME}" || true
podman image rm "${IMAGE_NAME}" || true
buildah manifest create "${IMAGE_NAME}"
for ARCH in amd64 arm64 386; do
    rm -f "main-${ARCH}"
    GOARCH="${ARCH}" go build -ldflags "-s -w" -o "main-${ARCH}" main.go

    WORKING_CONTAINER="$(buildah from --arch "${ARCH}" scratch)"
    buildah copy "${WORKING_CONTAINER}" "main-${ARCH}" "/runme"
    buildah config --entrypoint '["/runme"]' "${WORKING_CONTAINER}"
    buildah commit --manifest "${IMAGE_NAME}" "${WORKING_CONTAINER}"

    rm -f "main-${ARCH}"
done
