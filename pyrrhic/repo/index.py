from dataclasses import dataclass
from functools import cache
from pathlib import Path

import msgspec

from pyrrhic.crypto.keys import MasterKey, decrypt_mac


class Blob(msgspec.Struct):
    id: str
    type: str
    offset: int
    length: int


class BlobList(msgspec.Struct):
    id: str
    blobs: list[Blob]


class RecPackList(msgspec.Struct):
    packs: list[BlobList]


@dataclass(frozen=True)
class PackRef:
    id: str
    blob: Blob


@cache
def _get_index(key: MasterKey, repo_path: Path, index_prefix: str, glob: bool) -> list[BlobList]:
    if glob:
        paths = (repo_path / "index").glob(f"{index_prefix}*")
    else:
        paths = (repo_path / "index" / name for name in [index_prefix])
    return [packs for index_path in paths for packs in msgspec.json.decode(decrypt_mac(key, index_path.read_bytes()), type=RecPackList).packs]


class Index:
    "Internal Index representation"
    index: list[BlobList]

    def __init__(self, key: MasterKey, repo_path: Path, index_prefix: str, glob=True):
        self.index = _get_index(key, repo_path, index_prefix, glob)

    def get_packref(self, blob_id) -> PackRef:
        packrefs = [PackRef(id=blob_list.id, blob=blob) for blob_list in self.index for blob in blob_list.blobs if blob.id == blob_id]
        if len(packrefs) == 1:
            return packrefs[0]
        raise ValueError(f"Invalid blob id {blob_id}")
