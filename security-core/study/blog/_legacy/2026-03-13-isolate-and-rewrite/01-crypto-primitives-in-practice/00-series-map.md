# crypto-primitives-in-practice series map

이 시리즈는 `crypto-primitives-in-practice`를 "암호 함수 몇 개를 감싼 CLI"가 아니라, `hash`, `MAC`, `KDF`의 입력 경계를 reference vector와 demo profile로 고정하는 lab으로 다시 읽기 위한 지도다.

## 이 프로젝트가 답하는 질문

- 공개 입력과 비밀 입력을 쓰는 primitive를 같은 함수처럼 설명하지 않으려면 구현 surface를 어디서 잘라야 할까
- RFC vector와 deterministic demo를 같이 두면 primitive 설명이 단순 용어 정리보다 왜 더 단단해질까

## 읽는 순서

1. [10-chronology-primitives-vectors-and-demo-contract.md](10-chronology-primitives-vectors-and-demo-contract.md)

## 참조한 실제 파일

- `study/01-crypto-primitives-in-practice/README.md`
- `study/01-crypto-primitives-in-practice/problem/README.md`
- `study/01-crypto-primitives-in-practice/problem/data/sha256_vectors.json`
- `study/01-crypto-primitives-in-practice/problem/data/hkdf_sha256_vectors.json`
- `study/01-crypto-primitives-in-practice/problem/data/demo_profile.json`
- `study/01-crypto-primitives-in-practice/docs/concepts/hash-vs-mac-vs-kdf.md`
- `study/01-crypto-primitives-in-practice/python/README.md`
- `study/01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/primitives.py`
- `study/01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/vectors.py`
- `study/01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/cli.py`
- `study/01-crypto-primitives-in-practice/python/tests/test_primitives.py`
- `study/01-crypto-primitives-in-practice/python/tests/test_cli.py`

## Canonical CLI

```bash
cd study/01-crypto-primitives-in-practice
PYTHONPATH=python/src ../../.venv/bin/python -m pytest python/tests
PYTHONPATH=python/src ../../.venv/bin/python -m crypto_primitives_in_practice.cli check-vectors problem/data/sha256_vectors.json
PYTHONPATH=python/src ../../.venv/bin/python -m crypto_primitives_in_practice.cli demo problem/data/demo_profile.json
```

## Git Anchor

- `2026-03-12 e3be503 Track Appendix 에 대한 전반적인 개선 완료 (mobile / security)`

## 추론 원칙

- 날짜 단위 chronology는 남아 있지 않아서 `docs/concepts`가 먼저 고정한 primitive vocabulary와 `primitives.py` 함수 표면을 기준으로 순서를 복원했다.
- 구현의 끝은 `sha256_digest` 하나를 계산하는 지점이 아니라, manifest의 `encoding` 변형과 demo profile의 비교 포인트까지 CLI 계약으로 닫히는 지점으로 본다.
