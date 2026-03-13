# Distance-Vector Routing blog

이 디렉터리는 `Distance-Vector Routing`을 `strict source-only` 기준으로 다시 읽는 blog 시리즈다. chronology는 `problem/README.md`, `problem/Makefile`, `python/src/dv_routing.py`, `python/tests/test_dv_routing.py`를 중심으로 재구성했다.

## source set
- [`../../../04-Network-Diagnostics-and-Routing/routing/README.md`](../../../04-Network-Diagnostics-and-Routing/routing/README.md)
- [`../../../04-Network-Diagnostics-and-Routing/routing/problem/README.md`](../../../04-Network-Diagnostics-and-Routing/routing/problem/README.md)
- [`../../../04-Network-Diagnostics-and-Routing/routing/problem/Makefile`](../../../04-Network-Diagnostics-and-Routing/routing/problem/Makefile)
- [`../../../04-Network-Diagnostics-and-Routing/routing/python/src/dv_routing.py`](../../../04-Network-Diagnostics-and-Routing/routing/python/src/dv_routing.py)
- [`../../../04-Network-Diagnostics-and-Routing/routing/python/tests/test_dv_routing.py`](../../../04-Network-Diagnostics-and-Routing/routing/python/tests/test_dv_routing.py)

## 읽는 순서
1. [`00-series-map.md`](00-series-map.md)
2. [`10-development-timeline.md`](10-development-timeline.md)
3. [`../../../04-Network-Diagnostics-and-Routing/routing/README.md`](../../../04-Network-Diagnostics-and-Routing/routing/README.md)

## 검증 진입점
- `make -C study/04-Network-Diagnostics-and-Routing/routing/problem test`

## chronology 메모
- 이 프로젝트는 topology load, DV update, convergence 출력이라는 세 단계로 읽는 것이 가장 자연스러웠다.
