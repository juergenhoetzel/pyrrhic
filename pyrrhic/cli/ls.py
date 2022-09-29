import operator
import stat

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


def _ls_recursive(tree: Tree, path, table: Table | None = None) -> None:
    for node in tree.nodes:
        if table:
            _print_long(node, path, table)
        else:
            print(f"{path}/{node.name}")
        if node.type == "dir" and node.subtree:
            _ls_recursive(get_tree(state.repository, node.subtree), f"{path}/{node.name}", table)


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
        _ls_recursive(tree, "", table)
        print(table)
    else:
        _ls_recursive(tree, "")
