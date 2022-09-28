import operator

import pyrrhic.cli.state as state
from pyrrhic.repo.tree import Tree, get_tree


def _ls_recursive(tree: Tree, path="") -> None:
    for node in tree.nodes:
        if node.type == "dir":
            print(f"{path}/{node.name}")
            if node.subtree:
                _ls_recursive(get_tree(state.repository, node.subtree), path=f"{path}/{node.name}")
        else:
            print(f"{path}/{node.name}")


def ls(snapshot_prefix: str):
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
    _ls_recursive(tree)
