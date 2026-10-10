# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

"""Unit tests for docker_swarm."""

from __future__ import annotations

import collections
import copy
import typing as t

import pytest

from ansible_collections.community.docker.plugins.module_utils._util import (
    DOCKER_COMMON_ARGS,
)
from ansible_collections.community.docker.plugins.modules import docker_swarm

EXTERNAL_CAS = [
    {
        "Protocol": "cfssl",
        "URL": "https://ca.example.com",
        "Options": {"key": "value"},
        "CACert": "-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----\n",
    }
]

# The spec of a swarm that was customised, as the daemon returns it (GET /swarm). The log driver is only here to
# have the module pass it on: the daemon does not return TaskDefaults.LogDriver.
CURRENT_SPEC: dict[str, t.Any] = {
    "Name": "default",
    "Labels": {"env": "prod"},
    "Orchestration": {"TaskHistoryRetentionLimit": 7},
    "Raft": {
        "SnapshotInterval": 7777,
        "KeepOldSnapshots": 2,
        "LogEntriesForSlowFollowers": 500,
        "ElectionTick": 10,
        "HeartbeatTick": 1,
    },
    "Dispatcher": {"HeartbeatPeriod": 11000000000},
    "CAConfig": {
        "NodeCertExpiry": 3600000000000000,
        "ForceRotate": 1,
        "ExternalCAs": EXTERNAL_CAS,
    },
    "TaskDefaults": {"LogDriver": {"Name": "json-file", "Options": {"max-size": "1m"}}},
    "EncryptionConfig": {"AutoLockManagers": True},
}

# What the module passes to create_swarm_spec() for CURRENT_SPEC when no option is specified.
CURRENT_PARAMS: dict[str, t.Any] = {
    "name": "default",
    "labels": {"env": "prod"},
    "task_history_retention_limit": 7,
    "snapshot_interval": 7777,
    "keep_old_snapshots": 2,
    "log_entries_for_slow_followers": 500,
    "election_tick": 10,
    "heartbeat_tick": 1,
    "dispatcher_heartbeat_period": 11000000000,
    "node_cert_expiry": 3600000000000000,
    "ca_force_rotate": 1,
    "external_cas": EXTERNAL_CAS,
    "log_driver": {"Name": "json-file", "Options": {"max-size": "1m"}},
    "autolock_managers": True,
}

# The same swarm after a task that only sets one option damaged it: the daemon stores what is missing as zero,
# and leaves out the keys that are zero.
DAMAGED_SPEC: dict[str, t.Any] = {
    "Name": "default",
    "Labels": {},
    "Orchestration": {"TaskHistoryRetentionLimit": 3},
    "Raft": {"KeepOldSnapshots": 0, "ElectionTick": 0, "HeartbeatTick": 0},
    "Dispatcher": {},
    "CAConfig": {},
    "TaskDefaults": {},
    "EncryptionConfig": {"AutoLockManagers": False},
}

# Mirrors the argument_spec built in main() of the module, with the value each option has when it is not specified.
MODULE_OPTIONS = {
    "advertise_addr": None,
    "data_path_addr": None,
    "data_path_port": None,
    "state": "present",
    "force": False,
    "listen_addr": "0.0.0.0:2377",
    "remote_addrs": None,
    "join_token": None,
    "snapshot_interval": None,
    "task_history_retention_limit": None,
    "keep_old_snapshots": None,
    "log_entries_for_slow_followers": None,
    "heartbeat_tick": None,
    "election_tick": None,
    "dispatcher_heartbeat_period": None,
    "node_cert_expiry": None,
    "name": None,
    "labels": None,
    "signing_ca_cert": None,
    "signing_ca_key": None,
    "ca_force_rotate": None,
    "autolock_managers": None,
    "node_id": None,
    "rotate_worker_token": False,
    "rotate_manager_token": False,
    "default_addr_pool": None,
    "subnet_size": None,
    "keep_unspecified_options": False,
}


def make_client(
    mocker: t.Any,
    options: dict[str, t.Any],
    *,
    spec: dict[str, t.Any] | None = None,
    check_mode: bool = False,
    unsupported: tuple[str, ...] = (),
) -> t.Any:
    """A stand-in for AnsibleDockerSwarmClient talking to a manager of a swarm that has the given spec."""
    client = mocker.MagicMock()
    client.check_mode = check_mode
    client.module.params = {**MODULE_OPTIONS, **options}
    client.module._diff = False
    # Like the real client, it has an entry for every option, the ones common to all docker modules included.
    versions: collections.defaultdict[str, dict[str, bool]] = collections.defaultdict(
        lambda: {"supported": True}
    )
    for option in unsupported:
        versions[option] = {"supported": False}
    client.option_minimal_versions = versions
    client.check_if_swarm_manager.return_value = True
    # What the SDK builds depends on the options it is given, so a test sees which options a spec was built from.
    client.create_swarm_spec.side_effect = lambda **kwargs: {"built from": kwargs}
    client.get_unlock_key.return_value = {"UnlockKey": "SWMKEY-1-xxx"}
    client.inspect_swarm.return_value = {
        "ID": "swarm-id",
        "Version": {"Index": 42},
        "Spec": copy.deepcopy(CURRENT_SPEC if spec is None else spec),
    }
    return client


def make_keep_client(
    mocker: t.Any, options: dict[str, t.Any], **kwargs: t.Any
) -> t.Any:
    """Like make_client(), with keep_unspecified_options=true."""
    return make_client(mocker, {"keep_unspecified_options": True, **options}, **kwargs)


def run_module(client: t.Any) -> dict[str, t.Any]:
    results: dict[str, t.Any] = {"changed": False, "result": "", "actions": []}
    docker_swarm.SwarmManager(client, results)()
    return results


def spec_options(client: t.Any) -> dict[str, t.Any]:
    """The options the last create_swarm_spec() call got, which is the one the update is built from."""
    return dict(client.create_swarm_spec.call_args.kwargs)


def assert_updated_with_built_spec(client: t.Any, **kwargs: t.Any) -> None:
    """The spec sent to the daemon is the one built from the options of the last create_swarm_spec() call."""
    client.update_swarm.assert_called_once_with(
        version=42,
        swarm_spec={"built from": spec_options(client)},
        rotate_worker_token=kwargs.get("rotate_worker_token", False),
        rotate_manager_token=kwargs.get("rotate_manager_token", False),
    )


def test_update_passes_the_current_options_that_are_not_specified(
    mocker: t.Any,
) -> None:
    client = make_keep_client(mocker, {"task_history_retention_limit": 3})

    results = run_module(client)

    assert results["changed"] is True
    assert results["actions"] == ["Swarm cluster updated"]
    assert spec_options(client) == {**CURRENT_PARAMS, "task_history_retention_limit": 3}
    assert_updated_with_built_spec(client)


def test_update_applies_all_specified_options(mocker: t.Any) -> None:
    client = make_keep_client(
        mocker,
        {
            "task_history_retention_limit": 3,
            "snapshot_interval": 1000,
            "keep_old_snapshots": 1,
            "log_entries_for_slow_followers": 100,
            "heartbeat_tick": 2,
            "election_tick": 20,
            "dispatcher_heartbeat_period": 8000000000,
            "node_cert_expiry": 7200000000000,
            "ca_force_rotate": 2,
            "autolock_managers": False,
            "name": "other",
            "labels": {"a": "b"},
            "signing_ca_cert": "CERT",
            "signing_ca_key": "KEY",
        },
    )

    run_module(client)

    assert spec_options(client) == {
        "task_history_retention_limit": 3,
        "snapshot_interval": 1000,
        "keep_old_snapshots": 1,
        "log_entries_for_slow_followers": 100,
        "heartbeat_tick": 2,
        "election_tick": 20,
        "dispatcher_heartbeat_period": 8000000000,
        "node_cert_expiry": 7200000000000,
        "ca_force_rotate": 2,
        "autolock_managers": False,
        "name": "other",
        "labels": {"a": "b"},
        "signing_ca_cert": "CERT",
        "signing_ca_key": "KEY",
        "external_cas": CURRENT_PARAMS["external_cas"],
        "log_driver": CURRENT_PARAMS["log_driver"],
    }


@pytest.mark.parametrize(
    "option",
    [
        "task_history_retention_limit",
        "snapshot_interval",
        "keep_old_snapshots",
        "log_entries_for_slow_followers",
        "heartbeat_tick",
        "election_tick",
        "dispatcher_heartbeat_period",
        "node_cert_expiry",
        "ca_force_rotate",
    ],
)
def test_update_passes_an_option_that_is_set_to_zero(
    mocker: t.Any, option: str
) -> None:
    client = make_keep_client(mocker, {option: 0})

    run_module(client)

    assert spec_options(client) == {**CURRENT_PARAMS, option: 0}


def test_update_passes_autolock_managers_set_to_false(mocker: t.Any) -> None:
    client = make_keep_client(mocker, {"autolock_managers": False})

    run_module(client)

    assert spec_options(client) == {**CURRENT_PARAMS, "autolock_managers": False}


def test_update_replaces_labels_with_the_specified_ones(mocker: t.Any) -> None:
    client = make_keep_client(mocker, {"labels": {}})

    run_module(client)

    assert spec_options(client) == {**CURRENT_PARAMS, "labels": {}}


def test_rotating_a_token_alone_passes_the_current_options(mocker: t.Any) -> None:
    client = make_keep_client(mocker, {"rotate_worker_token": True})

    results = run_module(client)

    assert results["changed"] is True
    assert spec_options(client) == CURRENT_PARAMS
    assert_updated_with_built_spec(client, rotate_worker_token=True)


def test_update_of_a_swarm_that_lost_options_passes_what_is_left(
    mocker: t.Any,
) -> None:
    client = make_keep_client(
        mocker, {"task_history_retention_limit": 5}, spec=DAMAGED_SPEC
    )

    run_module(client)

    # Options the daemon left out of the spec are not passed; the ones it stores as zero are.
    assert spec_options(client) == {
        "name": "default",
        "labels": {},
        "task_history_retention_limit": 5,
        "keep_old_snapshots": 0,
        "election_tick": 0,
        "heartbeat_tick": 0,
        "autolock_managers": False,
    }


def test_update_without_difference_does_not_call_the_daemon(mocker: t.Any) -> None:
    client = make_keep_client(mocker, {"task_history_retention_limit": 7})

    results = run_module(client)

    assert results["changed"] is False
    assert results["actions"] == ["No modification"]
    client.update_swarm.assert_not_called()


def test_update_in_check_mode_does_not_call_the_daemon(mocker: t.Any) -> None:
    client = make_keep_client(
        mocker, {"task_history_retention_limit": 3}, check_mode=True
    )

    results = run_module(client)

    assert results["changed"] is True
    client.update_swarm.assert_not_called()


def test_update_skips_options_the_daemon_does_not_support(mocker: t.Any) -> None:
    client = make_keep_client(
        mocker,
        {"task_history_retention_limit": 3},
        unsupported=("labels", "autolock_managers", "external_cas"),
    )

    run_module(client)

    expected = {**CURRENT_PARAMS, "task_history_retention_limit": 3}
    for option in ("labels", "autolock_managers", "external_cas"):
        del expected[option]
    assert spec_options(client) == expected


def test_update_sends_only_the_specified_options_by_default(mocker: t.Any) -> None:
    client = make_client(mocker, {"task_history_retention_limit": 3})

    results = run_module(client)

    assert results["changed"] is True
    assert spec_options(client) == {"task_history_retention_limit": 3}
    assert_updated_with_built_spec(client)


def test_rotating_a_token_alone_sends_no_option_by_default(mocker: t.Any) -> None:
    client = make_client(mocker, {"rotate_worker_token": True})

    results = run_module(client)

    assert results["changed"] is True
    assert spec_options(client) == {}
    assert_updated_with_built_spec(client, rotate_worker_token=True)


def test_update_builds_the_whole_spec_with_the_sdk(mocker: t.Any) -> None:
    docker_types = pytest.importorskip("docker.types")
    client = make_keep_client(mocker, {"task_history_retention_limit": 3})
    client.create_swarm_spec.side_effect = lambda **kwargs: docker_types.SwarmSpec(
        "1.41", **kwargs
    )

    run_module(client)

    expected = copy.deepcopy(CURRENT_SPEC)
    expected["Orchestration"]["TaskHistoryRetentionLimit"] = 3
    assert client.update_swarm.call_args.kwargs["swarm_spec"] == expected


class _Stop(Exception):
    pass


def declarations_of_main(mocker: t.Any) -> dict[str, t.Any]:
    """What main() declares to the client: the argument spec, and the minimal versions of the options."""
    declared: dict[str, t.Any] = {}

    def fake_client(**kwargs: t.Any) -> t.NoReturn:
        declared.update(kwargs)
        raise _Stop()

    mocker.patch.object(docker_swarm, "AnsibleDockerSwarmClient", fake_client)
    with pytest.raises(_Stop):
        docker_swarm.main()
    return declared


def test_keep_unspecified_options_defaults_to_the_current_behavior(
    mocker: t.Any,
) -> None:
    declared = declarations_of_main(mocker)

    assert declared["argument_spec"]["keep_unspecified_options"] == {
        "type": "bool",
        "default": False,
    }
    assert MODULE_OPTIONS["keep_unspecified_options"] is False


def test_the_sdk_version_needed_for_the_new_options_is_declared(
    mocker: t.Any,
) -> None:
    versions = declarations_of_main(mocker)["option_minimal_versions"]

    # Before 2.6.0 the SDK cannot build labels, autolock, ca_force_rotate or the external CAs of a spec.
    assert versions["keep_unspecified_options"] == {"docker_py_version": "2.6.0"}
    assert versions["external_cas"] == {"docker_py_version": "2.6.0"}


def test_every_task_parameter_has_a_declaration(mocker: t.Any) -> None:
    declared = declarations_of_main(mocker)
    known = (
        set(DOCKER_COMMON_ARGS)
        | set(declared["argument_spec"])
        | set(declared["option_minimal_versions"])
    )

    # The real client has a minimal version entry for these keys only; any other attribute raises a KeyError.
    assert set(vars(docker_swarm.TaskParameters())) - {"spec"} <= known
