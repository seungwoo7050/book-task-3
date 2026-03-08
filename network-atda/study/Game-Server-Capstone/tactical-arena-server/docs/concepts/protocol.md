# Protocol

## TCP control channel

형식은 한 줄 끝에 `\n`이 붙는 `VERB key=value ...` 프로토콜이다.

### client commands

- `LOGIN name=<player_name>`
- `LIST_ROOMS`
- `CREATE_ROOM name=<room_name> max=<2|3|4>`
- `JOIN_ROOM room=<room_id>`
- `LEAVE_ROOM`
- `READY value=<0|1>`
- `RESUME token=<resume_token>`
- `UDP_BIND match=<match_id> nonce=<u32>`
- `PING`

### server events

- `LOGIN_OK player=<player_id> token=<resume_token> wins=<n> losses=<n> kills=<n> deaths=<n>`
- `ROOM_LIST rooms=<room_id:name:cur:max,...>`
- `ROOM_UPDATE room=<room_id> owner=<player_id> roster=<player_id:ready,...>`
- `MATCH_START match=<match_id> udp_port=<port> tick_hz=20 snapshot_hz=10 spawn=<x:y>`
- `MATCH_RESULT winner=<player_id> scoreboard=<player_id:kills:deaths,...>`
- `PONG ts=<server_ms>`
- `ERROR code=<slug> message=<slug>`

## UDP gameplay channel

공통 header:

- `version:uint8`
- `kind:uint8`
- `reserved:uint16`
- `match_id:uint32`
- `player_id:uint32`
- `sequence:uint32`

packet kinds:

- `INPUT`
  `move_x:int8`, `move_y:int8`, `aim_x:int16`, `aim_y:int16`, `fire:uint8`, `dash:uint8`
- `SNAPSHOT`
  `server_tick:uint32`, `entity_count:uint8`, `projectile_count:uint8`, `entities[]`
- `HEARTBEAT`
  header only

## 현재 정책

- TCP는 authoritative control source다.
- UDP는 unreliable 그대로 두고 custom reliable layer는 만들지 않는다.
- 입력 `sequence`가 역전되면 오래된 입력은 무시한다.
- snapshot은 full-state 전송이라 일부 손실을 허용한다.
- `UDP_BIND nonce`는 v1에서 endpoint arming 확인용으로만 쓰고, 강한 증명 절차는 구현하지 않았다.
