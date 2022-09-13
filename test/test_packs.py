from pathlib import Path

from pyrrhic.repo.pack import Pack
from pyrrhic.repo.repository import Repository, get_masterkey

import pytest

REPO_BASE = "restic_test_repositories"
INDEX_ID = "0de57faa699ec0450ddbafb789e165b4e1a3dbe3a09b071075f09ebbfbd6f4b2"
TEST_REPO = Path("./restic_test_repositories/restic_test_repository")


@pytest.fixture
def masterkey():
    return get_masterkey(TEST_REPO, "password")


def test_load_pack(masterkey):
    TEST_BLOB = TEST_REPO / "data/46/46771395523ccd6dda16694f0ce775f9508a4c3e4527c385f55d8efafa36807f"
    p = Pack(TEST_BLOB, masterkey)
    assert p


def test_index_matches_packs(masterkey):
    repo = Repository(Path(REPO_BASE) / "restic_test_repository", masterkey)
    index = repo.get_index(INDEX_ID)
    for index_pack in index.packs:
        pack_path = repo.repository / "data" / index_pack.id[:2] / index_pack.id
        p = Pack(pack_path, masterkey)
        for index_blob in index_pack.blobs:
            print("Checking ", index_blob.id)
            pack_blobs = p.get_blob_index()
            assert (matching_blob := next((blob for blob in pack_blobs if blob["id"] == index_blob.id)))
            assert matching_blob["offset"] == index_blob.offset
            assert matching_blob["length"] == index_blob.length
