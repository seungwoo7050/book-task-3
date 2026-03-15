# cpp-server 서버 개발 필수 문제지

`cpp-server`는 저수준 TCP 서버 학습 트랙이라, 서버 공통 필수 기준으로 남길 수 있는 문제가 비교적 분명합니다.
여기서는 특정 프로토콜이나 게임 규칙보다, 서버 런타임과 메시지 경계를 직접 설명하게 만드는 문제만 남깁니다.
이 트랙의 종합 과제는 [`../problem-subject-capstone/README.md`](../problem-subject-capstone/README.md)로 분리합니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [01-eventlab-cpp](01-eventlab-cpp.md) | 시작 위치의 구현을 완성해 지정한 포트에서 listening socket을 연다, 여러 클라이언트를 accept하고 read/write 이벤트를 처리한다, 줄 단위 텍스트 프로토콜에서 PING <token>에 PONG <token>으로 응답한다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/shared-core/01-eventlab/cpp test` |
| [02-msglab-cpp](02-msglab-cpp.md) | 시작 위치의 구현을 완성해 \r\n 또는 \n 경계를 기준으로 메시지를 분리한다, optional prefix를 인식한다, command token을 대문자로 정규화한다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/shared-core/02-msglab/cpp test` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
