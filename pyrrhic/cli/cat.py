import os
from pprint import pprint

from pyrrhic.cli.state import state
from pyrrhic.cli.util import catch_exception, get_dir_masterkey
from pyrrhic.crypto.keys import get_config

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
