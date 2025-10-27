# This code is part of the Ansible collection community.docker, but is an independent component.
# This particular file, and this file only, is based on the Docker SDK for Python (https://github.com/docker/docker-py/)
#
# Copyright (c) 2016-2025 Docker, Inc.
#
# It is licensed under the Apache 2.0 license (see LICENSES/Apache-2.0.txt in this collection)
# SPDX-License-Identifier: Apache-2.0

# Note that this module util is **PRIVATE** to the collection. It can have breaking changes at any time.
# Do not use this from other collections or standalone plugins/modules!

from __future__ import annotations

import hashlib
import json
import os

from ..constants import DEFAULT_UNIX_SOCKET, IS_WINDOWS_PLATFORM
from ..utils.config import find_config_file, get_default_config_file
from ..utils.utils import parse_host


METAFILE = "meta.json"


def get_current_context_name_with_source() -> tuple[str, str]:
    if os.environ.get("DOCKER_HOST"):
        return "default", "DOCKER_HOST environment variable set"
    if os.environ.get("DOCKER_CONTEXT"):
        return os.environ["DOCKER_CONTEXT"], "DOCKER_CONTEXT environment variable set"
    docker_cfg_path = find_config_file()
    if docker_cfg_path:
        try:
            with open(docker_cfg_path, "rt", encoding="utf-8") as f:
                return (
                    json.load(f).get("currentContext", "default"),
                    f"configuration file {docker_cfg_path}",
                )
        except Exception:  # pylint: disable=broad-exception-caught
            pass
    return "default", "fallback value"


def get_current_context_name() -> str:
    return get_current_context_name_with_source()[0]


def write_context_name_to_docker_config(name: str | None = None) -> Exception | None:
    if name == "default":
        name = None
    docker_cfg_path = find_config_file()
    config = {}
    if docker_cfg_path:
        try:
            with open(docker_cfg_path, "rt", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:  # pylint: disable=broad-exception-caught
            return e
    current_context = config.get("currentContext", None)
    if current_context and not name:
        del config["currentContext"]
    elif name:
        config["currentContext"] = name
    else:
        return None
    if not docker_cfg_path:
        docker_cfg_path = get_default_config_file()
    try:
        with open(docker_cfg_path, "wt", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        return None
    except Exception as e:  # pylint: disable=broad-exception-caught
        return e


def get_context_id(name: str) -> str:
    return hashlib.sha256(name.encode("utf-8")).hexdigest()


def get_context_dir() -> str:
    docker_cfg_path = find_config_file() or get_default_config_file()
    return os.path.join(os.path.dirname(docker_cfg_path), "contexts")


def get_meta_dir(name: str | None = None) -> str:
    meta_dir = os.path.join(get_context_dir(), "meta")
    if name:
        return os.path.join(meta_dir, get_context_id(name))
    return meta_dir


def get_meta_file(name: str) -> str:
    return os.path.join(get_meta_dir(name), METAFILE)


def get_tls_dir(name: str | None = None, endpoint: str = "") -> str:
    context_dir = get_context_dir()
    if name:
        return os.path.join(context_dir, "tls", get_context_id(name), endpoint)
    return os.path.join(context_dir, "tls")


def get_context_host(path: str | None = None, tls: bool = False) -> str:
    host = parse_host(path, IS_WINDOWS_PLATFORM, tls)
    if host == DEFAULT_UNIX_SOCKET and host.startswith("http+"):
        # remove http+ from default docker socket url
        host = host[5:]
    return host
