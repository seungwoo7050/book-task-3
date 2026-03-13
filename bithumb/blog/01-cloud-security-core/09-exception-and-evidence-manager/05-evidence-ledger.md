# 09 Exception and Evidence Manager 근거 정리

finding 이후의 거버넌스를 exception, evidence, audit trail로 분리해 모델링하는 작은 상태 관리기다. 이 문서는 그 흐름을 글로 풀기 전에, 실제 근거를 phase 단위로 다시 세워 둔 정리 노트다.

한 phase를 읽을 때는 `당시 목표 -> 실제 조치 -> CLI -> 검증 신호` 순서로 보면 무엇이 먼저 굳어졌는지 빠르게 따라갈 수 있다.

## Phase 1. 예외와 증적과 감사를 record로 분리했다

이 구간에서는 `예외와 증적과 감사를 record로 분리했다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 1
- 당시 목표: 예외 관리를 단순 플래그가 아니라 추적 가능한 데이터 모델로 바꾼다.
- 변경 단위: `python/src/exception_evidence_manager/manager.py`의 `ExceptionRecord`, `Evidence`, `AuditEvent`, `create_exception`
- 처음 가설: exception이 그냥 boolean이면 만료일, 승인자, 증적, 감사 로그를 설명할 수 없다. record를 분리해야 거버넌스가 된다.
- 실제 조치: `ExceptionRecord`, `Evidence`, `AuditEvent` 세 dataclass를 따로 두고, `ExceptionManager` 내부 저장소도 각각 분리했다. `create_exception`은 record 생성과 동시에 `exception.created` audit event를 남기게 했다.
- CLI:
  - `PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m exception_evidence_manager.cli`
- 검증 신호:
  - CLI 출력에 `exception_id`, `evidence_id`, `audit_event_count`가 모두 나타났다.
  - README가 exception/evidence/audit를 별도 모델의 핵심 범위로 문서화한다.
- 핵심 코드 앵커: `01-cloud-security-core/09-exception-and-evidence-manager/python/src/exception_evidence_manager/manager.py:44-56`
- 새로 배운 것: 예외 관리에서 중요한 것은 “예외가 있는가”보다 “왜 있었고 누가 승인했고 언제 끝나는가”를 설명할 수 있는가다.
- 다음: 이제 예외 승인과 만료를 suppression 판정과 연결해야 했다.

## Phase 2. approval과 expiry를 suppression 판정에 연결했다

이 구간에서는 `approval과 expiry를 suppression 판정에 연결했다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 2
- 당시 목표: 예외가 언제 finding을 실제로 억제하는지 코드로 정의한다.
- 변경 단위: `python/src/exception_evidence_manager/manager.py`의 `approve_exception`, `is_suppressed`
- 처음 가설: 예외가 존재하는 것만으로는 충분하지 않다. 승인되었고 아직 만료되지 않았을 때만 suppression이 성립해야 한다.
- 실제 조치: `approve_exception`은 기존 record를 immutable하게 복사해 `approved_by`와 `status`를 갱신했고, `is_suppressed`는 같은 scope_id에 대해 승인 상태이면서 expiry가 미래인 경우만 True를 반환하게 했다.
- CLI:
  - `PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m pytest 01-cloud-security-core/09-exception-and-evidence-manager/python/tests`
- 검증 신호:
  - pytest가 `2 passed in 0.01s`로 통과했다.
  - `test_exception_suppresses_scope_until_expiry`가 3일짜리 예외는 지금은 suppress하고, 10일 뒤엔 풀려야 한다고 요구한다.
- 핵심 코드 앵커: `01-cloud-security-core/09-exception-and-evidence-manager/python/src/exception_evidence_manager/manager.py:58-92`
- 새로 배운 것: suppression은 영구 mute가 아니라 시간과 승인에 의해 제한되는 상태 전이다.
- 다음: 마지막으로 evidence append와 audit trail이 append-only로 쌓이는지 확인해야 했다.

## Phase 3. evidence append와 append-only audit trail을 잠갔다

이 구간에서는 `evidence append와 append-only audit trail을 잠갔다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 3
- 당시 목표: 예외 흐름의 근거와 변경 이력이 함께 남는지 검증한다.
- 변경 단위: `python/src/exception_evidence_manager/manager.py`의 `append_evidence`, `_append_event`, `python/tests/test_manager.py`
- 처음 가설: 예외 승인만 기록하면 나중에 왜 그런 결정을 했는지 잊는다. evidence와 audit가 함께 쌓여야 거버넌스가 닫힌다.
- 실제 조치: `append_evidence`는 증적 레코드를 추가하면서 `evidence.added` audit event도 남겼다. 테스트는 예외 생성, 승인, 증적 연결까지 세 단계가 지나면 audit event가 정확히 3개가 되어야 한다고 고정했다.
- CLI:
  - `PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m exception_evidence_manager.cli`
  - `PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m pytest 01-cloud-security-core/09-exception-and-evidence-manager/python/tests`
- 검증 신호:
  - CLI가 실제로 `audit_event_count: 3`을 출력했다.
  - 테스트도 첫 audit event가 `exception.created`임을 확인해 append order를 잠갔다.
- 핵심 코드 앵커: `01-cloud-security-core/09-exception-and-evidence-manager/python/tests/test_manager.py:15-22`
- 새로 배운 것: append-only audit trail의 핵심은 수정이 불가능하다는 사실보다, 변화의 순서를 복원할 수 있다는 점이다.
- 다음: capstone에서는 이 모델을 SQLite/PostgreSQL 기반 DB 구조로 확장해 실제 API 흐름과 연결한다.
