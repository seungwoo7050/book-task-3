# 04. Network Diagnostics and Routing blog

이 트랙의 blog 시리즈는 raw socket 기반 진단 도구와 Bellman-Ford 시뮬레이션을 같은 흐름 안에서 복원한다. `problem/Makefile`, solution 코드, 테스트 코드, 개념 문서를 함께 읽으면서 `packet observation -> tool -> algorithm`으로 이어지는 구조를 보여 준다.

## 프로젝트

| 프로젝트 | blog | 원 프로젝트 |
| :--- | :--- | :--- |
| ICMP Pinger | [`README.md`](icmp-pinger/README.md) | [`../../04-Network-Diagnostics-and-Routing/icmp-pinger/README.md`](../../04-Network-Diagnostics-and-Routing/icmp-pinger/README.md) |
| Traceroute | [`README.md`](traceroute/README.md) | [`../../04-Network-Diagnostics-and-Routing/traceroute/README.md`](../../04-Network-Diagnostics-and-Routing/traceroute/README.md) |
| Distance-Vector Routing | [`README.md`](routing/README.md) | [`../../04-Network-Diagnostics-and-Routing/routing/README.md`](../../04-Network-Diagnostics-and-Routing/routing/README.md) |

## 읽는 순서
1. [`ICMP Pinger`](icmp-pinger/README.md)로 checksum, raw socket, echo request/reply를 본다.
2. [`Traceroute`](traceroute/README.md)로 TTL과 `ICMP Time Exceeded`를 경로 추적으로 연결한다.
3. [`Distance-Vector Routing`](routing/README.md)로 경로 계산을 알고리즘 시뮬레이션 수준에서 정리한다.

## source-first 메모
- `ICMP Pinger`, `Traceroute`는 live 명령과 non-privileged test를 분리해서 기록한다.
- `routing`은 JSON topology, `dv_routing.py`, test script, routing table 출력이 핵심 근거다.
- 세 프로젝트 모두 날짜 근거가 약하므로 `Day/Session`으로 chronology를 정리한다.
- 구현 순서는 소스와 테스트가 드러내는 일반적인 개발 흐름으로만 추론한다.
