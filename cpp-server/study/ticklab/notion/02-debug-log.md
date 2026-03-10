# ticklab 디버그 노트

이 문서는 현재 구현 기준으로, authoritative simulation에서 특히 쉽게 숨어 버리는 실패 지점을 다시 정리한 백업 노트다. 더 긴 기록은 [../notion-archive/](../notion-archive/)에 남겨 두었다.

## 사례 1. stale sequence가 조용히 덮어써지는 문제

### 증상

같은 seq 입력이 다시 들어왔을 때 명시적 에러 없이 마지막 값이 기존 입력을 덮어쓴다.

### 왜 위험한가

이 문제는 "last writer wins"처럼 보이지만 authoritative 서버에서는 위험하다. 이미 처리한 입력이 네트워크 지연 때문에 다시 들어왔을 때, 서버가 그 입력을 다시 반영해 버릴 수 있기 때문이다.

### 지금 확인할 파일

- [../cpp/src/MatchEngine.cpp](../cpp/src/MatchEngine.cpp)
- [../cpp/tests/test_ticklab.cpp](../cpp/tests/test_ticklab.cpp)

현재 테스트는 같은 seq를 두 번 넣었을 때 `stale_sequence`가 나는지 확인한다.

## 사례 2. 재접속은 되지만 현재 상태를 복구하지 못하는 문제

### 증상

rejoin 자체는 성공했는데, 클라이언트가 현재 라운드 상태를 모른 채 돌아온다.

### 왜 위험한가

재접속은 단순히 `connected = true`로 끝나지 않는다. 현재 phase, tick, snapshot이 같이 복구되지 않으면 세션 연속성이 아니라 "다시 붙은 껍데기"만 남는다.

### 지금 확인할 파일

- [../cpp/src/MatchEngine.cpp](../cpp/src/MatchEngine.cpp)
- [../cpp/tests/test_ticklab.cpp](../cpp/tests/test_ticklab.cpp)

테스트는 within-grace rejoin과 expired rejoin을 나눠 확인한다. 이 경계가 흐리면 `arenaserv`에서 더 큰 혼란으로 돌아온다.

## 사례 3. draw timeout이 이벤트 없이 끝나는 문제

### 증상

라운드는 종료되는데 `ROUND_END draw` 같은 종료 이벤트가 누락된다.

### 왜 위험한가

authoritative 엔진에서는 내부 상태 전이만큼 바깥으로 나가는 이벤트 계약도 중요하다. phase는 끝났는데 이벤트가 안 나가면, 나중에 네트워크 서버를 붙였을 때 "서버는 끝났다고 생각하지만 클라이언트는 모르는" 상태가 생긴다.

### 지금 확인할 파일

- [../cpp/src/MatchEngine.cpp](../cpp/src/MatchEngine.cpp)
- [../cpp/tests/test_ticklab.cpp](../cpp/tests/test_ticklab.cpp)

현재 테스트는 `max_round_ticks`까지 진행한 뒤 `ROUND_END draw`가 나오는지 확인한다.

## 다시 막히면 따를 순서

1. phase 전이가 정확한 tick에서 일어나는지 본다.
2. 입력 sequence가 단조 증가 조건을 만족하는지 본다.
3. reconnect 뒤 복구 이벤트가 충분한지 본다.
4. 라운드 종료 시 상태 전이와 이벤트 emit이 함께 일어나는지 본다.
