# Traceroute

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | ICMP/TTL 학습을 실제 경로 추적 도구로 연결하기 위해 이 저장소에서 직접 보강한 bridge 프로젝트 |
| 정식 검증 | `make -C study/Network-Diagnostics-and-Routing/traceroute/problem test` |

## 한 줄 요약

TTL 증가와 `ICMP Time Exceeded`를 이용해 hop-by-hop 경로를 드러내는 bridge 프로젝트입니다.

## 왜 이 프로젝트가 필요한가

`ICMP Pinger`와 `routing` 사이에서, 패킷 수준 TTL 개념이 실제 경로 탐색 도구로 어떻게 이어지는지 분명하게 보여 줍니다.

## 이런 학습자에게 맞습니다

- `TTL`과 `ICMP Time Exceeded`가 어떻게 traceroute가 되는지 구현 수준에서 보고 싶은 학습자
- live probing과 synthetic test를 구분하는 설계를 배우고 싶은 학습자

## 지금 바로 읽는 순서

1. `problem/README.md` - 구현 목표, 제공 자료, 성공 기준을 먼저 확인합니다.
2. `python/README.md` - 공개 구현 범위와 정식 검증 명령을 확인합니다.
3. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.
4. `notion/README.md` - 더 깊은 작업 기록과 회고가 필요할 때 참고합니다.

## 제공 자료

- `problem/code/traceroute_skeleton.py`: 시작용 skeleton 코드
- `python/src/traceroute.py`: 현재 공개 구현
- `python/tests/test_traceroute.py`: 비권한 parser + synthetic route 테스트

## 실행과 검증

- 실행: `make -C study/Network-Diagnostics-and-Routing/traceroute/problem run-client HOST=8.8.8.8`
- 검증: `make -C study/Network-Diagnostics-and-Routing/traceroute/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 학습 포인트

- TTL과 `ICMP Time Exceeded`의 연결
- embedded UDP port를 이용한 probe 매칭
- live probing과 synthetic integration test 분리
- 목적지 도달을 `Port Unreachable`로 판정하는 규칙

## 현재 한계

- IPv6 traceroute는 지원하지 않습니다.
- DNS reverse lookup은 포함하지 않습니다.
- ECMP나 비대칭 경로 같은 실제 인터넷 변동성은 모델링하지 않습니다.

## 포트폴리오로 확장하기

- reverse DNS, 여러 probe 평균 RTT, Paris traceroute 비교를 추가하면 포트폴리오 가치가 크게 올라갑니다.
- live 네트워크 결과가 환경에 따라 달라질 수 있다는 점을 테스트 정책과 함께 설명하세요.
- hop별 응답 시간을 표나 그래프로 정리하면 시각적으로 전달력이 좋아집니다.
