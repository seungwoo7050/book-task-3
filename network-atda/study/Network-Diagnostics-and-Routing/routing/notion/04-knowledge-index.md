# 04 지식 인덱스

## 핵심 용어
- **Bellman-Ford equation**: `D_x(y) = min_v { c(x,v) + D_v(y) }` 형태로 이웃을 거친 최소 비용을 계산하는 식이다.
- **distance vector**: 각 노드가 모든 목적지까지 알고 있다고 주장하는 현재 비용 표다.
- **convergence**: 더 이상 어떤 노드의 DV도 바뀌지 않는 상태다.
- **next-hop**: 목적지로 보내기 위해 첫 번째로 넘겨야 하는 이웃 노드다.

## 다시 볼 파일
- [`../problem/data/topology.json`](../problem/data/topology.json): 가장 작은 3노드 예제로 수렴 과정을 눈으로 확인할 때 좋다.
- [`../python/src/dv_routing.py`](../python/src/dv_routing.py): DVNode, 시뮬레이션 루프, 출력 형식이 모두 들어 있다.
- [`../python/tests/test_dv_routing.py`](../python/tests/test_dv_routing.py): 초기화, 수렴, self-link 예외, 5노드 토폴로지를 어떤 기준으로 검증하는지 보여준다.
- [`../docs/concepts/bellman-ford.md`](../docs/concepts/bellman-ford.md): 수식과 코드 갱신 규칙을 다시 연결할 때 본다.

## 자주 쓰는 확인 명령
- `make -C study/Network-Diagnostics-and-Routing/routing/problem test`
- `cd study/Network-Diagnostics-and-Routing/routing/python/tests && python3 -m pytest test_dv_routing.py -v`

## 참고 자료
- [`../docs/references/README.md`](../docs/references/README.md): 공개 문서를 정리할 때 다시 확인한 근거 모음
