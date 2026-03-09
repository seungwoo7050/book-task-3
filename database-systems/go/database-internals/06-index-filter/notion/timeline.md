# 개발 타임라인 — 06 Index Filter

이 문서는 프로젝트를 처음부터 재현할 수 있도록, 개발 과정을 시간순으로 기록한다.

---

## Phase 0: 프로젝트 초기화

### 디렉터리 생성

```bash
mkdir -p go/database-internals/06-index-filter/{cmd/index-filter,internal/{bloomfilter,sparseindex,sstable},tests,problem/{code,data,script},docs/{concepts,references}}
```

### Go 모듈 초기화

```bash
cd go/database-internals/06-index-filter
go mod init study.local/database-internals/06-index-filter
```

### 의존성 설정

```
require study.local/shared v0.0.0
replace study.local/shared => ../../shared
```

### shared/hash 패키지 확인

`shared/hash/hash.go`에 `MurmurHash3(data []byte, seed uint32) uint32` 함수가 필요하다.
기존에 CRC32만 있었다면, MurmurHash3를 추가한다.

```bash
go work use go/database-internals/06-index-filter
```

---

## Phase 1: Bloom Filter 구현

### 파일: `internal/bloomfilter/bloom_filter.go`

1. **`New(expectedItems, falsePositiveRate)` 생성자**
   - 최적 비트 수 $m$과 해시 함수 수 $k$ 계산
   - 비트 배열을 `[]byte`로 할당 ($\lceil m/8 \rceil$ 바이트)

2. **`Add(key)` 메서드**
   - double hashing으로 k개 위치 계산 → 해당 비트 set

3. **`MightContain(key)` 메서드**
   - 같은 k개 위치 확인 → 하나라도 0이면 false

4. **`Serialize()` / `Deserialize()` 메서드**
   - `[BitCount 4B][HashFunctions 4B][bits...]` 포맷

5. **내부 함수들**
   - `positions(key)`: double hashing으로 위치 배열 생성
   - `setBit(pos)`, `getBit(pos)`: 비트 조작

---

## Phase 2: Sparse Index 구현

### 파일: `internal/sparseindex/sparse_index.go`

1. **`Entry{Key, Offset}` 구조체**

2. **`Range{Start, End}` 구조체**: 블록 바이트 범위

3. **`New(blockSize)` 생성자**

4. **`Build(entries)` 메서드**
   - 전체 `(key, offset)` 목록에서 매 `blockSize`번째만 추출

5. **`FindBlock(key, dataSize)` 메서드**
   - 이진 탐색으로 key가 속하는 블록의 시작/끝 offset 반환

6. **`Serialize()` / `Deserialize()` 메서드**
   - `serializer.Record` 형태로 직렬화

---

## Phase 3: SSTable 통합 구현

### 파일: `internal/sstable/sstable.go`

02번의 SSTable과 다른 레이아웃:

```
[ Data ][ Bloom ][ Sparse Index ][ Footer 40B ]
```

1. **`Table` 구조체**: FilePath, BlockSize, DataSize, BloomOffset/Size, IndexOffset/Size, Filter, Index

2. **`Write(records)` 메서드**
   - Data Section 기록하면서 Bloom filter에 Add + offset 수집
   - Sparse index Build
   - Filter serialize → Index serialize
   - Data → Bloom → Index → Footer 순서로 파일 쓰기

3. **`Load()` 메서드**
   - 파일 끝 40바이트 footer 읽기 → magic 검증
   - Bloom filter와 Sparse index 역직렬화

4. **`Get(key)` / `GetWithStats(key)` 메서드**
   - Bloom check → block range 찾기 → block scan
   - `LookupStats` 반환: BloomRejected, BytesRead, BlockRange

---

## Phase 4: 테스트 작성 및 검증

### 테스트 실행

```bash
cd go/database-internals/06-index-filter
GOWORK=off go test ./...
```

### 데모 실행

```bash
GOWORK=off go run ./cmd/index-filter
```

---

## Phase 5: 개념 문서 작성

### docs/concepts/bloom-filter-sizing.md
파라미터 결정 공식과 false positive rate 관계.

### docs/concepts/sparse-index-scan.md
블록 범위 탐색 경로와 dense index 대비 장단점.

---

## 사용한 도구 요약

| 도구 | 용도 |
|------|------|
| Go 1.26.0 | 언어 런타임 |
| `go test ./...` | 테스트 실행 |
| `shared/hash` | MurmurHash3, CRC32 |
| `shared/serializer` | 레코드 직렬화 |
| `shared/fileio` | 파일 I/O |
| `math` | Bloom filter 파라미터 최적화 |

외부 패키지 의존성: **없음**
