# 06-remediation-pack-runner-python 문제지

## 왜 중요한가

탐지에서 끝나지 않고, 어떤 finding은 자동 패치 후보가 되고 어떤 finding은 수동 승인과 운영 절차가 필요하다는 점을 코드로 구분해야 합니다. 핵심은 “실행”보다 “검토 가능한 제안”을 우선하는 것입니다.

## 목표

시작 위치의 구현을 완성해 실제 patch 적용은 하지 않습니다와 외부 승인 시스템이나 rollback orchestration은 연결하지 않습니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../01-cloud-security-core/06-remediation-pack-runner/python/src/remediation_pack_runner/__init__.py`
- `../01-cloud-security-core/06-remediation-pack-runner/python/src/remediation_pack_runner/cli.py`
- `../01-cloud-security-core/06-remediation-pack-runner/python/src/remediation_pack_runner/runner.py`
- `../01-cloud-security-core/06-remediation-pack-runner/python/tests/test_runner.py`
- `../01-cloud-security-core/06-remediation-pack-runner/problem/data/sample_finding.json`

## starter code / 입력 계약

- `../01-cloud-security-core/06-remediation-pack-runner/python/src/remediation_pack_runner/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 실제 patch 적용은 하지 않습니다.
- 외부 승인 시스템이나 rollback orchestration은 연결하지 않습니다.

## 제외 범위

- `../01-cloud-security-core/06-remediation-pack-runner/problem/data/sample_finding.json` fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `dry_run`와 `RemediationPlan`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `_finding`와 `test_build_dry_run_returns_patch_for_public_access_finding`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../01-cloud-security-core/06-remediation-pack-runner/problem/data/sample_finding.json` fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/06-remediation-pack-runner/python && PYTHONPATH=src python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/06-remediation-pack-runner/python && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`06-remediation-pack-runner-python_answer.md`](06-remediation-pack-runner-python_answer.md)에서 확인한다.
