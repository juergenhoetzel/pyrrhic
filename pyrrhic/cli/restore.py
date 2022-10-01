import operator
import stat
from logging import info, warn
from pathlib import Path

import pyrrhic.cli.state as state
from pyrrhic.cli.util import catch_exception
from pyrrhic.repo.tree import Tree, get_node_blob, get_tree


def _restore_recursive(tree: Tree, target: Path):
    for node in tree.nodes:
        abs_path = target / node.name
        mode = stat.S_IMODE(node.mode)
        match node.type:
            case "file":
                # FIXME: Create temporary unique file
                abs_path.touch(mode, exist_ok=False)  # FIXME: UID/GID
                if node.content:  # possible empty file
                    info(f"Restoring {abs_path}: {len(node.content)} blobs")
                    with open(abs_path, "wb") as f:
                        for content_id in node.content:
                            f.write(get_node_blob(state.repository, content_id))

            case "dir":
                info(f"Restoring dir {abs_path}")
                abs_path.mkdir(mode)
                if node.subtree:
                    _restore_recursive(get_tree(state.repository, node.subtree), abs_path)
            case _:
                warn(f"{node.name}: {node.type} not implemented")


@catch_exception(OSError, exit_code=2)
def restore(snapshot_prefix: str, target: Path, help="Restore data from a snapshot"):
    state.repository.get_snapshot(snapshot_prefix)
    if snapshot_prefix == "latest":  # FIXME: Duplicated code (ls command)
        snapshots = iter(sorted(state.repository.get_snapshot(), key=operator.attrgetter("time"), reverse=True)[:1])
    else:
        snapshots = state.repository.get_snapshot(snapshot_prefix)
    snapshot = next(snapshots, None)
    if not snapshot:
        raise ValueError(f"Index: {snapshot_prefix} not found")
    if next(snapshots, None):
        raise ValueError(f"Prefix {snapshot_prefix} matches multiple snapshots")
    tree = get_tree(state.repository, snapshot.tree)
    _restore_recursive(tree, target)
