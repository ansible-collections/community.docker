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

import json
import json.decoder
import typing as t

from ..errors import StreamParseError


if t.TYPE_CHECKING:
    import re
    from collections.abc import Callable

    _T = t.TypeVar("_T")


json_decoder = json.JSONDecoder()


def stream_as_text(stream: t.Generator[bytes | str]) -> t.Generator[str]:
    """
    Given a stream of bytes or text, if any of the items in the stream
    are bytes convert them to text.
    This function can be removed once we return text streams
    instead of byte streams.
    """
    for data in stream:
        if not isinstance(data, str):
            data = data.decode("utf-8", "replace")
        yield data


def json_splitter(buffer: str) -> tuple[t.Any, str] | None:
    """Attempt to parse a json object from a buffer. If there is at least one
    object, return it and the rest of the buffer, otherwise return None.
    """
    buffer = buffer.strip()
    try:
        obj, index = json_decoder.raw_decode(buffer)
        ws: re.Pattern = json.decoder.WHITESPACE  # type: ignore[attr-defined]
        m = ws.match(buffer, index)
        rest = buffer[m.end() :] if m else buffer[index:]
        return obj, rest
    except ValueError:
        return None


def json_stream(stream: t.Generator[str | bytes]) -> t.Generator[t.Any]:
    """Given a stream of text, return a stream of json objects.
    This handles streams which are inconsistently buffered (some entries may
    be newline delimited, and others are not).
    """
    return split_buffer(stream, json_splitter, json_decoder.decode)


def line_splitter(buffer: str, separator: str = "\n") -> tuple[str, str] | None:
    index = buffer.find(str(separator))
    if index == -1:
        return None
    return buffer[: index + 1], buffer[index + 1 :]


def split_buffer(
    stream: t.Generator[str | bytes],
    splitter: Callable[[str], tuple[_T, str] | None],
    decoder: Callable[[str], _T],
) -> t.Generator[_T | str]:
    """Given a generator which yields strings and a splitter function,
    joins all input, splits on the separator and yields each chunk.
    Unlike string.split(), each chunk includes the trailing
    separator, except for the last one if none was found on the end
    of the input.
    """
    buffered = ""

    for data in stream_as_text(stream):
        buffered += data
        while True:
            buffer_split = splitter(buffered)
            if buffer_split is None:
                break

            item, buffered = buffer_split
            yield item

    if buffered:
        try:
            yield decoder(buffered)
        except Exception as e:
            raise StreamParseError(e) from e
