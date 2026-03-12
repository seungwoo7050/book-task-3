# 문제 정의

Go 표준 라이브러리만 사용해 간단한 Movie 리소스용 RESTful JSON API를 설계하고 구현한다.

## 성공 기준

- `GET /v1/healthcheck`와 Movie CRUD API를 제공한다.
- 모든 응답이 일관된 JSON envelope 구조를 따른다.
- 입력 검증, pagination, request logging, panic recovery, CORS를 포함한다.
- SIGINT/SIGTERM에서 graceful shutdown이 동작한다.
- third-party router 없이 `net/http` 기반으로 구현한다.

## 제공 자료와 출처

- legacy `01-foundation/01-go-api-standard` 문제를 한국어 canonical 형태로 다시 정리한 문서다.
- 원문 세부 요구사항은 legacy provenance로만 유지한다.
- 공개 구현은 [`solution/README.md`](../solution/README.md)와 `solution/go`에 둔다.

## 검증 기준

- `make -C problem build`
- `make -C problem test`

## 제외 범위

- 실제 DB 연동
- ORM
- third-party router
