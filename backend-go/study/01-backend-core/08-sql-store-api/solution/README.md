# Solution

## 답안 요약

- 구현 위치: `solution/go`
- 핵심 범위: SQLite-backed CRUD API, migrations, optimistic update
- 이 답안은 `verified` 상태 기준으로 공개 표면을 정리했다.

## 구현 진입점

- `cd solution/go && go run ./cmd/server`
- `cd solution/go && go test ./...`

## 현재 한계

- 외부 DB와 prepared statement tuning은 포함하지 않는다.
