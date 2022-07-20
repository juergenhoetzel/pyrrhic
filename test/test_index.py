from pyrrhic.crypto.keys import get_masterkey
from pyrrhic.repo.index import get_index

REPO_BASE = "restic_test_repositories"
INDEX_ID = "0de57faa699ec0450ddbafb789e165b4e1a3dbe3a09b071075f09ebbfbd6f4b2"
INDEX_FILE = f"{REPO_BASE}/restic_test_repository/index/{INDEX_ID}"
KEY_ID = "98f9e68226bf15a8e9616632df7c9df543e255b388bfca1cde0218009b77cdeb"
KEY_FILE = f"{REPO_BASE}/restic_test_repository/keys/{KEY_ID}"


def test_load_index():
    master_key = get_masterkey(KEY_FILE, b"password")
    index = get_index(INDEX_FILE, master_key)
    assert "packs" in index.keys()
    for pack in index["packs"]:
        assert "id" in pack.keys()
        assert "blobs" in pack.keys()
