import operator
import stat
from dataclasses import dataclass

import pyrrhic.cli.state as state
from pyrrhic.repo.tree import Node, Tree, get_tree
from pyrrhic.util import datetime_from_restic

from rich import print
from rich.table import Table


import typer

_MODE_STAT = {
    "dir": stat.S_IFDIR,
    "file": stat.S_IFREG,
    "symlink": stat.S_IFLNK,
    "dev": stat.S_IFBLK,
    "chardev": stat.S_IFCHR,
    "socket": stat.S_IFSOCK,
    "fifo": stat.S_IFIFO,
}


def _print_long(node: Node, path: str, table: Table) -> None:
    mtime_str = f"{datetime_from_restic(node.mtime):%Y-%m-%d %H:%M:%S}"  # rich compatible datetime str
    if node.type == "symlink":
        name = f"{node.name} -> {node.linktarget}"
    else:
        name = node.name
    mode = stat.filemode(stat.S_IMODE(node.mode) | _MODE_STAT.get(node.type, 0))
    table.add_row(f"{mode}", f"{node.uid}", f"{node.gid}", f"{node.size}", f"{mtime_str}", f"{path}/{name}")


@dataclass(frozen=True)
class PathNode:
    "Represent a Node located at path"
    path: str  # prefix path
    node: Node


def _ls_breadth_first(tree: Tree, table: Table | None = None) -> None:
    pathnodes = [PathNode(f"/{node.name}", node) for node in tree.nodes]
    while pathnodes:
        pleafes = [pnode for pnode in pathnodes if not pnode.node.subtree]
        pathnodes = [pnode for pnode in pathnodes if pnode.node.subtree]  # FIXME: traverses 2 times
        for pleaf in pleafes:
            if table:
                _print_long(pleaf.node, pleaf.path, table)
            else:
                print(f"{pleaf.path}/{pleaf.node.name}")
        if pathnodes:
            pnode = pathnodes.pop()
            tree = get_tree(state.repository, pnode.node.subtree or "0123")  # just make mypy happy?
            # FIXME: Order by packref to improve performance
            pathnodes = [*[PathNode(f"{pnode.path}/{node.name}", node) for node in tree.nodes], *pathnodes]


def ls(snapshot_prefix: str, long: bool = typer.Option(False, "--long", "-l", help="Use a long listing (Unix ls -l)")):
    "List files in a snapshot"
    state.repository.get_snapshot(snapshot_prefix)
    if snapshot_prefix == "latest":
        snapshots = iter(sorted(state.repository.get_snapshot(), key=operator.attrgetter("time"), reverse=True)[:1])
    else:
        snapshots = state.repository.get_snapshot(snapshot_prefix)
    snapshot = next(snapshots, None)
    if not snapshot:
        raise ValueError(f"Index: {snapshot_prefix} not found")
    if next(snapshots, None):
        raise ValueError(f"Prefix {snapshot_prefix} matches multiple snapshots")
    tree = get_tree(state.repository, snapshot.tree)
    if long:
        table = Table("mode", "user", "group", "size", "date", "filename", highlight=True)
        _ls_breadth_first(tree, table)
        print(table)
    else:
        _ls_breadth_first(tree)
