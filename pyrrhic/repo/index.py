from dataclasses import dataclass
from functools import cache
from pathlib import Path

import msgspec

from pyrrhic.crypto.keys import MasterKey, decrypt_mac
from pyrrhic.util import maybe_decompress

from rich.console import Console
from rich.progress import track


class Blob(msgspec.Struct):
    id: str
    type: str
    offset: int
    length: int
    uncompressed_length: int | None = None


class BlobList(msgspec.Struct):
    id: str
    blobs: list[Blob]


class RecPackList(msgspec.Struct):
    packs: list[BlobList]


@dataclass(frozen=True)
class PackRef:
    id: str
    blob: Blob


@cache
def _get_index(key: MasterKey, repo_path: Path, index_prefix: str, glob: bool) -> dict[str, PackRef]:
    if glob:
        paths = (repo_path / "index").glob(f"{index_prefix}*")
    else:
        paths = (repo_path / "index" / name for name in [index_prefix])
    if Console().is_terminal:  # FIXME: Should be configurable
        paths = track(list(paths), "Loading index")

    dec = msgspec.json.Decoder(type=RecPackList)

    d = {
        blob.id: PackRef(packs.id, blob)
        for index_path in paths
        for packs in dec.decode(maybe_decompress(decrypt_mac(key, index_path.read_bytes()))).packs
        for blob in packs.blobs
    }
    return d


class Index:
    "Internal Index representation"
    index: dict[str, PackRef]

    def __init__(self, key: MasterKey, repo_path: Path, index_prefix: str, glob=True):
        self.index = _get_index(key, repo_path, index_prefix, glob)

    def get_packref(self, blob_id) -> PackRef:
        if packref := self.index.get(blob_id):
            return packref
        raise ValueError(f"Invalid blob id {blob_id}")
