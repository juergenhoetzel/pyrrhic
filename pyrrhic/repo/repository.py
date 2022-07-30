"""
This module contains the repository abstractions used by pyrrhic.
"""
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from pyrrhic.crypto import keys
from pyrrhic.repo import index, snapshot


@dataclass
class Repository:
    """Class that is used for high level access of Repository."""

    password: Optional[str] = None
    repository: Optional[Path] = None
    masterkey: Optional[keys.MasterKey] = None

    def get_masterkey(self) -> keys.MasterKey:
        if not self.password:
            raise ValueError("Please specify password")
        if not self.repository:
            raise ValueError("Please specify repository location")
        if self.masterkey:
            return self.masterkey
        keys_path = Path(os.path.join(self.repository, "keys"))
        for kf in keys_path.iterdir():
            try:
                self.masterkey = keys.get_masterkey(str(kf), self.password.encode("utf8"))
                return self.masterkey
            except ValueError as err:
                last_err = err
        raise last_err

    def get_index(self, index_id: str) -> index.Index:
        masterkey = self.get_masterkey()
        return index.get_index(os.path.join(str(self.repository), "index", index_id), masterkey)

    def get_snapshot(self, snapshot_id: str) -> snapshot.Snapshot:
        masterkey = self.get_masterkey()
        return snapshot.get_snapshot(os.path.join(str(self.repository), "snapshots", snapshot_id), masterkey)

    def get_config(self):
        masterkey = self.get_masterkey()
        with open(os.path.join(self.repository, "config"), "rb") as f:
            bs = f.read()
            plain = keys.decrypt_mac(masterkey, bs)
            return json.loads(plain)
