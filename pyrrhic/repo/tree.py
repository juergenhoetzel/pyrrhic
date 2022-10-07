import hashlib
import json
from typing import List

from pydantic import BaseModel

from pyrrhic.crypto.keys import decrypt_mac
from pyrrhic.repo.pack import Pack
from pyrrhic.repo.repository import Repository


# FIXME: Move to msgspec
class Node(BaseModel):
    name: str
    type: str
    mode: int
    mtime: str
    atime: str
    ctime: str
    uid: int
    gid: int
    size: int = 0
    user: str
    inode: int
    content: List[str] | None
    linktarget: str | None
    subtree: str | None


class Tree(BaseModel):
    nodes: List[Node]


def get_node_blob(repo: Repository, blob_id: str) -> bytes:
    index = repo.get_index()
    packref = index.get_packref(blob_id)
    pack = Pack(repo.repository, repo.masterkey, packref.id)
    blob = packref.blob
    with open(repo.repository / "data" / pack.pack_id[:2] / pack.pack_id, "rb") as f:
        f.seek(blob.offset)
        buffer = f.read(blob.length)
        plaintext = decrypt_mac(repo.masterkey, buffer)
        if hashlib.sha256(plaintext).hexdigest() != blob.id:
            raise ValueError(f"Invalid hash for blob {blob.id}")
        return plaintext
    raise ValueError(f"Can't find blob id {blob_id}")


def get_tree(repo: Repository, tree_id: str) -> Tree:
    plaintext_blob = get_node_blob(repo, tree_id)
    return Tree(**json.loads(plaintext_blob))
