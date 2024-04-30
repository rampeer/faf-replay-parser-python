from fafreplay._fafreplay import *

import base64
import json
import zlib
try:
    import zstandard
except ImportError:
    zstandard = None


def extract_scfa(fobj):
    """extract_scfa(fobj: io.BytesIO) -> bytes

    Converts data from .fafreplay format to .scfareplay format.
    `zstandard` library must be installed if replays are compressed using zstd stream compression.
    (which is true for modern FAF replays)
    """
    header = json.loads(fobj.readline().decode())
    buf = fobj.read()
    compression_type = header.get("compression")

    if compression_type == "zlib":
        decoded = base64.decodebytes(buf)
        decoded = decoded[4:]  # skip the decoded size
        return zlib.decompress(decoded)
    elif compression_type == "zstd":
        if zstandard is None:
            raise RuntimeError(
                "zstandard is required for decompressing this replay; please install it!"
            )
        reader = zstandard.ZstdDecompressor().stream_reader(buf)
        data = reader.read()
        return data
