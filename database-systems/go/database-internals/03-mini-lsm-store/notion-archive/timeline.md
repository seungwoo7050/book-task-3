# 개발 타임라인 — 03 Mini LSM Store

이 문서는 프로젝트를 처음부터 재현할 수 있도록, 개발 과정을 시간순으로 기록한다.

---

## Phase 0: 프로젝트 초기화

### 디렉터리 생성

```bash
mkdir -p go/database-internals/03-mini-lsm-store/{cmd/mini-lsm-store,internal/{lsmstore,skiplist,sstable},tests,problem/{code,data,script},docs/{concepts,references}}
```

### Go 모듈 초기화

```bash
cd go/database-internals/03-mini-lsm-store
go mod init study.local/database-internals/03-mini-lsm-store
```

### 의존성 설정

`go.mod`에 shared 패키지 의존성 추가:

```
require study.local/shared v0.0.0
replace study.local/shared => ../../shared
```

### go.work 등록

```bash
# workspace 루트에서
go work use go/database-internals/03-mini-lsm-store
```

---

## Phase 1: 내부 패키지 복사

이전 프로젝트의 도메인 코드를 `internal/` 하위에 복사한다. cross-module import 대신 자급자족 방식을 선택했다.

### SkipList 복사

```bash
cp go/database-internals/01-memtable-skiplist/internal/skiplist/skiplist.go \
   go/database-internals/03-mini-lsm-store/internal/skiplist/skiplist.go
```

복사한 뒤 package 선언이 `package skiplist`로 동일한지 확인.

### SSTable 복사

```bash
cp go/database-internals/02-sstable-format/internal/sstable/sstable.go \
   go/database-internals/03-mini-lsm-store/internal/sstable/sstable.go
```

SSTable은 `shared/serializer`와 `shared/fileio`를 import하므로, `go.mod`의 `replace` 경로가 정확해야 한다.

### 복사 후 빌드 확인

```bash
cd go/database-internals/03-mini-lsm-store
GOWORK=off go build ./...
```

---

## Phase 2: LSM Store 핵심 구현

### 파일: `internal/lsmstore/store.go`

#### 구현 순서

1. **`LSMStore` 구조체 정의**
   - `DataDir`: SSTable 파일이 저장될 디렉터리
   - `MemtableSizeThreshold`: flush 트리거 기준 (기본 64KB)
   - `Memtable`: 현재 active SkipList
   - `ImmutableMemtable`: flush 중인 SkipList (보통 nil)
   - `SSTables`: newest-first 정렬된 SSTable 슬라이스
   - `nextSequence`: 다음 SSTable 파일 번호

2. **`New(dataDir, threshold)` 생성자**
   - threshold가 0이면 기본값(64KB) 사용
   - 빈 SkipList로 Memtable 초기화, nextSequence는 1부터

3. **`Open()` 메서드**
   - `fileio.EnsureDir`로 디렉터리 생성
   - `fileio.ListFiles(dataDir, ".sst")`로 기존 SSTable 파일 스캔
   - 각 파일에 대해 `LoadIndex()` 호출
   - 파일명에서 sequence 번호 추출, nextSequence 갱신
   - SSTable 목록을 역순(newest-first)으로 정렬

4. **`Put(key, value)` 메서드**
   - SkipList에 삽입 → `maybeFlush()` 호출

5. **`Delete(key)` 메서드**
   - SkipList에 tombstone 삽입 → `maybeFlush()` 호출

6. **`Get(key)` 메서드** — newest-first 읽기 경로
   - Active MemTable 조회 → Missing이 아니면 반환
   - Immutable MemTable 조회 → Missing이 아니면 반환
   - SSTable 순회 (newest→oldest) → found면 반환

7. **`flush()` 내부 메서드**
   - Active Memtable → ImmutableMemtable 전환
   - 새 빈 SkipList를 Active로
   - ImmutableMemtable의 Entries를 `serializer.Record` 슬라이스로 변환
   - SSTable Write → SSTables 맨 앞에 추가
   - ImmutableMemtable = nil

8. **`maybeFlush()` 내부 메서드**
   - ByteSize < threshold면 아무것도 안 함

9. **`ForceFlush()` / `Close()` 메서드**
   - ForceFlush: Size가 0이 아니면 flush
   - Close: ForceFlush 호출

---

## Phase 3: 데모 CLI

### 파일: `cmd/mini-lsm-store/main.go`

시나리오:
1. 작은 threshold(128B)로 store 생성
2. "apple"과 "banana" put → ForceFlush
3. "banana"를 새 값("ripe")으로 업데이트
4. "apple" 삭제
5. 세 키 조회 → MemTable 우선순위와 tombstone 확인

### 실행

```bash
cd go/database-internals/03-mini-lsm-store
GOWORK=off go run ./cmd/mini-lsm-store
```

### 예상 출력

```
apple => <tombstone>
banana => ripe
missing => <missing>
```

---

## Phase 4: 테스트 작성 및 검증

### 파일: `tests/lsm_store_test.go`

### 테스트 실행

```bash
cd go/database-internals/03-mini-lsm-store
GOWORK=off go test ./...
```

### 테스트 케이스 목록

| 테스트명 | 검증 대상 |
|----------|----------|
| `TestPutAndGet` | 기본 쓰기→읽기 |
| `TestMissingKey` | 없는 키 조회 |
| `TestUpdate` | 같은 키 갱신 |
| `TestDelete` | tombstone 확인 |
| `TestFlushCreatesSSTable` | threshold 초과 시 자동 flush |
| `TestReadAfterForceFlush` | ForceFlush 후 SSTable에서 읽기 |
| `TestMemtableWinsOverSSTable` | MemTable 값이 SSTable보다 우선 |
| `TestTombstoneAcrossLevels` | cross-level tombstone |
| `TestPersistenceAfterReopen` | Close→Open 후 데이터 유지 |

---

## Phase 5: 개념 문서 작성

### docs/concepts/flush-lifecycle.md
active → immutable → SSTable 전환 과정.

### docs/concepts/read-path.md
active MemTable → immutable → newest SSTable 순서의 읽기 경로.

---

## 사용한 도구 요약

| 도구 | 용도 |
|------|------|
| Go 1.26.0 | 언어 런타임 |
| `go mod init` | 모듈 초기화 |
| `go build ./...` | 복사 후 빌드 확인 |
| `go test ./...` | 테스트 실행 |
| `go run ./cmd/mini-lsm-store` | 데모 실행 |
| `cp` | 이전 프로젝트 소스 복사 |
| `t.TempDir()` | 테스트별 임시 디렉터리 (자동 정리) |

외부 패키지 의존성: **없음** (shared 패키지는 표준 라이브러리만 사용)
