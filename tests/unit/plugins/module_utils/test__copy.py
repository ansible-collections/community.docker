# Copyright 2022 Red Hat | Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import typing as t

import pytest

from ansible_collections.community.docker.plugins.module_utils._copy import (
    _stream_generator_to_fileobj,
)

if t.TYPE_CHECKING:
    from collections.abc import Sequence

    T = t.TypeVar("T")


def _simple_generator(sequence: Sequence[T]) -> t.Generator[T]:
    yield from sequence


@pytest.mark.parametrize(
    "chunks, read_sizes",
    [
        (
            [
                (1, b"1"),
                (1, b"2"),
                (1, b"3"),
                (1, b"4"),
            ],
            [
                1,
                2,
                3,
            ],
        ),
        (
            [
                (1, b"123"),
                (1, b"456"),
                (1, b"789"),
            ],
            [
                1,
                4,
                2,
                2,
                2,
            ],
        ),
        (
            [
                (10 * 1024 * 1024, b"0"),
                (10 * 1024 * 1024, b"1"),
            ],
            [
                1024 * 1024 - 5,
                5 * 1024 * 1024 - 3,
                10 * 1024 * 1024 - 2,
                2 * 1024 * 1024 - 1,
                2 * 1024 * 1024 + 5 + 3 + 2 + 1,
            ],
        ),
    ],
)
def test__stream_generator_to_fileobj(
    chunks: list[tuple[int, bytes]], read_sizes: list[int]
) -> None:
    data_chunks = [count * data for count, data in chunks]
    stream = _simple_generator(data_chunks)
    expected = b"".join(data_chunks)

    buffer = b""
    totally_read = 0
    f = _stream_generator_to_fileobj(stream)
    for read_size in read_sizes:
        chunk = f.read(read_size)
        assert len(chunk) == min(read_size, len(expected) - len(buffer))
        buffer += chunk
        totally_read += read_size

    assert buffer == expected[: len(buffer)]
    assert min(totally_read, len(expected)) == len(buffer)
