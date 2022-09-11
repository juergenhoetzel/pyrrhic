import json
from pathlib import Path
from typing import List

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


def get_index(path: Path, key: MasterKey) -> Index:
    with open(path, "rb") as f:
        bs = f.read()
        plain = decrypt_mac(key, bs)
    json_index = json.loads(plain)
    return Index(**json_index)
