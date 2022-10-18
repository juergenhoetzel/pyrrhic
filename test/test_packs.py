from pyrrhic.repo.index import Index
from pyrrhic.repo.pack import Pack

import pytest

from .params import params


@pytest.mark.parametrize("repo", [(p["repo"]) for p in params])
def test_index_matches_packs(repo):
    index = repo.get_index()
    assert type(index) == Index
    for blob_id, packref in index.index.items():
        p = Pack(repo.repository, repo.masterkey, packref.id)
        pack_blobs = p.get_blob_index()
        assert (matching_blob := next((blob for blob in pack_blobs if blob.hash.hex() == blob_id)))
        assert matching_blob.offset == packref.blob.offset
        assert matching_blob.length == packref.blob.length
        assert matching_blob.uncompressed_length == packref.blob.uncompressed_length
