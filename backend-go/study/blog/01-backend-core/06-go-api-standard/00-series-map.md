# 06 Go API Standard Series Map

`01-backend-core/06-go-api-standard`는 표준 라이브러리만으로 REST API, middleware, JSON envelope, graceful shutdown을 정리하는 본선 과제다.

## 이 시리즈가 복원하는 것

- 시작점: 표준 라이브러리만으로 RESTful JSON API를 설계해야 한다.
- 구현 축: Movie 리소스용 `net/http` API와 in-memory store를 `solution/go`에 구현했다.
- 검증 축: 2026-03-07 기준 `make -C problem test`가 통과했다.
- 글 수: 2편

## 읽는 순서

- [10-net-http-surface-and-store.md](10-net-http-surface-and-store.md)
- [20-middleware-shutdown-and-proof.md](20-middleware-shutdown-and-proof.md)

## 근거 기준

- 소스코드, README, docs, 테스트, CLI만 입력 근거로 사용했다.
- 기존 blog 초안과 `_legacy` 본문은 입력 근거로 사용하지 않았다.
