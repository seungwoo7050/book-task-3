    # Structure Design — Distance-Vector Routing

    ## opening
    - 시작 질문: 이 프로젝트를 실제로 어디서부터 만들기 시작했는가.
    - 바로 보여 줄 증거: `make -C study/04-Network-Diagnostics-and-Routing/routing/problem test`와 ``python/src/dv_routing.py::load_topology``.
    - 서술 원칙: 결과 요약보다 Session별 판단 이동을 우선한다.
    - 메모: `make -C study/04-Network-Diagnostics-and-Routing/routing/problem test`가 통과하는 상태를 출발점으로 삼되, 실제 글의 첫 장면은 ``python/src/dv_routing.py::load_topology``에서 시작한다.

    ## Session 1 — topology와 초기 DV 상태를 먼저 고정했다
- 다룰 파일/표면: `python/src/dv_routing.py::load_topology`, `python/src/dv_routing.py::DVNode.__init__`
- 글에서 먼저 던질 질문: "Bellman-Ford 식을 적용하기 전에 self/neighbor/INF 초기값이 맞아야 이후 iteration이 설명된다"
- 꼭 넣을 CLI: `make -C study/04-Network-Diagnostics-and-Routing/routing/problem run-solution`
- 꼭 남길 검증 신호: Iteration 0 출력이 topology와 같은 모양으로 정렬되기 시작했다.
- 핵심 전환 문장: DV 구현은 수식보다 초기 상태를 어떻게 배치하느냐가 더 직접적으로 드러난다.
## Session 2 — neighbor advertisement를 받아 relax를 반복했다
- 다룰 파일/표면: `python/src/dv_routing.py::receive_dv`, `python/src/dv_routing.py::simulate`
- 글에서 먼저 던질 질문: "`D_x(y) = min_v { c(x,v) + D_v(y) }`를 iteration loop에 그대로 옮기면 convergence 로그를 만들 수 있다"
- 꼭 넣을 CLI: `make -C study/04-Network-Diagnostics-and-Routing/routing/problem run-solution`
- 꼭 남길 검증 신호: Iteration N 출력과 final routing table이 topology별 shortest path와 맞아떨어졌다.
- 핵심 전환 문장: Bellman-Ford update 식
## Session 3 — 토폴로지 fixture와 개념 문서로 경계를 정리했다
- 다룰 파일/표면: `python/tests/test_dv_routing.py`, `docs/concepts/bellman-ford.md`, `docs/concepts/count-to-infinity.md`
- 글에서 먼저 던질 질문: "DV는 수렴 결과만 아니라 count-to-infinity 같은 한계까지 같이 적어야 이해가 닫힌다"
- 꼭 넣을 CLI: `make -C study/04-Network-Diagnostics-and-Routing/routing/problem test`
- 꼭 남길 검증 신호: Distance-Vector Routing Test Suite: 3-node/5-node topology convergence 모두 PASS
- 핵심 전환 문장: 2-phase synchronous simulation

    ## ending
    - 마지막 단락에서는 현재 한계를 README bullet 그대로 축약해 남긴다.
    - poisoned reverse는 구현하지 않았습니다.
- 동적 토폴로지 변화 실험은 포함하지 않습니다.
- 비동기 메시지 모델은 구현하지 않습니다.
