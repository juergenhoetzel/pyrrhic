import hashlib
from dataclasses import dataclass
from typing import Iterator, Optional

import msgspec

from pyrrhic.crypto.keys import decrypt_mac
from pyrrhic.repo.repository import Repository


class Node(msgspec.Struct):
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
    content: Optional[list[str]] = None
    linktarget: Optional[str] = None
    subtree: Optional[str] = None


class Tree(msgspec.Struct):
    nodes: list[Node]


def get_node_blob(repo: Repository, blob_id: str) -> bytes:
    index = repo.get_index()
    packref = index.get_packref(blob_id)
    blob = packref.blob
    with open(repo.repository / "data" / packref.id[:2] / packref.id, "rb") as f:
        f.seek(blob.offset)
        buffer = f.read(blob.length)
        plaintext = decrypt_mac(repo.masterkey, buffer)
        if hashlib.sha256(plaintext).hexdigest() != blob.id:
            raise ValueError(f"Invalid hash for blob {blob.id}")
        return plaintext
    raise ValueError(f"Can't find blob id {blob_id}")


def get_tree(repo: Repository, tree_id: str) -> Tree:
    plaintext_blob = get_node_blob(repo, tree_id)
    return msgspec.json.decode(plaintext_blob, type=Tree)


@dataclass(frozen=True)
class PathNode:
    "Represent a Node located at path"
    path: str  # prefix path
    node: Node


def walk_breadth_first(repository: Repository, tree: Tree) -> Iterator[PathNode]:
    pathnodes = [PathNode(f"/{node.name}", node) for node in tree.nodes]
    while pathnodes:
        pleafes = [pnode for pnode in pathnodes if not pnode.node.subtree]
        pathnodes = [pnode for pnode in pathnodes if pnode.node.subtree]  # FIXME: traverses 2 times
        for pleaf in pleafes + pathnodes:
            yield pleaf
        if pathnodes:
            pnode = pathnodes.pop()
            tree = get_tree(repository, pnode.node.subtree or "0123")  # just make mypy happy?
            pathnodes = [*[PathNode(f"{pnode.path}/{node.name}", node) for node in tree.nodes], *pathnodes]
