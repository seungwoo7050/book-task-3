# 09 Exception and Evidence Manager 구조 메모

## 이번 문서의 중심
- 예외를 mute 플래그가 아니라 governance record 집합으로 설명한다.
- 서사는 `record 분리 -> suppression 조건 -> audit와 key 한계` 순서로 둔다.
- happy path만 쓰지 않고 `scope_id` 단일 key라는 현재 경계를 같이 남긴다.

## 먼저 붙들 소스
- `../../../01-cloud-security-core/09-exception-and-evidence-manager/README.md`
- `../../../01-cloud-security-core/09-exception-and-evidence-manager/problem/README.md`
- `../../../01-cloud-security-core/09-exception-and-evidence-manager/python/README.md`
- `../../../01-cloud-security-core/09-exception-and-evidence-manager/docs/concepts/governance-flow.md`
- `../../../01-cloud-security-core/09-exception-and-evidence-manager/python/src/exception_evidence_manager/manager.py`
- `../../../01-cloud-security-core/09-exception-and-evidence-manager/python/src/exception_evidence_manager/cli.py`
- `../../../01-cloud-security-core/09-exception-and-evidence-manager/python/tests/test_manager.py`

## 본문 배치
- 도입
  - finding suppression을 bool이 아니라 거버넌스 기록 문제로 재정의한다.
- Phase 1
  - exception/evidence/audit dataclass와 demo JSON 출력을 먼저 보여 준다.
- Phase 2
  - `pending -> approved`, expiry, `is_suppressed()`를 중심으로 suppression 조건을 설명한다.
- Phase 3
  - append-only audit와 `scope_id` 단일 key 한계를 함께 다룬다.
- 마무리
  - persistence, revoke/renew, richer identity model이 아직 없다는 점을 정리한다.

## 꼭 남길 검증 신호
- CLI demo의 `approved_status=approved`, `audit_event_count=3`
- pytest `2 passed in 0.01s`
- 보조 재실행에서 `pending_suppressed False`, `approved_suppressed True`
- 서로 다른 `scope_type`이어도 같은 `scope_id`면 suppression이 묶이는 현재 semantics

## 탈락 기준
- exception을 단순 mute처럼 설명하면 안 된다.
- evidence/audit를 장식처럼 취급하면 안 된다.
- `scope_type` 미사용 같은 현재 한계를 빼면 문서가 너무 깨끗해진다.
