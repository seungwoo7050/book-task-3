# 02-auth-threat-modeling-python 문제지

## 왜 중요한가

auth 설계를 기능 이름이 아니라 control presence와 attack surface로 평가해야 합니다. 이 프로젝트는 JSON scenario를 읽어 auth control 누락을 AUTH-* finding으로 반환합니다.

## 목표

시작 위치의 구현을 완성해 secure baseline scenario는 0 finding이어야 합니다, insecure scenario는 기대한 AUTH-* control ID만 반환해야 합니다, check-scenarios <manifest>가 시나리오별 matched 여부와 finding 목록을 JSON으로 출력해야 합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/02-auth-threat-modeling/python/src/auth_threat_modeling/__init__.py`
- `../study/02-auth-threat-modeling/python/src/auth_threat_modeling/cli.py`
- `../study/02-auth-threat-modeling/python/src/auth_threat_modeling/evaluator.py`
- `../study/02-auth-threat-modeling/python/src/auth_threat_modeling/scenarios.py`
- `../study/02-auth-threat-modeling/python/tests/test_cli.py`
- `../study/02-auth-threat-modeling/python/tests/test_evaluator.py`
- `../study/02-auth-threat-modeling/problem/data/demo_profile.json`
- `../study/02-auth-threat-modeling/problem/data/scenario_bundle.json`

## starter code / 입력 계약

- `../study/02-auth-threat-modeling/python/src/auth_threat_modeling/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- secure baseline scenario는 0 finding이어야 합니다.
- insecure scenario는 기대한 AUTH-* control ID만 반환해야 합니다.
- check-scenarios <manifest>가 시나리오별 matched 여부와 finding 목록을 JSON으로 출력해야 합니다.
- demo <profile>가 하나의 auth 설계를 deterministic하게 설명해야 합니다.

## 제외 범위

- `../study/02-auth-threat-modeling/problem/data/demo_profile.json` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `check_scenarios`와 `demo`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `test_check_scenarios_cli_emits_deterministic_summary`와 `test_demo_cli_emits_deterministic_profile_output`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/02-auth-threat-modeling/problem/data/demo_profile.json` 등 fixture/trace 기준으로 결과를 대조했다.
- `make test-unit && make demo-auth`가 통과한다.

## 검증 방법

```bash
make test-unit && make demo-auth
```

```bash
cd /Users/woopinbell/work/book-task-3/security-core/study/02-auth-threat-modeling/python && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`02-auth-threat-modeling-python_answer.md`](02-auth-threat-modeling-python_answer.md)에서 확인한다.
