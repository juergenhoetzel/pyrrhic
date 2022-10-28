import operator
import stat

import pyrrhic.cli.state as state
from pyrrhic.repo.tree import Node, walk_breadth_first

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


def _format_name(node: Node) -> str:
    if node.type == "symlink":
        return f"{node.name} -> {node.linktarget}"
    return node.name


def _print_long(node: Node, path: str, table: Table) -> None:
    name = _format_name(node)
    mtime_str = f"{node.mtime:%Y-%m-%d %H:%M:%S}"  # rich compatible datetime str
    mode = stat.filemode(stat.S_IMODE(node.mode) | _MODE_STAT.get(node.type, 0))
    table.add_row(f"{mode}", f"{node.uid}", f"{node.gid}", f"{node.size}", f"{mtime_str}", f"{path}/{name}")


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
    if long:
        table = Table("mode", "user", "group", "size", "date", "filename", highlight=True)
        for pleaf in walk_breadth_first(state.repository, snapshot.tree):
            _print_long(pleaf.node, pleaf.path, table)
        print(table)
    else:
        for pleaf in walk_breadth_first(state.repository, snapshot.tree):
            name = _format_name(pleaf.node)
            print(f"{pleaf.path}/{name}")
