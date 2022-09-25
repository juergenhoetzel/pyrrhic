"""
This module contains the repository abstractions used by pyrrhic.
"""
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Generator


from pyrrhic.crypto import keys
from pyrrhic.repo import index, pack, snapshot


@dataclass(frozen=True)
class Repository:
    """Class that is used for high level access of Repository."""

    repository: Path
    masterkey: keys.MasterKey

    def get_index(self, index_prefix: str = "") -> Generator[index.Index, None, None]:
        return index.get_index(self.masterkey, self.repository, index_prefix)

    def get_snapshot(self, snapshot_id: str) -> snapshot.Snapshot:
        return snapshot.get_snapshot(self.repository / "snapshots" / snapshot_id, self.masterkey)

    def get_config(self):
        with open(self.repository / "config", "rb") as f:
            bs = f.read()
            plain = keys.decrypt_mac(self.masterkey, bs)
            return json.loads(plain)

    def get_pack(self, pack_id: str) -> pack.Pack:
        return pack.Pack(self.repository, self.masterkey, pack_id)


def get_masterkey(repository: Path, password: str) -> keys.MasterKey:
    if not password:
        raise ValueError("Please specify password")
    if not repository:
        raise ValueError("Please specify repository location")

    keys_path = repository / "keys"
    for kf in keys_path.iterdir():
        try:
            return keys.get_masterkey(str(kf), password.encode("utf8"))
        except ValueError as err:
            last_err = err
    raise last_err
