import operator

import pyrrhic.cli.state

from rich import print
from rich.table import Table


def snapshots():
    "List all snapshots"
    table = Table("ID", "datetime", "hostname", "tags", "paths", highlight=True)
    for s in sorted(pyrrhic.cli.state.repository.get_snapshot(), key=operator.attrgetter("time")):
        table.add_row(s.id[:6], f"{s.time:%c}", s.hostname, ", ".join(s.tags or []), ", ".join(s.paths or []))
    print(table)
