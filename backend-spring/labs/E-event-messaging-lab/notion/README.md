# E-event-messaging-lab 학습 노트 가이드

이 폴더는 outbox 중심 이벤트 랩을 설계하고 문서화한 과정을 기록한 공개 학습 노트 세트다.

## 먼저 읽을 문서

1. [00-problem-framing.md](00-problem-framing.md): 왜 request-response를 넘어 event boundary를 따로 다루는가
2. [05-development-timeline.md](05-development-timeline.md): outbox record와 publish 흐름을 어떤 순서로 만들었는가
3. [01-approach-log.md](01-approach-log.md): outbox를 먼저 택한 이유와 버린 선택지

## 목적별 읽기

- "Kafka를 쓴다"는 표현의 과장을 어떻게 다뤘는지 보려면 [02-debug-log.md](02-debug-log.md)
- outbox, DLQ, idempotency 개념을 복습하려면 [04-knowledge-index.md](04-knowledge-index.md)
- 현재 한계와 다음 개선을 보려면 [03-retrospective.md](03-retrospective.md)

## 문서 목록

- `00-problem-framing.md`: 문제 정의와 성공 기준
- `01-approach-log.md`: 선택지 비교와 최종 방향
- `02-debug-log.md`: 실패와 문서화 교정 기록
- `03-retrospective.md`: 강점, 약점, 다음 단계
- `04-knowledge-index.md`: 재사용 개념과 참고 자료
- `05-development-timeline.md`: 재현 가능한 개발 순서 기록
