# 01-crypto-primitives-in-practice-python 문제지

## 왜 중요한가

hash, MAC, KDF를 같은 보안 함수처럼 다루지 않고, 각 primitive의 입력과 목적을 reference vector로 검증 가능한 형태로 분리해야 합니다.

## 목표

시작 위치의 구현을 완성해 SHA-256, HMAC-SHA256, HKDF-SHA256, PBKDF2-HMAC-SHA1 vector가 모두 통과해야 합니다, check-vectors <manifest>가 primitive별 결과를 JSON으로 출력해야 합니다, demo <profile>가 hash, MAC, KDF 결과를 deterministic하게 출력해야 합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/__init__.py`
- `../study/01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/cli.py`
- `../study/01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/primitives.py`
- `../study/01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/vectors.py`
- `../study/01-crypto-primitives-in-practice/python/tests/test_cli.py`
- `../study/01-crypto-primitives-in-practice/python/tests/test_primitives.py`
- `../study/01-crypto-primitives-in-practice/problem/data/demo_profile.json`
- `../study/01-crypto-primitives-in-practice/problem/data/hkdf_sha256_vectors.json`

## starter code / 입력 계약

- `../study/01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- SHA-256, HMAC-SHA256, HKDF-SHA256, PBKDF2-HMAC-SHA1 vector가 모두 통과해야 합니다.
- check-vectors <manifest>가 primitive별 결과를 JSON으로 출력해야 합니다.
- demo <profile>가 hash, MAC, KDF 결과를 deterministic하게 출력해야 합니다.

## 제외 범위

- `../study/01-crypto-primitives-in-practice/problem/data/demo_profile.json` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `check_vectors`와 `demo`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `test_check_vectors_cli_emits_deterministic_summary`와 `test_demo_cli_emits_deterministic_profile_output`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/01-crypto-primitives-in-practice/problem/data/demo_profile.json` 등 fixture/trace 기준으로 결과를 대조했다.
- `make test-unit && make demo-crypto`가 통과한다.

## 검증 방법

```bash
make test-unit && make demo-crypto
```

```bash
cd /Users/woopinbell/work/book-task-3/security-core/study/01-crypto-primitives-in-practice/python && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`01-crypto-primitives-in-practice-python_answer.md`](01-crypto-primitives-in-practice-python_answer.md)에서 확인한다.
