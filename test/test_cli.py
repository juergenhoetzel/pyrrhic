import hashlib
import json
from ast import literal_eval
from pathlib import Path

import pyrrhic.cli.state
from pyrrhic.cli.cat import config, index, masterkey, pack, snapshot
from pyrrhic.cli.ls import ls
from pyrrhic.cli.snapshots import snapshots
from pyrrhic.repo.repository import Repository, get_masterkey


pyrrhic.cli.state.repository = Repository(
    Path("restic_test_repositories/restic_test_repository"),
    get_masterkey(Path("restic_test_repositories/restic_test_repository"), "password"),
)


def test_cat_masterkey(capfd):
    masterkey()
    assert literal_eval(capfd.readouterr().out) == {
        "encrypt": "Te0IPiu0wvEtr2+J59McgTrjCp/ynVxC/mmM9mX/t+E=",
        "mac": {"k": "aSbwRFL8rIOOxL4W+mAW1w==", "r": "hQYBDSD/JwpU8XMDIJmAAg=="},
    }


def test_cat_config(capfd):
    config()
    assert literal_eval(capfd.readouterr().out) == {
        "chunker_polynomial": "3833148ec41f8d",
        "id": "2ec6792a9c75a017ec4665a5e7733f45f8bffb67c7d0f3c9ec6cc96e58c6386b",
        "version": 1,
    }


def test_cat_snapshot(capfd):
    snapshot("dd62b535d10bd8f24440cc300a868d6bf2f472859f1218883b0a6faca364c10c")
    out = capfd.readouterr().out
    assert json.loads(out) == {
        "time": "2022-07-19T21:52:28.692251+02:00",
        "tree": "a5dbcc77f63f5dd4f4c67c988aba4a19817aaa9d6c34a6021236a5d40ce653e1",
        "paths": ["/home/juergen/shared/python/pyrrhic/test"],
        "hostname": "shaun",
        "username": "juergen",
        "id": "dd62b535d10bd8f24440cc300a868d6bf2f472859f1218883b0a6faca364c10c",
        "uid": 1000,
        "gid": 1000,
        "excludes": None,
        "tags": None,
    }


def test_cat_index(capfd):
    index("0de57faa699ec0450ddbafb789e165b4e1a3dbe3a09b071075f09ebbfbd6f4b2")
    assert "BlobList" in capfd.readouterr().out


def test_cat_pack(capfdbinary):
    sha = "4b24375f07a164e995d06303bfc26f79f94127e4e5c6e1c476495bbee0af7ccc"
    pack(sha, False)
    assert hashlib.sha256(capfdbinary.readouterr().out).hexdigest() == sha


def test_cat_pack_header(capfd):
    sha = "4b24375f07a164e995d06303bfc26f79f94127e4e5c6e1c476495bbee0af7ccc"
    pack(sha, True)
    assert literal_eval(capfd.readouterr().out) == [
        {"id": "82deec86c5611cb5ae02b967e49d7aeaca50a732432bd1a5923787bd5d0fbf80", "length": 1643, "offset": 0},
        {"id": "e20d6400fbd4e602c79c8bab98a88726865b168838cc8107d560da10f19b2ff8", "length": 1467, "offset": 1643},
        {"id": "a5dbcc77f63f5dd4f4c67c988aba4a19817aaa9d6c34a6021236a5d40ce653e1", "length": 413, "offset": 3110},
    ]


def test_snapshots(capfd):
    snapshots()
    output = capfd.readouterr().out
    assert output.startswith("ID")


def test_ls(capfd):
    "Returns a list of paths"
    ls("latest", False)
    lines = capfd.readouterr().out.splitlines()
    for s in lines:
        path = Path(s)
        assert path.is_absolute()
