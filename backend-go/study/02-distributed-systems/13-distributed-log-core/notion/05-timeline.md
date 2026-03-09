# 타임라인 — 분산 로그 핵심 구축 전체 과정

## 1단계: 프로젝트 초기화

```bash
mkdir -p 13-distributed-log-core/go/log
cd 13-distributed-log-core/go
go mod init distributed-log-core
```

Go 1.22 사용, 외부 의존성 없이 표준 라이브러리만으로 구현.

```
go/
├── go.mod
└── log/
```

## 2단계: Store 구현 (append-only 파일)

`log/store.go` 작성.

```bash
# 파일 생성 후 첫 컴파일 확인
go build ./...
```

주요 결정:
- `bufio.NewWriter`로 쓰기 버퍼링 (시스템 콜 최소화)
- 길이 접두사: `binary.BigEndian.PutUint64` (8바이트 고정)
- `sync.Mutex`로 동시 접근 보호
- `Read`에서 항상 `buf.Flush()` 먼저

```bash
# Store 단위 테스트
go test ./log/ -run TestStore -v
```

## 3단계: Index 구현 (mmap 기반)

`log/index.go` 작성.

주요 결정:
- 파일을 `maxBytes`로 미리 Truncate → mmap 매핑
- 엔트리 크기 12바이트 = offset(4B, uint32) + position(8B, uint64)
- `Read(-1)`로 마지막 엔트리 접근 지원
- Close 시: Sync → Munmap → Truncate(실제 크기) → Close

```bash
# Index 단위 테스트
go test ./log/ -run TestIndex -v
```

## 4단계: Segment 구현 (Store + Index 조합)

`log/segment.go` 작성.

주요 결정:
- 파일명: `{baseOffset}.store`, `{baseOffset}.index`
- `nextOffset`으로 다음 레코드 위치 추적
- `IsFull()`: Store 또는 Index 중 하나라도 한계 도달 시 true
- 기존 파일이 있으면 복원 (Index 마지막 엔트리에서 nextOffset 계산)

```bash
# Segment 단위 테스트
go test ./log/ -run TestSegment -v
```

## 5단계: Log 구현 (다중 Segment 관리)

`log/log.go` 작성.

주요 결정:
- `setup()`: 디렉토리 스캔 → `.store` 파일 파싱 → baseOffset 정렬 → Segment 복원
- `Append()`: activeSegment.IsFull()이면 newSegment() 호출
- `Read()`: `sort.Search`로 이진 탐색 → 올바른 Segment 찾기
- `Truncate(lowest)`: lowest 미만의 Segment 모두 삭제
- `Reset()`: `os.RemoveAll` → 새 Segment로 재시작

```bash
# Log 전체 테스트
go test ./log/ -run TestLog -v
```

## 6단계: 에러 정의

`log/errors.go` — 5개 sentinel error 정의.

```go
var (
    ErrIndexFull        = errors.New("index is full")
    ErrIndexEmpty       = errors.New("index is empty")
    ErrIndexOutOfRange  = errors.New("index entry out of range")
    ErrSegmentFull      = errors.New("segment is full")
    ErrOffsetOutOfRange = errors.New("offset out of range")
)
```

## 7단계: 전체 테스트 및 검증

```bash
# 전체 테스트 실행
cd 13-distributed-log-core/go
go test ./... -v

# 커버리지 측정
go test ./log/ -coverprofile=coverage.out
go tool cover -html=coverage.out

# Race condition 검사
go test ./log/ -race -v
```

## 8단계: go.work 등록

```bash
# study/go.work에 모듈 추가
cd ../../
# go.work에 use ./02-distributed-systems/13-distributed-log-core/go 추가
```

## 소스 코드에서 보이지 않는 것들

| 항목 | 설명 |
|------|------|
| Go 버전 선택 | 1.22 — `syscall.Mmap`이 안정적으로 지원되는 최소 버전 |
| 외부 의존성 0개 | 의도적으로 표준 라이브러리만 사용. mmap도 `syscall` 패키지 직접 사용 |
| Index 최대 크기 결정 | 테스트에서 `1024` 바이트 = 85개 엔트리(12B씩) |
| Store 최대 크기 결정 | 테스트에서 적절한 바이트로 설정, 몇 개 레코드 후 rotation 유도 |
| `-race` 플래그 | `sync.Mutex` 사용 부분의 동시성 버그 탐지 |
| TempDir 사용 | 모든 테스트에서 `t.TempDir()` — 테스트 간 파일 시스템 격리 |
| Windows 미지원 | `syscall.Mmap`/`Munmap`은 POSIX 전용. 의식적인 제약 |
