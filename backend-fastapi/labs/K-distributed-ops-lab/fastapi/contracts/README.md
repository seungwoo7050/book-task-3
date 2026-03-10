# 이벤트 / HTTP 계약

## HTTP 계약

- public API는 gateway 기준으로 `/api/v1/auth/*`, `/api/v1/platform/*`를 유지합니다.
- 내부 인증 계약은 `identity-service`의 `/api/v1/internal/auth/*`입니다.
- 내부 워크스페이스 계약은 `workspace-service`의 `/api/v1/internal/*`입니다.
- 내부 알림 계약은 `notification-service`의 `/api/v1/internal/notifications/*`입니다.

## 이벤트 계약

- `comment.created.v1`
  - source: `workspace-service`
  - sink: `notification-service`
  - transport: Redis Streams
- `invite.accepted.v1`
  - 이 학습 버전에서는 문서만 고정하고 실제 발행은 v2 후속 확장 대상으로 남깁니다.
