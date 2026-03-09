# 지식 인덱스: 실시간 통신 패턴 정리

## WebSocket 기본 개념

HTTP와의 차이:
| 항목 | HTTP | WebSocket |
|------|------|-----------|
| 연결 | 요청마다 새로 (keep-alive 제외) | 한 번 연결, 계속 유지 |
| 방향 | 클라이언트 → 서버 | 양방향 |
| 상태 | stateless | stateful (연결 자체가 상태) |
| 종료 | 응답 완료 시 | close frame 교환 |

Starlette의 `WebSocket` 객체:
- `await ws.accept()`: handshake 완료
- `await ws.send_json(data)`: JSON 전송
- `await ws.receive_text()`: 텍스트 수신 (blocking)
- `await ws.close(code=1008)`: 서버 측 종료

## ConnectionManager 패턴

```python
class ConnectionManager:
    _connections: dict[str, set[WebSocket]]
    
    def connect(user_id, ws): ...    # set에 추가
    def disconnect(user_id, ws): ... # set에서 제거 + empty set 정리
    def send_to_user(user_id, data): ...  # fan-out
```

핵심:
- user_id → set으로 다중 디바이스 지원
- disconnect 시 빈 set 삭제 → 메모리 누수 방지
- app.state에 저장해서 라우터 간 공유

## Presence 추적

```python
class PresenceTracker:
    _presence: dict[str, float]  # user_id → last_seen timestamp
    
    def heartbeat(user_id): ...  # 현재 시각으로 갱신
    def is_online(user_id): ...  # now - last_seen < ttl
```

설계 결정:
- TTL 기반 만료: 마지막 heartbeat로부터 TTL 이내면 online
- 별도 cleanup 없이 조회 시점에 판정 (lazy expiry)
- 인메모리이므로 프로세스 재시작 시 전체 초기화

프로덕션 확장:
- Redis SETEX로 key 저장 → TTL 자동 만료
- sorted set + score(timestamp)로 범위 조회 가능

## WebSocket 인증 패턴

이 랩에서: `ws://host/ws/notifications/{user_id}?token=xxx`
- token == user_id이면 통과
- 아니면 close(1008) — Policy Violation

프로덕션에서:
- Cookie에 JWT를 담거나, 첫 메시지로 JWT를 보내는 방식
- query param에 token을 넣으면 URL 로그에 노출될 수 있다
- WebSocket은 CORS가 적용되지 않으므로 Origin 검증이 필요

## WebSocket Close Codes

| 코드 | 의미 |
|------|------|
| 1000 | 정상 종료 |
| 1001 | Going Away (서버 셧다운 등) |
| 1008 | Policy Violation (인증 실패) |
| 1011 | Internal Error |

## HTTP + WebSocket 이중 표면 패턴

```
Client A ──POST /notifications──→ FastAPI
                                      │
                                      ↓ ConnectionManager.send_to_user
Client B ←──WebSocket message────── (user_id's websockets)
```

장점: REST API의 인증/검증 인프라를 그대로 활용하면서
실시간 전달만 WebSocket으로 處理한다.

## 용어 정리

| 용어 | 의미 |
|------|------|
| presence | 사용자의 온라인/오프라인 상태 |
| heartbeat | 클라이언트가 주기적으로 보내는 "아직 살아있다" 신호 |
| TTL | Time To Live — heartbeat 없이 online으로 간주하는 최대 시간 |
| fan-out | 한 메시지를 여러 수신자에게 동시 전달 |
| close frame | WebSocket 종료를 위한 프로토콜 메시지 |

## 참고 자료

| 제목 | 출처 | 확인 | 비고 |
|------|------|------|------|
| Starlette WebSocket docs | starlette.io | 2025-01 | accept/send/close API |
| RFC 6455 (WebSocket Protocol) | IETF | 2025-01 | close code 정의 |
| WebSocket Security (OWASP) | owasp.org | 2025-01 | Origin 검증, token 노출 |
