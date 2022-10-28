import zstandard


_zdec = zstandard.ZstdDecompressor()


def decompress(b: bytes, uncompressed_size: int) -> bytes:
    return _zdec.decompress(b, uncompressed_size)


def maybe_decompress(b: bytes) -> bytes:
    if b[0] == 2:  # compressed v2 format
        return _zdec.decompress(
            b[1:], max_output_size=2147483648
        )  # https://stackoverflow.com/questions/69270987/how-to-resolve-the-error-related-to-frame-used-in-zstandard-which-requires-too-m
    return b
