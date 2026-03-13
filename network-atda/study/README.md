# study/ 안내

`study/`는 이 저장소의 실제 학습 트리다. 최상위는 학습 단계 기준으로 정렬하고, 각 단계 안에서 프로젝트 README가 `문제 -> 답 -> 검증` 계약을 반복한다.

## 단계 인덱스

| 단계 | 핵심 질문 | 프로젝트 수 | 시작점 |
| :--- | :--- | :--- | :--- |
| [`01. Application Protocols and Sockets`](01-Application-Protocols-and-Sockets/README.md) | 소켓 위에서 애플리케이션 규칙을 직접 구현하면 어떤 계약이 드러나는가 | `4` | [`Web Server`](01-Application-Protocols-and-Sockets/web-server/README.md) |
| [`02. Reliable Transport`](02-Reliable-Transport/README.md) | ACK, checksum, timer, sliding window가 신뢰 전송을 어떻게 만드는가 | `2` | [`RDT Protocol`](02-Reliable-Transport/rdt-protocol/README.md) |
| [`03. Packet Analysis Top-Down`](03-Packet-Analysis-Top-Down/README.md) | 패킷 trace만으로 무엇을 근거 있게 설명할 수 있는가 | `7` | [`HTTP Packet Analysis`](03-Packet-Analysis-Top-Down/http/README.md) |
| [`04. Network Diagnostics and Routing`](04-Network-Diagnostics-and-Routing/README.md) | ICMP, TTL, Bellman-Ford가 진단 도구와 라우팅 알고리즘으로 어떻게 이어지는가 | `3` | [`ICMP Pinger`](04-Network-Diagnostics-and-Routing/icmp-pinger/README.md) |
| [`05. Game Server Capstone`](05-Game-Server-Capstone/README.md) | 앞선 학습을 하나의 설명 가능한 서버 프로젝트로 어떻게 통합할 것인가 | `1` | [`Tactical Arena Server`](05-Game-Server-Capstone/tactical-arena-server/README.md) |

## 읽는 순서

1. 단계 README에서 왜 이 순서로 배우는지 확인합니다.
2. 프로젝트 README에서 `문제가 뭐였나`, `이 레포의 답`, `어떻게 검증하나`를 먼저 확인합니다.
3. `problem/README.md`로 제공 자료와 성공 기준을 읽습니다.
4. 구현형 과제는 `python/README.md` 또는 `cpp/README.md`, 분석형 과제는 `analysis/README.md`로 내려갑니다.
5. 소스 기준의 개발 흐름을 따라가고 싶다면 `blog/README.md`와 프로젝트별 blog 문서를 읽습니다.
6. 개념 복습이 필요할 때만 `docs/README.md`를, 추가 노트가 필요할 때만 `notion/README.md`를 읽습니다.
