import re
from datetime import datetime
from typing import Any, Type

DATETIME_TRAILING_NS_RE = re.compile(r"(\.[0-9]{6})[0-9]*\+")


def datetime_from_restic(s: str) -> datetime:
    return datetime.fromisoformat(DATETIME_TRAILING_NS_RE.sub(r"\1+", s))


class resticdatetime(datetime):
    @classmethod
    def fromresticformat(cls, date_string):
        """Construct a datetime from the restic datetime str (strip nanoseconds)."""
        date_string = DATETIME_TRAILING_NS_RE.sub(r"\1+", date_string)
        dt = datetime.fromisoformat(date_string)
        return cls.fromisoformat(dt)


def resticdatetime_enc_hook(obj: Any) -> Any:
    if isinstance(obj, resticdatetime):
        return obj.isoformat()
    else:
        raise TypeError(f"Objects of type {type(obj)} are not supported")


def resticdatetime_dec_hook(type: Type, obj: Any) -> Any:
    if type is resticdatetime:
        return resticdatetime.fromisoformat(DATETIME_TRAILING_NS_RE.sub(r"\1+", obj))
    else:
        raise TypeError(f"Objects of type {type} are not supported")
