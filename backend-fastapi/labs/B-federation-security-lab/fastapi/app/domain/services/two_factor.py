from __future__ import annotations

import secrets
import string

import pyotp


class TwoFactorService:
    def build_setup_material(self, *, email: str, issuer_name: str) -> tuple[str, str]:
        secret = pyotp.random_base32()
        provisioning_uri = pyotp.TOTP(secret).provisioning_uri(email, issuer_name=issuer_name)
        return secret, provisioning_uri

    def verify_totp(self, *, secret: str, code: str) -> bool:
        return pyotp.TOTP(secret).verify(code, valid_window=1)

    def generate_recovery_codes(self, count: int = 8) -> list[str]:
        alphabet = string.ascii_uppercase + string.digits
        codes: list[str] = []
        for _ in range(count):
            left = "".join(secrets.choice(alphabet) for _ in range(4))
            right = "".join(secrets.choice(alphabet) for _ in range(4))
            codes.append(f"{left}-{right}")
        return codes
