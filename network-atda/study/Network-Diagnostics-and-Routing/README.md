# Network Diagnostics and Routing

ICMP 기반 진단 도구와 라우팅 알고리즘을 한 축으로 묶은 트랙이다.

## 왜 이 트랙인가

패킷 수준 진단에서 경로 계산까지 자연스럽게 이어지는 bridge를 제공한다.

## 프로젝트 순서

1. [ICMP Pinger](icmp-pinger/README.md) - `verified`
   핵심: Raw socket으로 ICMP Echo Request/Reply를 직접 구현하는 진단 도구 과제다.
2. [Traceroute](traceroute/README.md) - `verified`
   핵심: TTL 증가와 ICMP Time Exceeded를 이용해 hop-by-hop 경로를 드러내는 bridge project다.
3. [Distance-Vector Routing](routing/README.md) - `verified`
   핵심: Bellman-Ford 식을 분산 라우팅 테이블 갱신으로 옮기는 시뮬레이션 과제다.

## 공통 규칙

- 코드 과제는 `problem/`과 `python/`을 분리한다.
- 패킷 분석 랩은 `problem/`과 `analysis/`를 분리한다.
- 시행착오와 회고는 `notion/`으로 밀어내고, 공개 README는 인덱스 역할만 맡긴다.
