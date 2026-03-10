# Python 구현

아래 내용은 모두 레포 루트 기준입니다.

## 다루는 범위

- exception, evidence, audit trail을 모델링합니다.
- 예외 승인과 만료, 증적 연결 흐름을 다룹니다.
- append-only 성격의 감사 기록을 남깁니다.

## 실행 예시

```bash
make venv
PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m exception_evidence_manager.cli
```

## 테스트

```bash
PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m pytest 01-cloud-security-core/09-exception-and-evidence-manager/python/tests
```

## 상태

`verified`

## 구현 메모

manager는 작은 메모리 모델이지만, 캡스톤의 DB 구조로 옮기기 쉽게 핵심 필드를 명확히 나눕니다.
