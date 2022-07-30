"""
This module contains the repository abstractions used by pyrrhic.
"""
import json
import os
from dataclasses import dataclass
from pathlib import Path

from pyrrhic.crypto import keys
from pyrrhic.repo import index, snapshot


@dataclass(frozen=True)
class Repository:
    """Class that is used for high level access of Repository."""

    repository: Path
    masterkey: keys.MasterKey

    def get_index(self, index_id: str) -> index.Index:
        return index.get_index(os.path.join(str(self.repository), "index", index_id), self.masterkey)

    def get_snapshot(self, snapshot_id: str) -> snapshot.Snapshot:
        return snapshot.get_snapshot(os.path.join(str(self.repository), "snapshots", snapshot_id), self.masterkey)

    def get_config(self):
        with open(os.path.join(self.repository, "config"), "rb") as f:
            bs = f.read()
            plain = keys.decrypt_mac(self.masterkey, bs)
            return json.loads(plain)


def get_masterkey(repository: str, password: str) -> keys.MasterKey:
    if not password:
        raise ValueError("Please specify password")
    if not repository:
        raise ValueError("Please specify repository location")

    keys_path = Path(os.path.join(repository, "keys"))
    for kf in keys_path.iterdir():
        try:
            return keys.get_masterkey(str(kf), password.encode("utf8"))
        except ValueError as err:
            last_err = err
    raise last_err
