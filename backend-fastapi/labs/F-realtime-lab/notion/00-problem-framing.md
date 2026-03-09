# WebSocket과 Presence: 실시간을 직접 만들어 보기

## 왜 이 문제를 만들었는가

REST API는 "클라이언트가 요청하면 서버가 응답한다"는 한 방향이다.
하지만 채팅, 알림, 협업 편집 같은 기능은 서버가 먼저 메시지를 보내야 한다.
WebSocket은 이 양방향 통신의 가장 기본적인 프로토콜이지만,
HTTP와 겹쳐 보이면서도 전혀 다른 생명주기를 가진다.

F-realtime-lab은 WebSocket 연결 관리, 실시간 알림 전송,
presence(온라인 상태) 추적을 직접 구현해 보며
"상태가 있는 연결"이 HTTP의 "상태 없는 요청"과 어떻게 다른지 체험하는 랩이다.

## 어떤 상황을 기대하는가

- 클라이언트가 WebSocket으로 연결하면 서버가 연결을 유지한다.
- HTTP POST로 알림을 보내면 해당 사용자의 WebSocket에 메시지가 전달된다.
- heartbeat API를 호출하면 사용자의 last_seen이 갱신된다.
- TTL(1초)이 지나면 presence가 만료되어 offline으로 판정된다.
- 잘못된 token으로 WebSocket 연결을 시도하면 1008 코드로 즉시 끊긴다.

## 제약과 경계

| 항목 | 선택 |
|------|------|
| 프레임워크 | FastAPI (Starlette WebSocket) |
| 연결 저장소 | 인메모리 dict (ConnectionManager) |
| Presence 저장소 | 인메모리 dict (PresenceTracker) |
| DB | 없음 — PostgreSQL, Alembic 불필요 |
| Redis | compose에 포함되지만 핵심 기능이 의존하지 않음 |
| TTL | 1초 (테스트 편의) |
| 인증 | token == user_id (학습용 최소 검증) |

## 불확실한 것

- 단일 프로세스 인메모리 구조이므로, 스케일아웃 시 Redis pub/sub 같은
  cross-process 통신이 필요하다. 이 랩에서는 다루지 않는다.
- presence TTL 1초는 테스트 편의를 위한 값이다.
  프로덕션에서는 30~60초가 일반적이다.
- WebSocket 인증을 query parameter token으로 하는 것은
  학습 목적이며, 실제로는 JWT 검증이 필요하다.
