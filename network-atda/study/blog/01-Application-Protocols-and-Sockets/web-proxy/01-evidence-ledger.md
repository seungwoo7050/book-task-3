# Web Proxy Evidence Ledger

## 이번에 읽은 자료

- `problem/README.md`
- `python/src/web_proxy.py`
- `python/tests/test_web_proxy.py`

## 핵심 코드 근거

- `parse_url()`: scheme 제거, host/port/path 분리
- `get_cache_path()`: URL MD5 해시를 cache 파일명으로 사용
- `fetch_from_origin()`: origin에 `GET path HTTP/1.1` 요청 재구성
- `handle_client()`: cache hit/hit miss, 400/502/504 분기

## 테스트/검증 근거

`make -C network-atda/study/01-Application-Protocols-and-Sockets/web-proxy/problem test`

재실행 결과:

- 첫 fetch pass
- 두 번째 fetch cache check pass
- body non-empty pass

보조 단위 테스트:

- URL parsing 6개 케이스
- cache key 동일/상이 URL 검증

## 이번에 남긴 해석

- 이 lab의 핵심은 캐시 최적화보다 프록시의 이중 역할이다.
- cache는 HTTP semantics를 깊게 이해한 결과라기보다, same URL 재사용을 보여 주는 최소 구현이다.
