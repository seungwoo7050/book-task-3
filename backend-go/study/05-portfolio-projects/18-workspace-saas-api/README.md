# 18 Workspace SaaS API

## Status

`verified`

## Legacy source

- `study`에서 새로 추가한 대표 포트폴리오 과제

## Problem scope

- JWT access token + refresh rotation
- organization-based RBAC
- invitation flow
- project / issue / comment workflow
- outbox-driven async notification
- Redis dashboard cache
- local reproducibility with Postgres + Redis

## Build

```bash
cd go
mkdir -p ./bin
go build -o ./bin/api ./cmd/api
go build -o ./bin/worker ./cmd/worker
```

## Test

```bash
cd go
go test ./...
make e2e
make smoke
```

## Verification

- `2026-03-07`: `cd go && go test ./...`
- `2026-03-07`: `cd go && make e2e`
- `2026-03-07`: `cd go && make smoke`
- `2026-03-07`: `make test-portfolio-unit test-portfolio-repro`
- `2026-03-07`: `make test-all`
- `go/api/openapi.yaml`에 정의한 핵심 응답 필드는 `e2e`와 `smoke`에서 실제로 파싱해 확인했다.

## Known gaps

- Helm/GitOps 자산은 이 대표작의 필수 범위에 넣지 않았다.
