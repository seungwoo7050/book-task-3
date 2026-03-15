# 09-exception-and-evidence-manager-python 문제지

## 왜 중요한가

보안 거버넌스에서 중요한 예외와 증적 흐름을 작은 메모리 모델로 먼저 구현해야 합니다. 중요한 점은 예외를 단순 mute가 아니라 승인, 만료, 증적, audit가 분리된 관리 대상 레코드로 다루는 것입니다.

## 목표

시작 위치의 구현을 완성해 영속 저장소는 사용하지 않습니다와 외부 티켓 시스템이나 승인 워크플로와 연동하지 않습니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../01-cloud-security-core/09-exception-and-evidence-manager/python/src/exception_evidence_manager/__init__.py`
- `../01-cloud-security-core/09-exception-and-evidence-manager/python/src/exception_evidence_manager/cli.py`
- `../01-cloud-security-core/09-exception-and-evidence-manager/python/src/exception_evidence_manager/manager.py`
- `../01-cloud-security-core/09-exception-and-evidence-manager/python/tests/test_manager.py`

## starter code / 입력 계약

- `../01-cloud-security-core/09-exception-and-evidence-manager/python/src/exception_evidence_manager/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 영속 저장소는 사용하지 않습니다.
- 외부 티켓 시스템이나 승인 워크플로와 연동하지 않습니다.

## 제외 범위

- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `demo`와 `ExceptionRecord`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `test_exception_suppresses_scope_until_expiry`와 `test_evidence_and_audit_events_are_appended`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/09-exception-and-evidence-manager/python && PYTHONPATH=src python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/09-exception-and-evidence-manager/python && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`09-exception-and-evidence-manager-python_answer.md`](09-exception-and-evidence-manager-python_answer.md)에서 확인한다.
