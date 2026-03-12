# 개발 타임라인

## 1. 환경 준비

```bash
cd security-core
make venv
make doctor
```

성공 신호:

- `.venv`가 생성됩니다.
- `doctor ok`가 출력됩니다.

## 2. reference vector 검증

```bash
make test-unit
```

성공 신호:

- SHA-256, HMAC-SHA256, HKDF-SHA256, PBKDF2-HMAC-SHA1 vector 테스트가 모두 통과합니다.
- CLI smoke test가 `check-vectors`, `demo` JSON shape를 확인합니다.

## 3. demo 출력 확인

```bash
make demo-crypto
```

성공 신호:

- 고정 profile 기준으로 hash, MAC, KDF 결과가 JSON으로 출력됩니다.
- `hash_equals_mac`은 `false`, `mac_self_check`는 `true`로 나옵니다.

