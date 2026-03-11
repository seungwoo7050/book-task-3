from __future__ import annotations

import hashlib
import hmac
from secrets import compare_digest


def sha256_digest(message: bytes) -> str:
    return hashlib.sha256(message).hexdigest()


def hmac_sha256(key: bytes, message: bytes) -> str:
    return hmac.new(key, message, hashlib.sha256).hexdigest()


def hkdf_sha256(ikm: bytes, salt: bytes, info: bytes, length: int) -> str:
    if length <= 0:
        raise ValueError("length must be positive")
    if length > 255 * hashlib.sha256().digest_size:
        raise ValueError("length exceeds HKDF-SHA256 limit")

    prk = hmac.new(salt, ikm, hashlib.sha256).digest()
    okm = bytearray()
    previous_block = b""
    counter = 1

    while len(okm) < length:
        previous_block = hmac.new(
            prk,
            previous_block + info + bytes([counter]),
            hashlib.sha256,
        ).digest()
        okm.extend(previous_block)
        counter += 1

    return bytes(okm[:length]).hex()


def pbkdf2_hmac_sha1(password: bytes, salt: bytes, iterations: int, length: int) -> str:
    if iterations <= 0:
        raise ValueError("iterations must be positive")
    if length <= 0:
        raise ValueError("length must be positive")
    return hashlib.pbkdf2_hmac("sha1", password, salt, iterations, length).hex()


def constant_time_compare(left: str, right: str) -> bool:
    return compare_digest(left, right)

