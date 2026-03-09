# 개발 타임라인 — 04 WAL Recovery

이 문서는 프로젝트를 처음부터 재현할 수 있도록, 개발 과정을 시간순으로 기록한다.

---

## Phase 0: 프로젝트 초기화

### 디렉터리 생성

```bash
mkdir -p go/database-internals/04-wal-recovery/{cmd/wal-recovery,internal/{wal,store,skiplist,sstable},tests,problem/{code,data,script},docs/{concepts,references}}
```

### Go 모듈 초기화

```bash
cd go/database-internals/04-wal-recovery
go mod init study.local/database-internals/04-wal-recovery
```

### 의존성 설정

`go.mod`:

```
require study.local/shared v0.0.0
replace study.local/shared => ../../shared
```

shared 패키지의 `hash` 서브패키지를 새로 사용한다. `shared/hash/hash.go`에 `CRC32(data []byte) uint32` 함수가 있어야 한다.

### go.work 등록

```bash
go work use go/database-internals/04-wal-recovery
```

---

## Phase 1: 내부 패키지 복사

### SkipList, SSTable 복사

03번과 동일하게, 이전 프로젝트의 skiplist와 sstable 코드를 `internal/`에 복사한다.

```bash
cp go/database-internals/01-memtable-skiplist/internal/skiplist/skiplist.go \
   go/database-internals/04-wal-recovery/internal/skiplist/skiplist.go

cp go/database-internals/02-sstable-format/internal/sstable/sstable.go \
   go/database-internals/04-wal-recovery/internal/sstable/sstable.go
```

### shared/hash 패키지 확인

```bash
cat go/shared/hash/hash.go
```

`CRC32(data []byte) uint32` 함수가 있어야 한다. 없으면 작성해야 한다.
표준 라이브러리의 `hash/crc32`를 사용하며 IEEE polynomial을 쓴다.

---

## Phase 2: WAL 구현

### 파일: `internal/wal/wal.go`

#### 구현 순서

1. **상수 정의**: `OpPut = 0x01`, `OpDelete = 0x02`

2. **`Record` 구조체**: `Type string`, `Key string`, `Value *string`

3. **`WriteAheadLog` 구조체**: `FilePath`, `FsyncEnabled`, `handle *fileio.FileHandle`

4. **`Open()` 메서드**: append 모드(`"a"`)로 파일 열기

5. **`appendRecord()` 내부 메서드** — 핵심 직렬화
   - 헤더 9바이트 구성: `[type 1B][keyLen 4B][valLen 4B]`
   - payload = 헤더 + key bytes + value bytes
   - CRC32(payload) 계산 → 4바이트 prepend
   - 파일에 append
   - fsyncEnabled면 `Sync()` 호출

6. **`AppendPut(key, value)` / `AppendDelete(key)`**: `appendRecord` 래퍼

7. **`Recover()` 메서드** — 핵심 복구 로직
   - 파일 전체를 읽기 모드로 열어 버퍼에 적재
   - offset을 0부터 시작해 순회:
     - 남은 바이트 < 13이면 → break (truncated header)
     - 헤더에서 CRC, type, keyLen, valLen 추출
     - 실제 value 길이 계산 (tombstone이면 0)
     - 남은 바이트 < recordSize면 → break (truncated payload)
     - CRC 검증 실패면 → break (corruption)
     - Record 구성 후 결과에 추가
   - 존재하지 않는 파일은 빈 슬라이스 반환 (에러 아님)

8. **`Close()` 메서드**: 핸들 닫기

---

## Phase 3: DurableStore 구현

### 파일: `internal/store/store.go`

03번의 `LSMStore`를 기반으로 WAL을 통합한다.

#### 주요 변경점 (03번 대비)

1. **`DurableStore` 구조체에 `WALPath`, `writeAheadLog` 필드 추가**

2. **`Open()` 메서드에 WAL recovery 추가**
   - SSTable 로딩 (기존 로직 동일)
   - `wal.Recover()`로 WAL 레코드 읽기
   - 각 레코드를 MemTable에 replay
   - 새 WAL을 append 모드로 열기

3. **`Put()` / `Delete()` 메서드에 WAL append 선행**
   - 기존: `Memtable.Put(key, value)` → `maybeFlush()`
   - 변경: **`writeAheadLog.AppendPut(key, value)`** → `Memtable.Put(key, value)` → `maybeFlush()`

4. **`ForceFlush()` 메서드에 WAL rotation 추가**
   - SSTable 쓰기 (기존 로직)
   - WAL Close → 파일 삭제 → 새 WAL Open
   - MemTable Clear

5. **`Close()` 메서드 변경**
   - 03번: ForceFlush 호출
   - 04번: **WAL만 Close** (flush 없이 닫음 → 다음 Open에서 WAL replay로 복구)

---

## Phase 4: 데모 CLI

### 파일: `cmd/wal-recovery/main.go`

### 실행

```bash
cd go/database-internals/04-wal-recovery
GOWORK=off go run ./cmd/wal-recovery
```

---

## Phase 5: 테스트 작성 및 검증

### 파일: `tests/wal_test.go`

### 테스트 실행

```bash
cd go/database-internals/04-wal-recovery
GOWORK=off go test ./...
```

### 개별 테스트 실행 (corruption 테스트 디버깅 시)

```bash
GOWORK=off go test ./tests/ -run TestStopAtCorruptedRecord -v
```

### 테스트 케이스 목록

| 테스트명 | 검증 대상 |
|----------|----------|
| `TestRecoverPutRecords` | Put append → recover |
| `TestRecoverDeleteRecords` | Delete append → recover |
| `TestRecoverManyRecords` | 500개 레코드 대량 recover |
| `TestStopAtCorruptedRecord` | 정상 레코드 뒤 garbage → 정상 레코드만 복구 |
| `TestRecoverNonexistentAndTruncated` | 빈 파일 / truncated 파일 처리 |
| `TestStoreRecoversFromWALAfterReopen` | Put → Close(no flush) → reopen → WAL replay |
| `TestForceFlushRotatesWAL` | flush 후 WAL이 비었는지, SSTable에서 읽히는지 |

---

## 사용한 도구 요약

| 도구 | 용도 |
|------|------|
| Go 1.26.0 | 언어 런타임 |
| `go mod init` | 모듈 초기화 |
| `go test ./...` | 테스트 실행 |
| `go run ./cmd/wal-recovery` | 데모 실행 |
| `cp` | 이전 프로젝트 소스 복사 |
| `shared/hash` | CRC32 체크섬 계산 |
| `shared/fileio` | 파일 I/O (append, readAll, remove) |
| `os.OpenFile` (테스트) | corruption 시뮬레이션을 위한 직접 파일 쓰기 |

외부 패키지 의존성: **없음**
