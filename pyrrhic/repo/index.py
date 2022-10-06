import json
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import List

from pydantic import BaseModel

from pyrrhic.crypto.keys import MasterKey, decrypt_mac


class Blob(BaseModel):
    id: str
    type: str
    offset: int
    length: int


class PackList(BaseModel):
    id: str
    blobs: List[Blob]


@dataclass(frozen=True)
class PackRef:
    id: str
    blob: Blob


@cache
def _get_index(key: MasterKey, repo_path: Path, index_prefix: str, glob: bool) -> list[PackList]:
    if glob:
        paths = (repo_path / "index").glob(f"{index_prefix}*")
    else:
        paths = (repo_path / "index" / name for name in [index_prefix])
    return [PackList(**pack) for index_path in paths for pack in json.loads(decrypt_mac(key, index_path.read_bytes())).get("packs")]


class Index:
    "Internal Index representation"
    index: list[PackList]

    def __init__(self, key: MasterKey, repo_path: Path, index_prefix: str, glob=True):
        self.index = _get_index(key, repo_path, index_prefix, glob)

    def get_packref(self, blob_id) -> PackRef:
        if packref := next((PackRef(id=pack.id, blob=blob) for pack in self.index for blob in pack.blobs if blob.id == blob_id), None):
            return packref
        raise ValueError(f"Can't find blob id {blob_id}")
