import json
import re
from datetime import datetime
from pathlib import Path
from typing import Generator, List, Optional

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

    def __lt__(self, other):
        # Doesn't support more than 6 microsecond digits# Doesn't support more than 6 microsecond digits
        r = re.compile(r"(\.[0-9]{6})[0-9]*\+")
        dt = datetime.fromisoformat(r.sub(r"\1+", self.time))
        dt_other = datetime.fromisoformat(r.sub(r"\1+", other.time))
        return dt < dt_other


def get_snapshot(key: MasterKey, repo_path: Path, snapshot_prefix: str) -> Generator[Snapshot, None, None]:
    for snapshot_path in (repo_path / "snapshots").glob(f"{snapshot_prefix}*"):
        snapshot_json = json.loads(decrypt_mac(key, snapshot_path.read_bytes()))
        yield Snapshot(**snapshot_json)
