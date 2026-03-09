# 개발 타임라인 — 02 SSTable Format

이 문서는 프로젝트를 처음부터 재현할 수 있도록, 개발 과정을 시간순으로 기록한다.

---

## Phase 0: 프로젝트 초기화 및 의존성 설정

### 디렉터리 생성

```bash
mkdir -p go/database-internals/02-sstable-format/{cmd/sstable-format,internal/sstable,tests,problem/{code,data,script},docs/{concepts,references}}
```

### Go 모듈 초기화

```bash
cd go/database-internals/02-sstable-format
go mod init study.local/database-internals/02-sstable-format
```

### shared 패키지 의존성 설정

이 프로젝트부터 `go/shared/` 패키지를 사용한다. `go.mod`에 다음을 추가:

```
require study.local/shared v0.0.0
replace study.local/shared => ../../shared
```

`shared` 모듈이 아직 없다면 먼저 생성해야 한다:

```bash
cd go/shared
go mod init study.local/shared
```

`shared/` 아래에는 두 패키지가 있다:
- `serializer/serializer.go`: 바이너리 레코드 직렬화/역직렬화. `Record{Key, Value}`, `EncodeRecord`, `DecodeRecord`, `EncodeAll`, `DecodeAll`.
- `fileio/fileio.go`: 파일 핸들 래퍼. `Open`, `Append`, `ReadAt`, `WriteAt`, `Size`, `Sync`, `Close`.

### go.work 등록

```bash
# workspace 루트에서
go work use go/database-internals/02-sstable-format
```

---

## Phase 1: 문제 정의

### 요구사항 정리 → `problem/README.md`

레거시 `lsm-tree-core`에서 SSTable 파일 포맷 부분만 분리했다.

핵심 요구사항:
1. Data Section: 키 오름차순 레코드의 연속 바이트 배열
2. Index Section: `(key, offset)` 쌍 저장
3. Footer: 맨 끝 8바이트에 두 섹션 크기 기록
4. Tombstone: value length sentinel(`0xFFFFFFFF`)로 보존
5. 파일 reopen 후에도 `LoadIndex`→`Lookup` 동작 보장

---

## Phase 2: shared 패키지 구현 (선행 작업)

### serializer 패키지

`go/shared/serializer/serializer.go` 작성:

1. **`Record` 구조체**: `Key string`, `Value *string`. Value가 nil이면 tombstone.
2. **`TombstoneMarker` 상수**: `math.MaxUint32` (`0xFFFFFFFF`)
3. **`EncodeRecord`**: `[key_len: 4B big-endian][val_len: 4B big-endian][key bytes][value bytes]` 포맷으로 직렬화. tombstone이면 val_len에 `TombstoneMarker`, value bytes는 비움.
4. **`DecodeRecord`**: 역직렬화. 헤더 8바이트에서 길이 추출 → 키/값 바이트 슬라이싱.
5. **`EncodeAll` / `DecodeAll`**: batch 처리.
6. **`StringPtr` 헬퍼**: 테스트에서 live 레코드 구성용.

### fileio 패키지

`go/shared/fileio/fileio.go` 작성:

- `FileHandle` 구조체가 `os.File`을 래핑
- `Open(flags)`: "r", "w", "a" 등 Node.js 스타일 플래그를 Go의 `os.OpenFile` 플래그로 변환
- `ReadAt(position, length)`: 절대 위치 읽기
- `Append(data)`: 끝에 추가
- `Size()`: 파일 크기 반환
- `Sync()`: fsync
- `EnsureDir()`: 디렉터리 자동 생성

---

## Phase 3: SSTable 핵심 구현

### 파일: `internal/sstable/sstable.go`

#### 구현 순서

1. **타입 정의**
   - `IndexEntry{Key string, Offset int64}`: 인덱스 엔트리
   - `SSTable{FilePath, Index, dataSectionSize, indexSectionSize}`: 메인 구조체

2. **`Write(records)` 메서드**
   - 정렬 검증 (`validateSorted`) — 정렬되지 않은 입력은 즉시 에러
   - 각 레코드를 `serializer.EncodeRecord`로 인코딩하며 offset 누적
   - Index Section 구성: offset을 문자열로 변환해 `serializer.Record`로 만들고 `EncodeAll`
   - 섹션 크기가 `uint32` 범위를 초과하면 에러
   - Footer 8바이트 생성 (big-endian `uint32` × 2)
   - Data Section → Index Section → Footer 순서로 파일에 append
   - `Sync()` 호출로 디스크에 확정

3. **`LoadIndex()` 메서드**
   - 파일 끝 8바이트에서 footer 읽기
   - 두 섹션 크기의 합 + 8 = 파일 크기인지 검증
   - Index Section 바이트를 읽어 `serializer.DecodeAll`로 디코딩
   - offset 문자열을 `int64`로 파싱해 `IndexEntry` 슬라이스 구성

4. **`Lookup(key)` 메서드**
   - `binarySearch`로 인덱스에서 키 탐색
   - 찾은 offset에서 헤더 8바이트 읽기 → 레코드 전체 크기 계산 → 레코드 읽기 → 디코딩
   - 반환: `(value *string, found bool, err error)`

5. **`ReadAll()` 메서드**
   - footer에서 Data Section 크기 읽기 → Data Section 전체를 `DecodeAll`

6. **`binarySearch(key)` 내부 메서드**: 표준 이진 탐색

7. **`FileName(dataDir, sequence)` 함수**: `000001.sst` 형식의 파일명 생성

---

## Phase 4: 데모 CLI

### 파일: `cmd/sstable-format/main.go`

3개 레코드(하나는 tombstone)를 임시 디렉터리에 쓰고, 새 인스턴스로 열어서 4개 키를 각각 Lookup하는 시나리오.

### 실행

```bash
cd go/database-internals/02-sstable-format
GOWORK=off go run ./cmd/sstable-format
```

### 예상 출력

```
alpha => 1
beta => 2
gamma => <tombstone>
missing => <missing>
```

---

## Phase 5: 테스트 작성 및 검증

### 파일: `tests/sstable_test.go`

모든 테스트는 `t.TempDir()`로 임시 디렉터리를 사용한다. 테스트 종료 시 자동 정리되므로 디스크 잔여물이 없다.

### 테스트 실행

```bash
cd go/database-internals/02-sstable-format
GOWORK=off go test ./...
```

### 개별 테스트 실행

```bash
GOWORK=off go test ./tests/ -run TestTombstones -v
```

### 테스트 케이스 목록

| 테스트명 | 검증 대상 |
|----------|----------|
| `TestRoundTripSortedEntries` | Write → LoadIndex → Lookup 왕복 |
| `TestMissingKey` | 없는 키 조회 시 found=false |
| `TestTombstones` | tombstone이 found=true, value=nil로 구분됨 |
| `TestReadAll` | Data Section 전체 순차 디코딩 |
| `TestLargeDataset` | 1000개 레코드에서 이진 탐색 정확성 |
| `TestMalformedFooter` | 깨진 파일에서 LoadIndex 에러 반환 |

---

## Phase 6: 개념 문서 작성

### docs/concepts/sstable-layout.md
파일의 3-섹션 구조, tombstone의 sentinel 표현 정리.

### docs/concepts/lookup-path.md
reopen 시 footer → index 적재 → binary search → record read 경로 정리.

---

## 사용한 도구 요약

| 도구 | 용도 |
|------|------|
| Go 1.26.0 | 언어 런타임 및 빌드 |
| `go mod init` | 모듈 초기화 |
| `go mod edit -require` / `replace` | shared 패키지 의존성 설정 |
| `go work use` | workspace 등록 |
| `go test ./...` | 테스트 실행 |
| `go run ./cmd/sstable-format` | 데모 실행 |
| `t.TempDir()` | 테스트용 임시 디렉터리 (자동 정리) |

외부 패키지 의존성: **없음** (shared 패키지도 표준 라이브러리만 사용)
