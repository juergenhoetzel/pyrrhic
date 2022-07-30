import os
from functools import wraps

import typer


def get_file_by_prefix(dir: str, prefix: str) -> list[str]:
    return [file for file in os.listdir(dir) if file == str or file.startswith(prefix)]


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
