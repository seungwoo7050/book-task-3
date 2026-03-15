# 01-crypto-primitives-in-practice-python 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 SHA-256, HMAC-SHA256, HKDF-SHA256, PBKDF2-HMAC-SHA1 vector가 모두 통과해야 합니다, check-vectors <manifest>가 primitive별 결과를 JSON으로 출력해야 합니다, demo <profile>가 hash, MAC, KDF 결과를 deterministic하게 출력해야 합니다를 한 흐름으로 설명하고 검증한다. 핵심은 `check_vectors`와 `demo`, `sha256_digest` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- SHA-256, HMAC-SHA256, HKDF-SHA256, PBKDF2-HMAC-SHA1 vector가 모두 통과해야 합니다.
- check-vectors <manifest>가 primitive별 결과를 JSON으로 출력해야 합니다.
- demo <profile>가 hash, MAC, KDF 결과를 deterministic하게 출력해야 합니다.
- 첫 진입점은 `../study/01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/__init__.py`이고, 여기서 `check_vectors`와 `demo` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/__init__.py`: 패키지 진입점과 공개 API 경계를 고정하는 파일이다.
- `../study/01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/cli.py`: `check_vectors`, `demo`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/primitives.py`: `sha256_digest`, `hmac_sha256`, `hkdf_sha256`, `pbkdf2_hmac_sha1`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/vectors.py`: `load_json`, `_decode`, `_encoding`, `_compute_actual_hex`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/01-crypto-primitives-in-practice/python/tests/test_cli.py`: `test_check_vectors_cli_emits_deterministic_summary`, `test_demo_cli_emits_deterministic_profile_output`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/01-crypto-primitives-in-practice/python/tests/test_primitives.py`: `test_sha256_manifest_vectors_pass`, `test_hmac_manifest_vectors_pass`, `test_hkdf_manifest_vectors_pass`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/01-crypto-primitives-in-practice/problem/data/demo_profile.json`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.
- `../study/01-crypto-primitives-in-practice/problem/data/hkdf_sha256_vectors.json`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.

## 정답을 재구성하는 절차

1. `../study/01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/__init__.py`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `test_check_vectors_cli_emits_deterministic_summary` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make test-unit && make demo-crypto`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make test-unit && make demo-crypto
```

```bash
cd /Users/woopinbell/work/book-task-3/security-core/study/01-crypto-primitives-in-practice/python && PYTHONPATH=src python3 -m pytest
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `test_check_vectors_cli_emits_deterministic_summary`와 `test_demo_cli_emits_deterministic_profile_output`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make test-unit && make demo-crypto`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/__init__.py`
- `../study/01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/cli.py`
- `../study/01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/primitives.py`
- `../study/01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/vectors.py`
- `../study/01-crypto-primitives-in-practice/python/tests/test_cli.py`
- `../study/01-crypto-primitives-in-practice/python/tests/test_primitives.py`
- `../study/01-crypto-primitives-in-practice/problem/data/demo_profile.json`
- `../study/01-crypto-primitives-in-practice/problem/data/hkdf_sha256_vectors.json`
- `../study/01-crypto-primitives-in-practice/problem/data/hmac_sha256_vectors.json`
- `../study/01-crypto-primitives-in-practice/problem/data/pbkdf2_hmac_sha1_vectors.json`
