# 07 Buffer Pool

이 프로젝트는 disk-backed page를 메모리에 캐시하고, pin count와 dirty write-back 정책을 포함한 buffer pool manager를 구현한다.

- 상태: `verified`
- 검증 명령:

```bash
cd study/database-internals/07-buffer-pool/go
go test ./...
go run ./cmd/buffer-pool
```

