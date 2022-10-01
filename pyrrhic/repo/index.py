import json
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


class PackRef(BaseModel):
    id: str
    blobs: List[Blob]


class Index(BaseModel):
    packs: List[PackRef]


@cache
def get_index(key: MasterKey, repo_path: Path, index_prefix: str) -> List[Index]:
    return [Index(**json.loads(decrypt_mac(key, index_path.read_bytes()))) for index_path in (repo_path / "index").glob(f"{index_prefix}*")]
