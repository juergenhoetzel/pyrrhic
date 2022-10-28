import hashlib
import io
from collections import OrderedDict
from copy import copy
from dataclasses import dataclass
from datetime import datetime
from logging import info
from pathlib import Path
from typing import Iterator, Optional

import msgspec

from pyrrhic.crypto.keys import decrypt_mac
from pyrrhic.repo.repository import Repository
from pyrrhic.util import decompress


class Node(msgspec.Struct):
    name: str
    type: str
    mode: int
    mtime: datetime
    atime: datetime
    ctime: datetime
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


class ReaderCache:
    def __init__(self, capacity: int):
        self.cache: OrderedDict[Path, io.BufferedReader] = OrderedDict()
        self.misses = 0  # stats
        self.requests = 0
        self.capacity = capacity

    def get(self, key: Path) -> io.BufferedReader:
        self.requests += 1
        if key not in self.cache:
            self.cache[key] = open(key, "rb")
            self.misses += 1
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)
        self.cache.move_to_end(key)
        return self.cache[key]

    def flush(self):
        for item in self.cache.values():
            item.close()
        self.cache = OrderedDict()
        misses = self.misses / self.requests
        info(f"Cache misses: {misses:.2%}")


def get_node_blob(repo: Repository, rcache: ReaderCache, blob_id: str) -> bytes:
    index = repo.get_index()
    packref = index.get_packref(blob_id)
    blob = packref.blob
    f = rcache.get(repo.repository / "data" / packref.id[:2] / packref.id)
    f.seek(blob.offset)
    buffer = f.read(blob.length)
    plaintext = decrypt_mac(repo.masterkey, buffer)
    if uncompressed_length := blob.uncompressed_length:
        plaintext = decompress(plaintext, uncompressed_length)
    if hashlib.sha256(plaintext).hexdigest() != blob.id:
        raise ValueError(f"Invalid hash for blob {blob.id}")
    return plaintext


# FIXME: Use only one msgspec object
def get_tree(repo: Repository, rcache: ReaderCache, tree_id: str) -> Tree:
    plaintext_blob = get_node_blob(repo, rcache, tree_id)
    return msgspec.json.decode(plaintext_blob, type=Tree)


@dataclass(frozen=True)
class PathNode:
    "Represent a Node located at path"
    path: str  # prefix path
    node: Node


def walk_breadth_first(repository: Repository, tree_id: str, rcache=ReaderCache(64)) -> Iterator[PathNode]:
    tree = get_tree(repository, rcache, tree_id)
    pathnodes = [PathNode(f"/{node.name}", node) for node in tree.nodes]
    while pathnodes:
        pleafes = [pnode for pnode in pathnodes if not pnode.node.subtree]
        pathnodes = [pnode for pnode in pathnodes if pnode.node.subtree]  # FIXME: traverses 2 times
        for pleaf in pleafes:
            yield pleaf
        if pathnodes:
            pnode = pathnodes.pop()
            node_without_subdir = copy(pnode.node)
            node_without_subdir.subtree = None
            tree = get_tree(repository, rcache, pnode.node.subtree or "0123")  # just make mypy happy?
            pathnodes = [PathNode(pnode.path, node_without_subdir), *[PathNode(f"{pnode.path}/{node.name}", node) for node in tree.nodes], *pathnodes]
    rcache.flush()
