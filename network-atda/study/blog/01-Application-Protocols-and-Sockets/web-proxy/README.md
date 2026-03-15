# Web Proxy Blog

이 문서 묶음은 `web-proxy`를 "중간 서버"보다 "한 프로세스 안에서 client와 server 역할을 동시에 수행하는 구조 연습"으로 다시 읽는다. 현재 구현은 절대 URL을 origin request로 재구성하고, origin 응답을 그대로 캐시 파일에 저장한 뒤 다음 요청에 재사용한다.

이번 재작성은 `problem/README.md`, `python/README.md`, `python/src/web_proxy.py`, `python/tests/test_web_proxy.py`, 그리고 2026-03-14 재실행한 `make -C .../problem test`만 사용했다.

## 읽는 순서

1. [`00-series-map.md`](./00-series-map.md)
2. [`10-development-timeline.md`](./10-development-timeline.md)
3. [`01-evidence-ledger.md`](./01-evidence-ledger.md)
4. [`02-structure.md`](./02-structure.md)

## 이번에 다시 확인한 검증 상태

- 정식 검증: `make -C network-atda/study/01-Application-Protocols-and-Sockets/web-proxy/problem test`
- 결과: origin fetch pass, second fetch cache check pass, body non-empty pass

## 지금 남기는 한계

- `Cache-Control`/TTL 없음
- `HTTPS CONNECT` 미지원
- 캐시 동시성 제어 단순
