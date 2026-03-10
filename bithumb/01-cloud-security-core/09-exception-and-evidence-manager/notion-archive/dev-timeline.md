# 09 Exception & Evidence Manager — 개발 타임라인

이 문서는 프로젝트를 처음부터 다시 재현할 때 필요한 모든 단계를 순서대로 기록한다.

---

## 1단계: 환경 준비

```bash
cd study2
make venv
```

이 과제는 외부 패키지를 사용하지 않는다.
Python 표준 라이브러리(`datetime`, `uuid`)만 사용.

---

## 2단계: 프로젝트 디렉토리 구조 생성

```
09-exception-and-evidence-manager/
├── README.md
├── docs/
│   ├── README.md
│   ├── concepts/
│   │   └── exception-management.md
│   └── references/
│       └── README.md
├── problem/
│   └── README.md
└── python/
    ├── README.md
    ├── src/
    │   └── exception_evidence/
    │       ├── __init__.py
    │       └── manager.py
    └── tests/
        └── test_manager.py
```

```bash
mkdir -p 01-cloud-security-core/09-exception-and-evidence-manager/{docs/{concepts,references},problem,python/{src/exception_evidence,tests}}
```

이 과제에는 `problem/data/` 디렉토리가 없다.
fixture 데이터 없이, 테스트 코드에서 직접 데이터를 생성한다.

---

## 3단계: 데이터 모델 설계

ExceptionManager 내부에서 관리하는 데이터 구조:

```python
# 개별 예외
{
    "exception_id": "uuid",
    "finding_id": "...",
    "reason": "...",
    "status": "pending" | "approved",
    "expires": datetime,
    "evidence": [...],
    "audit_events": [...]
}
```

핵심 설계 결정:
- `exception_id`는 UUID로 자동 생성
- `evidence`와 `audit_events`는 리스트 (append-only)
- 저장소는 `dict[str, dict]` (exception_id → exception)

---

## 4단계: ExceptionManager 구현

### manager.py 작성 순서

1. **`__init__`**: 빈 딕셔너리 초기화

2. **`create_exception(finding_id, reason, expires)`**
   - UUID 생성
   - status를 `"pending"`으로 설정
   - audit event 추가: `{"type": "created", "at": now}`
   - 딕셔너리에 저장

3. **`approve_exception(exception_id, approved_by)`**
   - status를 `"approved"`로 변경
   - audit event 추가: `{"type": "approved", "by": approved_by, "at": now}`

4. **`add_evidence(exception_id, evidence_item)`**
   - 해당 exception의 evidence 리스트에 append

5. **`is_suppressed(finding_id)`**
   - 해당 finding_id의 exception을 찾음
   - status가 `"approved"`이고 expires가 아직 미래인지 확인
   - 둘 다 만족하면 `True`

6. **`get_exception(exception_id)`**
   - 딕셔너리에서 조회

```bash
touch python/src/exception_evidence/__init__.py
```

---

## 5단계: 테스트 작성

### test_manager.py

**테스트 1: `test_suppression_until_expired`**
```python
def test_suppression_until_expired():
    mgr = ExceptionManager()
    exc = mgr.create_exception(
        finding_id="F-001",
        reason="migration window",
        expires=datetime.now() + timedelta(days=30)
    )
    mgr.approve_exception(exc["exception_id"], approved_by="lead")
    assert mgr.is_suppressed("F-001") is True

    # 만료 시뮬레이션
    exc["expires"] = datetime.now() - timedelta(days=1)
    assert mgr.is_suppressed("F-001") is False
```

**테스트 2: `test_evidence_and_audit`**
```python
def test_evidence_and_audit():
    mgr = ExceptionManager()
    exc = mgr.create_exception(
        finding_id="F-002",
        reason="compensating control exists",
        expires=datetime.now() + timedelta(days=90)
    )
    mgr.add_evidence(exc["exception_id"], {
        "type": "url",
        "url": "https://wiki.internal/compensating-control"
    })
    mgr.approve_exception(exc["exception_id"], approved_by="ciso")

    result = mgr.get_exception(exc["exception_id"])
    assert len(result["evidence"]) == 1
    assert len(result["audit_events"]) >= 2  # created + approved
```

---

## 6단계: 실행과 검증

### 테스트 실행

```bash
cd study2
PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src \
  .venv/bin/python -m pytest 01-cloud-security-core/09-exception-and-evidence-manager/python/tests -v
```

또는:
```bash
make test-unit
```

### 수동 검증

```bash
cd python
PYTHONPATH=src python -c "
from exception_evidence.manager import ExceptionManager
from datetime import datetime, timedelta

mgr = ExceptionManager()
exc = mgr.create_exception('F-001', 'test', datetime.now() + timedelta(days=30))
print('status:', exc['status'])
mgr.approve_exception(exc['exception_id'], 'admin')
print('suppressed:', mgr.is_suppressed('F-001'))
"
```

---

## 환경 요약

| 항목 | 값 |
|------|-----|
| Python | 3.13+ |
| 핵심 의존성 | 없음 (stdlib만 사용) |
| 테스트 프레임워크 | pytest |
| AWS 계정 필요 여부 | 불필요 |
| 데이터베이스 | 없음 (in-memory) |
| 외부 서비스 의존 | 없음 |
| 테스트 카테고리 | Unit |

---

## 주의사항

- `is_suppressed`는 finding_id로 검색하므로, 같은 finding에 여러 exception이 있으면
  가장 최근 approved된 것을 기준으로 판단한다.
- 만료 시뮬레이션은 테스트에서 `exc["expires"]`를 직접 수정하는 방식이다.
  프로덕션에서는 시간 의존 로직을 테스트할 때 `freezegun` 같은 라이브러리를 쓰거나,
  clock을 주입하는 패턴을 사용한다.
- 이 과제의 코드는 과제 10에서 SQLAlchemy 모델 위에 재구현된다.
  핵심 로직(create → approve → is_suppressed)의 흐름은 동일하다.
