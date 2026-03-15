# 04-iam-policy-analyzer-python 문제지

## 왜 중요한가

IAM policy JSON을 읽고, 단순 allow/deny가 아니라 least privilege 관점에서 설명 가능한 finding을 만들어야 합니다. 정책이 왜 위험한지와 어떤 패턴이 remediation 우선순위를 높이는지 함께 드러나야 합니다.

## 목표

시작 위치의 구현을 완성해 조직 전체 권한 그래프는 추적하지 않습니다와 policy analyzer는 단일 policy 문서 기준의 위험 판단까지만 담당합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../01-cloud-security-core/04-iam-policy-analyzer/python/src/iam_policy_analyzer/__init__.py`
- `../01-cloud-security-core/04-iam-policy-analyzer/python/src/iam_policy_analyzer/analyzer.py`
- `../01-cloud-security-core/04-iam-policy-analyzer/python/src/iam_policy_analyzer/cli.py`
- `../01-cloud-security-core/04-iam-policy-analyzer/python/tests/test_analyzer.py`
- `../01-cloud-security-core/04-iam-policy-analyzer/problem/data/broad_admin_policy.json`
- `../01-cloud-security-core/04-iam-policy-analyzer/problem/data/passrole_policy.json`
- `../01-cloud-security-core/04-iam-policy-analyzer/problem/data/scoped_policy.json`

## starter code / 입력 계약

- `../01-cloud-security-core/04-iam-policy-analyzer/python/src/iam_policy_analyzer/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 조직 전체 권한 그래프는 추적하지 않습니다.
- policy analyzer는 단일 policy 문서 기준의 위험 판단까지만 담당합니다.

## 제외 범위

- `../01-cloud-security-core/04-iam-policy-analyzer/problem/data/broad_admin_policy.json` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `_as_list`와 `Finding`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `_policy`와 `test_broad_admin_policy_reports_multiple_findings`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../01-cloud-security-core/04-iam-policy-analyzer/problem/data/broad_admin_policy.json` 등 fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/04-iam-policy-analyzer/python && PYTHONPATH=src python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/04-iam-policy-analyzer/python && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`04-iam-policy-analyzer-python_answer.md`](04-iam-policy-analyzer-python_answer.md)에서 확인한다.
