import typer
from pprint import pprint
import pyrrhic
from pyrrhic.keys import load_key, get_masterkey

app = typer.Typer(add_completion=False)


@app.command()
def version():
    """Return version of pyrric application"""
    print(pyrrhic.__version__)


@app.command()
def masterkey(keyfile: str):
    """Return masterkey JSON to stdout"""
    key = load_key(keyfile)
    masterkey = get_masterkey(key, b"password")
    pprint(masterkey)


if __name__ == "__main__":
    app()
