# crypto-primitives-in-practice

## 이 프로젝트의 문제

보안 문서에서 `hash`, `MAC`, `KDF`는 자주 한 문단에 섞여 나오지만, 실제로는 입력과 목적이 다릅니다. 이 프로젝트는 각 primitive를 reference vector로 검증 가능한 작은 CLI 랩으로 분리해, secret input과 public input의 차이를 설명 가능한 형태로 고정합니다.

## 내가 만든 답

- SHA-256, HMAC-SHA256, HKDF-SHA256, PBKDF2-HMAC-SHA1을 각각 독립적으로 검증하는 vector evaluator
- `check-vectors` CLI로 manifest별 pass/fail과 actual/expected hex를 출력하는 도구
- `demo` CLI로 hash, MAC, KDF 결과와 비교 포인트를 deterministic하게 보여주는 프로필 실행기

## 검증 명령

```bash
make test-unit
make demo-crypto
PYTHONPATH=study/01-crypto-primitives-in-practice/python/src \
  .venv/bin/python -m crypto_primitives_in_practice.cli check-vectors \
  study/01-crypto-primitives-in-practice/problem/data/sha256_vectors.json
```

## 입출력 계약

- 입력: `problem/data/*_vectors.json`, `problem/data/demo_profile.json`
- 출력: primitive별 결과 JSON, deterministic demo JSON
- 핵심 판정 축: `actual_hex`, `expected_hex`, `matched`

## 읽는 순서

1. [problem/README.md](problem/README.md)
2. [docs/README.md](docs/README.md)
3. [python/README.md](python/README.md)
4. [notion/README.md](notion/README.md)
5. [guides/security/crypto-primitives.md](../../../guides/security/crypto-primitives.md)

## 배운 점과 한계

- primitive 수를 늘리는 것보다 각 primitive가 어떤 문제를 푸는지 분리해 설명하는 편이 학습 효과가 큽니다.
- Argon2id, scrypt, AEAD, digital signature는 현재 범위 밖입니다.
- PBKDF2-HMAC-SHA1은 reference vector 재현을 위해 남겨 두었고, production 기본 password KDF 추천안은 아닙니다.
