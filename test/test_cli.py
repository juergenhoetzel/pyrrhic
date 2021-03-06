from ast import literal_eval

from pyrrhic.cli.cat import config, masterkey
from pyrrhic.cli.state import state

import pytest


@pytest.fixture
def mock_test_repository(monkeypatch):
    """Set the CLI state to test repository."""
    monkeypatch.setattr(
        state,
        "repository",
        "restic_test_repositories/restic_test_repository",
    )
    monkeypatch.setattr(state, "password", "password")


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
