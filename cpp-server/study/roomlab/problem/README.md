# roomlab 문제 재구성

이 문서는 현재 저장소의 구현, 테스트, 보존된 기록을 바탕으로 다시 정리한 학습용 문제 설명이다. 이 lab의 핵심은 “작동하는 작은 IRC subset 서버”를 만드는 것이지, RFC 전체를 한 번에 구현하는 것이 아니다.

## 학습 목표

- registration과 room lifecycle을 실제 TCP 서버 위에서 다룬다.
- room membership과 broadcast가 어떤 인덱스 갱신을 요구하는지 이해한다.
- 네트워크 오류와 사용자 종료가 cleanup 단계에서 어떻게 다른지 구분한다.

## 구현해야 할 것

- `PASS`, `NICK`, `USER` 기반 등록
- `JOIN`, `PART` 기반 room create, join, leave
- `PRIVMSG`, `NOTICE` 전달
- `PING`, `PONG`, `QUIT`과 idle keep-alive 처리
- duplicate nick 거절과 disconnect cleanup

## 산출물

- raw TCP mini IRC room server
- registration, duplicate nick, room broadcast, cleanup smoke test

## 범위에서 제외하는 것

- `TOPIC`, `MODE`, `KICK`, `INVITE`, `CAP`
- TLS, SASL, services
- 게임 관련 command와 state

## 현재 저장소에서 확인할 수 있는 근거

- [../cpp/src/Executor.cpp](../cpp/src/Executor.cpp): core command 처리
- [../cpp/src/execute_join.cpp](../cpp/src/execute_join.cpp): JOIN/PART 흐름
- [../cpp/src/Server.cpp](../cpp/src/Server.cpp): 연결 수명주기와 cleanup
- [../cpp/tests/test_roomlab.py](../cpp/tests/test_roomlab.py): end-to-end smoke test
