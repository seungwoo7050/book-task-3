# roomlab 개념 노트

## 먼저 잡아야 할 질문

- registration 완료 전과 후의 command surface는 왜 달라져야 하는가
- room membership을 서버 전역과 connection 로컬에 동시에 기록해야 하는 이유는 무엇인가
- `QUIT`과 네트워크 disconnect를 같은 경로로 보면 어떤 정리 버그가 생기는가

## 코드 읽기 포인트

- [../cpp/src/Connection.cpp](../cpp/src/Connection.cpp): 사용자별 상태
- [../cpp/src/Executor.cpp](../cpp/src/Executor.cpp): PASS, NICK, USER, PRIVMSG, NOTICE
- [../cpp/src/execute_join.cpp](../cpp/src/execute_join.cpp): JOIN/PART와 room membership
- [../cpp/tests/test_roomlab.py](../cpp/tests/test_roomlab.py): multi-client 검증

## 흔한 오해

- IRC subset 서버라고 해서 상태 머신이 단순한 것은 아니다.
- room membership은 채널 컨테이너 하나만 고치면 끝나지 않는다.
- smoke test가 작아 보여도 registration과 cleanup을 함께 검증하면 충분히 강하다.

## 다음 단계로 이어지는 지점

`roomlab`까지 읽었다면 이제 IRC 축의 capstone으로 올라갈 준비가 됐다. 고급 channel command를 보고 싶다면 [../ircserv/README.md](../ircserv/README.md)를 보면 된다.
