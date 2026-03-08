# Traceroute

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 레거시 원본 | `legacy/Wireshark-Labs/ip-icmp + legacy/Programming-Assignments/icmp-pinger + 신규 보강 프로젝트` |
| 정식 검증 | `make -C study/Network-Diagnostics-and-Routing/traceroute/problem test` |

## 한 줄 요약

TTL 증가와 ICMP Time Exceeded를 이용해 hop-by-hop 경로를 드러내는 bridge project다.

## 문제 요약

UDP probe를 점점 큰 TTL로 보내고, raw ICMP socket으로 Time Exceeded와 Port Unreachable을 받아 각 hop의 응답 시간과 주소를 출력한다.

## 이 프로젝트를 여기 둔 이유

ICMP pinger와 routing 사이에서, 패킷 수준 TTL 개념이 실제 경로 탐색 도구로 어떻게 연결되는지 보여준다.

## 제공 자료

- `problem/code/traceroute_skeleton.py` 신규 skeleton
- `python/src/traceroute.py` 구현
- `python/tests/test_traceroute.py` 비권한 parser + synthetic route tests

## 학습 포인트

- TTL과 ICMP Time Exceeded의 연결
- embedded UDP port를 이용한 probe 매칭
- live probing과 synthetic integration test 분리
- destination 도달 조건으로 Port Unreachable 사용

## 실행과 검증

- 실행: `make -C study/Network-Diagnostics-and-Routing/traceroute/problem run-client HOST=8.8.8.8`
- 검증: `make -C study/Network-Diagnostics-and-Routing/traceroute/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 현재 범위와 한계

비권한 테스트가 parser/formatter와 synthetic hop discovery까지 검증한다. live hop trace는 수동 재현 명령으로 남기되, 완료 상태는 deterministic test 기준으로 판단한다.

- 현재 한계: IPv6 traceroute 미지원
- 현재 한계: DNS reverse lookup 미포함
- 현재 한계: ECMP/비대칭 경로 같은 실제 인터넷 변동성은 모델링하지 않음

## Public / Private 경계

- `problem/`은 제공 자료와 canonical 검증 래퍼만 둔다.
- `python/` 또는 `analysis/`는 공개 구현과 공개 답안만 둔다.
- `docs/`는 반복해서 참고할 개념 메모만 유지한다.
- `notion/`은 노션 업로드용 작업 노트이며 저장소 공개 구조에 의존하지 않는다.
