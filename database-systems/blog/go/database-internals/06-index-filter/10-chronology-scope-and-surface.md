# Scope, Reopen Surface, And First Bounded Read

## 1. 문제는 "더 빠른 lookup"보다 "왜 덜 읽는가"를 설명하는 데 있다

[`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/06-index-filter/problem/README.md)는 Bloom filter serialization, sparse index build, footer-based reopen, Bloom reject와 bounded block scan 노출을 요구한다. learned index, adaptive filter, range optimization, block cache는 뺀다.

즉 이 랩은 SSTable 전체를 뜯어고치는 게 아니라, read path에 filter와 index를 얹어 negative/positive lookup 비용을 줄이는 최소 경로를 보여 준다.

## 2. 코드 표면은 `GetWithStats()`가 거의 전부다

핵심 구현은 [`sstable.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/06-index-filter/internal/sstable/sstable.go)에 있다. 이 테이블은 평범한 `Get()`도 제공하지만, 실제로 중요한 표면은 `GetWithStats()`다.

이 메서드는 아래를 함께 돌려준다.

- value
- found 여부
- `LookupStats`
  - `BloomRejected`
  - `BytesRead`
  - `BlockRange`

즉 이 랩의 핵심은 "값을 찾았는가" 못지않게 "어떤 경로로 찾았는가"를 관찰 가능하게 만든 데 있다.

## 3. demo가 보여 주는 첫 positive lookup

2026-03-14에 아래 명령을 다시 실행했다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/06-index-filter
rm -rf .demo-data
GOWORK=off go run ./cmd/index-filter
rm -rf .demo-data
```

출력은 아래였다.

```text
durian=gold bytes_read=74
```

이 출력은 positive lookup 하나만 보여 주지만, 이미 중요한 사실을 담고 있다. `durian`을 찾기 위해 data section 전체를 읽지 않고, 정확히 74바이트 block만 읽었다는 것이다.

## 4. 추가 재실행으로 miss-fast와 footer layout도 고정했다

이번에 project root 내부 임시 Go 파일로 추가 재실행을 돌린 결과는 아래와 같았다.

```text
miss false true true 0
hit true gold 74 0 74
footer SIF1 96 112 4
```

이 결과를 해석하면 아래와 같다.

- missing key는 `BloomRejected=true`, `BytesRead=0`으로 끝난다
- `durian` hit는 `BytesRead=74`, block range `[0, 74)`만 읽는다
- footer magic은 `SIF1`
- Bloom filter는 offset `96`, sparse index는 offset `112`, block size는 `4`다

즉 footer가 filter/index 위치를 복원하고, Bloom이 miss를 잘라내고, sparse index가 bounded scan 범위를 만든다는 세 단계가 실제 숫자로 확인된다.
