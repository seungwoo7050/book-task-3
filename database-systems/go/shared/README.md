# Shared Go Utilities

`go/shared`는 여러 Go 프로젝트가 재사용하는 최소 공용 유틸리티를 모아 둔 위치입니다. 학습 포인트는 “공용 코드가 있다는 사실”보다도, 어떤 기능을 프로젝트 내부에 두고 어떤 기능을 공통 표면으로 뽑았는지 보는 데 있습니다.

## 들어 있는 패키지

- `serializer`: 간단한 binary record encoding 보조
- `hash`: CRC32, MurmurHash3 같은 공용 해시 기능
- `fileio`: 디렉터리 보장, 원자적 쓰기, 파일 정리 보조

## 어떻게 읽으면 좋은가

1. 먼저 각 프로젝트 README를 읽고, 왜 공용 기능이 필요한지 맥락을 잡습니다.
2. 그다음 `go/shared` 패키지를 보면 반복되는 I/O와 encoding 책임을 어떻게 줄였는지 보입니다.
3. 포트폴리오용 레포로 옮길 때는 “공용화 기준” 자체를 문서화하면 설계 판단이 더 잘 드러납니다.

## 검증 명령

```bash
cd go/shared
GOWORK=off go test ./...
```
