# Shared Go Utilities

공용 Go 유틸리티는 이후 프로젝트들이 재사용할 최소 표면을 제공한다.

## Packages

- `serializer`: 간단한 binary record encoding
- `hash`: CRC32, MurmurHash3
- `fileio`: FileHandle, EnsureDir, ListFiles, AtomicWrite, RemoveFile

## Verification

```bash
cd go/shared
GOWORK=off go test ./...
```
