# This code is part of the Ansible collection community.docker, but is an independent component.
# This particular file, and this file only, is based on the Docker SDK for Python (https://github.com/docker/docker-py/)
#
# Copyright (c) 2016-2022 Docker, Inc.
#
# It is licensed under the Apache 2.0 license (see LICENSES/Apache-2.0.txt in this collection)
# SPDX-License-Identifier: Apache-2.0

# Note that this module util is **PRIVATE** to the collection. It can have breaking changes at any time.
# Do not use this from other collections or standalone plugins/modules!

from __future__ import annotations

import re
import typing as t


if t.TYPE_CHECKING:
    from collections.abc import Collection, Sequence


PORT_SPEC = re.compile(
    "^"  # Match full string
    "("  # External part
    r"(\[?(?P<host>[a-fA-F\d.:]+)\]?:)?"  # Address
    r"(?P<ext>[\d]*)(-(?P<ext_end>[\d]+))?:"  # External range
    ")?"
    r"(?P<int>[\d]+)(-(?P<int_end>[\d]+))?"  # Internal range
    "(?P<proto>/(udp|tcp|sctp))?"  # Protocol
    "$"  # Match full string
)


def add_port_mapping(
    port_bindings: dict[str, list[str | tuple[str, str | None] | None]],
    internal_port: str,
    external: str | tuple[str, str | None] | None,
) -> None:
    if internal_port in port_bindings:
        port_bindings[internal_port].append(external)
    else:
        port_bindings[internal_port] = [external]


def add_port(
    port_bindings: dict[str, list[str | tuple[str, str | None] | None]],
    internal_port_range: list[str],
    external_range: list[str] | list[tuple[str, str | None]] | None,
) -> None:
    if external_range is None:
        for internal_port in internal_port_range:
            add_port_mapping(port_bindings, internal_port, None)
    else:
        for internal_port, external_port in zip(internal_port_range, external_range):
            # mypy loses the exact type of eternal_port elements for some reason...
            add_port_mapping(port_bindings, internal_port, external_port)  # type: ignore


def build_port_bindings(
    ports: Collection[str],
) -> dict[str, list[str | tuple[str, str | None] | None]]:
    port_bindings: dict[str, list[str | tuple[str, str | None] | None]] = {}
    for port in ports:
        internal_port_range, external_range = split_port(port)
        add_port(port_bindings, internal_port_range, external_range)
    return port_bindings


def _raise_invalid_port(port: str) -> t.NoReturn:
    raise ValueError(
        f'Invalid port "{port}", should be '
        "[[remote_ip:]remote_port[-remote_port]:]"
        "port[/protocol]"
    )


@t.overload
def port_range(
    start: str,
    end: str | None,
    proto: str,
    randomly_available_port: bool = False,
) -> list[str]: ...


@t.overload
def port_range(
    start: str | None,
    end: str | None,
    proto: str,
    randomly_available_port: bool = False,
) -> list[str] | None: ...


def port_range(
    start: str | None,
    end: str | None,
    proto: str,
    randomly_available_port: bool = False,
) -> list[str] | None:
    if start is None:
        return start
    if end is None:
        return [f"{start}{proto}"]
    if randomly_available_port:
        return [f"{start}-{end}{proto}"]
    return [f"{port}{proto}" for port in range(int(start), int(end) + 1)]


def split_port(
    port: str | int,
) -> tuple[list[str], list[str] | list[tuple[str, str | None]] | None]:
    port = str(port)
    match = PORT_SPEC.match(port)
    if match is None:
        _raise_invalid_port(port)
    parts = match.groupdict()

    host: str | None = parts["host"]
    proto: str = parts["proto"] or ""
    int_p: str = parts["int"]
    ext_p: str = parts["ext"]
    internal: list[str] = port_range(int_p, parts["int_end"], proto)  # type: ignore
    external = port_range(ext_p or None, parts["ext_end"], "", len(internal) == 1)

    if host is None:
        if (external is not None and len(internal) != len(external)) or ext_p == "":
            raise ValueError("Port ranges don't match in length")
        return internal, external
    external_or_none: Sequence[str | None]
    if not external:
        external_or_none = [None] * len(internal)
    else:
        external_or_none = external
        if len(internal) != len(external_or_none):
            raise ValueError("Port ranges don't match in length")
    return internal, [(host, ext_port) for ext_port in external_or_none]
