import os
from dataclasses import dataclass
from pathlib import Path
from struct import unpack
from typing import Optional

from pyrrhic.crypto.keys import MasterKey, decrypt_mac


@dataclass(frozen=True)
class Blob:
    type: str  # FIXME: Use enum
    pack_id: str
    offset: int
    length: int
    hash: bytes
    uncompressed_length: Optional[int] = None


class Pack:
    def __init__(self, repo_path: Path, key: MasterKey, pack_id: str):
        "Load Pack at path."
        self.pack_id = pack_id
        self.path = repo_path / "data" / pack_id[:2] / pack_id
        with open(self.path, "rb") as f:
            f.seek(-4, os.SEEK_END)
            buffer = f.read(4)
            header_length = unpack("<I", buffer)[0]
            f.seek(-4 - header_length, os.SEEK_END)
            buffer = f.read(header_length)
            self.header = decrypt_mac(key, buffer)

    def get_blobs(self):
        header = self.header
        offset = 0
        while len(header):
            match header[0]:
                case 0:
                    length_encrypted = unpack("<I", header[1:5])[0]
                    yield Blob("Data", self.pack_id, offset, length_encrypted, header[5 : 5 + 32])
                    header = header[(5 + 32) :]
                case 1:
                    length_encrypted = unpack("<I", header[1:5])[0]
                    yield Blob("Tree", self.pack_id, offset, length_encrypted, header[5 : 5 + 32])
                    header = header[(5 + 32) :]
                case 2:
                    length_encrypted, length_uncompressed = unpack("<II", header[1:9])  # FIXME: Wrong in Restic-specification, shoud be length_uncompressed?
                    yield Blob("Blob", self.pack_id, offset, length_encrypted, header[9 : 9 + 32], length_uncompressed)
                    header = header[9 + 32 :]
                case 3:
                    length_encrypted, length_uncompressed = unpack("<II", header[1:9])
                    yield Blob("Tree", self.pack_id, offset, length_encrypted, header[9 : 9 + 32], length_uncompressed)
                    header = header[9 + 32 :]
                case _:
                    raise ValueError(f"Invalid Tag: {header[0]}")
            offset += length_encrypted

    def get_blob_index(self) -> list[Blob]:
        "Return list of blobs"
        return self.get_blobs()


def blob_to_dict(blob: Blob) -> dict:
    d = {"id": blob.hash.hex(), "offset": blob.offset, "length": blob.length}
    if blob.uncompressed_length:
        return d | {"length_uncompressed": blob.uncompressed_length}
    return d
