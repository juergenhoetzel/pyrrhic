import os
from pyrrhic.crypto.keys import get_masterkey
from functools import wraps
import typer


def get_dir_masterkey(keys_dir: str, password: str):
    last_err = None
    for kf in os.listdir(keys_dir):
        try:
            masterkey = get_masterkey(
                os.path.join(keys_dir, kf), password.encode("utf8")
            )
            return masterkey
        except ValueError as err:
            last_err = err
    raise last_err


def catch_exception(which_exception, exit_code=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except which_exception as e:
                typer.secho(e, err=True, fg=typer.colors.RED)
                raise typer.Exit(code=exit_code)

        return wrapper

    return decorator