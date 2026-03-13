# 09 Exception and Evidence Manager: exception, evidence, audit를 따로 모델링하기

finding 이후의 거버넌스를 exception, evidence, audit trail로 분리해 모델링하는 작은 상태 관리기다. 이 글은 결과만 요약하지 않고, 어떤 기준을 먼저 세우고 어떤 검증으로 다음 단계로 넘어갔는지를 차근차근 따라간다.

아래 phase를 순서대로 읽으면 "왜 예외를 mute 플래그가 아니라 record 집합으로 봐야 하는가"라는 질문에 답이 어떻게 만들어졌는지 자연스럽게 연결된다.

## 구현 순서 요약
먼저 전체 흐름을 짧게 잡아 두면, 각 phase가 왜 그 순서로 배치됐는지 훨씬 덜 버겁게 읽힌다.
1. exception, evidence, audit를 서로 다른 record로 나눴다.
2. pending -> approved 상태 전이와 expiry 기반 suppression 판정을 구현했다.
3. evidence append와 append-only audit trail을 테스트로 잠가 capstone DB 모델의 씨앗을 만들었다.

## Phase 1. 예외와 증적과 감사를 record로 분리했다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `예외와 증적과 감사를 record로 분리했다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: 예외 관리를 단순 플래그가 아니라 추적 가능한 데이터 모델로 바꾼다.
- 변경 단위: `python/src/exception_evidence_manager/manager.py`의 `ExceptionRecord`, `Evidence`, `AuditEvent`, `create_exception`
- 처음 가설: exception이 그냥 boolean이면 만료일, 승인자, 증적, 감사 로그를 설명할 수 없다. record를 분리해야 거버넌스가 된다.
- 실제 진행: `ExceptionRecord`, `Evidence`, `AuditEvent` 세 dataclass를 따로 두고, `ExceptionManager` 내부 저장소도 각각 분리했다. `create_exception`은 record 생성과 동시에 `exception.created` audit event를 남기게 했다.

CLI:

```bash
$ PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m exception_evidence_manager.cli
```

검증 신호:
- CLI 출력에 `exception_id`, `evidence_id`, `audit_event_count`가 모두 나타났다.
- README가 exception/evidence/audit를 별도 모델의 핵심 범위로 문서화한다.

핵심 코드:

```python
    def create_exception(self, scope_type: str, scope_id: str, reason: str, days: int) -> ExceptionRecord:
        record = ExceptionRecord(
            id=str(uuid4()),
            scope_type=scope_type,
            scope_id=scope_id,
            reason=reason,
            expires_at=datetime.now(timezone.utc) + timedelta(days=days),
            approved_by=None,
            status="pending",
        )
        self.exceptions[record.id] = record
        self._append_event("exception.created", record.id, {"scope_id": scope_id})
        return record
```

왜 이 코드가 중요했는가: 예외 생성이 audit event를 동반하게 만든 순간, 프로젝트의 중심이 단순 suppress/un-suppress에서 추적 가능한 거버넌스로 이동했다.

새로 배운 것: 예외 관리에서 중요한 것은 “예외가 있는가”보다 “왜 있었고 누가 승인했고 언제 끝나는가”를 설명할 수 있는가다.

다음: 이제 예외 승인과 만료를 suppression 판정과 연결해야 했다.

## Phase 2. approval과 expiry를 suppression 판정에 연결했다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `approval과 expiry를 suppression 판정에 연결했다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: 예외가 언제 finding을 실제로 억제하는지 코드로 정의한다.
- 변경 단위: `python/src/exception_evidence_manager/manager.py`의 `approve_exception`, `is_suppressed`
- 처음 가설: 예외가 존재하는 것만으로는 충분하지 않다. 승인되었고 아직 만료되지 않았을 때만 suppression이 성립해야 한다.
- 실제 진행: `approve_exception`은 기존 record를 immutable하게 복사해 `approved_by`와 `status`를 갱신했고, `is_suppressed`는 같은 scope_id에 대해 승인 상태이면서 expiry가 미래인 경우만 True를 반환하게 했다.

CLI:

```bash
$ PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m pytest 01-cloud-security-core/09-exception-and-evidence-manager/python/tests
```

검증 신호:
- pytest가 `2 passed in 0.01s`로 통과했다.
- `test_exception_suppresses_scope_until_expiry`가 3일짜리 예외는 지금은 suppress하고, 10일 뒤엔 풀려야 한다고 요구한다.

핵심 코드:

```python
    def approve_exception(self, exception_id: str, approved_by: str) -> ExceptionRecord:
        record = self.exceptions[exception_id]
        approved = ExceptionRecord(
            id=record.id,
            scope_type=record.scope_type,
            scope_id=record.scope_id,
            reason=record.reason,
            expires_at=record.expires_at,
            approved_by=approved_by,
            status="approved",
        )
        self.exceptions[exception_id] = approved
        self._append_event("exception.approved", exception_id, {"approved_by": approved_by})
        return approved

    def append_evidence(self, finding_id: str, title: str, uri: str) -> Evidence:
        evidence = Evidence(
            id=str(uuid4()),
            finding_id=finding_id,
            title=title,
            uri=uri,
            added_at=datetime.now(timezone.utc),
        )
        self.evidence.append(evidence)
        self._append_event("evidence.added", finding_id, {"uri": uri})
        return evidence

    def is_suppressed(self, scope_id: str, now: datetime | None = None) -> bool:
        current = now or datetime.now(timezone.utc)
        return any(
            record.scope_id == scope_id
            and record.status == "approved"
            and record.expires_at > current
            for record in self.exceptions.values()
        )
```

왜 이 코드가 중요했는가: 예외 관리는 여기서 비로소 운영 로직이 된다. approval과 expiry 둘 중 하나라도 빠지면 suppression은 너무 쉽게 남용된다.

새로 배운 것: suppression은 영구 mute가 아니라 시간과 승인에 의해 제한되는 상태 전이다.

다음: 마지막으로 evidence append와 audit trail이 append-only로 쌓이는지 확인해야 했다.

## Phase 3. evidence append와 append-only audit trail을 잠갔다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `evidence append와 append-only audit trail을 잠갔다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: 예외 흐름의 근거와 변경 이력이 함께 남는지 검증한다.
- 변경 단위: `python/src/exception_evidence_manager/manager.py`의 `append_evidence`, `_append_event`, `python/tests/test_manager.py`
- 처음 가설: 예외 승인만 기록하면 나중에 왜 그런 결정을 했는지 잊는다. evidence와 audit가 함께 쌓여야 거버넌스가 닫힌다.
- 실제 진행: `append_evidence`는 증적 레코드를 추가하면서 `evidence.added` audit event도 남겼다. 테스트는 예외 생성, 승인, 증적 연결까지 세 단계가 지나면 audit event가 정확히 3개가 되어야 한다고 고정했다.

CLI:

```bash
$ PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m exception_evidence_manager.cli
$ PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m pytest 01-cloud-security-core/09-exception-and-evidence-manager/python/tests
```

검증 신호:
- CLI가 실제로 `audit_event_count: 3`을 출력했다.
- 테스트도 첫 audit event가 `exception.created`임을 확인해 append order를 잠갔다.

핵심 코드:

```python
def test_evidence_and_audit_events_are_appended() -> None:
    manager = ExceptionManager()
    created = manager.create_exception("finding", "finding-1", "temporary exception", 3)
    manager.approve_exception(created.id, "security.manager")
    manager.append_evidence("finding-1", "risk memo", "s3://bucket/risk.md")
    assert len(manager.audit_events) == 3
    assert manager.audit_events[0].event_type == "exception.created"

```

왜 이 코드가 중요했는가: 이 검증이 없으면 audit trail은 그냥 존재만 하는 보조 데이터가 된다. event 개수와 순서를 함께 고정해야 append-only 특성이 살아난다.

새로 배운 것: append-only audit trail의 핵심은 수정이 불가능하다는 사실보다, 변화의 순서를 복원할 수 있다는 점이다.

다음: capstone에서는 이 모델을 SQLite/PostgreSQL 기반 DB 구조로 확장해 실제 API 흐름과 연결한다.

## 여기서 남는 질문
이 문단은 단순한 회고가 아니라, 다음 프로젝트로 넘어갈 때 무엇을 들고 가야 하는지 짚어 두는 자리다.

이 메모리 모델은 소박하지만, 보안 거버넌스가 어떤 record와 상태 전이를 필요로 하는지 정확히 보여 준다. 그래서 capstone에서는 이 구조를 DB와 API로 옮겨도 개념이 흐려지지 않았다.
