# 02-leader-follower-replication 개발 타임라인

## Phase 0 — 프로젝트 초기화

```bash
mkdir -p go/ddia-distributed-systems/02-leader-follower-replication
cd go/ddia-distributed-systems/02-leader-follower-replication

go mod init study.local/ddia-distributed-systems/02-leader-follower-replication
```

디렉터리 구조 생성:
```bash
mkdir -p cmd/replication
mkdir -p internal/replication
mkdir -p tests
mkdir -p docs/concepts docs/references
mkdir -p problem/code problem/data problem/script
```

외부 의존성 없음. shared 패키지도 불필요. 순수 인메모리 로직.

## Phase 1 — 문제 정의

### 1-1. problem/README.md 작성
- Leader가 write를 local store에 적용하면서 append-only log에 기록
- Follower가 마지막 적용 offset 이후의 entry만 받아 적용
- 출처: `legacy/distributed-cluster/replication`

### 1-2. docs/concepts/ 작성
- `log-shipping.md`: "store state 자체"보다 "state를 만든 ordered mutation stream"을 보내는 것이 핵심
- `idempotent-follower.md`: `offset ≤ lastAppliedOffset`인 entry를 건너뛰어 재전송 안전성 확보

## Phase 2 — ReplicationLog 구현

파일: `internal/replication/replication.go`

### 2-1. LogEntry 구조체
```go
type LogEntry struct {
    Offset    int
    Operation string  // "put" | "delete"
    Key       string
    Value     *string // nil for delete
}
```
- `*string`: delete 시 값이 없음을 nil로 표현

### 2-2. ReplicationLog
```go
type ReplicationLog struct {
    entries []LogEntry
}
```

메서드 3개:
- **Append**: `len(entries)`를 offset으로 사용 → 순차 증가 보장
- **From(offset)**: 슬라이스 슬라이싱으로 O(1) 조회, 방어적 복사
- **LatestOffset**: `len(entries) - 1` 반환

### 2-3. stringPtr 헬퍼
```go
func stringPtr(value string) *string {
    copyValue := value
    return &copyValue
}
```
- 값 복사 후 포인터 반환 — 루프 변수 캡처 방지

## Phase 3 — Leader 구현

### 3-1. Leader 구조체
```go
type Leader struct {
    store map[string]string
    log   *ReplicationLog
}
```
- 로컬 store와 replication log를 동시에 유지

### 3-2. Put / Delete
- `Put`: store에 저장 + log에 `"put"` entry 추가
- `Delete`: store에서 삭제 + log에 `"delete"` entry 추가
- 반환값: offset (caller에게 기록 위치 전달)

### 3-3. Get / LogFrom / LatestOffset
- `Get`: 로컬 store 조회
- `LogFrom`: replication log의 From 위임
- `LatestOffset`: replication log의 LatestOffset 위임

## Phase 4 — Follower 구현

### 4-1. Follower 구조체
```go
type Follower struct {
    store             map[string]string
    lastAppliedOffset int  // -1로 초기화
}
```
- `lastAppliedOffset = -1`: 아무것도 적용하지 않은 상태

### 4-2. Apply 구현
- `entry.Offset <= lastAppliedOffset` → skip (idempotent)
- `"put"` → store에 저장
- `"delete"` → store에서 삭제
- `lastAppliedOffset` 갱신
- 반환값: 실제 적용된 entry 수

### 4-3. Get / Watermark
- `Get`: 로컬 store 조회
- `Watermark`: `lastAppliedOffset` 반환

## Phase 5 — ReplicateOnce 함수

```go
func ReplicateOnce(leader *Leader, follower *Follower) int {
    entries := leader.LogFrom(follower.Watermark() + 1)
    return follower.Apply(entries)
}
```
- Follower의 watermark + 1부터 Leader의 로그를 가져와 적용
- 이 함수 하나가 전체 복제 사이클을 캡슐화

## Phase 6 — 테스트 작성

파일: `tests/replication_test.go`

```bash
GOWORK=off go test -v ./tests/
```

| 테스트 | 검증 내용 |
|--------|----------|
| TestReplicationLogAssignsSequentialOffsets | offset이 0, 1, 2... 순차 증가 |
| TestFollowerApplyIsIdempotent | 같은 batch 재적용 → 0건 적용, 상태 불변 |
| TestReplicateOnceIncrementalAndDeletes | 증분 복제 + delete 반영 확인 |

테스트에서도 `stringPtr` 헬퍼 별도 정의 (tests 패키지이므로 internal 패키지의 unexported 함수 접근 불가).

## Phase 7 — 데모 CLI

파일: `cmd/replication/main.go`

```bash
cd cmd/replication
go run .
```

예상 출력:
```
alpha deleted
beta=2 watermark=2
```

시나리오:
1. Leader에 alpha=1, beta=2 순서로 Put
2. ReplicateOnce → Follower에 2건 적용
3. Leader에서 alpha Delete
4. ReplicateOnce → Follower에 1건 적용 (delete)
5. Follower 확인: alpha 없음, beta=2, watermark=2

## Phase 8 — 검증 및 마무리

```bash
GOWORK=off go test -v ./tests/
gofmt -w internal/ cmd/ tests/
go vet ./...
```

## 구현 통계

| 항목 | 수치 |
|------|------|
| 소스 파일 | 1개 (replication.go) |
| 소스 코드 | ~120줄 |
| 테스트 파일 | 1개 |
| 테스트 케이스 | 3개 |
| 외부 의존성 | 없음 |

## 이전/이후 프로젝트와의 관계

- **01-rpc-framing**: 이 프로젝트의 복제는 in-process 함수 호출. 실제 분산 환경에서는 01의 RPC 위에 올릴 것
- **03-shard-routing**: 한 대 Leader의 용량 한계 → 여러 샤드로 데이터 분산
- **database-internals/04-wal-recovery**: WAL과 replication log의 구조적 유사성 — 둘 다 append-only ordered mutation stream
