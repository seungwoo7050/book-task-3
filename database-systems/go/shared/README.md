# Shared Go Utilities

`go/shared/`는 여러 Go 프로젝트가 함께 쓰는 작은 utility 패키지를 모아 둔 위치입니다. 프로젝트 자체를 학습 단위로 읽을 때는 본문보다 보조 역할이지만, import 경로와 파일 포맷 이해에는 자주 등장합니다.

## 들어 있는 패키지

- [`hash/`](hash/): CRC32, MurmurHash3 같은 checksum/hash helper
- [`fileio/`](fileio/): file handle wrapper, atomic write, directory helper
- [`serializer/`](serializer/): key/value record binary encoding helper

## 검증 명령

```bash
cd go
go test ./shared/...
```
