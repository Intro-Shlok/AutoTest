import os
import time

CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
CROCKFORD_REV = {c: i for i, c in enumerate(CROCKFORD)}


def _encode_base32(value: int, length: int) -> str:
    chars = []
    for _ in range(length):
        chars.append(CROCKFORD[value & 0x1F])
        value >>= 5
    return "".join(reversed(chars))


def _random_chars(length: int) -> str:
    rand_bytes = os.urandom((length * 5 + 7) // 8)
    rand_int = int.from_bytes(rand_bytes, "big")
    return _encode_base32(rand_int, length)


def ulid() -> str:
    timestamp = int(time.time() * 1000)
    return _encode_base32(timestamp, 10) + _random_chars(16)


def prefixed_ulid(prefix: str) -> str:
    return f"{prefix}_{ulid()}"


def timestamp_from_ulid(uid: str) -> float:
    encoded = uid.split("_")[-1][:10]
    ts = 0
    for ch in encoded:
        ts = (ts << 5) | CROCKFORD_REV[ch.upper()]
    return ts / 1000.0
