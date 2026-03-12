# 06 Go API Standard

## 한 줄 요약

표준 라이브러리만으로 REST API, middleware, JSON envelope, graceful shutdown을 정리하는 본선 과제다.

## 이 프로젝트가 푸는 문제

- 표준 라이브러리만으로 RESTful JSON API를 설계해야 한다.
- JSON envelope, validation, pagination, middleware, graceful shutdown을 한 서버에서 설명해야 한다.
- 외부 라우터 없이 `net/http`와 `ServeMux` 패턴 매칭만으로 구조를 잡아야 한다.

## 내가 만든 답

- Movie 리소스용 `net/http` API와 in-memory store를 `solution/go`에 구현했다.
- request logging, recovery, CORS 같은 middleware와 JSON envelope를 직접 조립했다.
- DB를 제외하고도 표준 라이브러리 기반 API 기본기를 설명할 수 있게 했다.

## 핵심 설계 선택

- 외부 프레임워크를 빼고 표준 라이브러리만 사용해 HTTP 기초를 드러냈다.
- DB를 의도적으로 제외해 handler/model/middleware 구조와 종료 시퀀스에 집중하게 했다.

## 검증

- `make -C problem build`
- `make -C problem test`

## 제외 범위

- DB-backed persistence
- third-party router

## 읽는 순서

1. [problem/README.md](problem/README.md)에서 canonical 문제 정의와 성공 기준을 읽는다.
2. [solution/README.md](solution/README.md)에서 구현 범위와 검증 진입점을 확인한다.
3. [docs/README.md](docs/README.md)에서 개념 설명과 참고 문서를 따라간다.
4. [notion/README.md](notion/README.md)에서 접근 로그, 디버그 기록, 회고를 확인한다.

## 상태

- 상태: `verified`
- 제공 자료와 provenance: legacy/01-foundation/01-go-api-standard (`legacy/01-foundation/01-go-api-standard/README.md`, public repo에는 미포함)
