# This code is part of the Ansible collection community.docker, but is an independent component.
# This particular file, and this file only, is based on containerd's platforms Go module
# (https://github.com/containerd/containerd/tree/main/platforms)
#
# Copyright (c) 2023 Felix Fontein <felix@fontein.de>
# Copyright The containerd Authors
#
# It is licensed under the Apache 2.0 license (see LICENSES/Apache-2.0.txt in this collection)
# SPDX-License-Identifier: Apache-2.0

# Note that this module util is **PRIVATE** to the collection. It can have breaking changes at any time.
# Do not use this from other collections or standalone plugins/modules!

from __future__ import annotations

import re
import typing as t


_VALID_STR = re.compile("^[A-Za-z0-9_-]+$")


def _validate_part(string: str, part: str, part_name: str) -> str:
    if not part:
        raise ValueError(f'Invalid platform string "{string}": {part_name} is empty')
    if not _VALID_STR.match(part):
        raise ValueError(
            f'Invalid platform string "{string}": {part_name} has invalid characters'
        )
    return part


# See https://github.com/containerd/containerd/blob/main/platforms/database.go#L32-L38
_KNOWN_OS = (
    "aix",
    "android",
    "darwin",
    "dragonfly",
    "freebsd",
    "hurd",
    "illumos",
    "ios",
    "js",
    "linux",
    "nacl",
    "netbsd",
    "openbsd",
    "plan9",
    "solaris",
    "windows",
    "zos",
)

# See https://github.com/containerd/containerd/blob/main/platforms/database.go#L54-L60
_KNOWN_ARCH = (
    "386",
    "amd64",
    "amd64p32",
    "arm",
    "armbe",
    "arm64",
    "arm64be",
    "ppc64",
    "ppc64le",
    "loong64",
    "mips",
    "mipsle",
    "mips64",
    "mips64le",
    "mips64p32",
    "mips64p32le",
    "ppc",
    "riscv",
    "riscv64",
    "s390",
    "s390x",
    "sparc",
    "sparc64",
    "wasm",
)


def _normalize_os(os_str: str) -> str:
    # See normalizeOS() in https://github.com/containerd/containerd/blob/main/platforms/database.go
    os_str = os_str.lower()
    if os_str == "macos":
        os_str = "darwin"
    return os_str


_NORMALIZE_ARCH = {
    ("i386", None): ("386", ""),
    ("x86_64", "v1"): ("amd64", ""),
    ("x86-64", "v1"): ("amd64", ""),
    ("amd64", "v1"): ("amd64", ""),
    ("x86_64", None): ("amd64", None),
    ("x86-64", None): ("amd64", None),
    ("amd64", None): ("amd64", None),
    ("aarch64", "8"): ("arm64", ""),
    ("arm64", "8"): ("arm64", ""),
    ("aarch64", "v8"): ("arm64", ""),
    ("arm64", "v8"): ("arm64", ""),
    ("aarch64", None): ("arm64", None),
    ("arm64", None): ("arm64", None),
    ("armhf", None): ("arm", "v7"),
    ("armel", None): ("arm", "v6"),
    ("arm", ""): ("arm", "v7"),
    ("arm", "5"): ("arm", "v5"),
    ("arm", "6"): ("arm", "v6"),
    ("arm", "7"): ("arm", "v7"),
    ("arm", "8"): ("arm", "v8"),
    ("arm", None): ("arm", None),
}


def _normalize_arch(arch_str: str, variant_str: str) -> tuple[str, str]:
    # See normalizeArch() in https://github.com/containerd/containerd/blob/main/platforms/database.go
    arch_str = arch_str.lower()
    variant_str = variant_str.lower()
    res = _NORMALIZE_ARCH.get((arch_str, variant_str))
    if res is None:
        res = _NORMALIZE_ARCH.get((arch_str, None))
    if res is None:
        return arch_str, variant_str
    arch_str = res[0]
    if res[1] is not None:
        variant_str = res[1]
    return arch_str, variant_str


class _Platform:
    def __init__(
        self, os: str | None = None, arch: str | None = None, variant: str | None = None
    ) -> None:
        self.os = os
        self.arch = arch
        self.variant = variant
        if variant is not None:
            if arch is None:
                raise ValueError("If variant is given, architecture must be given too")
            if os is None:
                raise ValueError("If variant is given, os must be given too")

    @classmethod
    def parse_platform_string(
        cls,
        string: str | None,
        daemon_os: str | None = None,
        daemon_arch: str | None = None,
    ) -> t.Self:
        # See Parse() in https://github.com/containerd/containerd/blob/main/platforms/platforms.go
        if string is None:
            return cls()
        if not string:
            raise ValueError("Platform string must be non-empty")
        parts = string.split("/", 2)
        arch = None
        variant = None
        if len(parts) == 1:
            _validate_part(string, string, "OS/architecture")
            # The part is either OS or architecture
            os = _normalize_os(string)
            if os in _KNOWN_OS:
                if daemon_arch is not None:
                    arch, variant = _normalize_arch(daemon_arch, "")
                return cls(os=os, arch=arch, variant=variant)
            arch, variant = _normalize_arch(os, "")
            if arch in _KNOWN_ARCH:
                return cls(
                    os=_normalize_os(daemon_os) if daemon_os else None,
                    arch=arch or None,
                    variant=variant or None,
                )
            raise ValueError(
                f'Invalid platform string "{string}": unknown OS or architecture'
            )
        os = _validate_part(string, parts[0], "OS")
        if not os:
            raise ValueError(f'Invalid platform string "{string}": OS is empty')
        arch = (
            _validate_part(string, parts[1], "architecture") if len(parts) > 1 else None
        )
        if arch is not None and not arch:
            raise ValueError(
                f'Invalid platform string "{string}": architecture is empty'
            )
        variant = (
            _validate_part(string, parts[2], "variant") if len(parts) > 2 else None
        )
        if variant is not None and not variant:
            raise ValueError(f'Invalid platform string "{string}": variant is empty')
        assert arch is not None  # otherwise variant would be None as well
        arch, variant = _normalize_arch(arch, variant or "")
        if len(parts) == 2 and arch == "arm" and variant == "v7":
            variant = None
        if len(parts) == 3 and arch == "arm64" and variant == "":
            variant = "v8"
        return cls(os=_normalize_os(os), arch=arch, variant=variant or None)

    def __str__(self) -> str:
        if self.variant:
            assert (
                self.os is not None and self.arch is not None
            )  # ensured in constructor
            parts: list[str] = [self.os, self.arch, self.variant]
        elif self.os:
            if self.arch:
                parts = [self.os, self.arch]
            else:
                parts = [self.os]
        elif self.arch is not None:
            parts = [self.arch]
        else:
            parts = []
        return "/".join(parts)

    def __repr__(self) -> str:
        return (
            f"_Platform(os={self.os!r}, arch={self.arch!r}, variant={self.variant!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _Platform):
            return NotImplemented
        return (
            self.os == other.os
            and self.arch == other.arch
            and self.variant == other.variant
        )


def normalize_platform_string(
    string: str, daemon_os: str | None = None, daemon_arch: str | None = None
) -> str:
    return str(
        _Platform.parse_platform_string(
            string, daemon_os=daemon_os, daemon_arch=daemon_arch
        )
    )


def compose_platform_string(
    os: str | None = None,
    arch: str | None = None,
    variant: str | None = None,
    daemon_os: str | None = None,
    daemon_arch: str | None = None,
) -> str:
    if os is None and daemon_os is not None:
        os = _normalize_os(daemon_os)
    if arch is None and daemon_arch is not None:
        arch, variant = _normalize_arch(daemon_arch, variant or "")
        variant = variant or None
    return str(_Platform(os=os, arch=arch, variant=variant or None))


def compare_platform_strings(string1: str, string2: str) -> bool:
    return _Platform.parse_platform_string(string1) == _Platform.parse_platform_string(
        string2
    )
