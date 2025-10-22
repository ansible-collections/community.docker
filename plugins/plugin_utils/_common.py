# Copyright (c) 2019-2020, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Note that this module util is **PRIVATE** to the collection. It can have breaking changes at any time.
# Do not use this from other collections or standalone plugins/modules!

from __future__ import annotations

import typing as t

from ansible.errors import AnsibleConnectionFailure
from ansible.utils.display import Display

from ansible_collections.community.docker.plugins.module_utils._common import (
    AnsibleDockerClientBase,
)
from ansible_collections.community.docker.plugins.module_utils._util import (
    DOCKER_COMMON_ARGS,
)


if t.TYPE_CHECKING:
    from ansible.plugins import AnsiblePlugin


class AnsibleDockerClient(AnsibleDockerClientBase):
    def __init__(
        self,
        plugin: AnsiblePlugin,
        min_docker_version: str | None = None,
        min_docker_api_version: str | None = None,
    ) -> None:
        self.plugin = plugin
        self.display = Display()
        super().__init__(
            min_docker_version=min_docker_version,
            min_docker_api_version=min_docker_api_version,
        )

    def fail(self, msg: str, **kwargs: t.Any) -> t.NoReturn:
        if kwargs:
            msg += "\nContext:\n" + "\n".join(
                f"  {k} = {v!r}" for (k, v) in kwargs.items()
            )
        raise AnsibleConnectionFailure(msg)

    def deprecate(
        self,
        msg: str,
        version: str | None = None,
        date: str | None = None,
        collection_name: str | None = None,
    ) -> None:
        self.display.deprecated(
            msg, version=version, date=date, collection_name=collection_name
        )

    def _get_params(self) -> dict[str, t.Any]:
        return {option: self.plugin.get_option(option) for option in DOCKER_COMMON_ARGS}
