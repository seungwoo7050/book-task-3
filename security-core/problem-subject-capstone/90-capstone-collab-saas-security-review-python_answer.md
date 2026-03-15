# 90-capstone-collab-saas-security-review-python 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 secure_baseline_bundle.json은 빈 remediation board를 만들어야 합니다, review_bundle.json은 crypto, auth, backend, dependency 결과를 모두 만들어야 합니다, demo_bundle.json은 artifact 7개와 markdown report를 생성해야 합니다를 한 흐름으로 설명하고 검증한다. 핵심은 `_finding`와 `evaluate_scenario`, `scenario_control_ids` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- secure_baseline_bundle.json은 빈 remediation board를 만들어야 합니다.
- review_bundle.json은 crypto, auth, backend, dependency 결과를 모두 만들어야 합니다.
- demo_bundle.json은 artifact 7개와 markdown report를 생성해야 합니다.
- 첫 진입점은 `../study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/__init__.py`이고, 여기서 `_finding`와 `evaluate_scenario` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/__init__.py`: 패키지 진입점과 공개 API 경계를 고정하는 파일이다.
- `../study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/auth.py`: `_finding`, `evaluate_scenario`, `scenario_control_ids`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/backend.py`: `_finding`, `evaluate_case`, `case_control_ids`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/cli.py`: `review`, `demo`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/crypto.py`: `_finding`, `evaluate_crypto_review`, `crypto_control_ids`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/90-capstone-collab-saas-security-review/python/tests/test_cli.py`: `test_review_cli_emits_deterministic_consolidated_json`, `test_review_cli_writes_all_artifacts_when_output_dir_is_provided`, `test_demo_cli_writes_demo_assets_and_report_sections`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/90-capstone-collab-saas-security-review/python/tests/test_review.py`: `test_crypto_controls_map_to_stable_ids`, `test_secure_baseline_bundle_emits_empty_review`, `test_review_bundle_reuses_existing_control_and_priority_vocab`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/90-capstone-collab-saas-security-review/problem/data/demo_bundle.json`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.

## 정답을 재구성하는 절차

1. `../study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/__init__.py`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `test_review_cli_emits_deterministic_consolidated_json` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make test-capstone && make demo-capstone`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make test-capstone && make demo-capstone
```

```bash
cd /Users/woopinbell/work/book-task-3/security-core/study/90-capstone-collab-saas-security-review/python && PYTHONPATH=src python3 -m pytest
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `test_review_cli_emits_deterministic_consolidated_json`와 `test_review_cli_writes_all_artifacts_when_output_dir_is_provided`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make test-capstone && make demo-capstone`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/__init__.py`
- `../study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/auth.py`
- `../study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/backend.py`
- `../study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/cli.py`
- `../study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/crypto.py`
- `../study/90-capstone-collab-saas-security-review/python/tests/test_cli.py`
- `../study/90-capstone-collab-saas-security-review/python/tests/test_review.py`
- `../study/90-capstone-collab-saas-security-review/problem/data/demo_bundle.json`
- `../study/90-capstone-collab-saas-security-review/problem/data/review_bundle.json`
- `../study/90-capstone-collab-saas-security-review/problem/data/secure_baseline_bundle.json`
