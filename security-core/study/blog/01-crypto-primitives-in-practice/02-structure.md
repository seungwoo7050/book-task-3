# Structure Design — crypto-primitives-in-practice

이 outline는 최종 글이 어떤 리듬으로 읽혀야 하는지 정리한 메모다. 글의 중심은 “알고리즘 목록”이 아니라 primitive 경계가 어떻게 검증 계약으로 자라는가에 있다.

## opening

- 시작 질문: 왜 이 프로젝트는 알고리즘 개수보다 primitive 경계부터 분리해야 했는가.
- 첫 증거: `primitives.py`의 함수 목록과 `hash-vs-mac-vs-kdf.md`.
- 서술 원칙: README 요약보다 함수 경계가 어떻게 검증 계약으로 자라는지 먼저 보여 준다.

## Session 1 — primitive 함수를 먼저 갈랐다

- 다룰 표면: `python/src/crypto_primitives_in_practice/primitives.py`
- 먼저 던질 질문: “같은 hex 문자열을 내놓는다고 해서 같은 문제를 푸는 함수는 아니다.”
- 꼭 넣을 CLI: `PYTHONPATH=study/01-crypto-primitives-in-practice/python/src .venv/bin/python -m pytest study/01-crypto-primitives-in-practice/python/tests`
- 꼭 남길 검증 신호: `10 passed in 0.06s`
- 핵심 전환 문장: HKDF의 extract-expand loop를 보고 나면 KDF를 단순 hash 반복처럼 설명할 수 없게 된다.

## Session 2 — manifest 판정기로 경계를 고정했다

- 다룰 표면: `python/src/crypto_primitives_in_practice/vectors.py::_compute_actual_hex`, `check_vectors_manifest`
- 먼저 던질 질문: “분리된 함수가 실제로 무엇을 증명하는지는 vector manifest가 결정한다.”
- 꼭 넣을 CLI: `... cli check-vectors ... hkdf_sha256_vectors.json`
- 꼭 남길 검증 신호: `passed=1`, `failed=0`, `rfc-5869-case-1 matched=true`
- 핵심 전환 문장: `_decode`와 primitive dispatch가 있어야 같은 JSON 형식으로도 서로 다른 입력 규칙을 설명할 수 있다.

## Session 3 — demo와 CLI contract로 마감했다

- 다룰 표면: `python/src/crypto_primitives_in_practice/vectors.py::demo_from_profile`, `python/src/crypto_primitives_in_practice/cli.py`, `python/tests/test_cli.py`
- 먼저 던질 질문: “pass/fail만 남기면 학습자는 왜 hash와 MAC을 갈랐는지 다시 놓치기 쉽다.”
- 꼭 넣을 CLI: `... cli demo ... demo_profile.json`
- 꼭 남길 검증 신호: `hash_equals_mac=false`, `mac_self_check=true`
- 핵심 전환 문장: demo의 비교 항목이 primitive 차이를 사람이 읽는 문장으로 다시 번역해 준다.

## ending

- 마지막 단락에서는 범위 밖인 `Argon2id`, `scrypt`, `AEAD`, `digital signature`를 짧게 남긴다.
- 다음 질문은 “인증 설계 차이를 primitive가 아니라 control gap으로 어떻게 설명할까”로 이어진다.
