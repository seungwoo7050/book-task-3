# cpp-server 서버 캡스톤 답안지

이 문서는 `cpp-server` 캡스톤 문제의 해답을 실제 C++ 소스와 테스트만으로 읽히게 정리한 답안지다. 정답의 기준은 "기능이 많다"가 아니라, 앞선 shared core와 elective 규칙들을 하나의 실제 서버 프로세스 안에서 끝까지 연결하는 데 있다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [02-ircserv-cpp](02-ircserv-cpp_answer.md) | 시작 위치의 구현을 완성해 roomlab 범위의 core command를 유지한다, CAP LS 302, TOPIC, MODE, KICK, INVITE를 추가한다, registration 과정에서 005 ISUPPORT를 광고한다를 한 흐름으로 설명하고 검증한다. 핵심은 _do_leaks 흐름을 구현하고 테스트를 통과시키는 것이다. | `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/irc-track/02-ircserv/cpp test` |
| [03-arenaserv-cpp](03-arenaserv-cpp_answer.md) | 시작 위치의 구현을 완성해 HELLO, QUEUE, READY, INPUT, PING, REJOIN, LEAVE를 처리한다, WELCOME, ROOM, COUNTDOWN, SNAPSHOT, HIT, ELIM, ROUND_END, ERROR를 보낸다, x20 bounded tile arena, 2~4인 room, HP 3, 단일 action FIRE 규칙을 유지한다를 한 흐름으로 설명하고 검증한다. 핵심은 main 흐름을 구현하고 테스트를 통과시키는 것이다. | `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/game-track/03-arenaserv/cpp test` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
