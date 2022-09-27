import json
from datetime import datetime
from pathlib import Path
from typing import Generator, List, Optional

from pydantic import BaseModel

from pyrrhic.crypto.keys import MasterKey, decrypt_mac
from pyrrhic.util import datetime_from_restic


class Snapshot(BaseModel):
    id: str
    time: datetime
    tree: str
    paths: List[str]
    hostname: str
    username: str
    uid: Optional[int]  # Undocumented https://restic.readthedocs.io/en/stable/100_references.html#repository-format
    gid: Optional[int]
    excludes: Optional[List[str]]
    tags: Optional[List[str]]


def get_snapshot(key: MasterKey, repo_path: Path, snapshot_prefix: str) -> Generator[Snapshot, None, None]:
    for snapshot_path in (repo_path / "snapshots").glob(f"{snapshot_prefix}*"):
        snapshot_json = json.loads(decrypt_mac(key, snapshot_path.read_bytes()))
        snapshot_json["time"] = datetime_from_restic(snapshot_json["time"])
        yield Snapshot(id=snapshot_path.name, **snapshot_json)
