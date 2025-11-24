# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Tests for build_pull_arguments handling of tag@digest format.

When users specify an image with both tag and digest (e.g., nginx:1.21@sha256:abc...),
the parse_repository_tag function returns ("nginx", "1.21@sha256:abc...").

The Docker SDK and API don't accept "tag@digest" in the tag parameter.
build_pull_arguments handles this by:
- Returning full reference as name when tag contains @
- Returning None for tag in that case
"""

from __future__ import annotations

import unittest

from ansible_collections.community.docker.plugins.module_utils._util import (
    build_pull_arguments,
)


SHA = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


class TestBuildPullArguments(unittest.TestCase):
    """Test cases for build_pull_arguments function."""

    # ========== Tag-only tests ==========

    def test_tag_only_simple(self) -> None:
        """Tag-only should return name and tag separately."""
        assert build_pull_arguments("nginx", "1.21") == ("nginx", "1.21")

    def test_tag_only_latest(self) -> None:
        """Latest tag should return name and tag separately."""
        assert build_pull_arguments("nginx", "latest") == ("nginx", "latest")

    def test_tag_only_with_registry(self) -> None:
        """Tag-only with registry should return name and tag separately."""
        assert build_pull_arguments("ghcr.io/user/repo", "v1.0") == (
            "ghcr.io/user/repo",
            "v1.0",
        )

    def test_tag_only_with_registry_port(self) -> None:
        """Tag-only with registry port should return name and tag separately."""
        assert build_pull_arguments("localhost:5000/myapp", "v2.0") == (
            "localhost:5000/myapp",
            "v2.0",
        )

    # ========== Digest-only tests ==========

    def test_digest_only(self) -> None:
        """Digest-only (sha256:...) should return name and digest separately."""
        assert build_pull_arguments("nginx", f"sha256:{SHA}") == (
            "nginx",
            f"sha256:{SHA}",
        )

    def test_digest_only_with_registry(self) -> None:
        """Digest-only with registry should return name and digest separately."""
        assert build_pull_arguments("ghcr.io/user/repo", f"sha256:{SHA}") == (
            "ghcr.io/user/repo",
            f"sha256:{SHA}",
        )

    # ========== Combined tag@digest tests ==========

    def test_combined_tag_digest_simple(self) -> None:
        """Combined tag@digest should return full reference with None tag."""
        assert build_pull_arguments("nginx", f"1.21@sha256:{SHA}") == (
            f"nginx:1.21@sha256:{SHA}",
            None,
        )

    def test_combined_tag_digest_with_user_repo(self) -> None:
        """Combined tag@digest with user/repo should return full reference."""
        assert build_pull_arguments("portainer/portainer-ee", f"2.35.0-alpine@sha256:{SHA}") == (
            f"portainer/portainer-ee:2.35.0-alpine@sha256:{SHA}",
            None,
        )

    def test_combined_tag_digest_with_ghcr(self) -> None:
        """Combined tag@digest with GHCR should return full reference."""
        assert build_pull_arguments("ghcr.io/gethomepage/homepage", f"v1.7@sha256:{SHA}") == (
            f"ghcr.io/gethomepage/homepage:v1.7@sha256:{SHA}",
            None,
        )

    def test_combined_tag_digest_with_registry_port(self) -> None:
        """Combined tag@digest with registry port should return full reference."""
        assert build_pull_arguments("localhost:5000/myapp", f"v2.0@sha256:{SHA}") == (
            f"localhost:5000/myapp:v2.0@sha256:{SHA}",
            None,
        )

    # ========== Edge cases ==========

    def test_empty_tag_part_before_digest(self) -> None:
        """Handle edge case where tag part is empty like '@sha256:...'."""
        # This is an unusual case but should still work
        assert build_pull_arguments("nginx", f"@sha256:{SHA}") == (
            f"nginx:@sha256:{SHA}",
            None,
        )

    def test_tag_with_hyphen_and_digest(self) -> None:
        """Tag with hyphens and digest should work."""
        assert build_pull_arguments("nginx", f"1.21-alpine@sha256:{SHA}") == (
            f"nginx:1.21-alpine@sha256:{SHA}",
            None,
        )

    def test_tag_with_dots_and_digest(self) -> None:
        """Tag with dots and digest should work."""
        assert build_pull_arguments("nginx", f"1.21.0@sha256:{SHA}") == (
            f"nginx:1.21.0@sha256:{SHA}",
            None,
        )


class TestBuildPullArgumentsIntegration(unittest.TestCase):
    """Integration tests with parse_repository_tag."""

    def test_full_flow_docker_hub(self) -> None:
        """Test parse_repository_tag -> build_pull_arguments for Docker Hub."""
        from ansible_collections.community.docker.plugins.module_utils._api.utils.utils import (
            parse_repository_tag,
        )

        # User specifies: portainer/portainer-ee:2.35.0-alpine@sha256:abc...
        image_ref = f"portainer/portainer-ee:2.35.0-alpine@sha256:{SHA}"
        repo, tag = parse_repository_tag(image_ref)

        # parse_repository_tag returns repo and combined tag@digest
        assert repo == "portainer/portainer-ee"
        assert tag == f"2.35.0-alpine@sha256:{SHA}"

        # build_pull_arguments converts to full reference
        pull_name, pull_tag = build_pull_arguments(repo, tag)
        assert pull_name == f"portainer/portainer-ee:2.35.0-alpine@sha256:{SHA}"
        assert pull_tag is None

    def test_full_flow_ghcr(self) -> None:
        """Test parse_repository_tag -> build_pull_arguments for GHCR."""
        from ansible_collections.community.docker.plugins.module_utils._api.utils.utils import (
            parse_repository_tag,
        )

        # User specifies: ghcr.io/gethomepage/homepage:v1.7@sha256:abc...
        image_ref = f"ghcr.io/gethomepage/homepage:v1.7@sha256:{SHA}"
        repo, tag = parse_repository_tag(image_ref)

        assert repo == "ghcr.io/gethomepage/homepage"
        assert tag == f"v1.7@sha256:{SHA}"

        pull_name, pull_tag = build_pull_arguments(repo, tag)
        assert pull_name == f"ghcr.io/gethomepage/homepage:v1.7@sha256:{SHA}"
        assert pull_tag is None

    def test_full_flow_private_registry_with_port(self) -> None:
        """Test full flow for private registry with port number."""
        from ansible_collections.community.docker.plugins.module_utils._api.utils.utils import (
            parse_repository_tag,
        )

        # User specifies: localhost:5000/myapp:v2.0@sha256:abc...
        image_ref = f"localhost:5000/myapp:v2.0@sha256:{SHA}"
        repo, tag = parse_repository_tag(image_ref)

        # Port should be part of repo, not confused with tag
        assert repo == "localhost:5000/myapp"
        assert tag == f"v2.0@sha256:{SHA}"

        pull_name, pull_tag = build_pull_arguments(repo, tag)
        assert pull_name == f"localhost:5000/myapp:v2.0@sha256:{SHA}"
        assert pull_tag is None

    def test_full_flow_tag_only(self) -> None:
        """Test full flow for tag-only (no digest)."""
        from ansible_collections.community.docker.plugins.module_utils._api.utils.utils import (
            parse_repository_tag,
        )

        image_ref = "nginx:1.21"
        repo, tag = parse_repository_tag(image_ref)

        assert repo == "nginx"
        assert tag == "1.21"

        pull_name, pull_tag = build_pull_arguments(repo, tag)
        assert pull_name == "nginx"
        assert pull_tag == "1.21"

    def test_full_flow_digest_only(self) -> None:
        """Test full flow for digest-only (no tag)."""
        from ansible_collections.community.docker.plugins.module_utils._api.utils.utils import (
            parse_repository_tag,
        )

        image_ref = f"nginx@sha256:{SHA}"
        repo, tag = parse_repository_tag(image_ref)

        assert repo == "nginx"
        assert tag == f"sha256:{SHA}"

        pull_name, pull_tag = build_pull_arguments(repo, tag)
        assert pull_name == "nginx"
        assert pull_tag == f"sha256:{SHA}"
