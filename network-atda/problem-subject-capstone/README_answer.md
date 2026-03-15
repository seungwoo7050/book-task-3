# network-atda 종합 과제 답안지

이 문서는 network-atda capstone의 공식 답을 source-first로 정리한 답안지다. authoritative simulation, protocol, persistence, bot/load harness가 어떤 파일에서 만나는지 바로 읽게 한다.

## Capstone

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [tactical-arena-server](tactical-arena-server_answer.md) | 시작 위치의 구현을 완성해 기능 통합: TCP/UDP 분리, authoritative simulation, reconnect, persistence가 하나의 서버로 통합됩니다, 재현성: make test 한 번으로 unit + integration + load smoke를 재현합니다, 설명 가능성: 문제 정의, 설계, 검증, 한계를 문서로 설명할 수 있습니다를 한 흐름으로 설명하고 검증한다. 핵심은 send_line와 parse_args, trace_enabled 흐름을 구현하고 테스트를 통과시키는 것이다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/05-Game-Server-Capstone/tactical-arena-server/problem test` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
