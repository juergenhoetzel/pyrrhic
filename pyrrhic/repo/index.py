import json
from pathlib import Path
from typing import Generator, List

from pydantic import BaseModel

from pyrrhic.crypto.keys import MasterKey, decrypt_mac


class Blob(BaseModel):
    id: str
    type: str
    offset: int
    length: int


class Pack(BaseModel):
    id: str
    blobs: List[Blob]


class Index(BaseModel):
    packs: List[Pack]


def get_index(key: MasterKey, repo_path: Path, index_prefix: str) -> Generator[Index, None, None]:
    for index_path in (repo_path / "index").glob(f"{index_prefix}*"):
        bs = index_path.read_bytes()
        plain = decrypt_mac(key, bs)
        json_index = json.loads(plain)
        yield Index(**json_index)
