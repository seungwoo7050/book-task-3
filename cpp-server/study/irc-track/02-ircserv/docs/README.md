# ircserv 개념 메모

이 디렉터리는 capstone에서 무엇을 더했고 무엇을 일부러 남겼는지 정리한다. 핵심은 기능 목록보다 "경계를 다시 합쳤을 때도 설명 가능한가"에 있다.

## 먼저 볼 질문

- roomlab 대비 무엇이 정말 capstone 수준의 추가인가
- privilege와 advanced command를 어디까지 넣어야 설명력이 높아지는가
- `CAP`과 `005 ISUPPORT`는 왜 호환성의 최소 신호인가

## 읽기 포인트

- [../cpp/src/Executor.cpp](../cpp/src/Executor.cpp)
- [../cpp/src/Channel.cpp](../cpp/src/Channel.cpp)
- [../cpp/tests/test_irc_join.py](../cpp/tests/test_irc_join.py)

## 다음 단계

- 다른 축의 capstone은 [../../../game-track/03-arenaserv/README.md](../../../game-track/03-arenaserv/README.md)
