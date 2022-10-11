import hashlib
from pathlib import Path

from pyrrhic.cli import state
from pyrrhic.cli.restore import restore
from pyrrhic.repo.repository import Repository, get_masterkey

REPO_BASE = Path("restic_test_repositories")
SNAPSHOT_PREFIX = "fb56c7b6"

state.repository = Repository(
    Path("restic_test_repositories/restic_test_repository"),
    get_masterkey(Path("restic_test_repositories/restic_test_repository"), "password"),
)

RESTORE_FILES = [
    (Path("usr/share/cracklib/cracklib.magic"), "c4b2b3034acf5b35b60a8de27c7ac33f54c6b4ea"),
    (Path("usr/share/cracklib/cracklib-small"), "5f97502ab12eac2e3aa869d00a13af41a7f585e6"),
    (Path("usr/share/cracklib/pw_dict.hwm"), "5dfc5fa9b8fec7eff807ede3561f4b2cdca17277"),
    (Path("usr/share/cracklib/pw_dict.pwd"), "20973efecb1e0239800a6e2437fa3390d3fd415c"),
    (Path("usr/share/cracklib/pw_dict.pwi"), "398936961dff2e5f710723c36e67edca92943284"),
]


def test_restore(tmp_path):
    restore(SNAPSHOT_PREFIX, target=tmp_path)
    for snapshot_path, sha1sum in RESTORE_FILES:
        assert hashlib.sha1((tmp_path / snapshot_path).read_bytes()).hexdigest() == sha1sum
