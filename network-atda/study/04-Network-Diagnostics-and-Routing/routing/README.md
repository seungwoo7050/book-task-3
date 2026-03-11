# Distance-Vector Routing

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 distance-vector 라우팅 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 |
| 정식 검증 | `make -C study/04-Network-Diagnostics-and-Routing/routing/problem test` |

## 문제가 뭐였나
- 문제 배경: `Computer Networking: A Top-Down Approach`의 distance-vector 라우팅 과제를 현재 저장소 구조에 맞게 정리한 프로젝트
- 이 단계에서의 역할: 진단 도구 이후에 네트워크 경로 계산 원리를 알고리즘 수준에서 다루는 단계로 자연스럽게 이어집니다.

## 제공된 자료
- `problem/code/dv_skeleton.py`: 시작용 skeleton 코드
- `problem/data/topology.json`: 기본 3노드 토폴로지
- `problem/data/topology_5node.json`: 확장 5노드 토폴로지
- `problem/script/test_routing.sh`: 정식 검증 스크립트

## 이 레포의 답
- 한 줄 답: Bellman-Ford 식을 분산 라우팅 테이블 갱신으로 옮기는 시뮬레이션 과제입니다.
- 공개 답안 위치: `python/src/`
- 보조 공개 표면: `python/tests/`
- 보조 공개 표면: `docs/`
- 읽는 순서:
  1. `problem/README.md` - 문제 조건, 제공 자료, 성공 기준을 먼저 확인합니다.
  2. `python/README.md` - 현재 공개 답안 범위와 기준 명령을 확인합니다.
  3. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.
  4. `notion/README.md` - 공개 학습 노트이지만 엔트리포인트는 아닙니다.

## 어떻게 검증하나
- 실행: `make -C study/04-Network-Diagnostics-and-Routing/routing/problem run-solution`
- 검증: `make -C study/04-Network-Diagnostics-and-Routing/routing/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 무엇을 배웠나
- Bellman-Ford update 식
- 2-phase synchronous simulation
- 수렴 판정
- next hop과 cost를 함께 관리하는 방법

## 현재 한계
- poisoned reverse는 구현하지 않았습니다.
- 동적 토폴로지 변화 실험은 포함하지 않습니다.
- 비동기 메시지 모델은 구현하지 않습니다.
