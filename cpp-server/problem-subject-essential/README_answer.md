# cpp-server 서버 개발 필수 답안지

이 문서는 `cpp-server` 필수 문제의 해답을 실제 C++ 소스와 테스트만으로 읽히게 정리한 답안지다. 핵심은 "연결과 이벤트를 어떤 런타임으로 다룰 것인가"와 "한 줄 메시지를 어떤 경계로 파싱할 것인가"를 추상 설명이 아니라 코드 구조로 바로 재구성할 수 있게 만드는 데 있다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [01-eventlab-cpp](01-eventlab-cpp_answer.md) | 시작 위치의 구현을 완성해 지정한 포트에서 listening socket을 연다, 여러 클라이언트를 accept하고 read/write 이벤트를 처리한다, 줄 단위 텍스트 프로토콜에서 PING <token>에 PONG <token>으로 응답한다를 한 흐름으로 설명하고 검증한다. 핵심은 main 흐름을 구현하고 테스트를 통과시키는 것이다. | `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/shared-core/01-eventlab/cpp test` |
| [02-msglab-cpp](02-msglab-cpp_answer.md) | 시작 위치의 구현을 완성해 \r\n 또는 \n 경계를 기준으로 메시지를 분리한다, optional prefix를 인식한다, command token을 대문자로 정규화한다를 한 흐름으로 설명하고 검증한다. 핵심은 main이 요구하는 동작을 source에 반영하는 것이다. | `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/shared-core/02-msglab/cpp test` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
