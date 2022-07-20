import click.exceptions

from pyrrhic.cli.cat import masterkey
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
    monkeypatch.setattr(state, "password", "invalid!")


def test_cat_masterkey(capfd, mock_test_repository):
    with pytest.raises(click.exceptions.Exit):
        masterkey()
        assert capfd.readouterr().out == "Invalid Password"
