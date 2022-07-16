import typer
import os

from .util import get_dir_masterkey, catch_exception

from pprint import pprint
from pyrrhic.crypto.keys import get_config

app = typer.Typer(add_completion=False)


@app.command()
@catch_exception(ValueError, exit_code=1)
def masterkey(repo_path: str, password: str):
    """Return masterkey JSON to stdout"""
    keys_dir = os.path.join(repo_path, "keys")
    masterkey = get_dir_masterkey(keys_dir, password)
    pprint(masterkey)


@app.command()
@catch_exception(ValueError, exit_code=1)
def config(repo_path: str, password: str):
    """Return config JSON to stdout"""
    keys_dir = os.path.join(repo_path, "keys")
    masterkey = get_dir_masterkey(keys_dir, password)
    pprint(get_config(masterkey, os.path.join(repo_path, "config")))
