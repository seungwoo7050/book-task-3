# Core Invariants

## 1. write는 반드시 sorted record stream만 받는다

`Write()`의 첫 줄은 `validateSorted(records)`다. 이전 key가 다음 key보다 크면 즉시 에러를 낸다.

```go
if err := validateSorted(records); err != nil {
    return err
}
```

즉 이 SSTable은 정렬 책임을 호출자에게 요구한다. format layer는 정렬된 stream을 immutable file로 굳히는 역할만 맡고, sorting 자체는 하지 않는다.

## 2. footer는 두 section 길이를 8바이트에 저장한다

footer는 아래처럼 구성된다.

```go
footer := make([]byte, 8)
binary.BigEndian.PutUint32(footer[0:4], uint32(len(dataSection)))
binary.BigEndian.PutUint32(footer[4:8], uint32(len(indexSection)))
```

즉 data section size 4바이트, index section size 4바이트가 전부다. reopen 시 `LoadIndex()`와 `ReadAll()`은 이 길이를 합쳐 `data + index + 8 == fileSize`인지 검증한다. 포맷 메타데이터가 극단적으로 작기 때문에, 오히려 길이 합 검증이 무척 중요해진다.

## 3. tombstone은 shared serializer의 `math.MaxUint32` marker로 인코딩된다

shared [`serializer.go`](/Users/woopinbell/work/book-task-3/database-systems/go/shared/serializer/serializer.go)는 tombstone sentinel을 아래처럼 정의한다.

```go
const TombstoneMarker = math.MaxUint32
```

`EncodeRecord()`는 `record.Value == nil`이면 `valueLength`에 이 marker를 넣고 value bytes는 쓰지 않는다. `DecodeRecord()`는 같은 marker를 다시 만나면 `Value=nil`로 복원한다. docs가 말한 `0xFFFFFFFF` sentinel이 실제 shared serializer contract로 살아 있는 셈이다.

## 4. lookup은 index binary search보다 record header 재읽기가 더 중요하다

`Lookup()`은 먼저 메모리의 `Index []IndexEntry`에서 binary search를 돌린다. 여기까지는 흔한 sparse index다. 하지만 실제 구현에서 중요한 건 그 다음이다.

1. 찾은 offset에서 8-byte header만 먼저 읽는다.
2. `keyLength`, `valueLength`를 해석한다.
3. tombstone marker면 실제 value length를 0으로 바꾼다.
4. 정확한 record size를 계산한 뒤 해당 길이만큼 다시 읽는다.

즉 lookup은 "index에서 끝나는" 게 아니라 "header를 먼저 읽어 정확한 record boundary를 재계산하는" 2-step read path다. docs의 `lookup-path.md`가 말하는 순서가 바로 이 경로다.

## 5. malformed layout은 조용히 무시하지 않고 에러로 끝낸다

`LoadIndex()`와 `ReadAll()`은 footer 길이 합이 맞지 않으면 에러를 낸다. `Lookup()`도 header가 8바이트보다 짧으면 `truncated record header` 에러를 낸다. index record에 tombstone이 들어 있으면 그것도 즉시 에러다.

이 설계 덕분에 포맷 오류를 "missing key"처럼 조용히 삼키지 않는다. 학습용 프로젝트지만, 파일 포맷 경계만큼은 꽤 엄격하다.
