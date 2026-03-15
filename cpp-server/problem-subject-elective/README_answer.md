# cpp-server 서버 개발 비필수 답안지

이 문서는 `cpp-server` 비필수 문제의 해답을 실제 C++ 소스와 테스트만으로 읽히게 정리한 답안지다. 공유 코어를 바탕으로 IRC room 운영과 authoritative simulation을 각각 어느 수준까지 확장해야 하는지가 각 행의 핵심이다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [01-roomlab-cpp](01-roomlab-cpp_answer.md) | 시작 위치의 구현을 완성해 PASS, NICK, USER 기반 등록을 처리한다, JOIN, PART로 room create, join, leave를 처리한다, PRIVMSG, NOTICE를 전달한다를 한 흐름으로 설명하고 검증한다. 핵심은 _do_leaks 흐름을 구현하고 테스트를 통과시키는 것이다. | `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/irc-track/01-roomlab/cpp test` |
| [01-ticklab-cpp](01-ticklab-cpp_answer.md) | 시작 위치의 구현을 완성해 room queue와 ready 기반 countdown을 처리한다, monotonic input sequence를 검증한다, fixed tick마다 state를 advance하고 snapshot을 생성한다를 한 흐름으로 설명하고 검증한다. 핵심은 main이 요구하는 동작을 source에 반영하는 것이다. | `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/game-track/01-ticklab/cpp test` |
| [02-rollbacklab-cpp](02-rollbacklab-cpp_answer.md) | headless simulation만으로 rollback을 설명하는 프로젝트다. 여기서 핵심은 "입력이 늦게 도착했을 때 어느 시점으로 되돌아가야 하는가"이지, 서버 소켓을 여는 것이 아니다. 핵심은 main이 요구하는 동작을 source에 반영하는 것이다. | `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/game-track/02-rollbacklab/cpp test` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
