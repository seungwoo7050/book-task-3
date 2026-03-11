# 접근 기록

## 읽기 순서 제안
1. `../problem/README.md`에서 요구와 현재 재구성 범위를 먼저 확인합니다.
2. 구현 핵심 파일을 열어 어떤 타입과 함수가 중심인지 확인합니다.
3. `../tests/`를 읽어 이 프로젝트가 실제로 고정한 계약을 확인합니다.
4. 데모를 실행해 테스트가 말하는 계약이 출력으로도 드러나는지 봅니다.
5. 마지막에 개념 문서를 읽으며 용어와 설계 판단을 정리합니다.

## 코드가 택한 분해 방식
### append-ahead 규칙을 먼저 세운다
- 관련 파일: `../internal/store/store.go`, `../internal/wal/wal.go`
- 판단: write는 memtable 수정 전에 WAL record append가 먼저 일어나도록 두었습니다. 그래야 crash 이후 replay 대상이 명확해집니다.

### checksum이 어긋나는 지점에서 replay를 멈춘다
- 관련 파일: `../internal/wal/wal.go`
- 판단: Go는 shared CRC32를, Python은 `zlib.crc32`를 써 trailing corruption을 감지합니다. “어디까지 신뢰할 수 있는가”를 코드에서 바로 볼 수 있게 한 선택입니다.

### flush는 SSTable 생성과 WAL rotation을 한 흐름으로 묶는다
- 관련 파일: `../internal/store/store.go`
- 판단: `ForceFlush` 뒤에는 active WAL이 비워지거나 새 파일로 시작되어야 합니다. replay 범위를 줄이고 durability 경계를 분명하게 하기 위해서입니다.

## 검증 명령
```bash
cd go/database-internals/projects/04-wal-recovery
go test ./...
go run ./cmd/wal-recovery
```

## 포트폴리오 설명으로 바꿀 때 남길 장면
- WAL record format과 corruption stopping rule을 함께 보여 주면 durability 설명이 추상적이지 않게 됩니다.
- `active.wal` rotation 전후 파일 상태를 설명하면 flush가 단순 저장이 아니라 recovery boundary라는 점을 보여 줄 수 있습니다.
- Go와 Python 모두 CRC32를 쓰지만 구현 언어에 맞는 표준 라이브러리를 골랐다는 점도 비교 포인트입니다.
