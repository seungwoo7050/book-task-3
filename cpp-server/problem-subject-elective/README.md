# cpp-server 서버 개발 비필수 문제지

여기서 `비필수`는 중요하지 않다는 뜻이 아니라, 서버 공통 필수보다 특정 프로토콜이나 authoritative game loop 문맥 의존성이 더 강하다는 뜻입니다.
이 트랙의 종합 과제는 [`../problem-subject-capstone/README.md`](../problem-subject-capstone/README.md)로 분리합니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [01-roomlab-cpp](01-roomlab-cpp.md) | 시작 위치의 구현을 완성해 PASS, NICK, USER 기반 등록을 처리한다, JOIN, PART로 room create, join, leave를 처리한다, PRIVMSG, NOTICE를 전달한다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/irc-track/01-roomlab/cpp test` |
| [01-ticklab-cpp](01-ticklab-cpp.md) | 시작 위치의 구현을 완성해 room queue와 ready 기반 countdown을 처리한다, monotonic input sequence를 검증한다, fixed tick마다 state를 advance하고 snapshot을 생성한다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/game-track/01-ticklab/cpp test` |
| [02-rollbacklab-cpp](02-rollbacklab-cpp.md) | headless simulation만으로 rollback을 설명하는 프로젝트다. 여기서 핵심은 "입력이 늦게 도착했을 때 어느 시점으로 되돌아가야 하는가"이지, 서버 소켓을 여는 것이 아니다. | `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/game-track/02-rollbacklab/cpp test` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
