# network-atda 종합 과제 문제지

`network-atda` capstone은 앞선 소켓, 전송, 분석, 진단 과제를 하나의 authoritative 서버 프로젝트로 다시 묶게 만드는 종합 과제입니다.

## Capstone

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [tactical-arena-server](tactical-arena-server.md) | 시작 위치의 구현을 완성해 기능 통합: TCP/UDP 분리, authoritative simulation, reconnect, persistence가 하나의 서버로 통합됩니다, 재현성: make test 한 번으로 unit + integration + load smoke를 재현합니다, 설명 가능성: 문제 정의, 설계, 검증, 한계를 문서로 설명할 수 있습니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/05-Game-Server-Capstone/tactical-arena-server/problem test` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
