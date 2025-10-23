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

import json
import os
import typing as t
from shutil import copyfile, rmtree

from ..errors import ContextException
from ..tls import TLSConfig
from .config import (
    get_context_host,
    get_meta_dir,
    get_meta_file,
    get_tls_dir,
)


IN_MEMORY = "IN MEMORY"


class Context:
    """A context."""

    def __init__(
        self,
        name: str,
        orchestrator: str | None = None,
        host: str | None = None,
        endpoints: dict[str, dict[str, t.Any]] | None = None,
        skip_tls_verify: bool = False,
        tls: bool = False,
        description: str | None = None,
    ) -> None:
        if not name:
            raise ValueError("Name not provided")
        self.name = name
        self.context_type = None
        self.orchestrator = orchestrator
        self.endpoints = {}
        self.tls_cfg: dict[str, TLSConfig] = {}
        self.meta_path = IN_MEMORY
        self.tls_path = IN_MEMORY
        self.description = description

        if not endpoints:
            # set default docker endpoint if no endpoint is set
            default_endpoint = (
                "docker"
                if (not orchestrator or orchestrator == "swarm")
                else orchestrator
            )

            self.endpoints = {
                default_endpoint: {
                    "Host": get_context_host(host, skip_tls_verify or tls),
                    "SkipTLSVerify": skip_tls_verify,
                }
            }
            return

        # check docker endpoints
        for k, v in endpoints.items():
            if not isinstance(v, dict):
                # unknown format
                raise ContextException(
                    f"Unknown endpoint format for context {name}: {v}",
                )

            self.endpoints[k] = v
            if k != "docker":
                continue

            self.endpoints[k]["Host"] = v.get(
                "Host", get_context_host(host, skip_tls_verify or tls)
            )
            self.endpoints[k]["SkipTLSVerify"] = bool(
                v.get("SkipTLSVerify", skip_tls_verify)
            )

    def set_endpoint(
        self,
        name: str = "docker",
        host: str | None = None,
        tls_cfg: TLSConfig | None = None,
        skip_tls_verify: bool = False,
        def_namespace: str | None = None,
    ) -> None:
        self.endpoints[name] = {
            "Host": get_context_host(host, not skip_tls_verify or tls_cfg is not None),
            "SkipTLSVerify": skip_tls_verify,
        }
        if def_namespace:
            self.endpoints[name]["DefaultNamespace"] = def_namespace

        if tls_cfg:
            self.tls_cfg[name] = tls_cfg

    def inspect(self) -> dict[str, t.Any]:
        return self()

    @classmethod
    def load_context(cls, name: str) -> t.Self | None:
        meta = Context._load_meta(name)
        if meta:
            instance = cls(
                meta["Name"],
                orchestrator=meta["Metadata"].get("StackOrchestrator", None),
                endpoints=meta.get("Endpoints", None),
                description=meta["Metadata"].get("Description"),
            )
            instance.context_type = meta["Metadata"].get("Type", None)
            instance._load_certs()
            instance.meta_path = get_meta_dir(name)
            return instance
        return None

    @classmethod
    def _load_meta(cls, name: str) -> dict[str, t.Any] | None:
        meta_file = get_meta_file(name)
        if not os.path.isfile(meta_file):
            return None

        metadata: dict[str, t.Any] = {}
        try:
            with open(meta_file, "rt", encoding="utf-8") as f:
                metadata = json.load(f)
        except (OSError, KeyError, ValueError) as e:
            # unknown format
            raise RuntimeError(
                f"Detected corrupted meta file for context {name} : {e}"
            ) from e

        # for docker endpoints, set defaults for
        # Host and SkipTLSVerify fields
        for k, v in metadata["Endpoints"].items():
            if k != "docker":
                continue
            metadata["Endpoints"][k]["Host"] = v.get(
                "Host", get_context_host(None, False)
            )
            metadata["Endpoints"][k]["SkipTLSVerify"] = bool(
                v.get("SkipTLSVerify", True)
            )

        return metadata

    def _load_certs(self) -> None:
        certs = {}
        tls_dir = get_tls_dir(self.name)
        for endpoint in self.endpoints:
            if not os.path.isdir(os.path.join(tls_dir, endpoint)):
                continue
            ca_cert = None
            cert = None
            key = None
            for filename in os.listdir(os.path.join(tls_dir, endpoint)):
                if filename.startswith("ca"):
                    ca_cert = os.path.join(tls_dir, endpoint, filename)
                elif filename.startswith("cert"):
                    cert = os.path.join(tls_dir, endpoint, filename)
                elif filename.startswith("key"):
                    key = os.path.join(tls_dir, endpoint, filename)
            if all([cert, key]) or ca_cert:
                verify = None
                if endpoint == "docker" and not self.endpoints["docker"].get(
                    "SkipTLSVerify", False
                ):
                    verify = True
                certs[endpoint] = TLSConfig(
                    client_cert=(cert, key) if cert and key else None,
                    ca_cert=ca_cert,
                    verify=verify,
                )
        self.tls_cfg = certs
        self.tls_path = tls_dir

    def save(self) -> None:
        meta_dir = get_meta_dir(self.name)
        if not os.path.isdir(meta_dir):
            os.makedirs(meta_dir)
        with open(get_meta_file(self.name), "wt", encoding="utf-8") as f:
            f.write(json.dumps(self.Metadata))

        tls_dir = get_tls_dir(self.name)
        for endpoint, tls in self.tls_cfg.items():
            if not os.path.isdir(os.path.join(tls_dir, endpoint)):
                os.makedirs(os.path.join(tls_dir, endpoint))

            ca_file = tls.ca_cert
            if ca_file:
                copyfile(
                    ca_file, os.path.join(tls_dir, endpoint, os.path.basename(ca_file))
                )

            if tls.cert:
                cert_file, key_file = tls.cert
                copyfile(
                    cert_file,
                    os.path.join(tls_dir, endpoint, os.path.basename(cert_file)),
                )
                copyfile(
                    key_file,
                    os.path.join(tls_dir, endpoint, os.path.basename(key_file)),
                )

        self.meta_path = get_meta_dir(self.name)
        self.tls_path = get_tls_dir(self.name)

    def remove(self) -> None:
        if os.path.isdir(self.meta_path):
            rmtree(self.meta_path)
        if os.path.isdir(self.tls_path):
            rmtree(self.tls_path)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: '{self.name}'>"

    def __str__(self) -> str:
        return json.dumps(self.__call__(), indent=2)

    def __call__(self) -> dict[str, t.Any]:
        result = self.Metadata
        result.update(self.TLSMaterial)
        result.update(self.Storage)
        return result

    def is_docker_host(self) -> bool:
        return self.context_type is None

    @property
    def Name(self) -> str:  # pylint: disable=invalid-name
        return self.name

    @property
    def Host(self) -> str | None:  # pylint: disable=invalid-name
        if not self.orchestrator or self.orchestrator == "swarm":
            endpoint = self.endpoints.get("docker", None)
            if endpoint:
                return endpoint.get("Host", None)  # type: ignore
            return None

        return self.endpoints[self.orchestrator].get("Host", None)  # type: ignore

    @property
    def Orchestrator(self) -> str | None:  # pylint: disable=invalid-name
        return self.orchestrator

    @property
    def Metadata(self) -> dict[str, t.Any]:  # pylint: disable=invalid-name
        meta: dict[str, t.Any] = {}
        if self.orchestrator:
            meta = {"StackOrchestrator": self.orchestrator}
        return {"Name": self.name, "Metadata": meta, "Endpoints": self.endpoints}

    @property
    def TLSConfig(self) -> TLSConfig | None:  # pylint: disable=invalid-name
        key = self.orchestrator
        if not key or key == "swarm":
            key = "docker"
        if key in self.tls_cfg:
            return self.tls_cfg[key]
        return None

    @property
    def TLSMaterial(self) -> dict[str, t.Any]:  # pylint: disable=invalid-name
        certs: dict[str, t.Any] = {}
        for endpoint, tls in self.tls_cfg.items():
            paths = [tls.ca_cert, *tls.cert] if tls.cert else [tls.ca_cert]
            certs[endpoint] = [
                os.path.basename(path) if path else None for path in paths
            ]
        return {"TLSMaterial": certs}

    @property
    def Storage(self) -> dict[str, t.Any]:  # pylint: disable=invalid-name
        return {"Storage": {"MetadataPath": self.meta_path, "TLSPath": self.tls_path}}
