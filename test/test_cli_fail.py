from pathlib import Path

import pyrrhic.cli.state
from pyrrhic.repo.repository import Repository, get_masterkey

import pytest


def test_cat_masterkey(capfd):
    with pytest.raises(ValueError):
        pyrrhic.cli.state.repository = Repository(
            Path("restic_test_repositories/restic_test_repository"),
            get_masterkey(Path("restic_test_repositories/restic_test_repository"), "invalid!"),
        )
        assert capfd.readouterr().out == "Invalid Password"
