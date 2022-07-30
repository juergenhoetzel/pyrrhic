from pyrrhic.repo.index import Index
from pyrrhic.repo.repository import Repository, get_masterkey

REPO_BASE = "restic_test_repositories"
INDEX_ID = "0de57faa699ec0450ddbafb789e165b4e1a3dbe3a09b071075f09ebbfbd6f4b2"


def test_load_index():
    repo = Repository(
        f"{REPO_BASE}/restic_test_repository", get_masterkey(f"{REPO_BASE}/restic_test_repository", "password")
    )
    index = repo.get_index(INDEX_ID)
    assert type(index) == Index
    assert len(index.packs)
