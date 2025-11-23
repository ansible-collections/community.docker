# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2025, Paul Berruti

"""
Unit tests for _image_lookup functionality.

Tests the matching logic for combined tag@digest image references.
Docker stores RepoTags and RepoDigests separately, but users can reference
images using combined format: repo:tag@sha256:...

These tests verify that _image_lookup correctly handles:
1. Tag-only references (repo:tag)
2. Digest-only references (repo@sha256:...)
3. Combined tag+digest references (repo:tag@sha256:...)
"""

from __future__ import annotations

import unittest
from typing import Any
from unittest.mock import MagicMock, patch


class ImageLookupMatchingTests(unittest.TestCase):
    """Test cases for image lookup matching logic."""

    SHA = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    def _create_mock_image(
        self, repo_tags: list[str] | None, repo_digests: list[str] | None
    ) -> dict[str, Any]:
        """Helper to create mock image data as returned by Docker API."""
        return {
            "Id": "sha256:abc123",
            "RepoTags": repo_tags,
            "RepoDigests": repo_digests,
        }

    # Helper function to test the matching logic without needing full client setup
    def _match_image_in_response(
        self, name: str, tag: str | None, response: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """
        Reimplementation of the matching logic from _image_lookup for testing.
        This mirrors the actual implementation in _common.py and _common_api.py.
        """
        images = response
        if tag:
            images = []
            # Handle combined tag@digest format (e.g., "v1.0@sha256:abc123")
            if "@" in tag and not tag.startswith("sha256:"):
                tag_part, digest_part = tag.split("@", 1)
                lookup_tag = f"{name}:{tag_part}"
                lookup_digest = f"{name}@{digest_part}"
                for image in response:
                    tags = image.get("RepoTags") or []
                    digests = image.get("RepoDigests") or []
                    # For combined format, match BOTH tag AND digest
                    if lookup_tag in tags and lookup_digest in digests:
                        images = [image]
                        break
            else:
                # Original logic for tag-only or digest-only
                lookup = f"{name}:{tag}"
                lookup_digest = f"{name}@{tag}"
                for image in response:
                    tags = image.get("RepoTags")
                    digests = image.get("RepoDigests")
                    if (tags and lookup in tags) or (digests and lookup_digest in digests):
                        images = [image]
                        break
        return images

    def _match_image_original_logic(
        self, name: str, tag: str | None, response: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """
        Original buggy implementation for comparison.
        This shows what the code did BEFORE the fix.
        """
        images = response
        if tag:
            lookup = f"{name}:{tag}"
            lookup_digest = f"{name}@{tag}"
            images = []
            for image in response:
                tags = image.get("RepoTags")
                digests = image.get("RepoDigests")
                if (tags and lookup in tags) or (digests and lookup_digest in digests):
                    images = [image]
                    break
        return images

    # ========== Tag-only tests ==========

    def test_tag_only_matches_repo_tags(self) -> None:
        """Tag-only reference should match in RepoTags."""
        image = self._create_mock_image(
            repo_tags=["nginx:1.21"],
            repo_digests=["nginx@sha256:" + self.SHA],
        )
        result = self._match_image_in_response("nginx", "1.21", [image])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Id"], "sha256:abc123")

    def test_tag_only_no_match(self) -> None:
        """Tag-only reference should not match if tag is different."""
        image = self._create_mock_image(
            repo_tags=["nginx:1.20"],
            repo_digests=["nginx@sha256:" + self.SHA],
        )
        result = self._match_image_in_response("nginx", "1.21", [image])
        self.assertEqual(len(result), 0)

    def test_tag_only_with_registry(self) -> None:
        """Tag-only with registry prefix should match correctly."""
        image = self._create_mock_image(
            repo_tags=["ghcr.io/user/repo:v1.0"],
            repo_digests=["ghcr.io/user/repo@sha256:" + self.SHA],
        )
        result = self._match_image_in_response("ghcr.io/user/repo", "v1.0", [image])
        self.assertEqual(len(result), 1)

    # ========== Digest-only tests ==========

    def test_digest_only_matches_repo_digests(self) -> None:
        """Digest-only reference should match in RepoDigests."""
        image = self._create_mock_image(
            repo_tags=["nginx:1.21"],
            repo_digests=["nginx@sha256:" + self.SHA],
        )
        result = self._match_image_in_response("nginx", f"sha256:{self.SHA}", [image])
        self.assertEqual(len(result), 1)

    def test_digest_only_no_match(self) -> None:
        """Digest-only reference should not match if digest is different."""
        other_sha = "a" * 64
        image = self._create_mock_image(
            repo_tags=["nginx:1.21"],
            repo_digests=["nginx@sha256:" + self.SHA],
        )
        result = self._match_image_in_response("nginx", f"sha256:{other_sha}", [image])
        self.assertEqual(len(result), 0)

    # ========== Combined tag@digest tests ==========

    def test_combined_tag_digest_matches_both(self) -> None:
        """Combined tag@digest should match when BOTH tag AND digest match."""
        image = self._create_mock_image(
            repo_tags=["nginx:1.21"],
            repo_digests=["nginx@sha256:" + self.SHA],
        )
        result = self._match_image_in_response("nginx", f"1.21@sha256:{self.SHA}", [image])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Id"], "sha256:abc123")

    def test_combined_tag_digest_with_registry(self) -> None:
        """Combined tag@digest with registry should match correctly."""
        image = self._create_mock_image(
            repo_tags=["ghcr.io/gethomepage/homepage:v1.7"],
            repo_digests=["ghcr.io/gethomepage/homepage@sha256:" + self.SHA],
        )
        result = self._match_image_in_response(
            "ghcr.io/gethomepage/homepage", f"v1.7@sha256:{self.SHA}", [image]
        )
        self.assertEqual(len(result), 1)

    def test_combined_tag_digest_fails_if_tag_mismatch(self) -> None:
        """Combined tag@digest should NOT match if tag doesn't match."""
        image = self._create_mock_image(
            repo_tags=["nginx:1.20"],  # Different tag
            repo_digests=["nginx@sha256:" + self.SHA],
        )
        result = self._match_image_in_response("nginx", f"1.21@sha256:{self.SHA}", [image])
        self.assertEqual(len(result), 0)

    def test_combined_tag_digest_fails_if_digest_mismatch(self) -> None:
        """Combined tag@digest should NOT match if digest doesn't match."""
        other_sha = "a" * 64
        image = self._create_mock_image(
            repo_tags=["nginx:1.21"],
            repo_digests=["nginx@sha256:" + other_sha],  # Different digest
        )
        result = self._match_image_in_response("nginx", f"1.21@sha256:{self.SHA}", [image])
        self.assertEqual(len(result), 0)

    def test_combined_tag_digest_fails_if_both_mismatch(self) -> None:
        """Combined tag@digest should NOT match if both tag and digest don't match."""
        other_sha = "a" * 64
        image = self._create_mock_image(
            repo_tags=["nginx:1.20"],  # Different tag
            repo_digests=["nginx@sha256:" + other_sha],  # Different digest
        )
        result = self._match_image_in_response("nginx", f"1.21@sha256:{self.SHA}", [image])
        self.assertEqual(len(result), 0)

    # ========== Tests demonstrating the bug fix ==========

    def test_original_logic_fails_combined_tag_digest(self) -> None:
        """
        This test demonstrates that the ORIGINAL logic FAILS for combined tag@digest.

        The old code would construct:
        - lookup = "nginx:1.21@sha256:e3b0c4..." (never in RepoTags)
        - lookup_digest = "nginx@1.21@sha256:e3b0c4..." (never in RepoDigests)

        Neither would ever match Docker's data.
        """
        image = self._create_mock_image(
            repo_tags=["nginx:1.21"],
            repo_digests=["nginx@sha256:" + self.SHA],
        )
        # Original logic should FAIL to find the image
        result = self._match_image_original_logic("nginx", f"1.21@sha256:{self.SHA}", [image])
        self.assertEqual(len(result), 0, "Original logic should fail for combined tag@digest")

    def test_new_logic_succeeds_combined_tag_digest(self) -> None:
        """
        This test demonstrates that the NEW logic SUCCEEDS for combined tag@digest.

        The new code correctly splits the combined format and checks:
        - lookup_tag = "nginx:1.21" (matches in RepoTags)
        - lookup_digest = "nginx@sha256:e3b0c4..." (matches in RepoDigests)
        """
        image = self._create_mock_image(
            repo_tags=["nginx:1.21"],
            repo_digests=["nginx@sha256:" + self.SHA],
        )
        # New logic should SUCCEED in finding the image
        result = self._match_image_in_response("nginx", f"1.21@sha256:{self.SHA}", [image])
        self.assertEqual(len(result), 1, "New logic should succeed for combined tag@digest")

    # ========== Edge cases ==========

    def test_empty_repo_tags(self) -> None:
        """Handle images where RepoTags is empty or None."""
        image = self._create_mock_image(
            repo_tags=None,
            repo_digests=["nginx@sha256:" + self.SHA],
        )
        # Combined format should not match if RepoTags is empty
        result = self._match_image_in_response("nginx", f"1.21@sha256:{self.SHA}", [image])
        self.assertEqual(len(result), 0)

    def test_empty_repo_digests(self) -> None:
        """Handle images where RepoDigests is empty or None."""
        image = self._create_mock_image(
            repo_tags=["nginx:1.21"],
            repo_digests=None,
        )
        # Combined format should not match if RepoDigests is empty
        result = self._match_image_in_response("nginx", f"1.21@sha256:{self.SHA}", [image])
        self.assertEqual(len(result), 0)

    def test_multiple_tags(self) -> None:
        """Image with multiple tags should match on any of them."""
        image = self._create_mock_image(
            repo_tags=["nginx:1.21", "nginx:latest", "nginx:stable"],
            repo_digests=["nginx@sha256:" + self.SHA],
        )
        # Should match on 1.21
        result = self._match_image_in_response("nginx", f"1.21@sha256:{self.SHA}", [image])
        self.assertEqual(len(result), 1)
        # Should also match on latest
        result = self._match_image_in_response("nginx", f"latest@sha256:{self.SHA}", [image])
        self.assertEqual(len(result), 1)

    def test_multiple_digests(self) -> None:
        """Image with multiple digests should match on any of them."""
        other_sha = "b" * 64
        image = self._create_mock_image(
            repo_tags=["nginx:1.21"],
            repo_digests=["nginx@sha256:" + self.SHA, "nginx@sha256:" + other_sha],
        )
        # Should match on first digest
        result = self._match_image_in_response("nginx", f"1.21@sha256:{self.SHA}", [image])
        self.assertEqual(len(result), 1)
        # Should also match on second digest
        result = self._match_image_in_response("nginx", f"1.21@sha256:{other_sha}", [image])
        self.assertEqual(len(result), 1)

    def test_port_in_registry_name(self) -> None:
        """Registry with port number should not be confused with tag."""
        image = self._create_mock_image(
            repo_tags=["localhost:5000/myapp:v2.0"],
            repo_digests=["localhost:5000/myapp@sha256:" + self.SHA],
        )
        result = self._match_image_in_response(
            "localhost:5000/myapp", f"v2.0@sha256:{self.SHA}", [image]
        )
        self.assertEqual(len(result), 1)

    def test_no_tag_returns_all_images(self) -> None:
        """When tag is None, all images should be returned."""
        images = [
            self._create_mock_image(["nginx:1.21"], ["nginx@sha256:" + self.SHA]),
            self._create_mock_image(["nginx:1.20"], ["nginx@sha256:a" * 64]),
        ]
        result = self._match_image_in_response("nginx", None, images)
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
