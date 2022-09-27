import re
from datetime import datetime


DATETIME_RE = re.compile(r"(\.[0-9]{6})[0-9]*\+")


def datetime_from_restic(s: str) -> datetime:
    return datetime.fromisoformat(DATETIME_RE.sub(r"\1+", s))
