import typer
import pyrrhic
import pyrrhic.cli.cat as cat

app = typer.Typer(add_completion=False)
app.add_typer(cat.app, name="cat")


@app.command()
def version():
    """Return version of pyrric application"""
    print(pyrrhic.__version__)


if __name__ == "__main__":
    app()
