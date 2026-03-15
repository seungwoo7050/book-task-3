# Core Invariants

## 1. Bloom filter는 false negative를 허용하지 않는 방향으로만 설계된다

[`bloom_filter.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/06-index-filter/internal/bloomfilter/bloom_filter.go)는 docs의 공식 그대로 bit count와 hash function 수를 계산한다.

- `m = ceil(-(n * ln(p)) / (ln2)^2)`
- `k = round((m / n) * ln2)`

그리고 positions는 MurmurHash3 두 개(`seed 0`, `seed 42`)를 이용한 double hashing으로 만든다. 이 조합 덕분에 false positive는 남을 수 있어도 false negative는 생기면 안 된다. 테스트도 바로 이 점을 먼저 잡는다.

## 2. sparse index는 block boundary key만 기억한다

[`sparse_index.go`](/Users/woopinbell/work/book-task-3/database-internals/projects/06-index-filter/internal/sparseindex/sparse_index.go)의 `Build()`는 모든 key를 저장하지 않는다. `i % BlockSize == 0`인 entry만 `Index.Entries`에 넣는다.

즉 메모리에 드는 key 수를 줄이는 대신, lookup은 "largest indexed key <= target"이 가리키는 block 범위만 읽고 그 안을 순차 scan한다. docs의 [`sparse-index-scan.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/06-index-filter/docs/concepts/sparse-index-scan.md)가 말하는 bounded block scan이 정확히 이 구조다.

## 3. footer는 40바이트 고정 레이아웃으로 filter/index 위치를 복원한다

`sstable.go`는 footer를 40바이트로 만들고 아래를 기록한다.

- magic `SIF1`
- Bloom offset
- Bloom size
- Index offset
- Index size
- Block size

추가 재실행에서도 `footer SIF1 96 112 4`가 나왔다. 즉 reopen 시점의 `Load()`는 이 footer만 읽어 filter와 index 영역을 정확히 다시 찾아낸다.

## 4. lookup은 Bloom reject와 block scan이 완전히 분리된 두 단계다

`GetWithStats()`는 먼저 filter를 본다.

```go
if !table.Filter.MightContain(key) {
    return nil, false, LookupStats{BloomRejected: true}, nil
}
```

이 분기 덕분에 negative lookup은 디스크 read 없이 끝날 수 있다. 실제 추가 재실행 결과도 `miss ... true 0`이었다.

filter가 통과하면 그다음에야 sparse index로 block range를 찾고, 그 범위만 `ReadAt()`으로 읽는다. hit 결과 `74 bytes`도 바로 이 bounded read path의 증거다.

## 5. source-only nuance: docs와 달리 block miss도 nil stats가 아니라 block range를 남긴다

소스를 보면 block을 읽은 뒤 sequential decode를 하다가 `record.Key > key`가 되면 바로 `not found`를 반환한다. 이때도 이미 `LookupStats{BytesRead, BlockRange}`는 채워진 상태다.

즉 positive filter라고 해서 반드시 hit를 의미하는 건 아니고, sparse block 내부에서 miss가 날 수도 있다. 이 랩은 Bloom reject와 bounded block miss를 서로 다른 관찰값으로 남길 수 있게 설계돼 있다.
