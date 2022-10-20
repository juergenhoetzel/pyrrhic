import re
from datetime import datetime
from typing import Any, Type

import zstandard

DATETIME_TRAILING_NS_RE = re.compile(r"(\.[0-9]{6})[0-9]*\+")


def datetime_from_restic(s: str) -> datetime:
    return datetime.fromisoformat(DATETIME_TRAILING_NS_RE.sub(r"\1+", s))


class resticdatetime(datetime):
    @classmethod
    def fromresticformat(cls, date_string):
        """Construct a datetime from the restic datetime str (strip nanoseconds)."""
        date_string = DATETIME_TRAILING_NS_RE.sub(r"\1+", date_string)
        return cls.fromisoformat(date_string)


def resticdatetime_enc_hook(obj: Any) -> Any:
    if isinstance(obj, resticdatetime):
        return obj.isoformat()
    else:
        raise TypeError(f"Objects of type {type(obj)} are not supported")


def resticdatetime_dec_hook(type: Type, obj: Any) -> Any:
    if type is resticdatetime:
        return resticdatetime.fromresticformat(obj)
    else:
        raise TypeError(f"Objects of type {type} are not supported")


_zdec = zstandard.ZstdDecompressor()


def decompress(b: bytes, uncompressed_size: int) -> bytes:
    return _zdec.decompress(b, uncompressed_size)


def maybe_decompress(b: bytes) -> bytes:
    if b[0] == 2:  # compressed v2 format
        return _zdec.decompress(
            b[1:], max_output_size=2147483648
        )  # https://stackoverflow.com/questions/69270987/how-to-resolve-the-error-related-to-frame-used-in-zstandard-which-requires-too-m
    return b
