# 09 Cache Migrations Observability

## 한 줄 요약

cache-aside, cache invalidation, migration, metrics, trace header를 한 API로 묶어 운영 기본기를 붙이는 과제다.

## 이 프로젝트가 푸는 문제

- cache-aside hit/miss와 invalidation을 같이 경험해야 한다.
- migration up/down과 API 변경이 어떻게 맞물리는지 봐야 한다.
- 기본 metrics와 trace ID 전파를 응답 표면에 노출해야 한다.

## 내가 만든 답

- SQLite 저장소 위에 in-memory cache-aside 계층과 `/metrics` 노출을 `solution/go`에 구현했다.
- `X-Trace-ID`를 응답 헤더에 반영해 최소한의 요청 추적 표면을 만들었다.
- Redis 대신 in-memory adapter를 사용해 로컬 검증 난도를 낮췄다.

## 핵심 설계 선택

- 운영성 기본기는 인프라 의존도를 낮춘 상태에서 먼저 익히도록 in-memory cache를 사용했다.
- API, migration, metrics를 한 과제에 묶어 “기능 + 운영 표면”을 동시에 읽게 했다.

## 검증

- `cd solution/go && go run ./cmd/server`
- `cd solution/go && go test ./...`

## 제외 범위

- 실제 Redis
- 분산 tracing backend

## 읽는 순서

1. [problem/README.md](problem/README.md)에서 canonical 문제 정의와 성공 기준을 읽는다.
2. [solution/README.md](solution/README.md)에서 구현 범위와 검증 진입점을 확인한다.
3. [docs/README.md](docs/README.md)에서 개념 설명과 참고 문서를 따라간다.
4. [notion/README.md](notion/README.md)에서 접근 로그, 디버그 기록, 회고를 확인한다.

## 상태

- 상태: `verified`
- 제공 자료와 provenance: `study`에서 새로 추가한 브리지 과제
