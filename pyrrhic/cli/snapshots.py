import operator

import pyrrhic.cli.state


def snapshots():
    "List all snapshots"
    print("ID          Time                 Host      Tags         Paths")
    print("-----------------------------------------------------------------------------------------------")
    # FIXME: fixed width!
    for s in sorted(pyrrhic.cli.state.repository.get_snapshot(), key=operator.attrgetter("time")):
        tags_str = ", ".join(s.tags or [])
        print(f"{s.id:10.10}  {s.time:%c} {s.hostname:10.10} {tags_str:10.10} {', '.join(s.paths):40.40}")
