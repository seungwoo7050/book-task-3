# ICMP Pinger blog

이 디렉터리는 `ICMP Pinger`를 `strict source-only` 기준으로 다시 읽는 blog 시리즈다. chronology는 `problem/README.md`, `problem/Makefile`, `python/src/icmp_pinger.py`, `python/tests/test_icmp_pinger.py`를 바탕으로 일반적인 개발자 수준의 추론으로 복원했다.

## source set
- [`../../../04-Network-Diagnostics-and-Routing/icmp-pinger/README.md`](../../../04-Network-Diagnostics-and-Routing/icmp-pinger/README.md)
- [`../../../04-Network-Diagnostics-and-Routing/icmp-pinger/problem/README.md`](../../../04-Network-Diagnostics-and-Routing/icmp-pinger/problem/README.md)
- [`../../../04-Network-Diagnostics-and-Routing/icmp-pinger/problem/Makefile`](../../../04-Network-Diagnostics-and-Routing/icmp-pinger/problem/Makefile)
- [`../../../04-Network-Diagnostics-and-Routing/icmp-pinger/python/src/icmp_pinger.py`](../../../04-Network-Diagnostics-and-Routing/icmp-pinger/python/src/icmp_pinger.py)
- [`../../../04-Network-Diagnostics-and-Routing/icmp-pinger/python/tests/test_icmp_pinger.py`](../../../04-Network-Diagnostics-and-Routing/icmp-pinger/python/tests/test_icmp_pinger.py)

## 읽는 순서
1. [`00-series-map.md`](00-series-map.md)
2. [`10-development-timeline.md`](10-development-timeline.md)
3. [`../../../04-Network-Diagnostics-and-Routing/icmp-pinger/README.md`](../../../04-Network-Diagnostics-and-Routing/icmp-pinger/README.md)

## 검증 진입점
- `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test`

## chronology 메모
- raw socket live 실행과 deterministic fake-socket 테스트를 분리해 읽는 것이 이 프로젝트의 핵심 흐름이었다.
