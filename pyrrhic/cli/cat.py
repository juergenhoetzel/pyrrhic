import os
from pprint import pprint

from pyrrhic.cli.state import state
from pyrrhic.cli.util import catch_exception, get_dir_masterkey
from pyrrhic.crypto.keys import get_config
from pyrrhic.repo.index import get_index

import typer

app: typer.Typer = typer.Typer(add_completion=False)


@app.command()
@catch_exception(ValueError, exit_code=1)
def masterkey():
    """Return masterkey JSON to stdout"""
    if not state.repository:
        raise ValueError("Please specify repository location")
    keys_dir = os.path.join(state.repository, "keys")
    key = get_dir_masterkey(keys_dir, state.password)
    pprint(key.restic_json())


@app.command()
@catch_exception(ValueError, exit_code=1)
def config():
    """Return config JSON to stdout"""
    if not state.repository:
        raise ValueError("Please specify repository location")
    keys_dir = os.path.join(state.repository, "keys")
    masterkey = get_dir_masterkey(keys_dir, state.password)
    pprint(get_config(masterkey, os.path.join(state.repository, "config")))


@app.command()
@catch_exception(ValueError, exit_code=1)
def index(index_id: str):
    """Return index JSON to stdout"""
    if not state.repository:
        raise ValueError("Please specify repository location")
    keys_dir = os.path.join(state.repository, "keys")
    masterkey = get_dir_masterkey(keys_dir, state.password)
    index = get_index(os.path.join(state.repository, "index", index_id), masterkey)
    print(index.json(indent=2))
