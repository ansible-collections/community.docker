#!/usr/bin/python
#
# Copyright (c) 2021, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: docker_container_exec

short_description: Execute command in a docker container

version_added: 1.5.0

description:
  - Executes a command in a Docker container.

options:
  container:
    type: str
    required: true
    description:
      - The name of the container to execute the command in.
  argv:
    type: list
    elements: str
    description:
      - The command to execute.
      - Since this is a list of arguments, no quoting is needed.
      - Exactly one of I(argv) and I(command) must be specified.
  command:
    type: str
    description:
      - The command to execute.
      - Exactly one of I(argv) and I(command) must be specified.
  chdir:
    type: str
    description:
      - The directory to run the command in.
  user:
    type: str
    description:
      - If specified, the user to execute this command with.
  stdin:
    type: str
    description:
      - Set the stdin of the command directly to the specified value.
  stdin_add_newline:
    type: bool
    default: true
    description:
      - If set to C(true), appends a newline to I(stdin).
  strip_empty_ends:
    type: bool
    default: true
    description:
      - Strip empty lines from the end of stdout/stderr in result.
  tty:
    type: bool
    default: false
    description:
      - Whether to allocate a TTY.

extends_documentation_fragment:
  - community.docker.docker
  - community.docker.docker.docker_py_1_documentation
notes:
  - Does not support C(check_mode).
author:
  - "Felix Fontein (@felixfontein)"

requirements:
  - "L(Docker SDK for Python,https://docker-py.readthedocs.io/en/stable/) >= 1.8.0 (use L(docker-py,https://pypi.org/project/docker-py/) for Python 2.6)"
  - "Docker API >= 1.20"
'''

EXAMPLES = '''
- name: Run a simple command (command)
  community.docker.docker_container_exec:
    container: foo
    command: /bin/bash -c "ls -lah"
    chdir: /root
  register: result

- name: Print stdout
  debug:
    var: result.stdout

- name: Run a simple command (argv)
  community.docker.docker_container_exec:
    container: foo
    argv:
      - /bin/bash
      - "-c"
      - "ls -lah > /dev/stderr"
    chdir: /root
  register: result

- name: Print stderr lines
  debug:
    var: result.stderr_lines
'''

RETURN = '''
stdout:
    type: str
    returned: success
    description:
      - The standard output of the container command.
stderr:
    type: str
    returned: success
    description:
      - The standard error output of the container command.
rc:
    type: int
    returned: success
    sample: 0
    description:
      - The exit code of the command.
'''

import shlex
import traceback

from ansible.module_utils.common.text.converters import to_text, to_bytes, to_native

from ansible_collections.community.docker.plugins.module_utils.common import (
    AnsibleDockerClient,
    RequestException,
)

from ansible_collections.community.docker.plugins.module_utils.socket_helper import (
    shutdown_writing,
    write_to_socket,
)

from ansible_collections.community.docker.plugins.module_utils.socket_handler import (
    find_selectors,
    DockerSocketHandlerModule,
)

try:
    from docker.errors import DockerException, APIError, NotFound
except Exception:
    # missing Docker SDK for Python handled in ansible.module_utils.docker.common
    pass


def main():
    argument_spec = dict(
        container=dict(type='str', required=True),
        argv=dict(type='list', elements='str'),
        command=dict(type='str'),
        chdir=dict(type='str'),
        user=dict(type='str'),
        stdin=dict(type='str'),
        stdin_add_newline=dict(type='bool', default=True),
        strip_empty_ends=dict(type='bool', default=True),
        tty=dict(type='bool', default=False),
    )

    client = AnsibleDockerClient(
        argument_spec=argument_spec,
        min_docker_api_version='1.20',
        mutually_exclusive=[('argv', 'command')],
        required_one_of=[('argv', 'command')],
    )

    container = client.module.params['container']
    argv = client.module.params['argv']
    command = client.module.params['command']
    chdir = client.module.params['chdir']
    user = client.module.params['user']
    stdin = client.module.params['stdin']
    strip_empty_ends = client.module.params['strip_empty_ends']
    tty = client.module.params['tty']

    if command is not None:
        argv = shlex.split(command)

    if stdin is not None and client.module.params['stdin_add_newline']:
        stdin += '\n'

    selectors = None
    if stdin:
        selectors = find_selectors(client.module)

    try:
        exec_data = client.exec_create(
            container,
            argv,
            stdout=True,
            stderr=True,
            stdin=bool(stdin),
            user=user or '',
            workdir=chdir,
        )
        exec_id = exec_data['Id']

        if selectors:
            exec_socket = client.exec_start(
                exec_id,
                tty=tty,
                detach=False,
                socket=True,
            )
            try:
                with DockerSocketHandlerModule(exec_socket, client.module, selectors) as exec_socket_handler:
                    if stdin:
                        exec_socket_handler.write(to_bytes(stdin))

                    stdout, stderr = exec_socket_handler.consume()
            finally:
                exec_socket.close()
        else:
            stdout, stderr = client.exec_start(
                exec_id,
                tty=tty,
                detach=False,
                stream=False,
                socket=False,
                demux=True,
            )

        result = client.exec_inspect(exec_id)

        stdout = to_text(stdout or b'')
        stderr = to_text(stderr or b'')
        if strip_empty_ends:
            stdout = stdout.rstrip('\r\n')
            stderr = stderr.rstrip('\r\n')

        client.module.exit_json(
            changed=True,
            stdout=stdout,
            stderr=stderr,
            rc=result.get('ExitCode') or 0,
        )
    except NotFound:
        client.fail('Could not find container "{0}"'.format(container))
    except APIError as e:
        if e.response and e.response.status_code == 409:
            client.fail('The container "{0}" has been paused ({1})'.format(container, to_native(e)))
        client.fail('An unexpected docker error occurred: {0}'.format(to_native(e)), exception=traceback.format_exc())
    except DockerException as e:
        client.fail('An unexpected docker error occurred: {0}'.format(to_native(e)), exception=traceback.format_exc())
    except RequestException as e:
        client.fail(
            'An unexpected requests error occurred when docker-py tried to talk to the docker daemon: {0}'.format(to_native(e)),
            exception=traceback.format_exc())


if __name__ == '__main__':
    main()
