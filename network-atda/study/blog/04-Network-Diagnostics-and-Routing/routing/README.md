# Distance-Vector Routing Blog

이 문서 묶음은 `routing`을 "Bellman-Ford를 배웠다"보다 "분산 라우터가 synchronous round 안에서 서로의 distance vector를 주고받으면 어떤 수렴 패턴이 나타나는가"라는 질문으로 다시 읽는다. 현재 구현은 topology loader, `DVNode.receive_dv()`, 2-phase simulation loop를 분리해 두고, 3-node와 5-node 토폴로지에서 실제 convergence를 출력한다. 따라서 이 lab의 핵심은 shortest-path 공식 자체보다, 그 공식을 node-local state update로 옮겼을 때 어떤 제약이 생기는지 보는 데 있다.

이번 재작성은 기존 blog 본문이 아니라 다음 근거만 사용했다.

- 문제 정의: `study/04-Network-Diagnostics-and-Routing/routing/problem/README.md`
- 구현 경계: `README.md`, `python/README.md`, `python/src/dv_routing.py`
- 테스트 근거: `python/tests/test_dv_routing.py`, `problem/script/test_routing.sh`
- 실제 검증: 2026-03-14 재실행한 `make -C network-atda/study/04-Network-Diagnostics-and-Routing/routing/problem test`
- 보조 실행: `python3 python/src/dv_routing.py problem/data/topology.json`

## 읽는 순서

1. [`00-series-map.md`](./00-series-map.md)
2. [`10-development-timeline.md`](./10-development-timeline.md)
3. [`01-evidence-ledger.md`](./01-evidence-ledger.md)
4. [`02-structure.md`](./02-structure.md)

## 이번에 다시 확인한 검증 상태

- 정식 검증 명령: `make -C network-atda/study/04-Network-Diagnostics-and-Routing/routing/problem test`
- 결과: `4 passed, 0 failed`
- 보조 실행: 3-node topology는 2 iterations 뒤 수렴했고 `x -> z cost 3 via y`를 출력했다

## 지금 남기는 한계

- poisoned reverse, hold-down timer, count-to-infinity mitigation은 구현하지 않는다.
- asynchronous message delay나 topology churn은 모델링하지 않는다.
- 현재 simulation은 node들이 같은 round snapshot을 보는 synchronous model이다.
