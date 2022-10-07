from pathlib import Path
from typing import Generator, List, Optional

import msgspec

from pyrrhic.crypto.keys import MasterKey, decrypt_mac
from pyrrhic.util import resticdatetime, resticdatetime_dec_hook


class Snapshot(msgspec.Struct):
    id: Optional[str] = None  # filled by pyrrhic
    time: resticdatetime
    tree: str
    paths: List[str]
    hostname: str
    username: str
    uid: Optional[int] = None  # Undocumented https://restic.readthedocs.io/en/stable/100_references.html#repository-format
    gid: Optional[int] = None
    excludes: Optional[List[str]] = None
    tags: Optional[List[str]] = None


def get_snapshot(key: MasterKey, repo_path: Path, snapshot_prefix: str) -> Generator[Snapshot, None, None]:
    dec = msgspec.json.Decoder(Snapshot, dec_hook=resticdatetime_dec_hook)
    for snapshot_path in (repo_path / "snapshots").glob(f"{snapshot_prefix}*"):
        snapshot = dec.decode(decrypt_mac(key, snapshot_path.read_bytes()))
        snapshot.id = snapshot_path.name
        yield snapshot
