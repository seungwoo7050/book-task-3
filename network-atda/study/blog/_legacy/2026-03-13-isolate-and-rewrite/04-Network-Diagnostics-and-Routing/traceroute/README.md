# Traceroute blog

이 디렉터리는 `Traceroute`를 `strict source-only` 기준으로 다시 읽는 blog 시리즈다. chronology는 `problem/README.md`, `problem/Makefile`, `python/src/traceroute.py`, `python/tests/test_traceroute.py`를 중심으로 복원했다.

## source set
- [`../../../04-Network-Diagnostics-and-Routing/traceroute/README.md`](../../../04-Network-Diagnostics-and-Routing/traceroute/README.md)
- [`../../../04-Network-Diagnostics-and-Routing/traceroute/problem/README.md`](../../../04-Network-Diagnostics-and-Routing/traceroute/problem/README.md)
- [`../../../04-Network-Diagnostics-and-Routing/traceroute/problem/Makefile`](../../../04-Network-Diagnostics-and-Routing/traceroute/problem/Makefile)
- [`../../../04-Network-Diagnostics-and-Routing/traceroute/python/src/traceroute.py`](../../../04-Network-Diagnostics-and-Routing/traceroute/python/src/traceroute.py)
- [`../../../04-Network-Diagnostics-and-Routing/traceroute/python/tests/test_traceroute.py`](../../../04-Network-Diagnostics-and-Routing/traceroute/python/tests/test_traceroute.py)

## 읽는 순서
1. [`00-series-map.md`](00-series-map.md)
2. [`10-development-timeline.md`](10-development-timeline.md)
3. [`../../../04-Network-Diagnostics-and-Routing/traceroute/README.md`](../../../04-Network-Diagnostics-and-Routing/traceroute/README.md)

## 검증 진입점
- `make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem test`

## chronology 메모
- live traceroute보다 먼저 parser와 synthetic route 테스트를 고정하는 흐름으로 글을 구성했다.
