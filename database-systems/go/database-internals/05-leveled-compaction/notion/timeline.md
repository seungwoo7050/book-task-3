# 개발 타임라인 — 05 Leveled Compaction

이 문서는 프로젝트를 처음부터 재현할 수 있도록, 개발 과정을 시간순으로 기록한다.

---

## Phase 0: 프로젝트 초기화

### 디렉터리 생성

```bash
mkdir -p go/database-internals/05-leveled-compaction/{cmd/leveled-compaction,internal/{compaction,sstable},tests,problem/{code,data,script},docs/{concepts,references}}
```

### Go 모듈 초기화

```bash
cd go/database-internals/05-leveled-compaction
go mod init study.local/database-internals/05-leveled-compaction
```

### 의존성 설정

```
require study.local/shared v0.0.0
replace study.local/shared => ../../shared
```

### go.work 등록

```bash
go work use go/database-internals/05-leveled-compaction
```

---

## Phase 1: 내부 패키지 복사

SSTable 코드를 복사한다.

```bash
cp go/database-internals/02-sstable-format/internal/sstable/sstable.go \
   go/database-internals/05-leveled-compaction/internal/sstable/sstable.go
```

SSTable에 `Get` 메서드가 있어야 한다 (LoadIndex + Lookup 통합). 테스트에서 `compacted.Get("a")` 형태로 호출하기 때문에, SSTable에 편의 메서드를 추가하거나 기존 코드를 확인해야 한다.

```bash
GOWORK=off go build ./...
```

---

## Phase 2: Merge 알고리즘 구현

### 파일: `internal/compaction/compaction.go`

#### 구현 순서

1. **`mergeTwo(newer, older)` 함수**
   - 투 포인터로 두 정렬 배열 merge
   - 같은 키면 newer(왼쪽 인자) 우선

2. **`KWayMerge(sources, dropTombstones)` 함수**
   - sources[0]부터 순차적으로 pairwise merge
   - dropTombstones가 true면 결과에서 Value==nil인 레코드 제거

3. **헬퍼 함수들**
   - `readAll(path)`: SSTable 열어서 전체 레코드 반환
   - `sequenceFileName(sequence)`: `000001.sst` 형식 파일명 생성
   - `cloneLevels(levels)`: level map 깊은 복사

---

## Phase 3: Manager 구현

### 같은 파일: `internal/compaction/compaction.go`

1. **`Manager` 구조체**
   - `DataDir`, `Levels map[int][]string`, `NextSequence int`, `L0MaxFiles int`, `ManifestPath`

2. **`New(dataDir, l0MaxFiles)` 생성자**
   - L0 빈 슬라이스로 초기화, l0MaxFiles 기본값 4

3. **`AddToLevel(level, fileName)`**: 지정 레벨에 파일 추가

4. **`NeedsL0Compaction()`**: L0 파일 수 >= L0MaxFiles

5. **`CompactL0ToL1()` 메서드** — 핵심
   - L0 파일 목록을 reverse하여 newest-first source 배열 구성
   - L1 파일을 older source로 추가
   - `KWayMerge` 호출 (L2가 비어 있으면 dropTombstones=true)
   - 새 SSTable 기록
   - level map 업데이트 → manifest 저장 → 입력 파일 삭제
   - `Result{Added, Removed, DroppedTombstones}` 반환

6. **`SaveManifest()` / `LoadManifest()` 메서드**
   - JSON 직렬화/역직렬화
   - `fileio.AtomicWrite`로 원자적 저장

---

## Phase 4: shared/fileio에 AtomicWrite 추가

`shared/fileio/fileio.go`에 `AtomicWrite(path, data)` 함수가 필요하다:

```go
func AtomicWrite(path string, data []byte) error {
    tmpPath := path + ".tmp"
    if err := os.WriteFile(tmpPath, data, 0o644); err != nil {
        return err
    }
    return os.Rename(tmpPath, path)
}
```

또한 `RemoveFile(path)`, `ListFiles(dir, ext)` 함수도 확인/추가한다.

---

## Phase 5: 테스트 작성 및 검증

### 파일: `tests/compaction_test.go`

### 테스트 실행

```bash
cd go/database-internals/05-leveled-compaction
GOWORK=off go test ./...
```

### 테스트 케이스 목록

| 테스트명 | 검증 대상 |
|----------|----------|
| `TestKWayMergeKeepsNewerValue` | 같은 키 → newer 우선 |
| `TestKWayMergeDropsTombstonesAtDeepestLevel` | deepest level tombstone 제거 |
| `TestCompactL0ToL1` | 전체 compaction 흐름 + 파일 삭제 확인 |
| `TestManifestRoundTrip` | manifest 저장→로드 |

---

## Phase 6: 개념 문서 작성

### docs/concepts/merge-ordering.md
source 배열의 순서 규약과 L0 reverse 필요성.

### docs/concepts/manifest-atomicity.md
compaction 시 파일과 metadata 갱신의 순서와 원자성 전략.

---

## 사용한 도구 요약

| 도구 | 용도 |
|------|------|
| Go 1.26.0 | 언어 런타임 |
| `go test ./...` | 테스트 실행 |
| `go run ./cmd/leveled-compaction` | 데모 실행 |
| `encoding/json` | manifest JSON 직렬화 |
| `os.Rename` | manifest atomic write |
| `fileio.AtomicWrite` | 임시 파일 → rename 패턴 |
| `fileio.RemoveFile` | compaction 후 입력 파일 삭제 |

외부 패키지 의존성: **없음**
