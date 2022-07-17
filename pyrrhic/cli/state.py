from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class State(BaseModel):
    """Class that contain the state of the CLI applicaton."""

    password: Optional[str]
    repository: Optional[Path]


state = State()
