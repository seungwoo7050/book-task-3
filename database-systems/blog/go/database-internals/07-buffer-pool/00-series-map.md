# 07 Buffer Pool 시리즈 맵

이 시리즈는 Database Internals 트랙의 7번째 프로젝트 `07 Buffer Pool`를 따라간다. disk-backed page를 메모리에 캐시하고 pin count와 dirty write-back 정책을 포함한 buffer pool manager를 구현합니다. 기능 목록보다 먼저, 어떤 순서로 경계를 고정했는지 읽는 쪽에 무게를 두었다.

## 먼저 보고 갈 질문

- page id로 file path와 page number를 안정적으로 분리해야 합니다.
- fetch 시 cache hit면 pin count를 올리고, miss면 disk read 후 캐시에 올려야 합니다.

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md) — 테스트 이름과 파일 배치부터 훑으면서 문제의 테두리를 다시 좁히는 글
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md) — 핵심 함수와 상태 전이에서 invariant가 실제로 어디서 잠기는지 따라가는 글
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md) — 테스트와 demo를 다시 돌려 약속 범위와 남는 한계를 정리하는 글

## 재검증 명령

```bash
GOWORK=off go test ./...
GOWORK=off go run ./cmd/buffer-pool
```

## 이번 시리즈가 근거로 삼은 파일

- `database-systems/go/database-internals/projects/07-buffer-pool/internal/bufferpool/buffer_pool.go`
- `database-systems/go/database-internals/projects/07-buffer-pool/tests/buffer_pool_test.go`
- `database-systems/go/database-internals/projects/07-buffer-pool/README.md`
- `database-systems/go/database-internals/projects/07-buffer-pool/problem/README.md`
- `database-systems/go/database-internals/projects/07-buffer-pool/docs/README.md`
- `database-systems/go/database-internals/projects/07-buffer-pool/internal/lrucache/lru_cache.go`
- `database-systems/go/database-internals/projects/07-buffer-pool/cmd/buffer-pool/main.go`

## 보조 메모

작업 메모가 꼭 필요할 때만 [_evidence-ledger.md](_evidence-ledger.md)와 [_structure-outline.md](_structure-outline.md)를 보면 된다. 공개 시리즈는 `00 -> 10 -> 20 -> 30`만 따라가면 충분하다.

## Git Anchor

- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
