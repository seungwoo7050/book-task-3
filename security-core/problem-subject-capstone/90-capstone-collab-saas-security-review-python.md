# 90-capstone-collab-saas-security-review-python 문제지

## 왜 중요한가

이 capstone의 문제는 각 보안 판단을 따로 설명하는 것이 아니라, 서로 다른 finding을 한 서비스 remediation queue로 다시 정렬하는 것입니다. 입력은 서버 로그나 live scan feed가 아니라 review에 필요한 최소 정보만 담은 단일 JSON bundle로 고정합니다.

## 목표

시작 위치의 구현을 완성해 secure_baseline_bundle.json은 빈 remediation board를 만들어야 합니다, review_bundle.json은 crypto, auth, backend, dependency 결과를 모두 만들어야 합니다, demo_bundle.json은 artifact 7개와 markdown report를 생성해야 합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/__init__.py`
- `../study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/auth.py`
- `../study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/backend.py`
- `../study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/cli.py`
- `../study/90-capstone-collab-saas-security-review/python/tests/test_cli.py`
- `../study/90-capstone-collab-saas-security-review/python/tests/test_review.py`
- `../study/90-capstone-collab-saas-security-review/problem/data/demo_bundle.json`
- `../study/90-capstone-collab-saas-security-review/problem/data/review_bundle.json`

## starter code / 입력 계약

- `../study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- secure_baseline_bundle.json은 빈 remediation board를 만들어야 합니다.
- review_bundle.json은 crypto, auth, backend, dependency 결과를 모두 만들어야 합니다.
- demo_bundle.json은 artifact 7개와 markdown report를 생성해야 합니다.

## 제외 범위

- 실제 API 서버, DB, queue 운영
- live scan feed와 외부 advisory API 연동
- foundations 프로젝트를 runtime dependency로 직접 import하는 구조

## 성공 체크리스트

- 핵심 흐름은 `_finding`와 `evaluate_scenario`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `test_review_cli_emits_deterministic_consolidated_json`와 `test_review_cli_writes_all_artifacts_when_output_dir_is_provided`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/90-capstone-collab-saas-security-review/problem/data/demo_bundle.json` 등 fixture/trace 기준으로 결과를 대조했다.
- `make test-capstone && make demo-capstone`가 통과한다.

## 검증 방법

```bash
make test-capstone && make demo-capstone
```

```bash
cd /Users/woopinbell/work/book-task-3/security-core/study/90-capstone-collab-saas-security-review/python && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`90-capstone-collab-saas-security-review-python_answer.md`](90-capstone-collab-saas-security-review-python_answer.md)에서 확인한다.
