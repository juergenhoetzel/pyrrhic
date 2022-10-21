import operator
import os
import stat
from logging import debug, info, warn
from pathlib import Path

import pyrrhic.cli.state as state
from pyrrhic.cli.util import catch_exception
from pyrrhic.repo.tree import ReaderCache, get_node_blob, walk_breadth_first

from rich.progress import track

import typer


def _restore(tree_id: str, target: Path, resume=False):
    isroot = os.geteuid() == 0
    rcache = ReaderCache(64)
    index = state.repository.get_index()
    for pnode in walk_breadth_first(state.repository, tree_id, rcache):
        node = pnode.node
        abs_path = target / Path(pnode.path).relative_to("/")
        mode = stat.S_IMODE(node.mode)
        match node.type:
            case "file":
                # FIXME: Create temporary unique file and do atomic rename
                if node.content:  # possible empty file
                    resume_from = 0
                    blobs = [index.get_packref(content).blob for content in node.content]
                    if abs_path.is_file():
                        if not resume:
                            raise FileExistsError(f"File exists: {abs_path}")
                        resume_from = os.stat(abs_path).st_size
                        if resume_from == node.size:
                            debug(f"Already restored {pnode.path}")
                            continue
                        if resume_from > node.size:
                            raise ValueError(f"Existing file {abs_path} is larger")
                    with open(abs_path, "ab") as f:
                        current_pos = 0
                        for i, blob in enumerate(track(blobs, pnode.path)):
                            debug(f"Processing Blob {i} of {abs_path}")
                            blength = blob.uncompressed_length or (blob.length - 32)
                            if current_pos < resume_from:
                                if resume_from < (current_pos + blength):
                                    f.truncate(current_pos)
                                    info(f"Resuming from {current_pos}")
                                else:
                                    debug(f"{abs_path} Ignoring pos {current_pos} in resumed file")
                                    current_pos += blength
                                    continue
                            bs = get_node_blob(state.repository, rcache, blob.id)
                            current_pos += len(bs)
                            f.write(bs)

                    abs_path.chmod(mode)
                    if isroot:  # FIXME: chgrp to groups this user is member of
                        os.chown(abs_path, node.uid, node.gid)

            case "dir":
                debug(f"Creating directory {abs_path}")
                try:
                    abs_path.mkdir(mode)
                except FileExistsError as e:
                    if not resume:
                        raise e
            case "symlink":
                if abs_path.is_symlink():
                    if not resume:
                        raise FileExistsError(f"Symlink exists: {abs_path}")
                    debug(f"Symlink exists: {abs_path}")
                elif node.linktarget:
                    debug(f"Creating symlink {abs_path} -> {node.linktarget}")
                    os.symlink(node.linktarget, abs_path)
                    if isroot:  # FIXME: chgrp to groups this user is member of
                        os.chown(abs_path, node.uid, node.gid, follow_symlinks=False)
                else:
                    raise ValueError(f"Symlink target of {abs_path} does not exist")
            case _:
                warn(f"{node.name}: {node.type} not implemented")


@catch_exception(OSError, exit_code=2)
def restore(
    snapshot_prefix: str,
    target: Path,
    resume: bool = typer.Option(False, "--resume", "-r", help="resume exiting files in target"),
    help="Restore data from a snapshot",
):
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
    _restore(snapshot.tree, target, resume)
