# Go Implementation

- Scope: API server, worker, Postgres repository, Redis cache/session store, OpenAPI, e2e, smoke
- Build: `mkdir -p ./bin && go build -o ./bin/api ./cmd/api && go build -o ./bin/worker ./cmd/worker`
- Test: `go test ./...`, `make e2e`, `make smoke`
- Status: `verified`
- Known gaps: Helm/GitOps 배포 자산은 이 모듈의 필수 검증 범위가 아니다.
