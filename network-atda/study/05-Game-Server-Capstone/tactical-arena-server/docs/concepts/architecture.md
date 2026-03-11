# Architecture

## 목표 구조

서버는 단일 프로세스로 실행되지만, 내부 역할은 세 부분으로 나눈다.

- `TCP Control Gateway`
  로그인, 방 생성/참가, ready, reconnect, `MATCH_START`/`MATCH_RESULT` 같은 제어 흐름을 처리한다.
- `UDP Gameplay Gateway`
  입력 datagram을 받아 match state에 반영하고, snapshot을 각 플레이어 endpoint로 전송한다.
- `Match Engine`
  room 단위 authoritative state를 fixed tick으로 진행하고, projectile, respawn, forfeit, score 계산을 수행한다.

## 동시성 모델

- 프로세스 전체는 `Boost.Asio io_context + 고정 thread pool`로 돈다.
- TCP 세션마다 strand를 두어 read/write queue 경쟁을 막는다.
- room 단위 상태 변경은 room strand에서만 수행한다.
- SQLite 공유 연결은 repository 내부 mutex로 직렬화한다.

이 구조의 핵심은 "match state를 여기저기서 lock으로 공유하지 않는다"는 점이다. room owner execution context를 하나 두고, 바깥에서는 메시지만 전달한다.

## room lifecycle

1. host가 `CREATE_ROOM`으로 room을 연다.
2. joiner가 `JOIN_ROOM`으로 들어온다.
3. room 인원이 `max_players`를 채우고 전원이 `READY=1`이 되면 match를 시작한다.
4. match는 room strand에서 fixed tick으로 진행된다.
5. 종료 시 `MATCH_RESULT`를 브로드캐스트하고 SQLite에 결과를 반영한 뒤 room을 정리한다.

## 왜 이 구조인가

- TCP/UDP 분리를 공개 문서와 테스트에서 설명하기 쉽다.
- authoritative simulation, reconnect, persistence를 한 프로세스에서 검증할 수 있다.
- room strand와 per-session strand를 함께 쓰면 레이스 원인을 비교적 좁은 범위에서 통제할 수 있다.
