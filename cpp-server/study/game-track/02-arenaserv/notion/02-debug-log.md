# arenaserv 디버그 노트

이 문서는 현재 구현 기준으로, 네트워크와 authoritative simulation이 만나는 지점에서 특히 숨기 쉬운 실패 지점을 다시 정리한 백업 노트다. 더 긴 기록은 [../notion-archive/](../notion-archive/)에 남겨 두었다.

## 사례 1. engine 이벤트가 다음 tick까지 밀리는 문제

### 증상

`QUEUE`나 `READY` 직후 바로 와야 할 `ROOM` 또는 `COUNTDOWN`이 즉시 보이지 않고, 다음 tick 이후에 몰려오는 것처럼 보인다.

### 왜 위험한가

MatchEngine 내부에서는 상태가 이미 바뀌었는데, 소켓으로 이벤트를 flush하는 시점이 늦으면 테스트도 사용자 경험도 모두 흔들린다. 서버는 바뀌었다고 생각하고 클라이언트는 모르는 상태가 잠시 생긴다.

### 지금 확인할 파일

- [../cpp/src/Server.cpp](../cpp/src/Server.cpp)
- [../cpp/tests/test_arenaserv.py](../cpp/tests/test_arenaserv.py)

현재 구현을 읽을 때는 "tick 때만 이벤트를 비우는가, state mutation 직후에도 비우는가"를 구분해서 보는 것이 중요하다.

## 사례 2. disconnect 뒤 token과 fd 매핑이 엉키는 문제

### 증상

rejoin은 성공한 것처럼 보이는데, 이후 이벤트가 이전 fd로 가거나 현재 소켓에 도달하지 않는다.

### 왜 위험한가

reconnect 설계의 핵심은 token ownership과 socket ownership의 분리다. disconnect 뒤 이전 fd 매핑이 남아 있으면 이 경계가 바로 무너진다.

### 지금 확인할 파일

- [../cpp/src/Server.cpp](../cpp/src/Server.cpp)
- [../cpp/tests/test_arenaserv.py](../cpp/tests/test_arenaserv.py)

현재 smoke test는 within-grace rejoin과 expired rejoin을 모두 확인한다. 둘 다 통과해야 설계가 살아 있다고 볼 수 있다.

## 사례 3. room state machine 일부만 보고 전체를 안심하는 문제

### 증상

2인 duel만 통과하면 room state machine 전체도 괜찮다고 생각하기 쉽다.

### 왜 위험한가

실제 상태 전이는 2인 승리만으로 끝나지 않는다. 3인, 4인, room overflow, draw timeout은 서로 다른 경계를 검증한다. 하나만 보면 나머지 실패 모드가 그대로 숨는다.

### 지금 확인할 파일

- [../cpp/tests/test_arenaserv.py](../cpp/tests/test_arenaserv.py)
- [../cpp/src/MatchEngine.cpp](../cpp/src/MatchEngine.cpp)

## 다시 막히면 따를 순서

1. state mutation 직후 이벤트 flush가 되는지 본다.
2. disconnect와 rejoin 사이에 token, fd 매핑이 일관적인지 본다.
3. 2인, 3인, 4인, draw 시나리오가 모두 커버되는지 본다.
