# Python 구현

아래 내용은 모두 `security-core` 레포 루트 기준입니다.

## 다루는 범위

- SHA-256 digest 계산
- HMAC-SHA256 계산
- HKDF-SHA256 계산
- PBKDF2-HMAC-SHA1 계산
- manifest 검증용 `check-vectors` CLI
- deterministic 출력용 `demo` CLI

## 실행 예시

```bash
make venv
PYTHONPATH=study/Foundations-Security/crypto-primitives-in-practice/python/src \
  .venv/bin/python -m crypto_primitives_in_practice.cli check-vectors \
  study/Foundations-Security/crypto-primitives-in-practice/problem/data/hkdf_sha256_vectors.json
```

## 테스트

```bash
make test-unit
```

## 상태

`verified`

## 구현 메모

runtime 의존성은 `typer`만 사용하고, crypto 연산은 전부 Python stdlib(`hashlib`, `hmac`, `secrets`)로 처리합니다.
CLI는 primitive를 하나의 “보안 함수”로 묶지 않고, manifest와 demo를 통해 역할 차이를 바로 보이게 설계했습니다.

