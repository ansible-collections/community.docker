# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

"""Unit tests for docker_swarm."""

from __future__ import annotations

import collections
import copy
import typing as t

import pytest

from ansible_collections.community.docker.plugins.modules import docker_swarm

# The spec of a swarm that was customised, as the daemon returns it (GET /swarm).
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
        "ExternalCAs": [{"Protocol": "cfssl", "URL": "https://ca.example.com"}],
    },
    "TaskDefaults": {"LogDriver": {"Name": "json-file", "Options": {"max-size": "1m"}}},
    "EncryptionConfig": {"AutoLockManagers": True},
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
    check_mode: bool = False,
    unsupported: tuple[str, ...] = (),
) -> t.Any:
    """A stand-in for AnsibleDockerSwarmClient talking to a manager of a swarm that has CURRENT_SPEC."""
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
    client.create_swarm_spec.return_value = {}
    client.get_unlock_key.return_value = {"UnlockKey": "SWMKEY-1-xxx"}
    client.inspect_swarm.return_value = {
        "ID": "swarm-id",
        "Version": {"Index": 42},
        "Spec": copy.deepcopy(CURRENT_SPEC),
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


def expected_spec(**changes: dict[str, t.Any]) -> dict[str, t.Any]:
    """CURRENT_SPEC with the given sections updated key by key."""
    spec = copy.deepcopy(CURRENT_SPEC)
    for section, values in changes.items():
        spec[section].update(values)
    return spec


def test_update_keeps_options_that_are_not_specified(mocker: t.Any) -> None:
    client = make_keep_client(mocker, {"task_history_retention_limit": 3})

    results = run_module(client)

    assert results["changed"] is True
    assert results["actions"] == ["Swarm cluster updated"]
    client.update_swarm.assert_called_once_with(
        version=42,
        swarm_spec=expected_spec(Orchestration={"TaskHistoryRetentionLimit": 3}),
        rotate_worker_token=False,
        rotate_manager_token=False,
    )


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

    spec = client.update_swarm.call_args.kwargs["swarm_spec"]
    assert spec == {
        "Name": "other",
        "Labels": {"a": "b"},
        "Orchestration": {"TaskHistoryRetentionLimit": 3},
        "Raft": {
            "SnapshotInterval": 1000,
            "KeepOldSnapshots": 1,
            "LogEntriesForSlowFollowers": 100,
            "ElectionTick": 20,
            "HeartbeatTick": 2,
        },
        "Dispatcher": {"HeartbeatPeriod": 8000000000},
        "CAConfig": {
            "NodeCertExpiry": 7200000000000,
            "ForceRotate": 2,
            "SigningCACert": "CERT",
            "SigningCAKey": "KEY",
            "ExternalCAs": CURRENT_SPEC["CAConfig"]["ExternalCAs"],
        },
        "TaskDefaults": CURRENT_SPEC["TaskDefaults"],
        "EncryptionConfig": {"AutoLockManagers": False},
    }


@pytest.mark.parametrize(
    "option, section, key",
    [
        ("task_history_retention_limit", "Orchestration", "TaskHistoryRetentionLimit"),
        ("snapshot_interval", "Raft", "SnapshotInterval"),
        ("keep_old_snapshots", "Raft", "KeepOldSnapshots"),
        ("log_entries_for_slow_followers", "Raft", "LogEntriesForSlowFollowers"),
        ("heartbeat_tick", "Raft", "HeartbeatTick"),
        ("election_tick", "Raft", "ElectionTick"),
        ("dispatcher_heartbeat_period", "Dispatcher", "HeartbeatPeriod"),
        ("node_cert_expiry", "CAConfig", "NodeCertExpiry"),
        ("ca_force_rotate", "CAConfig", "ForceRotate"),
    ],
)
def test_update_sends_an_option_that_is_set_to_zero(
    mocker: t.Any, option: str, section: str, key: str
) -> None:
    client = make_keep_client(mocker, {option: 0})

    run_module(client)

    client.update_swarm.assert_called_once()
    assert client.update_swarm.call_args.kwargs["swarm_spec"] == expected_spec(
        **{section: {key: 0}}
    )


def test_update_sends_autolock_managers_set_to_false(mocker: t.Any) -> None:
    client = make_keep_client(mocker, {"autolock_managers": False})

    run_module(client)

    assert client.update_swarm.call_args.kwargs["swarm_spec"] == expected_spec(
        EncryptionConfig={"AutoLockManagers": False}
    )


def test_update_replaces_labels_with_the_specified_ones(mocker: t.Any) -> None:
    client = make_keep_client(mocker, {"labels": {}})

    run_module(client)

    spec = client.update_swarm.call_args.kwargs["swarm_spec"]
    assert spec["Labels"] == {}
    assert {**spec, "Labels": CURRENT_SPEC["Labels"]} == CURRENT_SPEC


def test_rotating_a_token_alone_keeps_the_spec(mocker: t.Any) -> None:
    client = make_keep_client(mocker, {"rotate_worker_token": True})

    results = run_module(client)

    assert results["changed"] is True
    client.update_swarm.assert_called_once_with(
        version=42,
        swarm_spec=CURRENT_SPEC,
        rotate_worker_token=True,
        rotate_manager_token=False,
    )


def test_update_without_difference_does_not_call_the_daemon(mocker: t.Any) -> None:
    client = make_keep_client(
        mocker,
        {
            "task_history_retention_limit": 7,
            "snapshot_interval": 7777,
            "labels": {"env": "prod"},
            "autolock_managers": True,
        },
    )

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
    assert results["actions"] == ["Swarm cluster updated"]
    client.update_swarm.assert_not_called()


def test_update_skips_options_the_daemon_does_not_support(mocker: t.Any) -> None:
    client = make_keep_client(
        mocker,
        {"task_history_retention_limit": 3, "ca_force_rotate": 5},
        unsupported=("ca_force_rotate",),
    )

    run_module(client)

    assert client.update_swarm.call_args.kwargs["swarm_spec"] == expected_spec(
        Orchestration={"TaskHistoryRetentionLimit": 3}
    )


def test_update_swarm_spec_does_not_modify_the_current_spec(mocker: t.Any) -> None:
    client = make_keep_client(mocker, {"election_tick": 3, "labels": {"x": "y"}})
    current_spec = copy.deepcopy(CURRENT_SPEC)
    parameters = docker_swarm.TaskParameters.from_ansible_params(client)

    spec = parameters.update_swarm_spec(current_spec, client)

    assert current_spec == CURRENT_SPEC
    assert spec["Raft"]["ElectionTick"] == 3
    assert spec["Labels"] == {"x": "y"}
    assert (
        spec["CAConfig"]["ExternalCAs"] is not current_spec["CAConfig"]["ExternalCAs"]
    )


def test_update_swarm_spec_adds_a_section_the_daemon_left_out(mocker: t.Any) -> None:
    client = make_keep_client(mocker, {"snapshot_interval": 5})
    parameters = docker_swarm.TaskParameters.from_ansible_params(client)

    spec = parameters.update_swarm_spec({"Name": "default"}, client)

    assert spec == {"Name": "default", "Raft": {"SnapshotInterval": 5}}


def test_update_swarm_spec_replaces_a_section_the_daemon_returned_as_null(
    mocker: t.Any,
) -> None:
    client = make_keep_client(mocker, {"snapshot_interval": 5})
    parameters = docker_swarm.TaskParameters.from_ansible_params(client)

    spec = parameters.update_swarm_spec({"Name": "default", "Raft": None}, client)

    assert spec == {"Name": "default", "Raft": {"SnapshotInterval": 5}}


def test_update_sends_only_the_specified_options_by_default(mocker: t.Any) -> None:
    client = make_client(mocker, {"task_history_retention_limit": 3})
    only_specified = {"Orchestration": {"TaskHistoryRetentionLimit": 3}}
    client.create_swarm_spec.return_value = only_specified

    results = run_module(client)

    assert results["changed"] is True
    client.create_swarm_spec.assert_called_with(task_history_retention_limit=3)
    client.update_swarm.assert_called_once_with(
        version=42,
        swarm_spec=only_specified,
        rotate_worker_token=False,
        rotate_manager_token=False,
    )


def test_rotating_a_token_alone_sends_an_empty_spec_by_default(
    mocker: t.Any,
) -> None:
    client = make_client(mocker, {"rotate_worker_token": True})

    results = run_module(client)

    assert results["changed"] is True
    client.create_swarm_spec.assert_called_with()
    client.update_swarm.assert_called_once_with(
        version=42,
        swarm_spec={},
        rotate_worker_token=True,
        rotate_manager_token=False,
    )


def test_keep_unspecified_options_does_not_send_what_create_swarm_spec_returns(
    mocker: t.Any,
) -> None:
    client = make_keep_client(mocker, {"task_history_retention_limit": 3})
    # The SDK's create_swarm_spec() only returns the specified options, and drops the ones set to zero.
    client.create_swarm_spec.return_value = {"Orchestration": {"Unexpected": 1}}

    run_module(client)

    assert client.update_swarm.call_args.kwargs["swarm_spec"] == expected_spec(
        Orchestration={"TaskHistoryRetentionLimit": 3}
    )
