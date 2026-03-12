# commerce-backend-v2 학습 노트 가이드

이 폴더는 대표 capstone을 설계하고 디버깅하고 재검증한 과정을 기록한 공개 학습 노트 세트다.

## 먼저 읽을 문서

1. [00-problem-framing.md](00-problem-framing.md): baseline을 같은 도메인에서 더 깊게 구현해야 했던 이유
2. [05-development-timeline.md](05-development-timeline.md): schema, Compose, 테스트를 어떤 순서로 쌓았는지
3. [01-approach-log.md](01-approach-log.md): modular monolith 유지, selective Redis, outbox handoff 선택의 근거

## 목적별 읽기

- schema/entity mismatch나 placeholder 실패 같은 실제 문제를 보려면 [02-debug-log.md](02-debug-log.md)
- refresh token hashing, optimistic locking, idempotency key, outbox pattern을 복습하려면 [04-knowledge-index.md](04-knowledge-index.md)
- 지금 강한 점과 아직 남은 약점을 보려면 [03-retrospective.md](03-retrospective.md)

## 문서 목록

- `00-problem-framing.md`: 문제 정의와 성공 기준
- `01-approach-log.md`: 선택지 비교와 최종 방향
- `02-debug-log.md`: 주요 실패와 수정 근거
- `03-retrospective.md`: 강점, 약점, 다음 단계
- `04-knowledge-index.md`: 재사용 개념과 참고 자료
- `05-development-timeline.md`: 재현 가능한 개발 순서 기록
