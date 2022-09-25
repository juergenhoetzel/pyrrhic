import os
from dataclasses import dataclass
from pathlib import Path
from struct import unpack

from pyrrhic.crypto.keys import MasterKey, decrypt_mac


@dataclass(frozen=True)
class Blob:
    pack_id: str
    offset: int
    length: int
    hash: bytes


@dataclass(frozen=True)
class DataBlob(Blob):
    pass


@dataclass(frozen=True)
class TreeBlob(Blob):
    pass


@dataclass(frozen=True)
class CompressedDataBlob(Blob):
    length_uncompressed: int


@dataclass(frozen=True)
class CompressedTreeBlob:
    length_uncompressed: int


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
                    yield DataBlob(self.pack_id, offset, length_encrypted, header[5 : 5 + 32])
                    header = header[(5 + 32) :]
                case 1:
                    length_encrypted = unpack("<I", header[1:5])[0]
                    yield TreeBlob(self.pack_id, offset, length_encrypted, header[5 : 5 + 32])
                    header = header[(5 + 32) :]
                case 2:
                    length_encrypted, length_plaintext = unpack("<I<I", header[1:9])  # FIXME: Wrong in Restic-specification, shoud be length_uncompressed?
                    yield CompressedDataBlob(self.pack_id, offset, length_encrypted, header[9 : 9 + 32], length_plaintext)
                    header = header[9 + 32 :]
                case 3:
                    length_encrypted, length_plaintext = unpack("<I<I", header[1:9])
                    yield CompressedTreeBlob(self.pack_id, offset, length_encrypted, header[9 : 9 + 32], length_plaintext)
                    header = header[9 + 32 :]
                case _:
                    raise ValueError(f"Invalid Tag: {header[0]}")
            offset += length_encrypted

    def get_blob_index(self):
        "Return blobs in index format"
        return ({"id": blob.hash.hex(), "offset": blob.offset, "length": blob.length} for blob in self.get_blobs())
