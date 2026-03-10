# ircserv 디버그 노트

이 문서는 현재 구현 기준으로, advanced IRC command를 붙일 때 특히 흔들리기 쉬운 실패 지점을 다시 정리한 백업 노트다. 더 긴 기록은 [../notion-archive/](../notion-archive/)에 남겨 두었다.

## 사례 1. KICK 뒤 target 쪽 membership 정리가 남는 문제

### 증상

KICK 자체는 성공한 것처럼 보이는데, 이후 target이 자기 로컬 상태에서는 아직 채널에 있는 것처럼 행동한다.

### 왜 위험한가

channel 쪽 membership과 connection 쪽 membership이 어긋나면, 이후 재입장, PART, QUIT cleanup에서 버그가 연쇄적으로 드러난다. 이 문제는 "KICK 이벤트가 나갔다"는 사실만 보면 놓치기 쉽다.

### 지금 확인할 파일

- [../cpp/src/Channel.cpp](../cpp/src/Channel.cpp)
- [../cpp/src/Executor.cpp](../cpp/src/Executor.cpp)
- [../cpp/tests/test_irc_join.py](../cpp/tests/test_irc_join.py)

현재 smoke test는 KICK 이후 bob의 재입장이 invite-only 규칙으로 정확히 거절되는지 본다. 이 시나리오가 cleanup 일관성을 간접적으로 확인한다.

## 사례 2. INVITE 직후 JOIN이 간헐적으로 흔들리는 문제

### 증상

초대는 받은 것처럼 보이는데, 초대받은 사용자의 JOIN이 간헐적으로 실패하거나 타이밍에 따라 흔들린다.

### 왜 이런 일이 생기기 쉬운가

INVITE 이벤트가 소켓에 도착한 시점과, 서버 내부 상태가 다음 명령을 처리할 준비가 끝난 시점은 테스트에서 쉽게 헷갈린다. 네트워크 smoke test에서는 작은 타이밍 차이도 불안정성으로 보일 수 있다.

### 지금 확인할 파일

- [../cpp/tests/test_irc_join.py](../cpp/tests/test_irc_join.py)
- [../cpp/src/Executor.cpp](../cpp/src/Executor.cpp)

현재 테스트는 INVITE를 받은 뒤 짧은 지연을 두고 JOIN을 보낸다. 운영 수준의 동기화는 아니지만, smoke test 안정화 관점에서는 이유가 있는 선택이다.

## 사례 3. 하위 lab에서 고친 parser 경계가 capstone에 반영되지 않는 문제

### 증상

`msglab`이나 `roomlab`에서 이미 정리한 parser, validation, cleanup 버그가 capstone에서 다시 튀어나온다.

### 왜 위험한가

이 capstone의 정체성은 통합이다. 하위 lab에서 확인한 수정이 여기서 빠지면, 커리큘럼이 한 층씩 좋아진다는 믿음이 무너진다.

### 지금 확인할 파일

- [../cpp/src/Executor.cpp](../cpp/src/Executor.cpp)
- [../cpp/src/Server.cpp](../cpp/src/Server.cpp)
- [../cpp/tests/test_irc_join.py](../cpp/tests/test_irc_join.py)

## 다시 막히면 따를 순서

1. channel state가 어떤 명령으로 바뀌는지 본다.
2. 명령 이후 membership cleanup이 양쪽 구조에 반영되는지 본다.
3. registration과 광고 메시지 순서를 본다.
4. 하위 lab에서 이미 해결한 문제인지 먼저 비교한다.
