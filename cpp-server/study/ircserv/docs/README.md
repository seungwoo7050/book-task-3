# ircserv 개념 노트

## 먼저 잡아야 할 질문

- capstone은 왜 새 기능을 많이 붙이는 프로젝트가 아니라, 앞선 경계를 다시 합치는 프로젝트여야 하는가
- `MODE`와 `INVITE`는 왜 channel state와 privilege model을 함께 건드리는가
- 최소한의 `CAP` 지원이 client compatibility에 어떤 차이를 만드는가

## 코드 읽기 포인트

- [../cpp/src/Executor.cpp](../cpp/src/Executor.cpp): advanced command 경로
- [../cpp/src/Channel.cpp](../cpp/src/Channel.cpp): privilege와 mode state
- [../cpp/tests/test_irc_join.py](../cpp/tests/test_irc_join.py): capstone 검증 시나리오

## 흔한 오해

- capstone은 단순히 더 큰 서버를 만드는 단계가 아니다.
- `CAP`는 부가 기능이라 없어도 된다고 보기 쉽지만, 호환성 설명에서 중요한 근거가 된다.
- IRC 서버 문서가 친절하려면 RFC 나열보다 “왜 여기까지 구현했는가”가 더 중요하다.

## 다음 단계로 이어지는 지점

IRC 축을 마쳤다면, 같은 저장소에서 authoritative game server가 어떻게 별도 capstone이 되는지 [../arenaserv/README.md](../arenaserv/README.md)와 비교해서 읽어 보면 좋다.
