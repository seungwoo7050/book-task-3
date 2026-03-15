# 01-aws-security-primitives-python 문제지

## 왜 중요한가

AWS IAM 전체를 구현하는 것이 아니라, 가장 자주 혼동되는 평가 규칙 몇 가지를 코드로 설명하는 것이 목표입니다. 특히 Effect, Action, Resource, explicit deny가 최종 decision에 어떤 순서로 반영되는지 보여 줘야 합니다.

## 목표

시작 위치의 구현을 완성해 실제 AWS API나 계정 상태를 조회하지 않습니다와 학습 범위는 statement 단위 match와 우선순위 설명까지로 제한합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../00-aws-security-foundations/01-aws-security-primitives/python/src/aws_security_primitives/__init__.py`
- `../00-aws-security-foundations/01-aws-security-primitives/python/src/aws_security_primitives/cli.py`
- `../00-aws-security-foundations/01-aws-security-primitives/python/src/aws_security_primitives/engine.py`
- `../00-aws-security-foundations/01-aws-security-primitives/python/tests/test_engine.py`
- `../00-aws-security-foundations/01-aws-security-primitives/problem/data/policy_allow_read.json`
- `../00-aws-security-foundations/01-aws-security-primitives/problem/data/request_read.json`

## starter code / 입력 계약

- `../00-aws-security-foundations/01-aws-security-primitives/python/src/aws_security_primitives/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 실제 AWS API나 계정 상태를 조회하지 않습니다.
- 학습 범위는 statement 단위 match와 우선순위 설명까지로 제한합니다.

## 제외 범위

- `../00-aws-security-foundations/01-aws-security-primitives/problem/data/policy_allow_read.json` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `explain`와 `_as_list`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `test_allow_matches_when_action_and_resource_match`와 `test_explicit_deny_overrides_allow`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../00-aws-security-foundations/01-aws-security-primitives/problem/data/policy_allow_read.json` 등 fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/bithumb/00-aws-security-foundations/01-aws-security-primitives/python && PYTHONPATH=src python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/bithumb/00-aws-security-foundations/01-aws-security-primitives/python && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`01-aws-security-primitives-python_answer.md`](01-aws-security-primitives-python_answer.md)에서 확인한다.
