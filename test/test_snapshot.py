from pathlib import Path

from pyrrhic.crypto.keys import get_masterkey
from pyrrhic.repo.snapshot import Snapshot, get_snapshot

import pytest

REPO_BASE = Path("restic_test_repositories")
SNAPSHOT_ID = "dd62b535d10bd8f24440cc300a868d6bf2f472859f1218883b0a6faca364c10c"
KEY_ID = "98f9e68226bf15a8e9616632df7c9df543e255b388bfca1cde0218009b77cdeb"
KEY_FILE = f"{REPO_BASE}/restic_test_repository/keys/{KEY_ID}"


@pytest.fixture
def masterkey():
    return get_masterkey(KEY_FILE, b"password")


def test_load_snapshot(masterkey):
    snapshot = get_snapshot(masterkey, REPO_BASE / "restic_test_repository", SNAPSHOT_ID)
    assert type(next(snapshot, None)) == Snapshot


def test_load_snapshot_prefix(masterkey):
    snapshots = get_snapshot(
        masterkey,
        REPO_BASE / "restic_test_repository",
        SNAPSHOT_ID,
    )
    snapshot = next(snapshots, None)
    assert snapshot
    assert next(snapshots, None) is None


def test_load_snapshot_invalid_prefix(masterkey):
    snapshot = next(get_snapshot(masterkey, REPO_BASE / "restic_test_repository", "invalid"), None)
    assert snapshot is None
