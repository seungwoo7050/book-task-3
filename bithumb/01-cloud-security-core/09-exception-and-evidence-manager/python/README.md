# Python 구현

아래 내용은 모두 레포 루트 기준입니다.

## 구현한 답의 범위

- exception, evidence, audit trail을 모델링합니다.
- 예외 승인과 만료, 증적 연결 흐름을 다룹니다.
- append-only 성격의 감사 기록을 남깁니다.

## 핵심 엔트리포인트

- `python/src/exception_evidence_manager/manager.py`
- `python/src/exception_evidence_manager/cli.py`

## 실행

```bash
make venv
PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m exception_evidence_manager.cli
```

## 테스트

```bash
PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m pytest 01-cloud-security-core/09-exception-and-evidence-manager/python/tests
```

## 대표 출력 예시

```json
{
  "exception_id": "54cbecc3-371e-480e-9f59-c71d48226f71",
  "approved_status": "approved",
  "evidence_id": "0df263ec-8e63-4964-8e07-014aa59019db",
  "audit_event_count": 3
}
```

## 구현 메모

manager는 작은 메모리 모델이지만, 캡스톤의 DB 구조로 옮기기 쉽게 핵심 필드를 명확히 나눕니다.
