from ast import literal_eval

from pyrrhic.cli.cat import config, index, masterkey, snapshot
from pyrrhic.cli.state import repository

import pytest


@pytest.fixture
def mock_test_repository(monkeypatch):
    """Set the CLI state to test repository."""
    monkeypatch.setattr(
        repository,
        "repository",
        "restic_test_repositories/restic_test_repository",
    )
    monkeypatch.setattr(repository, "password", "password")


def test_cat_masterkey(capfd, mock_test_repository):
    masterkey()
    assert literal_eval(capfd.readouterr().out) == {
        "encrypt": "Te0IPiu0wvEtr2+J59McgTrjCp/ynVxC/mmM9mX/t+E=",
        "mac": {"k": "aSbwRFL8rIOOxL4W+mAW1w==", "r": "hQYBDSD/JwpU8XMDIJmAAg=="},
    }


def test_cat_config(capfd, mock_test_repository):
    config()
    assert literal_eval(capfd.readouterr().out) == {
        "chunker_polynomial": "3833148ec41f8d",
        "id": "2ec6792a9c75a017ec4665a5e7733f45f8bffb67c7d0f3c9ec6cc96e58c6386b",
        "version": 1,
    }


def test_cat_snapshot(capfd, mock_test_repository):
    snapshot("dd62b535d10bd8f24440cc300a868d6bf2f472859f1218883b0a6faca364c10c")
    assert literal_eval(capfd.readouterr().out) == {
        "time": "2022-07-19T21:52:28.692251936+02:00",
        "tree": "a5dbcc77f63f5dd4f4c67c988aba4a19817aaa9d6c34a6021236a5d40ce653e1",
        "paths": ["/home/juergen/shared/python/pyrrhic/test"],
        "hostname": "shaun",
        "username": "juergen",
        "uid": 1000,
        "gid": 1000,
    }


def test_cat_index(capfd, mock_test_repository):
    index("0de57faa699ec0450ddbafb789e165b4e1a3dbe3a09b071075f09ebbfbd6f4b2")
    assert "packs" in literal_eval(capfd.readouterr().out)
