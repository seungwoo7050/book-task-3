# traceroute 문제지

## 왜 중요한가

이 문서는 Traceroute를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 구현 세부와 공개 구현 경로는 상위 프로젝트 README가 연결하는 경로를 따라가면 됩니다.

## 목표

시작 위치의 구현을 완성해 TTL 처리: TTL 증가에 따라 hop을 순서대로 드러냅니다, ICMP 파싱: Time Exceeded와 Port Unreachable을 구분합니다, Probe 매칭: 응답과 probe를 정확히 연결합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/04-Network-Diagnostics-and-Routing/traceroute/problem/code/traceroute_skeleton.py`
- `../study/04-Network-Diagnostics-and-Routing/traceroute/python/src/traceroute.py`
- `../study/04-Network-Diagnostics-and-Routing/traceroute/python/tests/test_traceroute.py`
- `../study/04-Network-Diagnostics-and-Routing/traceroute/problem/Makefile`

## starter code / 입력 계약

- ../study/04-Network-Diagnostics-and-Routing/traceroute/problem/code/traceroute_skeleton.py에서 starter 코드와 입력 경계를 잡는다.

## 핵심 요구사항

- TTL 처리: TTL 증가에 따라 hop을 순서대로 드러냅니다.
- ICMP 파싱: Time Exceeded와 Port Unreachable을 구분합니다.
- Probe 매칭: 응답과 probe를 정확히 연결합니다.
- 출력 형식: hop 주소와 지연을 읽기 쉽게 정리합니다.
- 검증 구조: live run과 deterministic test의 역할을 분리합니다.

## 제외 범위

- `../study/04-Network-Diagnostics-and-Routing/traceroute/problem/code/traceroute_skeleton.py` starter skeleton을 정답 구현으로 착각하지 않는다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- `../study/04-Network-Diagnostics-and-Routing/traceroute/problem/code/traceroute_skeleton.py`의 빈 확장 지점을 실제 구현으로 채웠다.
- 핵심 흐름은 `ProbeObservation`와 `build_probe_port`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `_build_icmp_packet`와 `test_build_probe_port_increments_per_hop_and_probe`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `make -C /Users/woopinbell/work/book-task-3/network-atda/study/04-Network-Diagnostics-and-Routing/traceroute/problem test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/network-atda/study/04-Network-Diagnostics-and-Routing/traceroute/problem test
```

- `traceroute`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`traceroute_answer.md`](traceroute_answer.md)에서 확인한다.
