import typer
import os

from .util import get_dir_masterkey

from pprint import pprint
from pyrrhic.crypto.keys import get_masterkey, get_config

app = typer.Typer(add_completion=False)


@app.command()
def masterkey(repo_path: str, password: str):
    """Return masterkey JSON to stdout"""
    keys_dir = os.path.join(repo_path, "keys")
    masterkey = get_masterkey(keys_dir, password.encode("utf8"))
    pprint(masterkey)


@app.command()
def config(repo_path: str, password: str):
    """Return config JSON to stdout"""
    keys_dir = os.path.join(repo_path, "keys")
    masterkey = get_dir_masterkey(keys_dir, password)
    pprint(get_config(masterkey, os.path.join(repo_path, "config")))
