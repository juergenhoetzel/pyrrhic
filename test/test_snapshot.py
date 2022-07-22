from pyrrhic.crypto.keys import get_masterkey
from pyrrhic.repo.snapshot import Snapshot, get_snapshot

REPO_BASE = "restic_test_repositories"
SNAPSHOT_ID = "dd62b535d10bd8f24440cc300a868d6bf2f472859f1218883b0a6faca364c10c"
SNAPSHOT_FILE = f"{REPO_BASE}/restic_test_repository/snapshots/{SNAPSHOT_ID}"
KEY_ID = "98f9e68226bf15a8e9616632df7c9df543e255b388bfca1cde0218009b77cdeb"
KEY_FILE = f"{REPO_BASE}/restic_test_repository/keys/{KEY_ID}"


def test_load_index():
    master_key = get_masterkey(KEY_FILE, b"password")
    snapshot = get_snapshot(SNAPSHOT_FILE, master_key)
    assert type(snapshot) == Snapshot
