from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class ValidState:
    """Class that contain the valid state of the CLI applicaton."""

    password: str
    repository: Path

    def raise_for_invalid_state(self):
        if not self.repository:
            raise ValueError("Please specify repository location")
        if not self.password:
            raise ValueError("Please specify password")


@dataclass
class State:
    """Class that contain the state of the CLI applicaton."""

    password: Optional[str] = None
    repository: Optional[Path] = None

    def get_valid_state(self) -> ValidState:
        if not self.repository:
            raise ValueError("Please specify repository location")
        if not self.password:
            raise ValueError("Please specify password")
        return ValidState(self.password, self.repository)


state = State()
