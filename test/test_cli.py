import hashlib
import json
from ast import literal_eval
from pathlib import Path

import pyrrhic.cli.state
from pyrrhic.cli.cat import config, index, masterkey, pack, snapshot
from pyrrhic.cli.ls import ls

import pytest

from .params import params


@pytest.mark.parametrize("repository,expected", [(p["repo"], p["masterkey"]) for p in params])
def test_cat_masterkey(capfd, repository, expected):
    pyrrhic.cli.state.repository = repository
    masterkey()
    assert literal_eval(capfd.readouterr().out) == expected


@pytest.mark.parametrize("repository,config_dict", [(p["repo"], p["config"]) for p in params])
def test_cat_config(capfd, repository, config_dict):
    pyrrhic.cli.state.repository = repository
    config()
    assert literal_eval(capfd.readouterr().out) == config_dict


@pytest.mark.parametrize("repository,snapshot_id,snapshot_json", [(p["repo"], p["snapshot_id"], p["snapshot_json"]) for p in params])
def test_cat_snapshot(capfd, repository, snapshot_id, snapshot_json):
    pyrrhic.cli.state.repository = repository
    snapshot(snapshot_id)
    out = capfd.readouterr().out
    assert json.loads(out) == snapshot_json


@pytest.mark.parametrize("repository,index_id,index_substr", [(p["repo"], p["index_id"], p["index_substr"]) for p in params])
def test_cat_index(capfd, repository, index_id, index_substr):
    pyrrhic.cli.state.repository = repository
    index(index_id)
    out = capfd.readouterr().out
    assert "PackRef" in out
    assert index_substr in out


@pytest.mark.parametrize("repository,pack_id", [(p["repo"], p["pack_id"]) for p in params])
def test_cat_pack(capfdbinary, repository, pack_id):
    pyrrhic.cli.state.repository = repository
    sha = pack_id
    pack(sha, False)
    assert hashlib.sha256(capfdbinary.readouterr().out).hexdigest() == sha


@pytest.mark.parametrize("repository,pack_id,pack_blobs", [(p["repo"], p["pack_id"], p["pack_blobs"]) for p in params])
def test_cat_pack_header(capfd, repository, pack_id, pack_blobs):
    pyrrhic.cli.state.repository = repository
    sha = pack_id
    pack(sha, True)
    assert literal_eval(capfd.readouterr().out) == pack_blobs


@pytest.mark.parametrize("repository", [(p["repo"]) for p in params])
def test_ls(capfd, repository):
    "Returns a list of paths"
    pyrrhic.cli.state.repository = repository
    ls("latest", False)
    lines = capfd.readouterr().out.splitlines()
    for s in lines:
        path = Path(s)
        assert path.is_absolute()
    with pytest.raises(ValueError, match="Index: invalid not found"):
        ls("invalid", False)
    with pytest.raises(ValueError, match="Prefix  matches multiple snapshots"):
        ls("", False)
