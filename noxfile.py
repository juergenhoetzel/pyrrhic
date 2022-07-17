"""
Nox automation tasks for pyrrhic
"""

import os
import nox
from pathlib import Path

# GitHub Actions
ON_CI = bool(os.getenv("CI"))

# Git info
DEFAULT_BRANCH = "master"

# Python to use for non-test sessions
DEFAULT_PYTHON: str = "3.10"

# Global project stuff
PROJECT_ROOT = Path(__file__).parent.resolve()

SOURCE_FILES = (
    "noxfile.py",
    "pyrrhic",
    "test",
)


@nox.session(python=DEFAULT_PYTHON)
def dev(session: nox.Session) -> None:
    """
    Sets up a python dev environment for the project if one doesn't already exist.
    """
    session.run("python", "-m", "venv", os.path.join(PROJECT_ROOT, ".venv"))
    session.run(
        "flit",
        "install",
        "--symlink",
        "--python",
        os.path.join(PROJECT_ROOT, ".venv", "bin", "python"),
        external=True,
        silent=True,
    )


@nox.session(python=["3.8", "3.9", "3.10"])
def test(session: nox.Session) -> None:
    """
    Runs the test suite.
    """
    session.install(
        ".",
        "pytest",
        "pytest-cov",
        "flake8",
    )
    session.run("flake8", *SOURCE_FILES)
    session.run("pytest", "-v", "-v", "--cov=pyrrhic", "--cov-branch")


@nox.session(python=DEFAULT_PYTHON)
def coverage(session: nox.Session):
    """Upload coverage data."""
    session.install("coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@nox.session(python=DEFAULT_PYTHON)
def mypy(session: nox.Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or ["pyrrhic", "test"]
    session.install("mypy")
    session.run("mypy", "--ignore-missing-imports", "--show-error-codes", *args)
