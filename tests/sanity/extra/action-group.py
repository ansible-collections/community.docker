#!/usr/bin/env python
# Copyright (c) 2024, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
"""Make sure all modules that should show up in the action group."""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import yaml


def main():
    """Main entry point."""

    # Load redirects
    meta_runtime = 'meta/runtime.yml'
    try:
        with open(meta_runtime, 'rb') as f:
            data = yaml.safe_load(f)
        action_group = data['action_groups']['docker']
    except Exception as exc:
        print('%s: cannot load action group: %s' % (meta_runtime, exc))
        return

    exclusions = ['current_container_facts']
    modules_directory = 'plugins/modules/'
    modules_suffix = '.py'

    for file in os.listdir(modules_directory):
        if not file.endswith(modules_suffix):
            continue
        module_name = file[:-len(modules_suffix)]

        should_be_in_action_group = module_name not in exclusions

        if should_be_in_action_group:
            if module_name not in action_group:
                print('%s: module %s is not part of docker action group' % (meta_runtime, module_name))
            else:
                action_group.remove(module_name)

        path = os.path.join(modules_directory, file)
        documentation = []
        in_docs = False
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('DOCUMENTATION ='):
                    in_docs = True
                elif line.startswith(("'''", '"""')) and in_docs:
                    in_docs = False
                elif in_docs:
                    documentation.append(line)
        if in_docs:
            print('%s: cannot find DOCUMENTATION end' % (path))
        if not documentation:
            print('%s: cannot find DOCUMENTATION' % (path))
            continue

        try:
            docs = yaml.safe_load('\n'.join(documentation))
            if not isinstance(docs, dict):
                raise Exception('is not a top-level dictionary')
        except Exception as exc:
            print('%s: cannot load DOCUMENTATION as YAML: %s' % (path, exc))
            continue

        docs_fragments = docs.get('extends_documentation_fragment') or []
        is_in_action_group = 'community.docker.attributes.actiongroup_docker' in docs_fragments

        if should_be_in_action_group != is_in_action_group:
            if should_be_in_action_group:
                print('%s: module does not document itself as part of action group, but it should' % (path))
            else:
                print('%s: module documents itself as part of action group, but it should not be' % (path))

    for module_name in action_group:
        print('%s: module %s mentioned in docker action group does not exist' % (meta_runtime, module_name))


if __name__ == '__main__':
    main()
