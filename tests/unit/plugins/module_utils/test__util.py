# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import typing as t

import pytest

from ansible_collections.community.docker.plugins.module_utils._util import (
    compare_dict_allow_more_present,
    compare_generic,
    convert_duration_to_nanosecond,
    filter_images_by_tag,
    parse_healthcheck,
)


if t.TYPE_CHECKING:

    class DAMSpec(t.TypedDict):
        av: dict[str, t.Any]
        bv: dict[str, t.Any]
        result: bool

    class Spec(t.TypedDict):
        a: t.Any
        b: t.Any
        method: t.Literal["strict", "ignore", "allow_more_present"]
        type: t.Literal["value", "list", "set", "set(dict)", "dict"]
        result: bool


DICT_ALLOW_MORE_PRESENT: list[DAMSpec] = [
    {"av": {}, "bv": {"a": 1}, "result": True},
    {"av": {"a": 1}, "bv": {"a": 1, "b": 2}, "result": True},
    {"av": {"a": 1}, "bv": {"b": 2}, "result": False},
    {"av": {"a": 1}, "bv": {"a": None, "b": 1}, "result": False},
    {"av": {"a": None}, "bv": {"b": 1}, "result": False},
]

DICT_ALLOW_MORE_PRESENT_SPECS: list[Spec] = [
    {
        "a": entry["av"],
        "b": entry["bv"],
        "method": "allow_more_present",
        "type": "dict",
        "result": entry["result"],
    }
    for entry in DICT_ALLOW_MORE_PRESENT
]

COMPARE_GENERIC: list[Spec] = [
    ########################################################################################
    # value
    {"a": 1, "b": 2, "method": "strict", "type": "value", "result": False},
    {"a": "hello", "b": "hello", "method": "strict", "type": "value", "result": True},
    {"a": None, "b": "hello", "method": "strict", "type": "value", "result": False},
    {"a": None, "b": None, "method": "strict", "type": "value", "result": True},
    {"a": 1, "b": 2, "method": "ignore", "type": "value", "result": True},
    {"a": None, "b": 2, "method": "ignore", "type": "value", "result": True},
    ########################################################################################
    # list
    {
        "a": [
            "x",
        ],
        "b": [
            "y",
        ],
        "method": "strict",
        "type": "list",
        "result": False,
    },
    {
        "a": [
            "x",
        ],
        "b": [
            "x",
            "x",
        ],
        "method": "strict",
        "type": "list",
        "result": False,
    },
    {
        "a": [
            "x",
            "y",
        ],
        "b": [
            "x",
            "y",
        ],
        "method": "strict",
        "type": "list",
        "result": True,
    },
    {
        "a": [
            "x",
            "y",
        ],
        "b": [
            "y",
            "x",
        ],
        "method": "strict",
        "type": "list",
        "result": False,
    },
    {
        "a": [
            "x",
            "y",
        ],
        "b": [
            "x",
        ],
        "method": "allow_more_present",
        "type": "list",
        "result": False,
    },
    {
        "a": [
            "x",
        ],
        "b": [
            "x",
            "y",
        ],
        "method": "allow_more_present",
        "type": "list",
        "result": True,
    },
    {
        "a": [
            "x",
            "x",
            "y",
        ],
        "b": [
            "x",
            "y",
        ],
        "method": "allow_more_present",
        "type": "list",
        "result": False,
    },
    {
        "a": [
            "x",
            "z",
        ],
        "b": [
            "x",
            "y",
            "x",
            "z",
        ],
        "method": "allow_more_present",
        "type": "list",
        "result": True,
    },
    {
        "a": [
            "x",
            "y",
        ],
        "b": [
            "y",
            "x",
        ],
        "method": "ignore",
        "type": "list",
        "result": True,
    },
    ########################################################################################
    # set
    {
        "a": [
            "x",
        ],
        "b": [
            "y",
        ],
        "method": "strict",
        "type": "set",
        "result": False,
    },
    {
        "a": [
            "x",
        ],
        "b": [
            "x",
            "x",
        ],
        "method": "strict",
        "type": "set",
        "result": True,
    },
    {
        "a": [
            "x",
            "y",
        ],
        "b": [
            "x",
            "y",
        ],
        "method": "strict",
        "type": "set",
        "result": True,
    },
    {
        "a": [
            "x",
            "y",
        ],
        "b": [
            "y",
            "x",
        ],
        "method": "strict",
        "type": "set",
        "result": True,
    },
    {
        "a": [
            "x",
            "y",
        ],
        "b": [
            "x",
        ],
        "method": "allow_more_present",
        "type": "set",
        "result": False,
    },
    {
        "a": [
            "x",
        ],
        "b": [
            "x",
            "y",
        ],
        "method": "allow_more_present",
        "type": "set",
        "result": True,
    },
    {
        "a": [
            "x",
            "x",
            "y",
        ],
        "b": [
            "x",
            "y",
        ],
        "method": "allow_more_present",
        "type": "set",
        "result": True,
    },
    {
        "a": [
            "x",
            "z",
        ],
        "b": [
            "x",
            "y",
            "x",
            "z",
        ],
        "method": "allow_more_present",
        "type": "set",
        "result": True,
    },
    {
        "a": [
            "x",
            "a",
        ],
        "b": [
            "y",
            "z",
        ],
        "method": "ignore",
        "type": "set",
        "result": True,
    },
    ########################################################################################
    # set(dict)
    {
        "a": [
            {"x": 1},
        ],
        "b": [
            {"y": 1},
        ],
        "method": "strict",
        "type": "set(dict)",
        "result": False,
    },
    {
        "a": [
            {"x": 1},
        ],
        "b": [
            {"x": 1},
        ],
        "method": "strict",
        "type": "set(dict)",
        "result": True,
    },
    {
        "a": [
            {"x": 1},
        ],
        "b": [
            {"x": 1, "y": 2},
        ],
        "method": "strict",
        "type": "set(dict)",
        "result": True,
    },
    {
        "a": [
            {"x": 1},
            {"x": 2, "y": 3},
        ],
        "b": [
            {"x": 1},
            {"x": 2, "y": 3},
        ],
        "method": "strict",
        "type": "set(dict)",
        "result": True,
    },
    {
        "a": [
            {"x": 1},
        ],
        "b": [
            {"x": 1, "z": 2},
            {"x": 2, "y": 3},
        ],
        "method": "allow_more_present",
        "type": "set(dict)",
        "result": True,
    },
    {
        "a": [
            {"x": 1, "y": 2},
        ],
        "b": [
            {"x": 1},
            {"x": 2, "y": 3},
        ],
        "method": "allow_more_present",
        "type": "set(dict)",
        "result": False,
    },
    {
        "a": [
            {"x": 1, "y": 3},
        ],
        "b": [
            {"x": 1},
            {"x": 1, "y": 3, "z": 4},
        ],
        "method": "allow_more_present",
        "type": "set(dict)",
        "result": True,
    },
    {
        "a": [
            {"x": 1},
            {"x": 2, "y": 3},
        ],
        "b": [
            {"x": 1},
        ],
        "method": "ignore",
        "type": "set(dict)",
        "result": True,
    },
    ########################################################################################
    # dict
    {"a": {"x": 1}, "b": {"y": 1}, "method": "strict", "type": "dict", "result": False},
    {
        "a": {"x": 1},
        "b": {"x": 1, "y": 2},
        "method": "strict",
        "type": "dict",
        "result": False,
    },
    {"a": {"x": 1}, "b": {"x": 1}, "method": "strict", "type": "dict", "result": True},
    {
        "a": {"x": 1, "z": 2},
        "b": {"x": 1, "y": 2},
        "method": "strict",
        "type": "dict",
        "result": False,
    },
    {
        "a": {"x": 1, "z": 2},
        "b": {"x": 1, "y": 2},
        "method": "ignore",
        "type": "dict",
        "result": True,
    },
]


@pytest.mark.parametrize("entry", DICT_ALLOW_MORE_PRESENT)
def test_dict_allow_more_present(entry: DAMSpec) -> None:
    assert compare_dict_allow_more_present(entry["av"], entry["bv"]) == entry["result"]


@pytest.mark.parametrize("entry", COMPARE_GENERIC + DICT_ALLOW_MORE_PRESENT_SPECS)
def test_compare_generic(entry: Spec) -> None:
    assert (
        compare_generic(entry["a"], entry["b"], entry["method"], entry["type"])
        == entry["result"]
    )


def test_convert_duration_to_nanosecond() -> None:
    nanoseconds = convert_duration_to_nanosecond("5s")
    assert nanoseconds == 5000000000
    nanoseconds = convert_duration_to_nanosecond("1m5s")
    assert nanoseconds == 65000000000
    with pytest.raises(ValueError):
        convert_duration_to_nanosecond([1, 2, 3])  # type: ignore
    with pytest.raises(ValueError):
        convert_duration_to_nanosecond("10x")


def test_parse_healthcheck() -> None:
    result, disabled = parse_healthcheck(
        {
            "test": "sleep 1",
            "interval": "1s",
        }
    )
    assert disabled is False
    assert result == {"test": ["CMD-SHELL", "sleep 1"], "interval": 1000000000}

    result, disabled = parse_healthcheck(
        {
            "test": ["NONE"],
        }
    )
    assert result is None
    assert disabled

    result, disabled = parse_healthcheck({"test": "sleep 1", "interval": "1s423ms"})
    assert result == {"test": ["CMD-SHELL", "sleep 1"], "interval": 1423000000}
    assert disabled is False

    result, disabled = parse_healthcheck(
        {"test": "sleep 1", "interval": "1h1m2s3ms4us"}
    )
    assert result == {"test": ["CMD-SHELL", "sleep 1"], "interval": 3662003004000}
    assert disabled is False


# ========== filter_images_by_tag tests ==========
# Docker stores RepoTags and RepoDigests separately, never combined.
# This function handles tag-only, digest-only, and combined tag@digest formats.

SHA = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def _create_mock_image(
    repo_tags: list[str] | None, repo_digests: list[str] | None
) -> dict[str, t.Any]:
    """Helper to create mock image data as returned by Docker API."""
    return {
        "Id": "sha256:abc123",
        "RepoTags": repo_tags,
        "RepoDigests": repo_digests,
    }


class TestFilterImagesByTag:
    """Test cases for filter_images_by_tag function."""

    # ========== Tag-only tests ==========

    def test_tag_only_matches_repo_tags(self) -> None:
        """Tag-only reference should match in RepoTags."""
        image = _create_mock_image(
            repo_tags=["nginx:1.21"],
            repo_digests=["nginx@sha256:" + SHA],
        )
        result = filter_images_by_tag("nginx", "1.21", [image])
        assert len(result) == 1
        assert result[0]["Id"] == "sha256:abc123"

    def test_tag_only_no_match(self) -> None:
        """Tag-only reference should not match if tag is different."""
        image = _create_mock_image(
            repo_tags=["nginx:1.20"],
            repo_digests=["nginx@sha256:" + SHA],
        )
        result = filter_images_by_tag("nginx", "1.21", [image])
        assert len(result) == 0

    def test_tag_only_with_registry(self) -> None:
        """Tag-only with registry prefix should match correctly."""
        image = _create_mock_image(
            repo_tags=["ghcr.io/user/repo:v1.0"],
            repo_digests=["ghcr.io/user/repo@sha256:" + SHA],
        )
        result = filter_images_by_tag("ghcr.io/user/repo", "v1.0", [image])
        assert len(result) == 1

    # ========== Digest-only tests ==========

    def test_digest_only_matches_repo_digests(self) -> None:
        """Digest-only reference should match in RepoDigests."""
        image = _create_mock_image(
            repo_tags=["nginx:1.21"],
            repo_digests=["nginx@sha256:" + SHA],
        )
        result = filter_images_by_tag("nginx", f"sha256:{SHA}", [image])
        assert len(result) == 1

    def test_digest_only_no_match(self) -> None:
        """Digest-only reference should not match if digest is different."""
        other_sha = "a" * 64
        image = _create_mock_image(
            repo_tags=["nginx:1.21"],
            repo_digests=["nginx@sha256:" + SHA],
        )
        result = filter_images_by_tag("nginx", f"sha256:{other_sha}", [image])
        assert len(result) == 0

    # ========== Combined tag@digest tests ==========

    def test_combined_tag_digest_matches_both(self) -> None:
        """Combined tag@digest should match when BOTH tag AND digest match."""
        image = _create_mock_image(
            repo_tags=["nginx:1.21"],
            repo_digests=["nginx@sha256:" + SHA],
        )
        result = filter_images_by_tag("nginx", f"1.21@sha256:{SHA}", [image])
        assert len(result) == 1
        assert result[0]["Id"] == "sha256:abc123"

    def test_combined_tag_digest_with_registry(self) -> None:
        """Combined tag@digest with registry should match correctly."""
        image = _create_mock_image(
            repo_tags=["ghcr.io/gethomepage/homepage:v1.7"],
            repo_digests=["ghcr.io/gethomepage/homepage@sha256:" + SHA],
        )
        result = filter_images_by_tag(
            "ghcr.io/gethomepage/homepage", f"v1.7@sha256:{SHA}", [image]
        )
        assert len(result) == 1

    def test_combined_tag_digest_fails_if_tag_mismatch(self) -> None:
        """Combined tag@digest should NOT match if tag doesn't match."""
        image = _create_mock_image(
            repo_tags=["nginx:1.20"],  # Different tag
            repo_digests=["nginx@sha256:" + SHA],
        )
        result = filter_images_by_tag("nginx", f"1.21@sha256:{SHA}", [image])
        assert len(result) == 0

    def test_combined_tag_digest_fails_if_digest_mismatch(self) -> None:
        """Combined tag@digest should NOT match if digest doesn't match."""
        other_sha = "a" * 64
        image = _create_mock_image(
            repo_tags=["nginx:1.21"],
            repo_digests=["nginx@sha256:" + other_sha],  # Different digest
        )
        result = filter_images_by_tag("nginx", f"1.21@sha256:{SHA}", [image])
        assert len(result) == 0

    def test_combined_tag_digest_fails_if_both_mismatch(self) -> None:
        """Combined tag@digest should NOT match if both tag and digest don't match."""
        other_sha = "a" * 64
        image = _create_mock_image(
            repo_tags=["nginx:1.20"],  # Different tag
            repo_digests=["nginx@sha256:" + other_sha],  # Different digest
        )
        result = filter_images_by_tag("nginx", f"1.21@sha256:{SHA}", [image])
        assert len(result) == 0

    # ========== Edge cases ==========

    def test_empty_repo_tags(self) -> None:
        """Handle images where RepoTags is empty or None."""
        image = _create_mock_image(
            repo_tags=None,
            repo_digests=["nginx@sha256:" + SHA],
        )
        # Combined format should not match if RepoTags is empty
        result = filter_images_by_tag("nginx", f"1.21@sha256:{SHA}", [image])
        assert len(result) == 0

    def test_empty_repo_digests(self) -> None:
        """Handle images where RepoDigests is empty or None."""
        image = _create_mock_image(
            repo_tags=["nginx:1.21"],
            repo_digests=None,
        )
        # Combined format should not match if RepoDigests is empty
        result = filter_images_by_tag("nginx", f"1.21@sha256:{SHA}", [image])
        assert len(result) == 0

    def test_multiple_tags(self) -> None:
        """Image with multiple tags should match on any of them."""
        image = _create_mock_image(
            repo_tags=["nginx:1.21", "nginx:latest", "nginx:stable"],
            repo_digests=["nginx@sha256:" + SHA],
        )
        # Should match on 1.21
        result = filter_images_by_tag("nginx", f"1.21@sha256:{SHA}", [image])
        assert len(result) == 1
        # Should also match on latest
        result = filter_images_by_tag("nginx", f"latest@sha256:{SHA}", [image])
        assert len(result) == 1

    def test_multiple_digests(self) -> None:
        """Image with multiple digests should match on any of them."""
        other_sha = "b" * 64
        image = _create_mock_image(
            repo_tags=["nginx:1.21"],
            repo_digests=["nginx@sha256:" + SHA, "nginx@sha256:" + other_sha],
        )
        # Should match on first digest
        result = filter_images_by_tag("nginx", f"1.21@sha256:{SHA}", [image])
        assert len(result) == 1
        # Should also match on second digest
        result = filter_images_by_tag("nginx", f"1.21@sha256:{other_sha}", [image])
        assert len(result) == 1

    def test_port_in_registry_name(self) -> None:
        """Registry with port number should not be confused with tag."""
        image = _create_mock_image(
            repo_tags=["localhost:5000/myapp:v2.0"],
            repo_digests=["localhost:5000/myapp@sha256:" + SHA],
        )
        result = filter_images_by_tag(
            "localhost:5000/myapp", f"v2.0@sha256:{SHA}", [image]
        )
        assert len(result) == 1

    def test_no_tag_returns_all_images(self) -> None:
        """When tag is None, all images should be returned."""
        images = [
            _create_mock_image(["nginx:1.21"], ["nginx@sha256:" + SHA]),
            _create_mock_image(["nginx:1.20"], ["nginx@sha256:" + "a" * 64]),
        ]
        result = filter_images_by_tag("nginx", None, images)
        assert len(result) == 2

    # ========== Additional edge cases ==========

    def test_multiple_at_symbols_in_digest(self) -> None:
        """Handle edge case where digest has extra content after sha."""
        # Using split("@", 1) should handle this correctly
        image = _create_mock_image(
            repo_tags=["nginx:1.21"],
            repo_digests=["nginx@sha256:" + SHA],
        )
        # The sha256:... part should be treated as the digest
        result = filter_images_by_tag("nginx", f"1.21@sha256:{SHA}", [image])
        assert len(result) == 1

    def test_empty_tag_part_in_combined_format(self) -> None:
        """Handle edge case where tag part is empty like ':@sha256:...'."""
        image = _create_mock_image(
            repo_tags=["nginx:"],  # Empty tag
            repo_digests=["nginx@sha256:" + SHA],
        )
        # Should construct lookup_tag as "nginx:" which matches
        result = filter_images_by_tag("nginx", f"@sha256:{SHA}", [image])
        assert len(result) == 1
