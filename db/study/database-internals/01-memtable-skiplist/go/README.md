# Go Implementation

## Scope

- SkipList insertion and update
- tombstone semantics
- ordered iteration
- approximate byte-size accounting

## Build Command

```bash
go test ./...
```

## Demo Command

```bash
go run ./cmd/skiplist-demo
```

## Status

- 상태: `verified`
- 알려진 공백: flush threshold, SSTable serialization, recovery path는 아직 이 프로젝트 범위 밖이다.

## Notes

- 구현은 `internal/skiplist` 패키지에 둔다.
- 테스트는 tombstone과 ordered iteration을 우선 검증한다.

