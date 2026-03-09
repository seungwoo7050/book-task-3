# 디버그 기록 — 파일 I/O와 mmap에서 만나는 함정들

## bufio.Writer Flush 타이밍

`Append`로 데이터를 쓴 직후 `Read`를 하면, 아직 버퍼에만 있고 파일에는 없을 수 있다. `Read`에서 `s.buf.Flush()`를 먼저 호출하는 이유다.

```go
func (s *store) Read(pos uint64) ([]byte, error) {
    s.mu.Lock()
    defer s.mu.Unlock()
    if err := s.buf.Flush(); err != nil {
        return nil, err
    }
    // ...
}
```

**교훈**: 쓰기 버퍼링과 읽기를 동시에 지원하는 경우, 읽기 전에 반드시 flush.

## mmap과 Truncate 순서

Index 생성 시:
1. 파일을 `maxBytes`로 Truncate (확장)
2. mmap으로 매핑

Close 시:
1. `file.Sync()` — 디스크 동기화
2. `syscall.Munmap` — 매핑 해제
3. `file.Truncate(actualSize)` — 실 데이터 크기로 축소
4. `file.Close()`

이 순서를 지키지 않으면:
- Close 전에 Truncate하면 mmap이 유효하지 않은 메모리를 참조 (SIGBUS)
- Munmap 전에 Close하면 데이터 유실 가능

## Offset은 uint32, 하지만 Position은 uint64

인덱스 엔트리에서 offset은 4바이트(uint32), position은 8바이트(uint64)다. offset은 Segment 내 상대 오프셋이라 4바이트로 충분하지만, position은 Store 파일 내 바이트 위치라 대용량 파일을 위해 8바이트가 필요하다.

uint32의 최대값은 ~42억. 한 Segment에 42억 개 레코드를 넣지 않는 한 overflow가 일어나지 않는다.

## Segment 복원 시 nextOffset 계산

서버 재시작 후 기존 Segment를 열 때, nextOffset을 어떻게 아느냐:

```go
if idx.Entries() > 0 {
    off, _, _ := idx.Read(-1)  // 마지막 엔트리의 오프셋
    seg.nextOffset = baseOffset + uint64(off) + 1
}
```

Index의 마지막 엔트리가 상대 오프셋 5이면, 다음은 6이다. baseOffset이 100이면 nextOffset은 106.

## sort.Search로 Segment 탐색

Log.Read에서 올바른 Segment를 찾을 때:

```go
idx := sort.Search(len(l.segments), func(i int) bool {
    return l.segments[i].nextOffset > off
})
```

`sort.Search`는 이진 탐색이다. segments가 baseOffset 순으로 정렬되어 있으므로 O(log n).

## 파일명 규칙

`0.store`, `0.index`, `100.store`, `100.index` ... baseOffset이 파일명이다. `setup()`에서 디렉토리를 스캔할 때 파일명의 숫자를 파싱해 segment 순서를 복원한다.

## os.RemoveAll 위험성

`Reset()`은 `os.RemoveAll(l.dir)`을 호출한다. 디렉토리 전체를 삭제하므로, 잘못된 경로를 넘기면 데이터가 모두 사라진다. 프로덕션에서는 이 함수를 직접 노출하지 않고, 관리자 API 뒤에 두어야 한다.
