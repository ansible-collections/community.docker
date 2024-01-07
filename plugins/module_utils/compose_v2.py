# Copyright (c) 2023, Felix Fontein <felix@fontein.de>
# Copyright (c) 2023, Léo El Amri (@lel-amri)
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import re
from collections import namedtuple

from ansible.module_utils.common.text.converters import to_native
from ansible.module_utils.six.moves import shlex_quote


DOCKER_STATUS_DONE = frozenset((
    'Started',
    'Healthy',
    'Exited',
    'Restarted',
    'Running',
    'Created',
    'Stopped',
    'Killed',
    'Removed',
    # An extra, specific to containers
    'Recreated',
    # Extras for pull events
    'Pulled',
))
DOCKER_STATUS_WORKING = frozenset((
    'Creating',
    'Starting',
    'Waiting',
    'Restarting',
    'Stopping',
    'Killing',
    'Removing',
    # An extra, specific to containers
    'Recreate',
    # Extras for pull events
    'Pulling',
))
DOCKER_STATUS_PULL = frozenset((
    'Pulled',
    'Pulling',
))
DOCKER_STATUS_ERROR = frozenset((
    'Error',
))
DOCKER_STATUS = frozenset(DOCKER_STATUS_DONE | DOCKER_STATUS_WORKING | DOCKER_STATUS_PULL | DOCKER_STATUS_ERROR)


class ResourceType(object):
    UNKNOWN = "unknown"
    NETWORK = "network"
    IMAGE = "image"
    VOLUME = "volume"
    CONTAINER = "container"
    SERVICE = "service"

    @classmethod
    def from_docker_compose_event(cls, resource_type):
        # type: (Type[ResourceType], Text) -> Any
        return {
            "Network": cls.NETWORK,
            "Image": cls.IMAGE,
            "Volume": cls.VOLUME,
            "Container": cls.CONTAINER,
        }[resource_type]


Event = namedtuple(
    'Event',
    ['resource_type', 'resource_id', 'status', 'msg']
)


_DRY_RUN_MARKER = 'DRY-RUN MODE -'

_RE_RESOURCE_EVENT = re.compile(
    r'^'
    r'\s*'
    r'(?P<resource_type>Network|Image|Volume|Container)'
    r'\s+'
    r'(?P<resource_id>\S+)'
    r'\s+'
    r'(?P<status>\S(?:|.*\S))'
    r'\s*'
    r'$'
)

_RE_PULL_EVENT = re.compile(
    r'^'
    r'\s*'
    r'(?P<service>\S+)'
    r'\s+'
    r'(?P<status>%s)'
    r'\s*'
    r'$'
    % '|'.join(re.escape(status) for status in DOCKER_STATUS_PULL)
)

_RE_ERROR_EVENT = re.compile(
    r'^'
    r'\s*'
    r'(?P<resource_id>\S+)'
    r'\s+'
    r'(?P<status>%s)'
    r'\s*'
    r'$'
    % '|'.join(re.escape(status) for status in DOCKER_STATUS_ERROR)
)


def parse_events(stderr, dry_run=False, warn_function=None):
    events = []
    error_event = None
    for line in stderr.splitlines():
        line = to_native(line.strip())
        if not line:
            continue
        if dry_run:
            if line.startswith(_DRY_RUN_MARKER):
                line = line[len(_DRY_RUN_MARKER):].lstrip()
            elif error_event is None and warn_function:
                # This could be a bug, a change of docker compose's output format, ...
                # Tell the user to report it to us :-)
                warn_function(
                    'Event line is missing dry-run mode marker: {0!r}. Please report this at '
                    'https://github.com/ansible-collections/community.docker/issues/new?assignees=&labels=&projects=&template=bug_report.md'
                    .format(line)
                )
        match = _RE_RESOURCE_EVENT.match(line)
        if match is not None:
            status = match.group('status')
            msg = None
            if status not in DOCKER_STATUS:
                status, msg = msg, status
            event = Event(
                ResourceType.from_docker_compose_event(match.group('resource_type')),
                match.group('resource_id'),
                status,
                msg,
            )
            events.append(event)
            if status in DOCKER_STATUS_ERROR:
                error_event = event
            else:
                error_event = None
            continue
        match = _RE_PULL_EVENT.match(line)
        if match:
            events.append(
                Event(
                    ResourceType.SERVICE,
                    match.group('service'),
                    match.group('status'),
                    None,
                )
            )
            error_event = None
            continue
        match = _RE_ERROR_EVENT.match(line)
        if match:
            error_event = Event(
                ResourceType.UNKNOWN,
                match.group('resource_id'),
                match.group('status'),
                None,
            )
            events.append(error_event)
            continue
        if error_event is not None:
            # Unparsable line that apparently belongs to the previous error event
            error_event = Event(
                error_event.resource_type,
                error_event.resource_id,
                error_event.status,
                '\n'.join(msg for msg in [error_event.msg, line] if msg is not None),
            )
            events[-1] = error_event
            continue
        if line.startswith('Error '):
            # Error message that is independent of an error event
            error_event = Event(
                ResourceType.UNKNOWN,
                '',
                'Error',
                line,
            )
            events.append(error_event)
            continue
        # This could be a bug, a change of docker compose's output format, ...
        # Tell the user to report it to us :-)
        if warn_function:
            warn_function(
                'Cannot parse event from line: {0!r}. Please report this at '
                'https://github.com/ansible-collections/community.docker/issues/new?assignees=&labels=&projects=&template=bug_report.md'
                .format(line)
            )
    return events


def has_changes(events):
    for event in events:
        if event.status in DOCKER_STATUS_WORKING:
            return True
    return False


def extract_actions(events):
    actions = []
    for event in events:
        if event.status in DOCKER_STATUS_WORKING:
            actions.append({
                'what': event.resource_type,
                'id': event.resource_id,
                'status': event.status,
            })
    return actions


def emit_warnings(events, warn_function):
    for event in events:
        # If a message is present, assume it is a warning
        if event.status is None and event.msg is not None:
            warn_function('Docker compose: {resource_type} {resource_id}: {msg}'.format(
                resource_type=event.resource_type,
                resource_id=event.resource_id,
                msg=event.msg,
            ))


def is_failed(events, rc):
    if rc:
        return True
    for event in events:
        if event.status in DOCKER_STATUS_ERROR:
            return True
    return False


def update_failed(result, events, args, stdout, stderr, rc, cli):
    errors = []
    for event in events:
        if event.status in DOCKER_STATUS_ERROR:
            msg = 'Error when processing {resource_type} {resource_id}: '
            if event.resource_type == 'unknown':
                msg = 'Error when processing {resource_id}: '
                if event.resource_id == '':
                    msg = 'General error: '
            msg += '{status}' if event.msg is None else '{msg}'
            errors.append(msg.format(
                resource_type=event.resource_type,
                resource_id=event.resource_id,
                status=event.status,
                msg=event.msg,
            ))
    if not errors and not rc:
        return False
    if not errors:
        errors.append('Return code {code} is non-zero'.format(code=rc))
    result['failed'] = True
    result['msg'] = '\n'.join(errors)
    result['cmd'] = ' '.join(shlex_quote(arg) for arg in [cli] + args)
    result['stdout'] = to_native(stdout)
    result['stderr'] = to_native(stderr)
    result['rc'] = rc
    return True
