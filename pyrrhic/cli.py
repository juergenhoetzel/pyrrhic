import typer
import os
from pprint import pprint
import pyrrhic
from pyrrhic.keys import get_masterkey, get_config

app = typer.Typer(add_completion=False)


@app.command()
def version():
    """Return version of pyrric application"""
    print(pyrrhic.__version__)


@app.command()
def masterkey(keyfile: str, password: str):
    """Return masterkey JSON to stdout"""
    masterkey = get_masterkey(keyfile, password.encode("utf8"))
    pprint(masterkey)


@app.command()
def config(repo_path: str, password: str):
    """Return config to stdout"""
    masterkey = None
    last_err = None
    keys_dir = os.path.join(repo_path, "keys")
    for kf in os.listdir(keys_dir):
        try:
            masterkey = get_masterkey(
                os.path.join(keys_dir, kf), password.encode("utf8")
            )
            pprint(get_config(masterkey, os.path.join(repo_path, "config")))
            return
        except ValueError as err:
            last_err = err
    raise last_err


if __name__ == "__main__":
    app()
