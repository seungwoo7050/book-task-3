# Core Concepts

## 핵심 개념

- organization이 tenant boundary이고, role은 membership에 붙는다.
- access token은 짧게, refresh token은 회전시키며 Redis에 필수 상태를 둔다.
- write flow는 issue/comment 이벤트를 outbox에 남기고 worker가 notification으로 변환한다.
- dashboard summary는 org 단위 aggregate이며 Redis 캐시 miss 또는 장애 시 DB로 fallback 한다.
- 대표작의 검증 가치는 API 문서, e2e, smoke가 같이 돌아갈 때 생긴다.

## Trade-offs

- refresh session을 Postgres와 Redis에 같이 두면 운영 설명은 좋아지지만 cross-store consistency가 복잡해진다.
- notification worker를 별도 프로세스로 분리하면 구조는 분명해지지만 로컬 검증 절차가 늘어난다.
- dashboard를 org-wide summary로 제한해야 Redis 캐시 키를 단순하게 유지할 수 있다.

## 실패하기 쉬운 지점

- projectID와 issueID 경로에서 조직 경계를 역추적하지 않으면 tenant boundary가 무너진다.
- refresh rotation은 Redis 실패와 DB 기록 실패를 같은 오류로 다루면 디버깅이 어렵다.
- idempotency key를 단순 unique로만 쓰면 동일 키의 다른 payload 충돌을 설명하기 어렵다.
