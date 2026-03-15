# 09 Exception and Evidence Manager 근거 정리

이 문서는 "예외를 관리한다"는 설명을 실제 데이터 경계로 바꿔 놓기 위한 메모다. 이번 lab은 상태가 단순해 보이지만, 무엇이 suppression 조건이고 무엇이 단순 기록인지 구분해 읽지 않으면 실제 의미가 흐려진다.

## Phase 1. exception, evidence, audit를 처음부터 분리된 record로 잡았다

- 당시 목표: finding 거버넌스를 mute flag가 아니라 추적 가능한 레코드 집합으로 바꾼다.
- 핵심 근거:
  - `ExceptionRecord`는 `scope_type`, `scope_id`, `reason`, `expires_at`, `approved_by`, `status`를 가진다.
  - `Evidence`는 `finding_id`, `title`, `uri`, `added_at`을 가진다.
  - `AuditEvent`는 `event_type`, `entity_id`, `created_at`, `payload`를 가진다.
  - `create_exception()`은 예외를 만들자마자 `exception.created` audit event를 append 한다.
- 재실행:
  - `PYTHONPATH=/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/09-exception-and-evidence-manager/python/src /Users/woopinbell/work/book-task-3/bithumb/.venv/bin/python -m exception_evidence_manager.cli`
- 검증 신호:
  - CLI demo는 `exception_id`, `approved_status`, `evidence_id`, `audit_event_count`를 한 번에 출력했다.
  - `audit_event_count`는 demo happy path에서 `3`이었다.
- 해석:
  - 이 lab의 시작점은 suppression 로직이 아니라, 나중에 설명 가능한 governance record를 먼저 나누는 데 있다.

## Phase 2. suppression은 승인과 만료를 통과해야만 생긴다

- 당시 목표: 예외가 존재하는 것과 실제로 finding을 억제하는 것을 분리한다.
- 핵심 근거:
  - `create_exception()`이 만든 record의 초기 상태는 `pending`
  - `approve_exception()` 이후에만 `status='approved'`, `approved_by=<name>`이 된다
  - `is_suppressed()`는 `status == 'approved'`이면서 `expires_at > current`인 record만 본다
- 재실행:
  - `PYTHONPATH=/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/09-exception-and-evidence-manager/python/src /Users/woopinbell/work/book-task-3/bithumb/.venv/bin/python - <<'PY'`
  - `from exception_evidence_manager.manager import ExceptionManager`
  - `m = ExceptionManager()`
  - `r = m.create_exception('finding', 'shared-1', 'temp exception', 7)`
  - `print('pending_suppressed', m.is_suppressed('shared-1'))`
  - `m.approve_exception(r.id, 'security.manager')`
  - `print('approved_suppressed', m.is_suppressed('shared-1'))`
  - `PY`
- 검증 신호:
  - `pending_suppressed False`
  - `approved_suppressed True`
  - pytest의 `test_exception_suppresses_scope_until_expiry()`는 만료 후 `False`까지 고정한다
- 해석:
  - 이 모델에서 suppression은 예외 존재 여부가 아니라, 승인과 시간 조건을 모두 통과한 상태다.

## Phase 3. append-only audit는 남지만, suppression key는 아직 좁다

- 당시 목표: governance 흐름의 이력을 append-only로 남기되, 현재 key semantics도 분명히 본다.
- 핵심 근거:
  - `approve_exception()`은 기존 record를 새 record로 교체하고 `exception.approved` audit event를 추가한다.
  - `append_evidence()`는 evidence를 list에 append 하고 `evidence.added` audit event를 남긴다.
  - `_append_event()`는 모든 이벤트를 list append-only로 기록한다.
  - `is_suppressed()`는 `scope_id`만 비교하고 `scope_type`은 비교하지 않는다.
- 추가 재실행:
  - 서로 다른 `scope_type`이지만 같은 `scope_id='shared-1'`인 예외 두 개를 승인한 뒤 `is_suppressed('shared-1')`를 확인했다.
- 검증 신호:
  - `exception_count 2`
  - `audit_types ['exception.created', 'exception.approved', 'exception.created', 'exception.approved']`
  - `suppressed_same_scope_id True`
- 해석:
  - 현재 suppression key는 사실상 `scope_id` 단일 축이다. 그래서 `finding/shared-1`과 `image/shared-1`을 별개로 다루는 정교한 모델은 아직 아니다.
- 추가 관찰:
  - `evidence.added` 이벤트의 `entity_id`는 evidence 레코드 ID가 아니라 finding ID다. 감사 흐름은 남지만, evidence entity 자체를 중심으로 역추적하는 구조는 아직 약하다.

## 이번 Todo에서 남긴 한계

- 저장소가 메모리뿐이라 프로세스가 끝나면 상태가 사라진다.
- suppression 판정이 `scope_id`에만 의존한다.
- revoke, renew, partial scope 같은 거버넌스 동작은 아직 없다.
- 외부 티켓 시스템, approver directory, immutable store는 연결되지 않았다.
