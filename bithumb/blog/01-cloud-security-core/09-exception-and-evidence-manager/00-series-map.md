# 09 Exception and Evidence Manager 읽기 지도

이 lab은 finding 이후의 운영을 "예외를 하나 체크하고 끝"으로 보지 않고, exception, evidence, audit trail을 각각 별도 record로 남기는 작은 거버넌스 모델이다. 읽을 때도 suppression 결과만 보지 말고 `생성 -> 승인 -> 증적 추가 -> 억제 판정`이 어떤 데이터로 나뉘는지를 먼저 붙드는 편이 맞다.

## 먼저 붙들 질문
- 왜 suppression을 boolean 플래그가 아니라 record 집합으로 다뤄야 하는가?
- 언제 예외가 실제로 finding을 억제하고, 언제는 억제하지 못하는가?
- audit trail은 무엇을 entity로 기록하고, 무엇은 아직 분리하지 못하는가?

## 이 글은 이렇게 읽으면 된다
1. `ExceptionRecord`, `Evidence`, `AuditEvent` 세 dataclass를 먼저 본다.
2. `create_exception()`, `approve_exception()`, `append_evidence()`를 본다. 어떤 이벤트가 어떤 순서로 쌓이는지 확인한다.
3. 마지막으로 `is_suppressed()`와 테스트를 본다. approval/expiry가 suppression을 어떻게 결정하는지 확인한다.

## 특히 눈여겨볼 장면
- 예외 생성과 승인, 증적 추가가 각각 별도 audit event를 append 한다.
- `pending` 예외는 존재해도 suppression을 만들지 않는다.
- suppression 판정은 현재 `scope_type`이 아니라 `scope_id`만 본다.
- evidence audit의 `entity_id`는 evidence record ID가 아니라 finding ID라서, evidence entity 자체의 추적 축은 아직 약하다.

## 먼저 열 문서
- [10-development-timeline.md](10-development-timeline.md)

## 이번 문서의 근거
- `README.md`
- `problem/README.md`
- `python/README.md`
- `docs/concepts/governance-flow.md`
- `python/src/exception_evidence_manager/manager.py`
- `python/src/exception_evidence_manager/cli.py`
- `python/tests/test_manager.py`
