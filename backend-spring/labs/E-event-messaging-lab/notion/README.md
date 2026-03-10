# E-event-messaging-lab — Notion 문서 가이드

이 폴더는 E-event-messaging-lab의 개발 과정과 설계 결정을 기록한 문서 모음이다. request-response만으로 끝나지 않는 서비스에서 이벤트를 어떻게 안전하게 다루는지, outbox 패턴을 중심으로 탐구한 과정을 담고 있다.

## 문서 구성

| 순번 | 문서 | 핵심 질문 |
|------|------|-----------|
| 00 | [Problem Framing](00-problem-framing.md) | 왜 request-response를 넘어서야 하고 무엇을 다루는가? |
| 01 | [Approach Log](01-approach-log.md) | 왜 Outbox를 먼저 배우는 방향을 택했는가? |
| 02 | [Debug Log](02-debug-log.md) | "Kafka를 쓴다"는 표현이 만드는 과장을 어떻게 잡았는가? |
| 03 | [Retrospective](03-retrospective.md) | Outbox에서 무엇을 배웠고 무엇이 아직 부족한가? |
| 04 | [Knowledge Index](04-knowledge-index.md) | Outbox, DLQ, Idempotency 등 재사용 가능한 개념은? |
| 05 | [Timeline](05-timeline.md) | 소스 코드에서 보이지 않는 개발 과정은? |

## 목적별 읽기 가이드

### "이 프로젝트가 뭔지 빠르게 알고 싶다"
→ [00-problem-framing.md](00-problem-framing.md)의 "이 랩이 존재하는 이유"와 "구체적으로 무엇을 다루는가" 섹션을 읽는다.

### "Outbox 패턴이 왜 필요한지 알고 싶다"
→ [04-knowledge-index.md](04-knowledge-index.md)의 "Outbox 패턴" 섹션에서 개념을 이해하고, [01-approach-log.md](01-approach-log.md)의 "영속성 선택" 섹션에서 코드 구현을 확인한다.

### "Kafka가 compose에 있는데 왜 실제로 안 쓰는 건지 궁금하다"
→ [02-debug-log.md](02-debug-log.md)에서 keyword inflation 문제를 다루고 있다. [00-problem-framing.md](00-problem-framing.md)의 "의도적으로 다루지 않는 것들"에서 현재 범위의 한계를 명시한다.

### "이벤트의 PENDING → PUBLISHED 흐름을 따라가고 싶다"
→ [05-timeline.md](05-timeline.md)의 Phase 4에서 `emitOrderPlaced()`와 `publishPending()` 구현 과정을, Phase 7에서 테스트 시나리오의 3단계 흐름을 확인한다.

### "Outbox와 Event Sourcing의 차이가 궁금하다"
→ [04-knowledge-index.md](04-knowledge-index.md)의 "Event Sourcing과의 차이" 섹션을 읽는다.

### "이 프로젝트를 처음부터 따라 만들고 싶다"
→ [05-timeline.md](05-timeline.md)를 Phase 1부터 순서대로 따라간다.

### "면접에서 이 프로젝트를 설명하고 싶다"
→ [03-retrospective.md](03-retrospective.md)에서 "나아진 점"(Kafka를 handoff boundary로 바라보게 됨)과 "아직 약한 점"(long-running publisher 없음, DLQ 미구현)을 중심으로 준비한다.

## 관련 문서

- [docs/README.md](../docs/README.md) — 현재 구현 범위와 단순화, 다음 개선 방향
- [problem/README.md](../problem/README.md) — 한 줄 문제 정의
- [spring/README.md](../spring/README.md) — 빌드, 실행, 테스트 명령어
