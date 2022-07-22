import json
from typing import List

from pydantic import BaseModel

from pyrrhic.crypto.keys import MasterKey, decrypt_mac


class Snapshot(BaseModel):
    time: str
    tree: str
    paths: List[str]
    hostname: str
    username: str
    uid: int
    gid: int


def get_snapshot(path: str, key: MasterKey) -> Snapshot:
    with open(path, "rb") as f:
        bs = f.read()
        snapshot_json = json.loads(decrypt_mac(key, bs))
        return Snapshot(**snapshot_json)
