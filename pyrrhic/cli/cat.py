import typer
import os

from pyrrhic.cli.util import get_dir_masterkey, catch_exception

from pprint import pprint
from pyrrhic.cli.main import state
from pyrrhic.crypto.keys import get_config

app = typer.Typer(add_completion=False)


@app.command()
@catch_exception(ValueError, exit_code=1)
def masterkey():
    """Return masterkey JSON to stdout"""
    if not state["repository"]:
        raise ValueError("Please specify repository location")
    keys_dir = os.path.join(state["repository"], "keys")
    masterkey = get_dir_masterkey(keys_dir, state["password"])
    pprint(masterkey)


@app.command()
@catch_exception(ValueError, exit_code=1)
def config():
    """Return config JSON to stdout"""
    if not state["repository"]:
        raise ValueError("Please specify repository location")
    keys_dir = os.path.join(state["repository"], "keys")
    masterkey = get_dir_masterkey(keys_dir, state["password"])
    pprint(get_config(masterkey, os.path.join(state["repository"], "config")))
