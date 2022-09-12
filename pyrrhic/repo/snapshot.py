import json
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel

from pyrrhic.crypto.keys import MasterKey, decrypt_mac


class Snapshot(BaseModel):
    time: str
    tree: str
    paths: List[str]
    hostname: str
    username: str
    uid: Optional[int]  # Undocumented https://restic.readthedocs.io/en/stable/100_references.html#repository-format
    gid: Optional[int]
    excludes: Optional[List[str]]
    tags: Optional[List[str]]


def get_snapshot(path: Path, key: MasterKey) -> Snapshot:
    with open(path, "rb") as f:
        bs = f.read()
        snapshot_json = json.loads(decrypt_mac(key, bs))
        return Snapshot(**snapshot_json)
