# 04. Network Diagnostics and Routing

ICMP 기반 진단 도구와 distance-vector routing 구현으로 네트워크 계층 감각을 확장하는 단계입니다.

## 프로젝트 카탈로그

| 프로젝트 | 문제 | 이 레포의 답 | 검증 | 상태 | 왜 이 단계에 있는가 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`ICMP Pinger`](icmp-pinger/README.md) | `Computer Networking: A Top-Down Approach`의 ICMP ping 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 | `python/src/` | `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test` | `verified` | 응용 계층 소켓 과제보다 한 단계 아래로 내려가 IP/ICMP 레벨에서 무엇이 직접 보이는지 체감하게 합니다. |
| [`Traceroute`](traceroute/README.md) | ICMP/TTL 학습을 실제 경로 추적 도구로 연결하기 위해 이 저장소에서 직접 보강한 bridge 프로젝트 | `python/src/` | `make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem test` | `verified` | `ICMP Pinger`와 `routing` 사이에서, 패킷 수준 TTL 개념이 실제 경로 탐색 도구로 어떻게 이어지는지 분명하게 보여 줍니다. |
| [`Distance-Vector Routing`](routing/README.md) | `Computer Networking: A Top-Down Approach`의 distance-vector 라우팅 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 | `python/src/` | `make -C study/04-Network-Diagnostics-and-Routing/routing/problem test` | `verified` | 진단 도구 이후에 네트워크 경로 계산 원리를 알고리즘 수준에서 다루는 단계로 자연스럽게 이어집니다. |

## 공통 읽기 순서

1. 프로젝트 README에서 문제, 답, 검증 명령을 먼저 확인합니다.
2. `problem/README.md`에서 제공 자료와 성공 기준을 확인합니다.
3. 구현형 과제는 `python/README.md` 또는 `cpp/README.md`, 분석형 과제는 `analysis/README.md`로 내려갑니다.
4. `docs/README.md`는 개념을 다시 확인할 때만 참고하고, `notion/README.md`는 보조 기록으로만 읽습니다.
