# Copyright (c) 2025 Felix Fontein
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Note that this module util is **PRIVATE** to the collection. It can have breaking changes at any time.
# Do not use this from other collections or standalone plugins/modules!

from __future__ import annotations

import re
import typing as t
from dataclasses import dataclass

_PATH_RE = re.compile(
    r"^[a-z0-9]+((\.|_|__|-+)[a-z0-9]+)*(\/[a-z0-9]+((\.|_|__|-+)[a-z0-9]+)*)*$"
)
_TAG_RE = re.compile(r"^[a-zA-Z0-9_][a-zA-Z0-9._-]{0,127}$")
_DIGEST_RE = re.compile(r"^sha256:[0-9a-fA-F]{64}$")


def is_digest(name: str, allow_empty: bool = False) -> bool:
    """Check whether the given name is in fact an image ID (hash)."""
    if not name:
        return allow_empty
    return _DIGEST_RE.match(name) is not None


def is_tag(name: str, allow_empty: bool = False) -> bool:
    """Check whether the given name can be an image tag."""
    if not name:
        return allow_empty
    return _TAG_RE.match(name) is not None


@dataclass
class ImageName:
    registry: str | None
    path: str
    tag: str | None
    digest: str | None

    @classmethod
    def parse(cls, name: str) -> t.Self:
        registry: str | None = None
        tag: str | None = None
        digest: str | None = None
        parts = name.rsplit("@", 1)
        if len(parts) == 2:
            name, digest = parts
        parts = name.rsplit(":", 1)
        if len(parts) == 2 and "/" not in parts[1]:
            name, tag = parts
        parts = name.split("/", 1)
        if len(parts) == 2 and (
            "." in parts[0] or ":" in parts[0] or parts[0] == "localhost"
        ):
            registry, name = parts
        return cls(registry, name, tag, digest)

    def validate(self) -> t.Self:
        if self.registry:
            if self.registry[0] == "-" or self.registry[-1] == "-":
                raise ValueError(
                    f'Invalid registry name ({self.registry}): must not begin or end with a "-".'
                )
            if self.registry[-1] == ":":
                raise ValueError(
                    f'Invalid registry name ({self.registry}): must not end with ":".'
                )
        if not _PATH_RE.match(self.path):
            raise ValueError(f"Invalid path ({self.path}).")
        if self.tag and not is_tag(self.tag):
            raise ValueError(f"Invalid tag ({self.tag}).")
        if self.digest and not is_digest(self.digest):
            raise ValueError(f"Invalid digest ({self.digest}).")
        return self

    def combine(self) -> str:
        parts = []
        if self.registry:
            parts.append(self.registry)
            if self.path:
                parts.append("/")
        parts.append(self.path)
        if self.tag:
            parts.append(":")
            parts.append(self.tag)
        if self.digest:
            parts.append("@")
            parts.append(self.digest)
        return "".join(parts)

    def normalize(self) -> ImageName:
        registry = self.registry
        path = self.path
        if registry in ("", None, "index.docker.io", "registry.hub.docker.com"):
            registry = "docker.io"
        if registry == "docker.io" and "/" not in path and path:
            path = f"library/{path}"
        return ImageName(registry, path, self.tag, self.digest)

    def get_hostname_and_port(self) -> tuple[str, int]:
        if self.registry is None:
            raise ValueError(
                "Cannot get hostname when there is no registry. Normalize first!"
            )
        if self.registry == "docker.io":
            return "index.docker.io", 443
        parts = self.registry.split(":", 1)
        if len(parts) == 2:
            try:
                port = int(parts[1])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Cannot parse port {parts[1]!r}") from exc
            return parts[0], port
        return self.registry, 443
