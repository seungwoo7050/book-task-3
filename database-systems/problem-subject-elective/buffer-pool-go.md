# buffer-pool-go 문제지

## 왜 중요한가

page id로 file path와 page number를 안정적으로 분리해야 합니다. fetch 시 cache hit면 pin count를 올리고, miss면 disk read 후 캐시에 올려야 합니다. dirty page는 eviction이나 explicit flush 때 write-back해야 합니다. pinned page는 eviction하면 안 됩니다.

## 목표

시작 위치의 구현을 완성해 page id로 file path와 page number를 안정적으로 분리해야 합니다, fetch 시 cache hit면 pin count를 올리고, miss면 disk read 후 캐시에 올려야 합니다, dirty page는 eviction이나 explicit flush 때 write-back해야 합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../go/database-internals/projects/07-buffer-pool/cmd/buffer-pool/main.go`
- `../go/database-internals/projects/07-buffer-pool/internal/bufferpool/buffer_pool.go`
- `../go/database-internals/projects/07-buffer-pool/internal/lrucache/lru_cache.go`
- `../go/database-internals/projects/07-buffer-pool/tests/buffer_pool_test.go`
- `../go/database-internals/projects/07-buffer-pool/tests/lru_cache_test.go`

## starter code / 입력 계약

- `../go/database-internals/projects/07-buffer-pool/cmd/buffer-pool/main.go`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- page id로 file path와 page number를 안정적으로 분리해야 합니다.
- fetch 시 cache hit면 pin count를 올리고, miss면 disk read 후 캐시에 올려야 합니다.
- dirty page는 eviction이나 explicit flush 때 write-back해야 합니다.
- pinned page는 eviction하면 안 됩니다.

## 제외 범위

- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `main`와 `must`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `TestFetchPageFromDisk`와 `TestReturnCachedPage`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/07-buffer-pool && GOWORK=off go test ./...`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/07-buffer-pool && GOWORK=off go test ./...
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`buffer-pool-go_answer.md`](buffer-pool-go_answer.md)에서 확인한다.
