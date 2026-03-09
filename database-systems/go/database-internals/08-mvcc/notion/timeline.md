# 08-mvcc 개발 타임라인

## Phase 0 — 프로젝트 초기화

```bash
mkdir -p go/database-internals/08-mvcc
cd go/database-internals/08-mvcc

go mod init study.local/database-internals/08-mvcc
```

디렉터리 구조 생성:
```bash
mkdir -p cmd/mvcc
mkdir -p internal/mvcc
mkdir -p tests
mkdir -p docs/concepts docs/references
mkdir -p problem/code problem/data problem/script
```

이전 프로젝트들(01~07)과 달리, 이 프로젝트는 shared 패키지에 의존하지 않는다. 파일 I/O, 직렬화, 해시 함수 없이 순수 인메모리 동시성 제어만 다룬다. `go.mod`에 `replace` 디렉티브도 필요 없다.

## Phase 1 — 문제 정의 및 설계 문서 작성

### 1-1. problem/README.md 작성
- 목적: 스냅샷 격리 기반 MVCC 트랜잭션 매니저 구현
- 출처: `legacy/transaction-engine/mvcc` 레거시 코드 참조
- 핵심 요구사항 정리:
  - 버전 체인 저장소 (VersionStore)
  - 스냅샷 가시성 (Snapshot Visibility)
  - First-Committer-Wins 충돌 감지
  - 구버전 가비지 컬렉션

### 1-2. docs/concepts/ 작성
```bash
# 스냅샷 가시성 규칙 문서화
cat > docs/concepts/snapshot-visibility.md << 'EOF'
# Snapshot Visibility
- transaction은 시작 시점의 committed watermark를 snapshot으로 잡는다.
- read는 snapshot 이하의 committed version만 볼 수 있다.
- 자기 자신의 uncommitted write는 예외적으로 read-your-own-writes로 보인다.
EOF

# 쓰기 충돌 규칙 문서화
cat > docs/concepts/write-conflict.md << 'EOF'
# Write Conflict
- 이 프로젝트는 first-committer-wins 규칙을 사용한다.
- 내 snapshot 이후에 다른 committed transaction이 같은 key를 썼다면 commit은 실패한다.
- abort는 해당 tx가 쓴 version만 version chain에서 제거한다.
EOF
```

## Phase 2 — VersionStore 구현

파일: `internal/mvcc/mvcc.go`

### 2-1. Version 구조체 정의
```go
type Version struct {
    Value   any
    TxID    int
    Deleted bool
}
```
- `any` 타입으로 값의 유연성 확보
- `Deleted` 플래그로 tombstone 표현 (이전 프로젝트들의 sentinel 값 방식과 다름)

### 2-2. VersionStore 구현
```go
type VersionStore struct {
    Store map[string][]Version
}
```

핵심 메서드 4개를 순서대로 구현:

1. **Append**: TxID 내림차순 삽입 정렬. `copy`로 한 칸씩 밀어서 삽입 위치 확보.
2. **GetVisible**: 체인을 앞에서 순회, `TxID ≤ snapshot && committed[TxID]` 첫 번째 반환.
3. **RemoveByTxID**: abort 시 특정 트랜잭션 버전 제거. 슬라이스가 비면 키 자체 삭제.
4. **GC**: `minSnapshot` 기준으로 old 버전 중 최신 1개만 보존.

### 2-3. 설계 결정 기록
- 삽입 정렬 vs append + sort: 대부분 맨 앞 삽입이므로 삽입 정렬이 효율적
- 포인터 반환 시 복사: `copyVersion := version` → 외부 수정 방어
- GC에서 old[0] 보존: 활성 트랜잭션의 스냅샷 읽기 보장

## Phase 3 — TransactionManager 구현

### 3-1. 트랜잭션 상태 모델
```go
const (
    txActive    = "active"
    txCommitted = "committed"
    txAborted   = "aborted"
)
```
열거형 대신 문자열 상수 사용. 상태 전이: active → committed 또는 active → aborted.

### 3-2. Transaction 구조체
```go
type Transaction struct {
    Snapshot int
    Status   string
    WriteSet map[string]bool
}
```
- `Snapshot`: Begin 시점의 committed watermark
- `WriteSet`: 이 트랜잭션이 쓴 키 집합 (충돌 감지 + 롤백용)

### 3-3. TransactionManager 구조체
```go
type TransactionManager struct {
    NextTxID     int
    VersionStore *VersionStore
    Transactions map[int]*Transaction
    Committed    map[int]bool
}
```
- `NextTxID`: 단조 증가 카운터 (1부터 시작)
- `Committed`: 빠른 committed 여부 조회용 별도 맵

### 3-4. Begin 구현
- NextTxID 할당 후 증가
- `Committed` 맵에서 최대 ID를 찾아 snapshot으로 설정
- 새 Transaction 등록

### 3-5. Read 구현 (이중 경로)
1. WriteSet에 해당 키가 있으면 → 자기 txID 버전을 직접 탐색 (read-your-own-writes)
2. 아니면 → `GetVisible(key, snapshot, committed)` 호출

### 3-6. Write / Delete 구현
- VersionStore.Append 호출 + WriteSet 기록
- Delete은 `Deleted: true`로 append

### 3-7. Commit 구현 (충돌 감지)
- WriteSet의 모든 키에 대해 체인 전체 검사
- 조건: `version.TxID > tx.Snapshot && version.TxID != txID && committed[version.TxID]`
- 충돌 시: `abortInternal` 자동 호출 + error 반환
- 통과 시: status를 committed로 변경, `Committed[txID] = true`

### 3-8. Abort 구현
- WriteSet의 모든 키에 대해 `RemoveByTxID` 호출 → 물리적 버전 제거
- status를 aborted로 변경

### 3-9. GC 구현
- 활성 트랜잭션 중 최소 snapshot을 `minSnapshot`으로 계산
- `VersionStore.GC(minSnapshot)` 호출

### 3-10. activeTx 헬퍼
- 존재하지 않거나 active가 아닌 트랜잭션 접근 시 panic

## Phase 4 — 테스트 작성

파일: `tests/mvcc_test.go`

```bash
cd tests
```

### 테스트 실행
```bash
GOWORK=off go test -v ./tests/
```

7개 테스트 케이스:

| 테스트 | 검증 내용 |
|--------|----------|
| TestBasicReadWrite | read-your-own-writes, missing key → nil |
| TestSnapshotIsolation | 커밋된 변경이 이전 스냅샷에 안 보임 |
| TestLatestCommittedValue | 순차 커밋 후 최신 값 조회 |
| TestWriteWriteConflict | 동시 쓰기 → 후커밋자 에러 |
| TestDifferentKeysNoConflict | 다른 키는 충돌 없음 |
| TestAbortAndDelete | abort 롤백 + delete 후 nil |
| TestGC | 가비지 컬렉션 후 최신 값 유지, 체인 축소 |

헬퍼 함수 `mustCommit` 정의: 커밋 실패 시 `t.Fatalf`.

## Phase 5 — 데모 CLI

파일: `cmd/mvcc/main.go`

```bash
cd cmd/mvcc
go run .
```

예상 출력:
```
t2 sees x=v1
```

시나리오:
1. t1이 x="v1" 쓰고 커밋
2. t2 시작 (snapshot=t1)
3. t3 시작, x="v2" 쓰고 커밋
4. t2가 x를 읽음 → "v1" (t3의 변경은 t2의 snapshot 이후이므로 안 보임)

## Phase 6 — 검증 및 마무리

### 전체 테스트 실행
```bash
cd go/database-internals/08-mvcc
GOWORK=off go test -v ./tests/
```

### 코드 포맷팅
```bash
gofmt -w internal/ cmd/ tests/
```

### 코드 정적 분석
```bash
go vet ./...
```

## 구현 통계

| 항목 | 수치 |
|------|------|
| 소스 파일 | 1개 (mvcc.go) |
| 소스 코드 | ~200줄 |
| 테스트 파일 | 1개 (mvcc_test.go) |
| 테스트 케이스 | 7개 |
| 외부 의존성 | 없음 (shared 패키지 미사용) |
| 핵심 구조체 | Version, VersionStore, Transaction, TransactionManager |

## 이전 프로젝트와의 관계

- **01~07 누적**: 이전 프로젝트들은 저장소 엔진의 물리적 계층을 다뤘다. 이 프로젝트는 논리적 계층(트랜잭션)을 다룬다.
- **shared 패키지 미사용**: 파일 I/O, 직렬화, 해시 함수 불필요. 순수 인메모리 로직.
- **Deleted 플래그**: 이전 프로젝트들은 tombstone을 `TombstoneMarker(0xFFFFFFFF)` 같은 센티널 값으로 표현했지만, MVCC에서는 구조체 필드로 명시적 표현.
