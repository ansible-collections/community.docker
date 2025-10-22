# Copyright (c) 2019-2020, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Note that this module util is **PRIVATE** to the collection. It can have breaking changes at any time.
# Do not use this from other collections or standalone plugins/modules!

from __future__ import annotations

import typing as t

from ansible_collections.community.docker.plugins.module_utils._socket_handler import (
    DockerSocketHandlerBase,
)


if t.TYPE_CHECKING:
    from ansible.utils.display import Display

    from ansible_collections.community.docker.plugins.module_utils._socket_helper import (
        SocketLike,
    )


class DockerSocketHandler(DockerSocketHandlerBase):
    def __init__(
        self, display: Display, sock: SocketLike, container: str | None = None
    ) -> None:
        super().__init__(sock, log=lambda msg: display.vvvv(msg, host=container))
