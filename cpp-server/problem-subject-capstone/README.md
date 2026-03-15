# cpp-server 서버 캡스톤 문제지

`cpp-server`의 capstone은 shared-core에서 나눈 런타임과 parser 책임을 각 도메인 서버에 다시 합치면서도, 범위를 설명 가능한 수준으로 유지하게 만드는 종합 과제입니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [02-ircserv-cpp](02-ircserv-cpp.md) | 시작 위치의 구현을 완성해 roomlab 범위의 core command를 유지한다, CAP LS 302, TOPIC, MODE, KICK, INVITE를 추가한다, registration 과정에서 005 ISUPPORT를 광고한다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/irc-track/02-ircserv/cpp test` |
| [03-arenaserv-cpp](03-arenaserv-cpp.md) | 시작 위치의 구현을 완성해 HELLO, QUEUE, READY, INPUT, PING, REJOIN, LEAVE를 처리한다, WELCOME, ROOM, COUNTDOWN, SNAPSHOT, HIT, ELIM, ROUND_END, ERROR를 보낸다, x20 bounded tile arena, 2~4인 room, HP 3, 단일 action FIRE 규칙을 유지한다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/game-track/03-arenaserv/cpp test` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
