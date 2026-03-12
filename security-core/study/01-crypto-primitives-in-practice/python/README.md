# Python 구현

## 구현 개요

이 구현은 vector manifest를 읽어 primitive별 actual hex를 계산하고, demo profile에서 hash, MAC, KDF 결과를 함께 출력하는 Python CLI 패키지입니다.

## 핵심 모듈

- `src/crypto_primitives_in_practice/primitives.py`: SHA-256, HMAC-SHA256, HKDF-SHA256, PBKDF2-HMAC-SHA1 계산
- `src/crypto_primitives_in_practice/vectors.py`: manifest 로딩, vector 판정, demo profile 출력
- `src/crypto_primitives_in_practice/cli.py`: `check-vectors`, `demo` 명령 공개

## CLI 계약

```bash
PYTHONPATH=study/01-crypto-primitives-in-practice/python/src \
  .venv/bin/python -m crypto_primitives_in_practice.cli check-vectors \
  study/01-crypto-primitives-in-practice/problem/data/hkdf_sha256_vectors.json
```

- `check-vectors <manifest>`: `primitive`, `passed`, `failed`, `results`를 JSON으로 출력합니다.
- `demo <profile>`: `hash`, `mac`, `kdf`, `comparisons`를 JSON으로 출력합니다.

## 테스트

```bash
make test-unit
```

runtime 의존성은 `typer`만 사용하고, crypto 연산은 Python stdlib(`hashlib`, `hmac`, `secrets`)로 처리합니다.
