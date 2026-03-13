# Web Proxy blog

이 디렉터리는 `Web Proxy`를 `source-first` 방식으로 다시 읽는 blog 시리즈다. chronology는 프로젝트 README, `problem/README.md`, `problem/Makefile`, `python/src/web_proxy.py`, `python/tests/test_web_proxy.py`를 바탕으로 재구성했다.

## source set
- [`../../../01-Application-Protocols-and-Sockets/web-proxy/README.md`](../../../01-Application-Protocols-and-Sockets/web-proxy/README.md)
- [`../../../01-Application-Protocols-and-Sockets/web-proxy/problem/README.md`](../../../01-Application-Protocols-and-Sockets/web-proxy/problem/README.md)
- [`../../../01-Application-Protocols-and-Sockets/web-proxy/problem/Makefile`](../../../01-Application-Protocols-and-Sockets/web-proxy/problem/Makefile)
- [`../../../01-Application-Protocols-and-Sockets/web-proxy/python/src/web_proxy.py`](../../../01-Application-Protocols-and-Sockets/web-proxy/python/src/web_proxy.py)
- [`../../../01-Application-Protocols-and-Sockets/web-proxy/python/tests/test_web_proxy.py`](../../../01-Application-Protocols-and-Sockets/web-proxy/python/tests/test_web_proxy.py)

## 읽는 순서
1. [`00-series-map.md`](00-series-map.md)
2. [`10-development-timeline.md`](10-development-timeline.md)
3. [`../../../01-Application-Protocols-and-Sockets/web-proxy/README.md`](../../../01-Application-Protocols-and-Sockets/web-proxy/README.md)

## 검증 진입점
- `make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem test`

## chronology 메모
- 이 프로젝트의 핵심은 origin fetch보다 먼저 "proxy가 어떤 URL을 어떤 cache key로 재해석하는가"를 고정하는 데 있었다.
- git history는 거칠어 `Day / Session` 형식을 사용했다.
