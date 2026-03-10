# 접근 기록: 인메모리 실시간 서버 설계

## 처음 본 선택지들

실시간 기능을 구현하는 방법은 여러 가지가 있었다.

**1) Server-Sent Events (SSE)**
서버→클라이언트 단방향만 필요하면 SSE가 단순하다.
하지만 양방향 통신과 presence를 함께 다루려면 부족하다.

**2) Redis pub/sub + WebSocket**
다중 프로세스 환경에서는 필수적이지만,
단일 프로세스 학습 랩에서는 인프라 복잡도만 올라간다.

**3) 인메모리 ConnectionManager + WebSocket**
가장 단순하고, WebSocket 프로토콜 자체에 집중할 수 있다.
스케일 한계가 명확하지만, 학습 목적에는 최적이다.

세 번째 방식을 선택했다.

## 핵심 설계 결정

### ConnectionManager

`dict[str, set[WebSocket]]` 구조다.
한 사용자가 여러 탭/디바이스에서 접속할 수 있으므로 user_id → set으로 관리한다.

- `connect(user_id, ws)`: set에 추가
- `disconnect(user_id, ws)`: set에서 제거, empty면 key 삭제
- `send_to_user(user_id, data)`: 해당 user의 모든 WebSocket에 JSON 전송

`app.state`에 인스턴스를 저장해서 라우터에서 접근한다.

### PresenceTracker

`dict[str, float]` — user_id → last_seen timestamp.

- `heartbeat(user_id)`: 현재 시각으로 갱신
- `is_online(user_id)`: `now - last_seen < ttl`이면 online

TTL은 Settings의 `presence_ttl_seconds`로 설정하며, 기본값은 1초다.
테스트에서 `time.sleep(1.1)` 후 offline이 되는지 검증한다.

### WebSocket 인증

연결 시 `?token=` query parameter를 확인한다.
token이 user_id와 일치하면 인증 통과, 아니면 `close(code=1008)`.
이것은 학습용 최소 인증이며, 프로덕션에서는 JWT 검증으로 대체해야 한다.

### HTTP + WebSocket 이중 표면

알림 전송은 HTTP POST `/notifications`로 받아서
ConnectionManager를 통해 WebSocket으로 fan-out한다.
이 구조는 "HTTP로 쓰고, WebSocket으로 읽는다"는 패턴을 보여준다.

## 버린 아이디어

- Redis pub/sub 기반 구현은 이 랩의 범위를 넘긴다고 판단했다.
  다중 프로세스 시나리오는 capstone에서 고려할 수 있다.
- socket.io 라이브러리 사용은 Starlette 네이티브 WebSocket을 직접
  다루는 학습 가치를 없앤다고 판단했다.
- DB에 presence를 저장하는 방식은 쓰기 빈도 대비 과도하다.
