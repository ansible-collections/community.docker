# Copyright (c) 2023, Felix Fontein <felix@fontein.de>
# Copyright (c) 2023, Léo El Amri (@lel-amri)
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Note that this module util is **PRIVATE** to the collection. It can have breaking changes at any time.
# Do not use this from other collections or standalone plugins/modules!

from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
import traceback
import typing as t
from collections import namedtuple
from shlex import quote

from ansible.module_utils.basic import missing_required_lib
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.community.docker.plugins.module_utils._logfmt import (
    InvalidLogFmt as _InvalidLogFmt,
)
from ansible_collections.community.docker.plugins.module_utils._logfmt import (
    parse_line as _parse_logfmt_line,
)
from ansible_collections.community.docker.plugins.module_utils._util import (
    DockerBaseClass,
)
from ansible_collections.community.docker.plugins.module_utils._version import (
    LooseVersion,
)


PYYAML_IMPORT_ERROR: None | str  # pylint: disable=invalid-name
try:
    import yaml

    try:
        # use C version if possible for speedup
        from yaml import CSafeDumper as _SafeDumper
    except ImportError:
        from yaml import SafeDumper as _SafeDumper  # type: ignore
except ImportError:
    HAS_PYYAML = False
    PYYAML_IMPORT_ERROR = traceback.format_exc()  # pylint: disable=invalid-name
else:
    HAS_PYYAML = True
    PYYAML_IMPORT_ERROR = None  # pylint: disable=invalid-name

if t.TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from ansible_collections.community.docker.plugins.module_utils._common_cli import (
        AnsibleModuleDockerClient as _Client,
    )


DOCKER_COMPOSE_FILES = (
    "compose.yaml",
    "compose.yml",
    "docker-compose.yaml",
    "docker-compose.yml",
)

DOCKER_STATUS_DONE = frozenset(
    (
        "Started",
        "Healthy",
        "Exited",
        "Restarted",
        "Running",
        "Created",
        "Stopped",
        "Killed",
        "Removed",
        # An extra, specific to containers
        "Recreated",
        # Extras for pull events
        "Pulled",
        # Extras for built events
        "Built",
    )
)
DOCKER_STATUS_WORKING = frozenset(
    (
        "Creating",
        "Starting",
        "Restarting",
        "Stopping",
        "Killing",
        "Removing",
        # An extra, specific to containers
        "Recreate",
        # Extras for pull events
        "Pulling",
        # Extras for build start events
        "Building",
    )
)
DOCKER_STATUS_PULL = frozenset(
    (
        "Pulled",
        "Pulling",
    )
)
DOCKER_STATUS_BUILD = frozenset(
    (
        "Built",
        "Building",
    )
)
DOCKER_STATUS_ERROR = frozenset(("Error",))
DOCKER_STATUS_WARNING = frozenset(("Warning",))
DOCKER_STATUS_WAITING = frozenset(("Waiting",))
DOCKER_STATUS = frozenset(
    DOCKER_STATUS_DONE
    | DOCKER_STATUS_WORKING
    | DOCKER_STATUS_PULL
    | DOCKER_STATUS_ERROR
    | DOCKER_STATUS_WAITING
)
DOCKER_STATUS_AND_WARNING = frozenset(DOCKER_STATUS | DOCKER_STATUS_WARNING)

DOCKER_PULL_PROGRESS_DONE = frozenset(
    (
        "Already exists",
        "Download complete",
        "Pull complete",
    )
)
DOCKER_PULL_PROGRESS_WORKING = frozenset(
    (
        "Pulling fs layer",
        "Waiting",
        "Downloading",
        "Verifying Checksum",
        "Extracting",
    )
)


class ResourceType:
    UNKNOWN = "unknown"
    NETWORK = "network"
    IMAGE = "image"
    IMAGE_LAYER = "image-layer"
    VOLUME = "volume"
    CONTAINER = "container"
    SERVICE = "service"

    @classmethod
    def from_docker_compose_event(cls, resource_type: str) -> t.Any:
        return {
            "Network": cls.NETWORK,
            "Image": cls.IMAGE,
            "Volume": cls.VOLUME,
            "Container": cls.CONTAINER,
            "Service": cls.SERVICE,
        }[resource_type]


Event = namedtuple("Event", ["resource_type", "resource_id", "status", "msg"])


_DRY_RUN_MARKER = "DRY-RUN MODE -"

_RE_RESOURCE_EVENT = re.compile(
    r"^"
    r"\s*"
    r"(?P<resource_type>Network|Image|Volume|Container)"
    r"\s+"
    r"(?P<resource_id>\S+)"
    r"\s+"
    r"(?P<status>\S(?:|.*\S))"
    r"\s*"
    r"$"
)

_RE_PULL_EVENT = re.compile(
    r"^"
    r"\s*"
    r"(?P<service>\S+)"
    r"\s+"
    f"(?P<status>{'|'.join(re.escape(status) for status in DOCKER_STATUS_PULL)})"
    r"\s*"
    r"$"
)

_DOCKER_PULL_PROGRESS_WD = sorted(
    DOCKER_PULL_PROGRESS_DONE | DOCKER_PULL_PROGRESS_WORKING
)

_RE_PULL_PROGRESS = re.compile(
    r"^"
    r"\s*"
    r"(?P<layer>\S+)"
    r"\s+"
    f"(?P<status>{'|'.join(re.escape(status) for status in _DOCKER_PULL_PROGRESS_WD)})"
    r"\s*"
    r"(?:|\s\[[^]]+\]\s+\S+\s*|\s+[0-9.kKmMgGbB]+/[0-9.kKmMgGbB]+\s*)"
    r"$"
)

_RE_ERROR_EVENT = re.compile(
    r"^"
    r"\s*"
    r"(?P<resource_id>\S+)"
    r"\s+"
    f"(?P<status>{'|'.join(re.escape(status) for status in DOCKER_STATUS_ERROR)})"
    r"\s*"
    r"(?P<msg>\S.*\S)?"
    r"$"
)

_RE_WARNING_EVENT = re.compile(
    r"^"
    r"\s*"
    r"(?P<resource_id>\S+)"
    r"\s+"
    f"(?P<status>{'|'.join(re.escape(status) for status in DOCKER_STATUS_WARNING)})"
    r"\s*"
    r"(?P<msg>\S.*\S)?"
    r"$"
)

_RE_CONTINUE_EVENT = re.compile(r"^\s*(?P<resource_id>\S+)\s+-\s*(?P<msg>\S(?:|.*\S))$")

_RE_SKIPPED_EVENT = re.compile(
    r"^"
    r"\s*"
    r"(?P<resource_id>\S+)"
    r"\s+"
    r"Skipped(?: -"
    r"\s*"
    r"(?P<msg>\S(?:|.*\S))|\s*)"
    r"$"
)

_RE_BUILD_START_EVENT = re.compile(r"^\s*build service\s+(?P<resource_id>\S+)$")

_RE_BUILD_PROGRESS_EVENT = re.compile(r"^\s*==>\s+(?P<msg>.*)$")

# The following needs to be kept in sync with the MINIMUM_VERSION compose_v2 docs fragment
MINIMUM_COMPOSE_VERSION = "2.18.0"


def _extract_event(
    line: str, warn_function: Callable[[str], None] | None = None
) -> tuple[Event | None, bool]:
    match = _RE_RESOURCE_EVENT.match(line)
    if match is not None:
        status = match.group("status")
        msg = None
        if status not in DOCKER_STATUS:
            status, msg = msg, status
        return (
            Event(
                ResourceType.from_docker_compose_event(match.group("resource_type")),
                match.group("resource_id"),
                status,
                msg,
            ),
            True,
        )
    match = _RE_PULL_EVENT.match(line)
    if match:
        return (
            Event(
                ResourceType.SERVICE,
                match.group("service"),
                match.group("status"),
                None,
            ),
            True,
        )
    match = _RE_ERROR_EVENT.match(line)
    if match:
        return (
            Event(
                ResourceType.UNKNOWN,
                match.group("resource_id"),
                match.group("status"),
                match.group("msg") or None,
            ),
            True,
        )
    match = _RE_WARNING_EVENT.match(line)
    if match:
        if warn_function:
            if match.group("msg"):
                msg = f"{match.group('resource_id')}: {match.group('msg')}"
            else:
                msg = f"Unspecified warning for {match.group('resource_id')}"
            warn_function(msg)
        return None, True
    match = _RE_PULL_PROGRESS.match(line)
    if match:
        return (
            Event(
                ResourceType.IMAGE_LAYER,
                match.group("layer"),
                match.group("status"),
                None,
            ),
            True,
        )
    match = _RE_SKIPPED_EVENT.match(line)
    if match:
        return (
            Event(
                ResourceType.UNKNOWN,
                match.group("resource_id"),
                "Skipped",
                match.group("msg"),
            ),
            True,
        )
    match = _RE_BUILD_START_EVENT.match(line)
    if match:
        return (
            Event(
                ResourceType.SERVICE,
                match.group("resource_id"),
                "Building",
                None,
            ),
            True,
        )
    return None, False


def _extract_logfmt_event(
    line: str, warn_function: Callable[[str], None] | None = None
) -> tuple[Event | None, bool]:
    try:
        result = _parse_logfmt_line(line, logrus_mode=True)
    except _InvalidLogFmt:
        return None, False
    if "time" not in result or "level" not in result or "msg" not in result:
        return None, False
    if result["level"] == "warning":
        if warn_function:
            warn_function(result["msg"])
        return None, True
    # TODO: no idea what to do with this
    return None, False


def _warn_missing_dry_run_prefix(
    line: str,
    warn_missing_dry_run_prefix: bool,
    warn_function: Callable[[str], None] | None,
) -> None:
    if warn_missing_dry_run_prefix and warn_function:
        # This could be a bug, a change of docker compose's output format, ...
        # Tell the user to report it to us :-)
        warn_function(
            f"Event line is missing dry-run mode marker: {line!r}. Please check with the latest community.docker version,"
            " and if the problem still happens there, please report this at "
            "https://github.com/ansible-collections/community.docker/issues/new?assignees=&labels=&projects=&template=bug_report.md"
        )


def _warn_unparsable_line(
    line: str, warn_function: Callable[[str], None] | None
) -> None:
    # This could be a bug, a change of docker compose's output format, ...
    # Tell the user to report it to us :-)
    if warn_function:
        warn_function(
            f"Cannot parse event from line: {line!r}. Please check with the latest community.docker version,"
            " and if the problem still happens there, please report this at "
            "https://github.com/ansible-collections/community.docker/issues/new?assignees=&labels=&projects=&template=bug_report.md"
        )


def _find_last_event_for(
    events: list[Event], resource_id: str
) -> tuple[int, Event] | None:
    for index, event in enumerate(reversed(events)):
        if event.resource_id == resource_id:
            return len(events) - 1 - index, event
    return None


def _concat_event_msg(event: Event, append_msg: str) -> Event:
    return Event(
        event.resource_type,
        event.resource_id,
        event.status,
        "\n".join(msg for msg in [event.msg, append_msg] if msg is not None),
    )


_JSON_LEVEL_TO_STATUS_MAP = {
    "warning": "Warning",
    "error": "Error",
}


def parse_json_events(
    stderr: bytes, warn_function: Callable[[str], None] | None = None
) -> list[Event]:
    events = []
    stderr_lines = stderr.splitlines()
    if stderr_lines and stderr_lines[-1] == b"":
        del stderr_lines[-1]
    for line in stderr_lines:
        line = line.strip()
        if not line.startswith(b"{") or not line.endswith(b"}"):
            if line.startswith(b"Warning: "):
                # This is a bug in Compose that will get fixed by https://github.com/docker/compose/pull/11996
                event = Event(
                    ResourceType.UNKNOWN,
                    None,
                    "Warning",
                    to_text(line[len(b"Warning: ") :]),
                )
                events.append(event)
                continue
            if warn_function:
                warn_function(
                    f"Cannot parse event from non-JSON line: {line!r}. Please check with the latest community.docker version,"
                    " and if the problem still happens there, please report this at "
                    "https://github.com/ansible-collections/community.docker/issues/new?assignees=&labels=&projects=&template=bug_report.md"
                )
            continue
        try:
            line_data = json.loads(line)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            if warn_function:
                warn_function(
                    f"Cannot parse event from line: {line!r}: {exc}. Please check with the latest community.docker version,"
                    " and if the problem still happens there, please report this at "
                    "https://github.com/ansible-collections/community.docker/issues/new?assignees=&labels=&projects=&template=bug_report.md"
                )
            continue
        if line_data.get("tail"):
            resource_type = ResourceType.UNKNOWN
            msg = line_data.get("text")
            status = "Error"
            if isinstance(msg, str) and msg.lower().startswith("warning:"):
                # For some reason, Writer.TailMsgf() is always used for errors *except* in one place,
                # where its message is prepended with 'WARNING: ' (in pkg/compose/pull.go).
                status = "Warning"
                msg = msg[len("warning:") :].lstrip()
            event = Event(
                resource_type,
                None,
                status,
                msg,
            )
        elif line_data.get("error"):
            resource_type = ResourceType.UNKNOWN
            event = Event(
                resource_type,
                line_data.get("id"),
                "Error",
                line_data.get("message"),
            )
        else:
            resource_type = ResourceType.UNKNOWN
            resource_id = line_data.get("id")
            status = line_data.get("status")
            text = line_data.get("text")
            if resource_id == " " and text and text.startswith("build service "):
                # Example:
                # {"dry-run":true,"id":" ","text":"build service app"}
                resource_id = "S" + text[len("build s") :]
                text = "Building"
            if (
                isinstance(resource_id, str)
                and resource_id.endswith("==>")
                and text
                and text.startswith("==> writing image ")
            ):
                # Example:
                # {"dry-run":true,"id":"==>","text":"==> writing image dryRun-7d1043473d55bfa90e8530d35801d4e381bc69f0"}
                # {"dry-run":true,"id":"ansible-docker-test-dc713f1f-container ==>","text":"==> writing image dryRun-5d9204268db1a73d57bbd24a25afbeacebe2bc02"}
                # (The longer form happens since Docker Compose 2.39.0)
                continue
            if (
                isinstance(resource_id, str)
                and resource_id.endswith("==> ==>")
                and text
                and text.startswith("naming to ")
            ):
                # Example:
                # {"dry-run":true,"id":"==> ==>","text":"naming to display-app"}
                # {"dry-run":true,"id":"ansible-docker-test-dc713f1f-container ==> ==>","text":"naming to ansible-docker-test-dc713f1f-image"}
                # (The longer form happens since Docker Compose 2.39.0)
                continue
            if isinstance(resource_id, str) and " " in resource_id:
                resource_type_str, resource_id = resource_id.split(" ", 1)
                try:
                    resource_type = ResourceType.from_docker_compose_event(
                        resource_type_str
                    )
                except KeyError:
                    if warn_function:
                        warn_function(
                            f"Unknown resource type {resource_type_str!r} in line {line!r}. Please check with the latest community.docker version,"
                            " and if the problem still happens there, please report this at "
                            "https://github.com/ansible-collections/community.docker/issues/new?assignees=&labels=&projects=&template=bug_report.md"
                        )
                    resource_type = ResourceType.UNKNOWN
            elif text in DOCKER_STATUS_PULL:
                resource_type = ResourceType.IMAGE
                status, text = text, status
            elif (
                text in DOCKER_PULL_PROGRESS_DONE
                or line_data.get("text") in DOCKER_PULL_PROGRESS_WORKING
            ):
                resource_type = ResourceType.IMAGE_LAYER
                status, text = text, status
            elif (
                status is None
                and isinstance(text, str)
                and text.startswith("Skipped - ")
            ):
                status, text = text.split(" - ", 1)
            elif (
                line_data.get("level") in _JSON_LEVEL_TO_STATUS_MAP
                and "msg" in line_data
            ):
                status = _JSON_LEVEL_TO_STATUS_MAP[line_data["level"]]
                text = line_data["msg"]
            if (
                status not in DOCKER_STATUS_AND_WARNING
                and text in DOCKER_STATUS_AND_WARNING
            ):
                status, text = text, status
            event = Event(
                resource_type,
                resource_id,
                status,
                text,
            )

        events.append(event)
    return events


def parse_events(
    stderr: bytes,
    dry_run: bool = False,
    warn_function: Callable[[str], None] | None = None,
    nonzero_rc: bool = False,
) -> list[Event]:
    events = []
    error_event = None
    stderr_lines = stderr.splitlines()
    if stderr_lines and stderr_lines[-1] == b"":
        del stderr_lines[-1]
    for index, line_b in enumerate(stderr_lines):
        line = to_text(line_b.strip())
        if not line:
            continue
        warn_missing_dry_run_prefix = False
        if dry_run:
            if line.startswith(_DRY_RUN_MARKER):
                line = line[len(_DRY_RUN_MARKER) :].lstrip()
            else:
                warn_missing_dry_run_prefix = True
        event, parsed = _extract_event(line, warn_function=warn_function)
        if event is not None:
            events.append(event)
            if event.status in DOCKER_STATUS_ERROR:
                error_event = event
            else:
                error_event = None
            _warn_missing_dry_run_prefix(
                line, warn_missing_dry_run_prefix, warn_function
            )
            continue
        if parsed:
            continue
        match = _RE_BUILD_PROGRESS_EVENT.match(line)
        if match:
            # Ignore this
            continue
        match = _RE_CONTINUE_EVENT.match(line)
        if match:
            # Continuing an existing event
            index_event = _find_last_event_for(events, match.group("resource_id"))
            if index_event is not None:
                index, event = index_event
                events[index] = _concat_event_msg(event, match.group("msg"))
        event, parsed = _extract_logfmt_event(line, warn_function=warn_function)
        if event is not None:
            events.append(event)
        elif parsed:
            continue
        if error_event is not None:
            # Unparsable line that apparently belongs to the previous error event
            events[-1] = _concat_event_msg(error_event, line)
            continue
        if line.startswith("Error "):
            # Error message that is independent of an error event
            error_event = Event(
                ResourceType.UNKNOWN,
                "",
                "Error",
                line,
            )
            events.append(error_event)
            continue
        if len(stderr_lines) == 1 or (nonzero_rc and index == len(stderr_lines) - 1):
            # **Very likely** an error message that is independent of an error event
            error_event = Event(
                ResourceType.UNKNOWN,
                "",
                "Error",
                line,
            )
            events.append(error_event)
            continue
        _warn_missing_dry_run_prefix(line, warn_missing_dry_run_prefix, warn_function)
        _warn_unparsable_line(line, warn_function)
    return events


def has_changes(
    events: Sequence[Event],
    ignore_service_pull_events: bool = False,
    ignore_build_events: bool = False,
) -> bool:
    for event in events:
        if event.status in DOCKER_STATUS_WORKING:
            if ignore_service_pull_events and event.status in DOCKER_STATUS_PULL:
                continue
            if ignore_build_events and event.status in DOCKER_STATUS_BUILD:
                continue
            return True
        if (
            event.resource_type == ResourceType.IMAGE_LAYER
            and event.status in DOCKER_PULL_PROGRESS_WORKING
        ):
            return True
    return False


def extract_actions(events: Sequence[Event]) -> list[dict[str, t.Any]]:
    actions = []
    pull_actions = set()
    for event in events:
        if (
            event.resource_type == ResourceType.IMAGE_LAYER
            and event.status in DOCKER_PULL_PROGRESS_WORKING
        ):
            pull_id = (event.resource_id, event.status)
            if pull_id not in pull_actions:
                pull_actions.add(pull_id)
                actions.append(
                    {
                        "what": event.resource_type,
                        "id": event.resource_id,
                        "status": event.status,
                    }
                )
        if (
            event.resource_type != ResourceType.IMAGE_LAYER
            and event.status in DOCKER_STATUS_WORKING
        ):
            actions.append(
                {
                    "what": event.resource_type,
                    "id": event.resource_id,
                    "status": event.status,
                }
            )
    return actions


def emit_warnings(
    events: Sequence[Event], warn_function: Callable[[str], None]
) -> None:
    for event in events:
        # If a message is present, assume it is a warning
        if (
            event.status is None and event.msg is not None
        ) or event.status in DOCKER_STATUS_WARNING:
            warn_function(
                f"Docker compose: {event.resource_type} {event.resource_id}: {event.msg}"
            )


def is_failed(events: Sequence[Event], rc: int) -> bool:
    return bool(rc)


def update_failed(
    result: dict[str, t.Any],
    events: Sequence[Event],
    args: list[str],
    stdout: str | bytes,
    stderr: str | bytes,
    rc: int,
    cli: str,
) -> bool:
    if not rc:
        return False
    errors = []
    for event in events:
        if event.status in DOCKER_STATUS_ERROR:
            if event.resource_id is None:
                if event.resource_type == "unknown":
                    msg = (
                        "General error: "
                        if event.resource_type == "unknown"
                        else f"Error when processing {event.resource_type}: "
                    )
            else:
                msg = (
                    f"Error when processing {event.resource_type} {event.resource_id}: "
                )
                if event.resource_type == "unknown":
                    msg = f"Error when processing {event.resource_id}: "
                    if event.resource_id == "":
                        msg = "General error: "
            msg += f"{event.status}" if event.msg is None else f"{event.msg}"
            errors.append(msg)
    if not errors:
        errors.append(f"Return code {rc} is non-zero")
    result["failed"] = True
    result["msg"] = "\n".join(errors)
    result["cmd"] = " ".join(quote(arg) for arg in [cli] + args)
    result["stdout"] = to_text(stdout)
    result["stderr"] = to_text(stderr)
    result["rc"] = rc
    return True


def common_compose_argspec() -> dict[str, t.Any]:
    return {
        "project_src": {"type": "path"},
        "project_name": {"type": "str"},
        "files": {"type": "list", "elements": "path"},
        "definition": {"type": "dict"},
        "env_files": {"type": "list", "elements": "path"},
        "profiles": {"type": "list", "elements": "str"},
        "check_files_existing": {"type": "bool", "default": True},
    }


def common_compose_argspec_ex() -> dict[str, t.Any]:
    return {
        "argspec": common_compose_argspec(),
        "mutually_exclusive": [("definition", "project_src"), ("definition", "files")],
        "required_one_of": [
            ("definition", "project_src"),
        ],
        "required_by": {
            "definition": ("project_name",),
        },
    }


def combine_binary_output(*outputs: bytes | None) -> bytes:
    return b"\n".join(out for out in outputs if out)


def combine_text_output(*outputs: str | None) -> str:
    return "\n".join(out for out in outputs if out)


class BaseComposeManager(DockerBaseClass):
    def __init__(
        self, client: _Client, min_version: str = MINIMUM_COMPOSE_VERSION
    ) -> None:
        super().__init__()
        self.client = client
        self.check_mode = self.client.check_mode
        self.cleanup_dirs = set()
        parameters = self.client.module.params

        if parameters["definition"] is not None and not HAS_PYYAML:
            self.fail(missing_required_lib("PyYAML"), exception=PYYAML_IMPORT_ERROR)

        self.project_name = parameters["project_name"]
        if parameters["definition"] is not None:
            self.project_src = tempfile.mkdtemp(prefix="ansible")
            self.cleanup_dirs.add(self.project_src)
            compose_file = os.path.join(self.project_src, "compose.yaml")
            self.client.module.add_cleanup_file(compose_file)
            try:
                with open(compose_file, "wb") as f:
                    yaml.dump(
                        parameters["definition"],
                        f,
                        encoding="utf-8",
                        Dumper=_SafeDumper,
                    )
            except Exception as exc:  # pylint: disable=broad-exception-caught
                self.fail(f"Error writing to {compose_file} - {exc}")
        else:
            self.project_src = os.path.abspath(parameters["project_src"])

        self.files = parameters["files"]
        self.env_files = parameters["env_files"]
        self.profiles = parameters["profiles"]

        compose_version = self.get_compose_version()
        self.compose_version = LooseVersion(compose_version)
        if self.compose_version < LooseVersion(min_version):
            self.fail(
                f"Docker CLI {self.client.get_cli()} has the compose plugin with version {compose_version}; need version {min_version} or later"
            )

        if not os.path.isdir(self.project_src):
            self.fail(f'"{self.project_src}" is not a directory')

        self.check_files_existing = parameters["check_files_existing"]
        if self.files:
            for file in self.files:
                path = os.path.join(self.project_src, file)
                if not os.path.exists(path):
                    self.fail(
                        f'Cannot find Compose file "{file}" relative to project directory "{self.project_src}"'
                    )
        elif self.check_files_existing and all(
            not os.path.exists(os.path.join(self.project_src, f))
            for f in DOCKER_COMPOSE_FILES
        ):
            filenames = ", ".join(DOCKER_COMPOSE_FILES[:-1])
            self.fail(
                f'"{self.project_src}" does not contain {filenames}, or {DOCKER_COMPOSE_FILES[-1]}'
            )

        # Support for JSON output was added in Compose 2.29.0 (https://github.com/docker/compose/releases/tag/v2.29.0);
        # more precisely in https://github.com/docker/compose/pull/11478
        self.use_json_events = self.compose_version >= LooseVersion("2.29.0")

    def get_compose_version(self) -> str:
        return (
            self.get_compose_version_from_cli() or self.get_compose_version_from_api()
        )

    def get_compose_version_from_cli(self) -> str | None:
        rc, version_info, dummy_stderr = self.client.call_cli(
            "compose", "version", "--format", "json"
        )
        if rc:
            return None
        try:
            version = json.loads(version_info)["version"]
            if version == "dev":
                return None
            return version.lstrip("v")
        except Exception:  # pylint: disable=broad-exception-caught
            return None

    def get_compose_version_from_api(self) -> str:
        compose = self.client.get_client_plugin_info("compose")
        if compose is None:
            self.fail(
                f"Docker CLI {self.client.get_cli()} does not have the compose plugin installed"
            )
        if compose["Version"] == "dev":
            self.fail(
                f'Docker CLI {self.client.get_cli()} has a compose plugin installed, but it reports version "dev".'
                " Please use a version of the plugin that returns a proper version."
            )
        return compose["Version"].lstrip("v")

    def fail(self, msg: str, **kwargs: t.Any) -> t.NoReturn:
        self.cleanup()
        self.client.fail(msg, **kwargs)

    def get_base_args(self, plain_progress: bool = False) -> list[str]:
        args = ["compose", "--ansi", "never"]
        if self.use_json_events and not plain_progress:
            args.extend(["--progress", "json"])
        elif self.compose_version >= LooseVersion("2.19.0"):
            # https://github.com/docker/compose/pull/10690
            args.extend(["--progress", "plain"])
        args.extend(["--project-directory", self.project_src])
        if self.project_name:
            args.extend(["--project-name", self.project_name])
        for file in self.files or []:
            args.extend(["--file", file])
        for env_file in self.env_files or []:
            args.extend(["--env-file", env_file])
        for profile in self.profiles or []:
            args.extend(["--profile", profile])
        return args

    def _handle_failed_cli_call(
        self, args: list[str], rc: int, stdout: str | bytes, stderr: bytes
    ) -> t.NoReturn:
        events = parse_json_events(stderr, warn_function=self.client.warn)
        result: dict[str, t.Any] = {}
        self.update_failed(result, events, args, stdout, stderr, rc)
        self.client.module.exit_json(**result)

    def list_containers_raw(self) -> list[dict[str, t.Any]]:
        args = self.get_base_args() + ["ps", "--format", "json", "--all"]
        if self.compose_version >= LooseVersion("2.23.0"):
            # https://github.com/docker/compose/pull/11038
            args.append("--no-trunc")
        if self.compose_version >= LooseVersion("2.21.0"):
            # Breaking change in 2.21.0: https://github.com/docker/compose/pull/10918
            rc, containers, stderr = self.client.call_cli_json_stream(
                *args, cwd=self.project_src, check_rc=not self.use_json_events
            )
        else:
            rc, containers, stderr = self.client.call_cli_json(
                *args, cwd=self.project_src, check_rc=not self.use_json_events
            )
        if self.use_json_events and rc != 0:
            self._handle_failed_cli_call(args, rc, json.dumps(containers), stderr)
        return containers

    def list_containers(self) -> list[dict[str, t.Any]]:
        result = []
        for container in self.list_containers_raw():
            labels = {}
            if container.get("Labels"):
                for part in container["Labels"].split(","):
                    label_value = part.split("=", 1)
                    labels[label_value[0]] = (
                        label_value[1] if len(label_value) > 1 else ""
                    )
            container["Labels"] = labels
            container["Names"] = container.get("Names", container["Name"]).split(",")
            container["Networks"] = container.get("Networks", "").split(",")
            container["Publishers"] = container.get("Publishers") or []
            result.append(container)
        return result

    def list_images(self) -> list[str]:
        args = self.get_base_args() + ["images", "--format", "json"]
        rc, images, stderr = self.client.call_cli_json(
            *args, cwd=self.project_src, check_rc=not self.use_json_events
        )
        if self.use_json_events and rc != 0:
            self._handle_failed_cli_call(args, rc, images, stderr)
        if isinstance(images, dict):
            # Handle breaking change in Docker Compose 2.37.0; see
            # https://github.com/ansible-collections/community.docker/issues/1082
            # and https://github.com/docker/compose/issues/12916 for details
            images = list(images.values())
        return images

    def parse_events(
        self, stderr: bytes, dry_run: bool = False, nonzero_rc: bool = False
    ) -> list[Event]:
        if self.use_json_events:
            return parse_json_events(stderr, warn_function=self.client.warn)
        return parse_events(
            stderr,
            dry_run=dry_run,
            warn_function=self.client.warn,
            nonzero_rc=nonzero_rc,
        )

    def emit_warnings(self, events: Sequence[Event]) -> None:
        emit_warnings(events, warn_function=self.client.warn)

    def update_result(
        self,
        result: dict[str, t.Any],
        events: Sequence[Event],
        stdout: str | bytes,
        stderr: str | bytes,
        ignore_service_pull_events: bool = False,
        ignore_build_events: bool = False,
    ) -> None:
        result["changed"] = result.get("changed", False) or has_changes(
            events,
            ignore_service_pull_events=ignore_service_pull_events,
            ignore_build_events=ignore_build_events,
        )
        result["actions"] = result.get("actions", []) + extract_actions(events)
        result["stdout"] = combine_text_output(result.get("stdout"), to_text(stdout))
        result["stderr"] = combine_text_output(result.get("stderr"), to_text(stderr))

    def update_failed(
        self,
        result: dict[str, t.Any],
        events: Sequence[Event],
        args: list[str],
        stdout: str | bytes,
        stderr: bytes,
        rc: int,
    ) -> bool:
        return update_failed(
            result,
            events,
            args=args,
            stdout=stdout,
            stderr=stderr,
            rc=rc,
            cli=self.client.get_cli(),
        )

    def cleanup_result(self, result: dict[str, t.Any]) -> None:
        if not result.get("failed"):
            # Only return stdout and stderr if it is not empty
            for res in ("stdout", "stderr"):
                if result.get(res) == "":
                    result.pop(res)

    def cleanup(self) -> None:
        for directory in self.cleanup_dirs:
            try:
                shutil.rmtree(directory, True)
            except Exception:  # pylint: disable=broad-exception-caught
                # should not happen, but simply ignore to be on the safe side
                pass
