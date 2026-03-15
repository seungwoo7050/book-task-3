# 08-container-guardrails-python 문제지

## 왜 중요한가

EKS나 대형 플랫폼 없이도 학습할 수 있도록, Kubernetes manifest와 이미지 메타데이터 자체를 검사하는 guardrail 엔진을 만들어야 합니다. 핵심은 manifest 수준에서 충분히 설명 가능한 위험과 범위 밖을 명확히 나누는 것입니다.

## 목표

시작 위치의 구현을 완성해 실제 클러스터, admission controller, 런타임 이벤트는 다루지 않습니다와 manifest와 image metadata에서 설명 가능한 규칙만 다룹니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../01-cloud-security-core/08-container-guardrails/python/src/container_guardrails/__init__.py`
- `../01-cloud-security-core/08-container-guardrails/python/src/container_guardrails/cli.py`
- `../01-cloud-security-core/08-container-guardrails/python/src/container_guardrails/scanner.py`
- `../01-cloud-security-core/08-container-guardrails/python/tests/test_scanner.py`
- `../01-cloud-security-core/08-container-guardrails/problem/data/insecure_image.json`
- `../01-cloud-security-core/08-container-guardrails/problem/data/insecure_k8s.yaml`
- `../01-cloud-security-core/08-container-guardrails/problem/data/secure_image.json`

## starter code / 입력 계약

- `../01-cloud-security-core/08-container-guardrails/python/src/container_guardrails/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 실제 클러스터, admission controller, 런타임 이벤트는 다루지 않습니다.
- manifest와 image metadata에서 설명 가능한 규칙만 다룹니다.

## 제외 범위

- `../01-cloud-security-core/08-container-guardrails/problem/data/insecure_image.json` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `scan`와 `Finding`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `_problem_data`와 `test_insecure_inputs_report_expected_findings`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../01-cloud-security-core/08-container-guardrails/problem/data/insecure_image.json` 등 fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/08-container-guardrails/python && PYTHONPATH=src python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/08-container-guardrails/python && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`08-container-guardrails-python_answer.md`](08-container-guardrails-python_answer.md)에서 확인한다.
