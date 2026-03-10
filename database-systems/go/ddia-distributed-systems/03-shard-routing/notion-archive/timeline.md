# 03-shard-routing 개발 타임라인

## Phase 0 — 프로젝트 초기화

```bash
mkdir -p go/ddia-distributed-systems/03-shard-routing
cd go/ddia-distributed-systems/03-shard-routing

go mod init study.local/ddia-distributed-systems/03-shard-routing
```

디렉터리 구조 생성:
```bash
mkdir -p cmd/shard-routing
mkdir -p internal/routing
mkdir -p tests
mkdir -p docs/concepts docs/references
mkdir -p problem/code problem/data problem/script
```

### go.mod 의존성 설정
```bash
# shared 패키지 사용 (MurmurHash3)
go mod edit -require study.local/shared@v0.0.0
go mod edit -replace study.local/shared=../../shared
```

이 프로젝트는 `shared/hash` 패키지의 `MurmurHash3` 함수를 사용한다. database-internals 시리즈 이후 처음으로 shared 의존성이 생긴 분산 시스템 프로젝트.

## Phase 1 — 문제 정의

### 1-1. problem/README.md 작성
- Virtual node가 있는 consistent hash ring 구현
- 단일 key 라우팅 + 배치 라우팅
- 노드 추가/제거 시 재배치 key 수 측정
- 출처: `legacy/distributed-cluster/sharding`

### 1-2. docs/concepts/ 작성
- `virtual-nodes.md`: 물리 노드를 `nodeID#v<index>` 형태로 ring 위에 분산 배치
- `rebalance-accounting.md`: 기존 assignment vs 새 assignment 비교로 moved key 수 계산

## Phase 2 — Ring 자료구조 구현

파일: `internal/routing/routing.go`

### 2-1. ringEntry와 Ring 구조체
```go
type ringEntry struct {
    Hash   uint32
    NodeID string
}

type Ring struct {
    VirtualNodes int
    ring         []ringEntry  // Hash 오름차순 정렬
    nodes        map[string]struct{}
}
```
- `ring` 슬라이스: 항상 Hash 기준 오름차순 유지
- `nodes` 맵: 물리 노드 중복 등록 방지

### 2-2. NewRing
- `virtualNodes ≤ 0` → 기본값 150
- 빈 ring과 빈 nodes 맵으로 초기화

### 2-3. AddNode 구현
- 중복 체크: 이미 존재하면 무시
- `VirtualNodes`개의 virtual node 생성
- 해시 키: `nodeID + "#v" + itoa(i)` → `MurmurHash3` (seed=0)
- `slices.IndexFunc`로 정렬 위치 탐색
- 해당 위치에 삽입 (`append + 슬라이스 확장`)
- 끝보다 큰 경우: 맨 뒤에 append

### 2-4. RemoveNode 구현
- nodes 맵에서 제거
- ring에서 해당 nodeID의 모든 entry 필터링
- 새 슬라이스로 교체 (in-place 삭제 대신 필터링)

### 2-5. NodeForKey 구현
- 빈 ring → `("", false)` 반환
- `MurmurHash3(key, 0)` → target hash 계산
- `slices.IndexFunc`로 `hash >= target`인 첫 entry 탐색
- `index == -1` → wrap-around: `index = 0`
- 해당 entry의 NodeID 반환

### 2-6. itoa 헬퍼
- `strconv` 없이 정수 → 문자열 변환
- 수동 나머지 연산으로 각 자릿수 추출

## Phase 3 — Assignments와 MovedKeys

### 3-1. Assignments
```go
func (ring *Ring) Assignments(keys []string) map[string]string
```
- 키 슬라이스에 대해 `key → nodeID` 맵 생성
- `NodeForKey`를 각 키에 호출

### 3-2. MovedKeys
```go
func (ring *Ring) MovedKeys(keys []string, previous map[string]string) int
```
- 현재 ring의 assignment와 `previous` assignment 비교
- `previous[key] != "" && previous[key] != current[key]` → moved 카운트
- 이전에 할당이 없던 키는 "이동"으로 세지 않음

## Phase 4 — Router 래퍼

### 4-1. Router 구조체
```go
type Router struct {
    Ring *Ring
}
```

### 4-2. Route / RouteBatch
- `Route`: 단일 키 → `Ring.NodeForKey` 위임
- `RouteBatch`: 키 배열 → `nodeID → []keys` 그룹핑
  - 실제 분산 시스템에서 노드별 배치 전송에 사용

## Phase 5 — 테스트 작성

파일: `tests/routing_test.go`

```bash
GOWORK=off go test -v ./tests/
```

| 테스트 | 검증 내용 |
|--------|----------|
| TestEmptyAndSingleNodeRouting | 빈 ring → false 반환, 노드 1개 → 모든 키 해당 노드 |
| TestDistributionAndRebalance | 3노드 3000키 분포 20%~50%, 노드 추가 moved 50~500, 제거 후 미라우팅 |
| TestBatchRouting | 2노드 5키 배치 라우팅 → 총 5개 결과 |

테스트에서도 `itoa`와 `keyString` 헬퍼 별도 정의 (tests 패키지이므로).

## Phase 6 — 데모 CLI

파일: `cmd/shard-routing/main.go`

```bash
cd cmd/shard-routing
go run .
```

예상 출력 (해시에 따라 결과가 달라질 수 있음):
```
alpha -> node-X
beta -> node-Y
gamma -> node-Z
```

시나리오: 3노드(64 virtual nodes each) ring 생성, alpha/beta/gamma 라우팅 출력

## Phase 7 — 검증 및 마무리

```bash
GOWORK=off go test -v ./tests/
gofmt -w internal/ cmd/ tests/
go vet ./...
```

## 구현 통계

| 항목 | 수치 |
|------|------|
| 소스 파일 | 1개 (routing.go) |
| 소스 코드 | ~130줄 |
| 테스트 파일 | 1개 |
| 테스트 케이스 | 3개 |
| 외부 의존성 | shared/hash (MurmurHash3) |

## 이전/이후 프로젝트와의 관계

- **shared/hash**: `MurmurHash3` 해시 함수 사용 (database-internals/06-index-filter의 블룸 필터와 동일)
- **02-leader-follower-replication**: 복제(같은 데이터 여러 곳) vs 샤딩(다른 데이터 나눠 저장) — 상호 보완 관계
- **04-raft-lite**: 샤드 내 리더 선출 → consistent hashing과 합쳐져 완전한 분산 시스템 구성
