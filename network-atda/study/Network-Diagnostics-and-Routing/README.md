# Network Diagnostics and Routing

ICMP 기반 진단 도구와 라우팅 알고리즘을 한 축으로 묶어, 패킷 관찰에서 경로 계산까지 연결하는 트랙입니다.

## 이 트랙이 맡는 역할

네트워크 계층을 "패킷을 읽는 대상"에서 끝내지 않고, 실제 진단 도구와 분산 라우팅 알고리즘으로 이어 줍니다. 실습 간 연결 고리가 분명한 편입니다.

## 추천 선수 지식

- IP, ICMP, TTL 같은 네트워크 계층 기본 용어
- Python 소켓 프로그래밍 기초
- 권한이 필요한 raw socket 실행과 비권한 테스트를 구분해 읽을 준비

## 권장 프로젝트 순서

1. [ICMP Pinger](icmp-pinger/README.md) - `verified`
   ICMP Echo Request/Reply를 직접 만들어 RTT와 손실을 측정합니다.
2. [Traceroute](traceroute/README.md) - `verified`
   TTL 증가와 ICMP Time Exceeded를 이용해 hop-by-hop 경로를 드러냅니다.
3. [Distance-Vector Routing](routing/README.md) - `verified`
   Bellman-Ford 식을 distance-vector 시뮬레이션으로 옮겨 수렴 과정을 확인합니다.

## 공통 읽기 방법

- `problem/README.md`로 문제의 네트워크 동작을 먼저 파악합니다.
- `python/README.md`에서 live 실행과 deterministic 검증의 경계를 확인합니다.
- `docs/README.md`에서 RFC/알고리즘 배경을 보강합니다.
- `notion/README.md`는 디버그와 회고를 추적하고 싶을 때만 읽으면 됩니다.

## 포트폴리오로 확장하기

- 실제 네트워크 환경에서 결과가 왜 흔들리는지와, 저장소에서는 왜 deterministic test를 기준으로 삼는지 함께 설명하세요.
- ICMP pinger, traceroute, routing을 하나의 "진단과 경로 이해" 스토리로 묶으면 레포 구조가 더 설득력 있어집니다.
- 시연 캡처를 추가한다면 raw socket 권한, 방화벽, DNS reverse lookup 같은 현실 제약도 함께 적어 두는 편이 좋습니다.
