from pydantic import BaseModel
from typing import Optional
from pathlib import Path


class State(BaseModel):
    """Class that contain the state of the CLI applicaton."""

    password: Optional[str]
    repository: Optional[Path]


state = State()
