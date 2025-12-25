# Copyright (c) 2025 Felix Fontein
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import re
import typing as t

import pytest

from ansible_collections.community.docker.plugins.module_utils._image_name import (
    ImageName,
    is_digest,
    is_tag,
)

TEST_IS_DIGEST: list[tuple[str, dict[str, t.Any], bool]] = [
    ("", {}, False),
    ("", {"allow_empty": True}, True),
    ("sha256:abc", {}, False),
    (f"sha256:{'a' * 63}", {}, False),
    (f"sha256:{'a' * 64}", {}, True),
    (f"sha256:{'a' * 65}", {}, False),
    (
        "sha256:d02f9b9db4d759ef27dc26b426b842ff2fb881c5c6079612d27ec36e36b132dd",
        {},
        True,
    ),
    ("1.25.3", {}, False),
]


@pytest.mark.parametrize("name, kwargs, expected", TEST_IS_DIGEST)
def test_is_digest(name: str, kwargs: dict[str, t.Any], expected: bool) -> None:
    assert is_digest(name, **kwargs) == expected


TEST_IS_TAG: list[tuple[str, dict[str, t.Any], bool]] = [
    ("", {}, False),
    ("", {"allow_empty": True}, True),
    ("foo", {}, True),
    ("-foo", {}, False),
    ("f" * 128, {}, True),
    ("f" * 129, {}, False),
    (
        "sha256:d02f9b9db4d759ef27dc26b426b842ff2fb881c5c6079612d27ec36e36b132dd",
        {},
        False,
    ),
    ("1.25.3", {}, True),
]


@pytest.mark.parametrize("name, kwargs, expected", TEST_IS_TAG)
def test_is_tag(name: str, kwargs: dict[str, t.Any], expected: bool) -> None:
    assert is_tag(name, **kwargs) == expected


TEST_IMAGE_NAME_VALIDATE_SUCCESS: list[ImageName] = [
    ImageName(registry="localhost", path="nginx", tag=None, digest=None),
    ImageName(registry=None, path="nginx", tag="1.25.3", digest=None),
    ImageName(
        registry=None,
        path="nginx",
        tag=None,
        digest="sha256:d02f9b9db4d759ef27dc26b426b842ff2fb881c5c6079612d27ec36e36b132dd",
    ),
    ImageName(
        registry=None,
        path="nginx",
        tag="1.25.3",
        digest="sha256:d02f9b9db4d759ef27dc26b426b842ff2fb881c5c6079612d27ec36e36b132dd",
    ),
]


@pytest.mark.parametrize("data", TEST_IMAGE_NAME_VALIDATE_SUCCESS)
def test_imagename_validate_success(data: ImageName) -> None:
    assert data.validate() is data


TEST_IMAGE_NAME_VALIDATE_FAILED: list[tuple[ImageName, str]] = [
    (
        ImageName(registry="-foo", path="", tag=None, digest=None),
        'Invalid registry name (-foo): must not begin or end with a "-".',
    ),
    (
        ImageName(registry="foo:", path="", tag=None, digest=None),
        'Invalid registry name (foo:): must not end with ":".',
    ),
    (ImageName(registry=None, path="", tag=None, digest=None), "Invalid path ()."),
    (ImageName(registry=None, path="-", tag=None, digest=None), "Invalid path (-)."),
    (ImageName(registry=None, path="/", tag=None, digest=None), "Invalid path (/)."),
    (ImageName(registry=None, path="a", tag="-", digest=None), "Invalid tag (-)."),
    (ImageName(registry=None, path="a", tag=None, digest="-"), "Invalid digest (-)."),
]


@pytest.mark.parametrize("data, expected", TEST_IMAGE_NAME_VALIDATE_FAILED)
def test_imagename_validate_failed(data: ImageName, expected: str) -> None:
    with pytest.raises(ValueError, match=f"^{re.escape(expected)}$"):
        data.validate()


TEST_IMAGE_NAME_PARSE: list[tuple[str, ImageName]] = [
    ("", ImageName(registry=None, path="", tag=None, digest=None)),
    ("foo", ImageName(registry=None, path="foo", tag=None, digest=None)),
    ("foo:5000", ImageName(registry=None, path="foo", tag="5000", digest=None)),
    ("foo:5000/", ImageName(registry="foo:5000", path="", tag=None, digest=None)),
    ("foo:5000/bar", ImageName(registry="foo:5000", path="bar", tag=None, digest=None)),
    ("/bar", ImageName(registry=None, path="/bar", tag=None, digest=None)),
    (
        "localhost/foo:5000",
        ImageName(registry="localhost", path="foo", tag="5000", digest=None),
    ),
    (
        "foo.bar/baz:5000",
        ImageName(registry="foo.bar", path="baz", tag="5000", digest=None),
    ),
    (
        "foo:bar/baz:bam:5000",
        ImageName(registry="foo:bar", path="baz:bam", tag="5000", digest=None),
    ),
    ("foo:bar:baz", ImageName(registry=None, path="foo:bar", tag="baz", digest=None)),
    ("foo@bar@baz", ImageName(registry=None, path="foo@bar", tag=None, digest="baz")),
    ("nginx:1.25.3", ImageName(registry=None, path="nginx", tag="1.25.3", digest=None)),
    (
        "nginx@sha256:d02f9b9db4d759ef27dc26b426b842ff2fb881c5c6079612d27ec36e36b132dd",
        ImageName(
            registry=None,
            path="nginx",
            tag=None,
            digest="sha256:d02f9b9db4d759ef27dc26b426b842ff2fb881c5c6079612d27ec36e36b132dd",
        ),
    ),
    (
        "nginx:1.25.3@sha256:d02f9b9db4d759ef27dc26b426b842ff2fb881c5c6079612d27ec36e36b132dd",
        ImageName(
            registry=None,
            path="nginx",
            tag="1.25.3",
            digest="sha256:d02f9b9db4d759ef27dc26b426b842ff2fb881c5c6079612d27ec36e36b132dd",
        ),
    ),
]


@pytest.mark.parametrize("name, expected", TEST_IMAGE_NAME_PARSE)
def test_imagename_parse(name: str, expected: ImageName) -> None:
    assert ImageName.parse(name) == expected


TEST_IMAGE_NAME_COMBINE: list[tuple[ImageName, str]] = [
    (ImageName(registry=None, path="", tag=None, digest=None), ""),
    (ImageName(registry=None, path="nginx", tag="1.25.3", digest=None), "nginx:1.25.3"),
    (
        ImageName(
            registry=None,
            path="nginx",
            tag=None,
            digest="sha256:d02f9b9db4d759ef27dc26b426b842ff2fb881c5c6079612d27ec36e36b132dd",
        ),
        "nginx@sha256:d02f9b9db4d759ef27dc26b426b842ff2fb881c5c6079612d27ec36e36b132dd",
    ),
    (
        ImageName(
            registry=None,
            path="nginx",
            tag="1.25.3",
            digest="sha256:d02f9b9db4d759ef27dc26b426b842ff2fb881c5c6079612d27ec36e36b132dd",
        ),
        "nginx:1.25.3@sha256:d02f9b9db4d759ef27dc26b426b842ff2fb881c5c6079612d27ec36e36b132dd",
    ),
]


@pytest.mark.parametrize("data, expected", TEST_IMAGE_NAME_COMBINE)
def test_imagename_combine(data: ImageName, expected: str) -> None:
    assert data.combine() == expected


TEST_IMAGE_NAME_NORMALIZE: list[tuple[ImageName, ImageName]] = [
    (
        ImageName(registry=None, path="", tag=None, digest=None),
        ImageName(registry="docker.io", path="", tag=None, digest=None),
    ),
    (
        ImageName(registry="", path="", tag=None, digest=None),
        ImageName(registry="docker.io", path="", tag=None, digest=None),
    ),
    (
        ImageName(registry="index.docker.io", path="", tag=None, digest=None),
        ImageName(registry="docker.io", path="", tag=None, digest=None),
    ),
    (
        ImageName(registry="registry.hub.docker.com", path="", tag=None, digest=None),
        ImageName(registry="docker.io", path="", tag=None, digest=None),
    ),
    (
        ImageName(registry=None, path="foo/bar", tag=None, digest=None),
        ImageName(registry="docker.io", path="foo/bar", tag=None, digest=None),
    ),
    (
        ImageName(registry=None, path="nginx", tag="1.25.3", digest=None),
        ImageName(
            registry="docker.io", path="library/nginx", tag="1.25.3", digest=None
        ),
    ),
    (
        ImageName(
            registry=None,
            path="nginx",
            tag=None,
            digest="sha256:d02f9b9db4d759ef27dc26b426b842ff2fb881c5c6079612d27ec36e36b132dd",
        ),
        ImageName(
            registry="docker.io",
            path="library/nginx",
            tag=None,
            digest="sha256:d02f9b9db4d759ef27dc26b426b842ff2fb881c5c6079612d27ec36e36b132dd",
        ),
    ),
    (
        ImageName(
            registry=None,
            path="nginx",
            tag="1.25.3",
            digest="sha256:d02f9b9db4d759ef27dc26b426b842ff2fb881c5c6079612d27ec36e36b132dd",
        ),
        ImageName(
            registry="docker.io",
            path="library/nginx",
            tag="1.25.3",
            digest="sha256:d02f9b9db4d759ef27dc26b426b842ff2fb881c5c6079612d27ec36e36b132dd",
        ),
    ),
]


@pytest.mark.parametrize("data, expected", TEST_IMAGE_NAME_NORMALIZE)
def test_imagename_normalize(data: ImageName, expected: ImageName) -> None:
    assert data.normalize() == expected


TEST_IMAGE_NAME_HOSTNAME_AND_PORT: list[tuple[ImageName, str, int]] = [
    (
        ImageName(registry="docker.io", path="", tag=None, digest=None),
        "index.docker.io",
        443,
    ),
    (ImageName(registry="localhost", path="", tag=None, digest=None), "localhost", 443),
    (ImageName(registry="foo:5000", path="", tag=None, digest=None), "foo", 5000),
]


@pytest.mark.parametrize(
    "data, expected_hostname, expected_port", TEST_IMAGE_NAME_HOSTNAME_AND_PORT
)
def test_imagename_get_hostname_and_port(
    data: ImageName, expected_hostname: str, expected_port: int
) -> None:
    hostname, port = data.get_hostname_and_port()
    assert hostname == expected_hostname
    assert port == expected_port


def test_imagename_get_hostname_and_port_fail() -> None:
    msg = "Cannot get hostname when there is no registry. Normalize first!"
    with pytest.raises(ValueError, match=f"^{re.escape(msg)}$"):
        ImageName(registry=None, path="", tag=None, digest=None).get_hostname_and_port()
