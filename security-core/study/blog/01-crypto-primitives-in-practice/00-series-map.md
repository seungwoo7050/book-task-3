# Series Map — crypto-primitives-in-practice

이 시리즈는 `hash`, `MAC`, `KDF`를 한 문단에 묶어 설명하지 않고, 서로 다른 입력과 목적을 가진 primitive로 어떻게 갈라서 보여 줄 수 있는지 따라간다. 읽는 순서도 그 질문에 맞춰 잡혀 있다. 먼저 primitive 함수를 분리하고, 그 다음 reference vector로 경계를 고정한 뒤, 마지막에 demo CLI로 사람이 읽는 출력 surface까지 닫는다.

## 범위

- 핵심 질문: `hash`, `MAC`, `KDF`를 한 덩어리 보안 함수처럼 설명하지 않고, 입력과 목적이 다른 primitive로 어떻게 갈라서 보여 줄 것인가.
- 글의 단위: primitive 함수 분리 -> vector manifest 판정 -> demo/CLI 계약.
- chronology 표지: 세부 git history가 없어서 `Session 1`부터 `Session 3`까지로 복원한다.

## source set

아래 문서와 코드가 이 시리즈의 직접 근거다. README는 문제를 설명하고, `docs`는 개념 경계를 정리하며, `python/src`와 `python/tests`는 실제 구현과 검증 surface를 맡는다.

- `../../01-crypto-primitives-in-practice/README.md`
- `../../01-crypto-primitives-in-practice/problem/README.md`
- `../../01-crypto-primitives-in-practice/docs/README.md`
- `../../01-crypto-primitives-in-practice/docs/concepts/hash-vs-mac-vs-kdf.md`
- `../../01-crypto-primitives-in-practice/python/README.md`
- `../../01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/primitives.py`
- `../../01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/vectors.py`
- `../../01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/cli.py`
- `../../01-crypto-primitives-in-practice/python/tests/test_primitives.py`
- `../../01-crypto-primitives-in-practice/python/tests/test_cli.py`

## canonical CLI

```bash
PYTHONPATH=study/01-crypto-primitives-in-practice/python/src \
  .venv/bin/python -m pytest study/01-crypto-primitives-in-practice/python/tests

PYTHONPATH=study/01-crypto-primitives-in-practice/python/src \
  .venv/bin/python -m crypto_primitives_in_practice.cli check-vectors \
  study/01-crypto-primitives-in-practice/problem/data/hkdf_sha256_vectors.json

PYTHONPATH=study/01-crypto-primitives-in-practice/python/src \
  .venv/bin/python -m crypto_primitives_in_practice.cli demo \
  study/01-crypto-primitives-in-practice/problem/data/demo_profile.json
```

## series

1. [01-evidence-ledger.md](01-evidence-ledger.md)
2. [02-structure.md](02-structure.md)
3. [10-chronology-separating-primitives-vectors-and-demo-surface.md](10-chronology-separating-primitives-vectors-and-demo-surface.md)
