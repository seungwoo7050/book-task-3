# Traceroute

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | ICMP/TTL 학습을 실제 경로 추적 도구로 연결하기 위해 이 저장소에서 직접 보강한 bridge 프로젝트 |
| 정식 검증 | `make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem test` |

## 문제가 뭐였나
- 문제 배경: ICMP/TTL 학습을 실제 경로 추적 도구로 연결하기 위해 이 저장소에서 직접 보강한 bridge 프로젝트
- 이 단계에서의 역할: `ICMP Pinger`와 `routing` 사이에서, 패킷 수준 TTL 개념이 실제 경로 탐색 도구로 어떻게 이어지는지 분명하게 보여 줍니다.

## 제공된 자료
- `problem/code/traceroute_skeleton.py`: 시작용 skeleton 코드
- `python/src/traceroute.py`: 현재 공개 구현
- `python/tests/test_traceroute.py`: 비권한 parser + synthetic route 테스트

## 이 레포의 답
- 한 줄 답: TTL 증가와 `ICMP Time Exceeded`를 이용해 hop-by-hop 경로를 드러내는 bridge 프로젝트입니다.
- 공개 답안 위치: `python/src/`
- 보조 공개 표면: `python/tests/`
- 보조 공개 표면: `docs/`
- 읽는 순서:
  1. `problem/README.md` - 문제 조건, 제공 자료, 성공 기준을 먼저 확인합니다.
  2. `python/README.md` - 현재 공개 답안 범위와 기준 명령을 확인합니다.
  3. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.
  4. `notion/README.md` - 공개 학습 노트이지만 엔트리포인트는 아닙니다.

## 어떻게 검증하나
- 실행: `make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem run-client HOST=8.8.8.8`
- 검증: `make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 무엇을 배웠나
- TTL과 `ICMP Time Exceeded`의 연결
- embedded UDP port를 이용한 probe 매칭
- live probing과 synthetic integration test 분리
- 목적지 도달을 `Port Unreachable`로 판정하는 규칙

## 현재 한계
- IPv6 traceroute는 지원하지 않습니다.
- DNS reverse lookup은 포함하지 않습니다.
- ECMP나 비대칭 경로 같은 실제 인터넷 변동성은 모델링하지 않습니다.
