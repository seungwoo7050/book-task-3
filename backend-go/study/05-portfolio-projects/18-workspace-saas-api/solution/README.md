# Solution

## 답안 요약

- 구현 위치: `solution/go`
- 핵심 범위: API server, worker, Postgres repository, Redis cache/session store, OpenAPI, e2e, smoke
- 이 답안은 `verified` 상태 기준으로 공개 표면을 정리했다.

## 구현 진입점

- `cd solution/go && mkdir -p ./bin && go build -o ./bin/api ./cmd/api`
- `cd solution/go && go build -o ./bin/worker ./cmd/worker`
- `cd solution/go && go test ./...`
- `cd solution/go && make e2e`
- `cd solution/go && make smoke`

## 현재 한계

- Helm/GitOps 배포 자산은 이 대표작의 필수 검증 범위가 아니다.
