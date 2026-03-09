# 접근 과정 — 커밋 로그를 바닥부터 쌓기

## Layer 1: Store — 파일에 레코드 쓰기

레코드 포맷:
```
┌──────────┬──────────────────┐
│ len (8B) │ data (len bytes) │
└──────────┴──────────────────┘
```

length prefix(8바이트, big-endian uint64) + 데이터. 이 포맷이면 파일 어디에서든 `pos` 위치에서 8바이트를 읽어 길이를 알고, 바로 뒤에서 데이터를 읽을 수 있다.

```go
type store struct {
    mu   sync.Mutex
    file *os.File
    buf  *bufio.Writer
    size uint64
}
```

`bufio.Writer`를 사용해 작은 쓰기를 버퍼링한다. `Append`마다 디스크를 건드리면 느리다. 대신 `Read` 전에 `Flush`를 호출해 아직 버퍼에 있는 데이터를 파일로 내보낸다.

`io.ReaderAt` 인터페이스를 구현한다(`ReadAt`). Segment가 Store에서 특정 위치를 바로 읽을 수 있게.

## Layer 2: Index — 오프셋을 파일 위치로 매핑

인덱스 엔트리 포맷:
```
[ offset (4B uint32) | position (8B uint64) ]  = 12 bytes
```

**mmap(memory-mapped file)**을 사용해 인덱스를 메모리에 매핑한다:

```go
data, err := syscall.Mmap(
    int(f.Fd()), 0, int(maxBytes),
    syscall.PROT_READ|syscall.PROT_WRITE,
    syscall.MAP_SHARED,
)
```

mmap의 장점:
- 파일을 마치 바이트 배열처럼 접근 (OS가 페이지 단위로 캐시)
- `Read`/`Write` 시스템 콜 없이 메모리 접근만으로 I/O
- 특히 랜덤 읽기가 많은 인덱스에 적합

파일을 미리 `maxBytes`로 확장(`Truncate`)해두고, Close 시 실제 데이터 크기로 줄인다.

## Layer 3: Segment — Store + Index 묶기

```go
type segment struct {
    store      *store
    index      *index
    baseOffset uint64
    nextOffset uint64
    config     Config
}
```

하나의 Segment는 하나의 `.store` 파일과 하나의 `.index` 파일을 갖는다. 파일명은 `${baseOffset}.store`, `${baseOffset}.index`.

`Append`:
1. Store에 데이터 쓰기 → 파일 위치(pos) 반환
2. Index에 (상대 오프셋, pos) 기록
3. nextOffset 증가

`Read(off)`:
1. 절대 오프셋에서 baseOffset을 빼 상대 오프셋 산출
2. Index에서 pos 조회
3. Store에서 pos 위치의 데이터 읽기

`IsFull()`: Store 크기가 MaxStoreBytes 이상이면 true.

## Layer 4: Log — Segment 관리

```go
type Log struct {
    mu            sync.RWMutex
    dir           string
    config        Config
    segments      []*segment
    activeSegment *segment
}
```

`Append`:
1. activeSegment가 가득 찼으면 새 Segment 생성 (rotation)
2. activeSegment에 데이터 쓰기

`Read`:
1. `sort.Search`로 해당 오프셋을 포함하는 Segment를 이진 탐색
2. Segment의 Read 호출

`setup()`: 디렉토리를 스캔해 기존 `.store`/`.index` 파일에서 Segment를 복원한다. 서버가 재시작해도 데이터가 유지된다.

`Reset()`: 모든 Segment 삭제 후 새 Log 초기화.

`Truncate(lowest)`: 지정 오프셋 이하의 오래된 Segment들을 삭제.
