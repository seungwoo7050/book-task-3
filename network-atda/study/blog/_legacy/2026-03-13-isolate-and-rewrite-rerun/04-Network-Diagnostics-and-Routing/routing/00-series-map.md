    # Series Map — Distance-Vector Routing

    | 항목 | 내용 |
    | :--- | :--- |
    | 대상 프로젝트 | `04-Network-Diagnostics-and-Routing/routing` |
    | 문제 배경 | `Computer Networking: A Top-Down Approach`의 distance-vector 라우팅 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 |
    | 공개 답안 표면 | `python/src/dv_routing.py` |
    | 정식 검증 | `make -C study/04-Network-Diagnostics-and-Routing/routing/problem test` |
    | rewrite 방식 | `isolate-and-rewrite` |
    | legacy 보관 위치 | `_legacy/2026-03-13-isolate-and-rewrite/04-Network-Diagnostics-and-Routing/routing` |

    ## 프로젝트 경계
    - 이 프로젝트는 JSON topology를 읽고 distributed Bellman-Ford를 iteration 단위로 수렴시키는 distance-vector simulator를 독립 문제로 다룬다.
    - `README.md`, `problem/`, `python/`, `docs/`가 한 폴더 아래에 닫혀 있어 다른 lab 없이도 범위 설명과 재검증이 가능하다.
    - canonical entrypoint는 `make -C study/04-Network-Diagnostics-and-Routing/routing/problem test`이며, 이번 재실행에서도 Distance-Vector Routing Test Suite: 3-node/5-node topology convergence 모두 PASS 신호를 확인했다.

    ## 이번 rewrite의 입력 표면
    - `problem/code/dv_skeleton.py`: 시작용 skeleton 코드
- `problem/data/topology.json`: 기본 3노드 토폴로지
- `problem/data/topology_5node.json`: 확장 5노드 토폴로지
- `problem/script/test_routing.sh`: 정식 검증 스크립트
    - 소스 파일: `python/src/dv_routing.py`
    - 테스트 파일: `python/tests/test_dv_routing.py`
    - `docs/concepts/bellman-ford.md` - Bellman-Ford Equation
- `docs/concepts/count-to-infinity.md` - Count-to-Infinity Problem
- `docs/concepts/distance-vector.md` - Distance-Vector Algorithm
- `docs/concepts/dv-vs-ls.md` - Distance-Vector vs Link-State 라우팅 비교

    ## 이번 rewrite에서 제외한 입력
    - 기존 `study/blog/04-Network-Diagnostics-and-Routing/routing` 초안
    - `notion/`, `notion-archive/` 계열 노트
    - track 단위 회고나 다른 프로젝트 blog

    ## 이번 글에서 꼭 복원할 장면
    - Session 1: topology와 초기 DV 상태를 먼저 고정했다
- Session 2: neighbor advertisement를 받아 relax를 반복했다
- Session 3: 토폴로지 fixture와 개념 문서로 경계를 정리했다

    ## 이번 프로젝트가 남긴 학습 포인트
    - Bellman-Ford update 식
- 2-phase synchronous simulation
- 수렴 판정
- next hop과 cost를 함께 관리하는 방법
