# Distance-Vector Routing

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 레거시 원본 | `legacy/Programming-Assignments/routing` |
| 정식 검증 | `make -C study/Network-Diagnostics-and-Routing/routing/problem test` |

## 한 줄 요약

Bellman-Ford 식을 분산 라우팅 테이블 갱신으로 옮기는 시뮬레이션 과제다.

## 문제 요약

각 노드는 이웃의 distance vector를 받아 자신의 최소 비용을 갱신하고, 더 이상 변경이 없으면 수렴으로 판단한다.

## 이 프로젝트를 여기 둔 이유

진단 도구 이후에 네트워크 경로 계산 원리를 알고리즘 수준에서 다루는 단계로 적합하다.

## 제공 자료

- `problem/code/dv_skeleton.py` skeleton
- `problem/data/topology*.json` 토폴로지
- `problem/script/test_routing.sh` 검증

## 학습 포인트

- Bellman-Ford update 식
- 2-phase synchronous simulation
- 수렴 판정
- next hop과 cost를 함께 관리하는 법

## 실행과 검증

- 실행: `make -C study/Network-Diagnostics-and-Routing/routing/problem run-solution`
- 검증: `make -C study/Network-Diagnostics-and-Routing/routing/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 현재 범위와 한계

기본 DV 알고리즘에 집중한다. poisoned reverse와 동적 링크 변동은 문서 수준 보강에 머문다.

- 현재 한계: poisoned reverse 미구현
- 현재 한계: 동적 토폴로지 실험 부재
- 현재 한계: 비동기 메시지 모델 미구현

## Public / Private 경계

- `problem/`은 제공 자료와 canonical 검증 래퍼만 둔다.
- `python/` 또는 `analysis/`는 공개 구현과 공개 답안만 둔다.
- `docs/`는 반복해서 참고할 개념 메모만 유지한다.
- `notion/`은 노션 업로드용 작업 노트이며 저장소 공개 구조에 의존하지 않는다.
