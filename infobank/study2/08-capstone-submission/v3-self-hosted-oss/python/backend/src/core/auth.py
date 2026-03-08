from __future__ import annotations

import base64
import hashlib
import hmac
import os
import time

SESSION_COOKIE_NAME = "qualbot_session"


def _urlsafe_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _urlsafe_decode(raw: str) -> bytes:
    padding = "=" * (-len(raw) % 4)
    return base64.urlsafe_b64decode(raw + padding)


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
    return f"pbkdf2_sha256${_urlsafe_encode(salt)}${_urlsafe_encode(digest)}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        algorithm, salt_raw, digest_raw = password_hash.split("$", 2)
    except ValueError:
        return False
    if algorithm != "pbkdf2_sha256":
        return False
    salt = _urlsafe_decode(salt_raw)
    expected = _urlsafe_decode(digest_raw)
    actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
    return hmac.compare_digest(actual, expected)


def create_session_cookie(*, secret: str, user_id: str, email: str, issued_at: int | None = None) -> str:
    issued = issued_at or int(time.time())
    payload = f"{user_id}:{email}:{issued}"
    signature = hmac.new(secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()
    return _urlsafe_encode(f"{payload}:{signature}".encode())


def parse_session_cookie(*, secret: str, cookie_value: str, max_age_seconds: int) -> dict[str, str] | None:
    try:
        raw = _urlsafe_decode(cookie_value).decode("utf-8")
        user_id, email, issued_raw, signature = raw.rsplit(":", 3)
        issued = int(issued_raw)
    except (ValueError, UnicodeDecodeError):
        return None

    payload = f"{user_id}:{email}:{issued}"
    expected = hmac.new(secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        return None
    if int(time.time()) - issued > max_age_seconds:
        return None
    return {"user_id": user_id, "email": email, "issued_at": str(issued)}
