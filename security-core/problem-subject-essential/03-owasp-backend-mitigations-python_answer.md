# 03-owasp-backend-mitigations-python 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 secure baseline case는 0 finding이어야 합니다, insecure case는 기대한 OWASP-* control ID만 반환해야 합니다, check-cases <manifest>가 case별 matched 여부와 finding 목록을 JSON으로 출력해야 합니다를 한 흐름으로 설명하고 검증한다. 핵심은 `load_json`와 `check_case_manifest`, `demo_profile` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- secure baseline case는 0 finding이어야 합니다.
- insecure case는 기대한 OWASP-* control ID만 반환해야 합니다.
- check-cases <manifest>가 case별 matched 여부와 finding 목록을 JSON으로 출력해야 합니다.
- 첫 진입점은 `../study/03-owasp-backend-mitigations/python/src/owasp_backend_mitigations/__init__.py`이고, 여기서 `load_json`와 `check_case_manifest` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/03-owasp-backend-mitigations/python/src/owasp_backend_mitigations/__init__.py`: 패키지 진입점과 공개 API 경계를 고정하는 파일이다.
- `../study/03-owasp-backend-mitigations/python/src/owasp_backend_mitigations/cases.py`: `load_json`, `check_case_manifest`, `demo_profile`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/03-owasp-backend-mitigations/python/src/owasp_backend_mitigations/cli.py`: `check_cases`, `demo`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/03-owasp-backend-mitigations/python/src/owasp_backend_mitigations/evaluator.py`: `_finding`, `evaluate_case`, `case_control_ids`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/03-owasp-backend-mitigations/python/tests/test_cli.py`: `test_check_cases_cli_emits_deterministic_summary`, `test_demo_cli_emits_deterministic_profile_output`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/03-owasp-backend-mitigations/python/tests/test_evaluator.py`: `_case`, `test_secure_baseline_has_no_findings`, `test_each_negative_case_returns_expected_control`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/03-owasp-backend-mitigations/problem/data/case_bundle.json`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.
- `../study/03-owasp-backend-mitigations/problem/data/demo_profile.json`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.

## 정답을 재구성하는 절차

1. `../study/03-owasp-backend-mitigations/python/src/owasp_backend_mitigations/__init__.py`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `test_check_cases_cli_emits_deterministic_summary` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make test-unit && make demo-owasp`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make test-unit && make demo-owasp
```

```bash
cd /Users/woopinbell/work/book-task-3/security-core/study/03-owasp-backend-mitigations/python && PYTHONPATH=src python3 -m pytest
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `test_check_cases_cli_emits_deterministic_summary`와 `test_demo_cli_emits_deterministic_profile_output`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make test-unit && make demo-owasp`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/03-owasp-backend-mitigations/python/src/owasp_backend_mitigations/__init__.py`
- `../study/03-owasp-backend-mitigations/python/src/owasp_backend_mitigations/cases.py`
- `../study/03-owasp-backend-mitigations/python/src/owasp_backend_mitigations/cli.py`
- `../study/03-owasp-backend-mitigations/python/src/owasp_backend_mitigations/evaluator.py`
- `../study/03-owasp-backend-mitigations/python/tests/test_cli.py`
- `../study/03-owasp-backend-mitigations/python/tests/test_evaluator.py`
- `../study/03-owasp-backend-mitigations/problem/data/case_bundle.json`
- `../study/03-owasp-backend-mitigations/problem/data/demo_profile.json`
