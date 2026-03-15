# Web Server Blog

이 문서 묶음은 `web-server`를 "정적 파일 서버"보다 "TCP accept loop에서 HTTP 응답 한 건을 끝까지 책임지는 가장 작은 서버"로 다시 읽는다. 현재 구현은 요청 라인 파싱, 파일 열기, `Content-Type` 추정, `200/404` 응답 생성, 연결 종료까지 서버 생애주기를 가장 짧은 경로로 보여 준다.

이번 재작성은 `problem/README.md`, `python/README.md`, `python/src/web_server.py`, `python/tests/test_web_server.py`, 그리고 2026-03-14 재실행한 `make -C .../problem test`만 사용했다.

## 읽는 순서

1. [`00-series-map.md`](./00-series-map.md)
2. [`10-development-timeline.md`](./10-development-timeline.md)
3. [`01-evidence-ledger.md`](./01-evidence-ledger.md)
4. [`02-structure.md`](./02-structure.md)

## 이번에 다시 확인한 검증 상태

- 정식 검증: `make -C network-atda/study/01-Application-Protocols-and-Sockets/web-server/problem test`
- 결과: `GET /hello.html 200`, `GET /nonexistent 404`, body HTML 확인, 총 `3 passed`

## 지금 남기는 한계

- path traversal 방어 없음
- thread pool 없음
- GET 외 메서드 미지원
