# arenaserv — 디버그 기록: 이벤트 flush, fd 매핑, room overflow

작성일: 2026-03-09

## 문제 1: room event가 즉시 클라이언트에게 전달되지 않았다

### 어떻게 발견했는가

smoke test에서 `QUEUE` 명령을 보낸 직후 `ROOM arena-1 lobby`를 기다리는데, 기대한 응답이 제시간에 오지 않는 경우가 있었다. 서버 로그를 보면 MatchEngine 내부에서는 `ROOM` 이벤트가 이미 생성되어 있었지만, 클라이언트의 소켓에는 아직 쓰이지 않은 상태였다.

### 무엇이 문제였는가

`MatchEngine`은 이벤트를 내부 큐(`events_`)에 쌓는다. 이 큐는 `drain_events()`를 호출해야 비워진다. 처음 구현에서는 `drain_events()`를 **tick advance 시에만** 호출했다. 즉, `QUEUE`나 `READY` 같은 state mutation이 일어나도, 다음 tick(최대 100ms 후)까지 이벤트가 발송되지 않았다.

100ms가 짧아 보이지만, smoke test에서 `recv_until`의 타임아웃이 짧으면 간헐적으로 실패하거나, 여러 이벤트가 한 번에 밀려와서 순서가 꼬여 보일 수 있다.

### 무엇을 했는가

state mutation 직후에도 `dispatch_engine_events()`를 호출하게 했다. 구체적으로, `process_input()`에서 `HELLO`, `QUEUE`, `READY`, `REJOIN`, `LEAVE` 같은 명령을 처리한 직후에 `dispatch_engine_events()`를 호출한다. 이렇게 하면 이벤트가 다음 tick을 기다리지 않고 즉시 소켓으로 전달된다.

`dispatch_engine_events()`는 MatchEngine의 `drain_events()`를 호출하고, 각 이벤트의 scope(Room vs Single)에 따라 해당하는 클라이언트의 send buffer에 쓴 뒤 `sendq`에 등록한다.

### 검증

smoke test에서 `QUEUE` 직후 `ROOM arena-1 lobby`, `READY` 직후 `COUNTDOWN 3`이 즉시 도착하는 것을 확인했다.

## 문제 2: disconnect 후 rejoin 대상의 fd 매핑이 남아 있었다

### 어떻게 발견했는가

within-grace rejoin 테스트에서, 재접속한 클라이언트에게 이벤트가 올 때 있고 안 올 때 있었다. 디버깅해보니, 끊어진 연결의 이전 fd가 `token_to_fd` 맵에 남아 있어서, 서버가 이벤트를 이전 fd(이미 닫힌 소켓)에 쓰려고 시도하는 경우가 있었다.

### 무엇이 문제였는가

`disconnect()` 함수에서 소켓을 닫고 `clients` 맵에서 제거하는 것은 했지만, `token_to_fd` 맵에서 해당 token의 fd 매핑을 제거하지 않았다. 그래서 `dispatch_engine_events()`가 token으로 fd를 찾을 때 이미 닫힌 fd를 얻는 것이다.

### 무엇을 했는가

`disconnect()`에서 두 가지를 함께 처리하도록 수정했다:

1. `engine.disconnect_player(token)` — MatchEngine에 연결 끊김을 알린다
2. `token_to_fd.erase(token)` — fd 매핑을 제거한다

이렇게 하면 rejoin 시 새로운 fd가 `token_to_fd`에 깨끗하게 등록된다.

### 검증

within-grace rejoin과 expired rejoin을 둘 다 smoke test에 넣어 확인했다. within-grace에서는 `WELCOME <token>`이 오고, expired에서는 `ERROR expired_session`이 온다.

## 문제 3: 4인 로비의 overflow가 검증되지 않았다

### 어떻게 발견했는가

3인과 4인 lobby 테스트를 작성하고 나서, "5번째 플레이어가 QUEUE하면 어떻게 되는가?"를 확인하지 않았다는 것을 깨달았다. 이건 코드 버그가 아니라 **테스트 커버리지 부족**이다.

### 무엇을 했는가

`scenario_party_lobby()` 함수에서 `size == 4`일 때 추가 client(overflow)를 하나 더 연결하고, `QUEUE`를 보내면 `ERROR room_full`이 반환되는지 확인하는 케이스를 추가했다.

MatchEngine에서 `room_order_.size() >= max_players`일 때 `room_full` 에러를 반환하는 로직은 이미 있었다(ticklab에서 구현). 빠진 것은 이 경로를 네트워크 레벨에서 검증하는 테스트였다.

### 검증

`scenario_party_lobby(server_path, base_port + 2, 4)` 시나리오에서 5번째 client가 `ERROR room_full`을 수신하는 것을 확인했다.
