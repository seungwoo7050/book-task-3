# Distance-Vector Routing

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 distance-vector 라우팅 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 |
| 정식 검증 | `make -C study/Network-Diagnostics-and-Routing/routing/problem test` |

## 한 줄 요약

Bellman-Ford 식을 분산 라우팅 테이블 갱신으로 옮기는 시뮬레이션 과제입니다.

## 왜 이 프로젝트가 필요한가

진단 도구 이후에 네트워크 경로 계산 원리를 알고리즘 수준에서 다루는 단계로 자연스럽게 이어집니다.

## 이런 학습자에게 맞습니다

- 라우팅 프로토콜의 핵심 식이 실제 테이블 갱신으로 어떻게 이어지는지 보고 싶은 학습자
- 수렴과 next hop 계산을 시뮬레이션으로 이해하고 싶은 학습자

## 지금 바로 읽는 순서

1. `problem/README.md` - 구현 목표, 제공 자료, 성공 기준을 먼저 확인합니다.
2. `python/README.md` - 공개 구현 범위와 정식 검증 명령을 확인합니다.
3. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.
4. `notion/README.md` - 더 깊은 작업 기록과 회고가 필요할 때 참고합니다.

## 제공 자료

- `problem/code/dv_skeleton.py`: 시작용 skeleton 코드
- `problem/data/topology.json`: 기본 3노드 토폴로지
- `problem/data/topology_5node.json`: 확장 5노드 토폴로지
- `problem/script/test_routing.sh`: 정식 검증 스크립트

## 실행과 검증

- 실행: `make -C study/Network-Diagnostics-and-Routing/routing/problem run-solution`
- 검증: `make -C study/Network-Diagnostics-and-Routing/routing/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 학습 포인트

- Bellman-Ford update 식
- 2-phase synchronous simulation
- 수렴 판정
- next hop과 cost를 함께 관리하는 방법

## 현재 한계

- poisoned reverse는 구현하지 않았습니다.
- 동적 토폴로지 변화 실험은 포함하지 않습니다.
- 비동기 메시지 모델은 구현하지 않습니다.

## 포트폴리오로 확장하기

- 토폴로지 시각화나 라우팅 테이블 변화 애니메이션을 추가하면 발표력이 크게 좋아집니다.
- link cost 변화와 count-to-infinity를 후속 실험으로 붙이면 알고리즘 이해가 더 잘 드러납니다.
- deterministic simulation을 채택한 이유를 설명하면 테스트 설계 관점도 보여 줄 수 있습니다.
