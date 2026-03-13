# UDP Pinger blog

이 디렉터리는 `UDP Pinger`를 `source-first` 방식으로 다시 읽는 blog 시리즈다. chronology는 프로젝트 README, `problem/README.md`, `problem/Makefile`, `python/src/udp_pinger_client.py`, `python/tests/test_udp_pinger.py`를 기준으로 복원했다.

## source set
- [`../../../01-Application-Protocols-and-Sockets/udp-pinger/README.md`](../../../01-Application-Protocols-and-Sockets/udp-pinger/README.md)
- [`../../../01-Application-Protocols-and-Sockets/udp-pinger/problem/README.md`](../../../01-Application-Protocols-and-Sockets/udp-pinger/problem/README.md)
- [`../../../01-Application-Protocols-and-Sockets/udp-pinger/problem/Makefile`](../../../01-Application-Protocols-and-Sockets/udp-pinger/problem/Makefile)
- [`../../../01-Application-Protocols-and-Sockets/udp-pinger/python/src/udp_pinger_client.py`](../../../01-Application-Protocols-and-Sockets/udp-pinger/python/src/udp_pinger_client.py)
- [`../../../01-Application-Protocols-and-Sockets/udp-pinger/python/tests/test_udp_pinger.py`](../../../01-Application-Protocols-and-Sockets/udp-pinger/python/tests/test_udp_pinger.py)

## 읽는 순서
1. [`00-series-map.md`](00-series-map.md)
2. [`10-development-timeline.md`](10-development-timeline.md)
3. [`../../../01-Application-Protocols-and-Sockets/udp-pinger/README.md`](../../../01-Application-Protocols-and-Sockets/udp-pinger/README.md)

## 검증 진입점
- `make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem test`

## chronology 메모
- 이 프로젝트도 일시 근거가 충분하지 않아 `Day / Session` 기준으로 정리했다.
- 글의 핵심 근거는 `timeout`, RTT 계산, 손실률 요약, 테스트 조건이다.
