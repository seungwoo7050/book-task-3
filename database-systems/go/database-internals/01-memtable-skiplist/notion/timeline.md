# 개발 타임라인 — 01 MemTable SkipList

이 문서는 프로젝트를 처음부터 재현할 수 있도록, 개발 과정을 시간순으로 기록한다.
소스코드에서는 알 수 없는 CLI 명령, 디렉터리 구성 판단, 실행 결과 등을 포함한다.

---

## Phase 0: 프로젝트 초기화

### 디렉터리 생성

```bash
mkdir -p go/database-internals/01-memtable-skiplist/{cmd/skiplist-demo,internal/skiplist,tests,problem/{code,data,script},docs/{concepts,references}}
```

### Go 모듈 초기화

```bash
cd go/database-internals/01-memtable-skiplist
go mod init study.local/database-internals/01-memtable-skiplist
```

- 모듈 경로에 `study.local`을 사용한 이유: 이 프로젝트는 퍼블릭 레지스트리에 배포할 의도가 없다. `study.local` 네임스페이스로 로컬 전용임을 명시했다.
- Go 버전은 `1.26.0`을 사용했다.

### go.work 등록

workspace 루트의 `go.work`에 이 모듈을 등록해야 IDE에서 cross-module 참조가 동작한다.
단, 테스트나 빌드 시에는 `GOWORK=off`를 써서 해당 모듈만 독립적으로 검증한다.

```bash
# workspace 루트에서
go work use go/database-internals/01-memtable-skiplist
```

---

## Phase 1: 문제 정의

### 레거시 프로젝트에서 요구사항 추출

원본 `legacy/storage-engine/lsm-tree-core/problem/README.md`에서 MemTable 부분만 분리했다.
SkipList에 해당하는 요구사항을 5개(R1-R5)로 정리해 `problem/README.md`에 기록했다:

- R1: 정렬 삽입 (키 사전순 유지)
- R2: 세 가지 상태를 구분하는 조회 (Present / Tombstone / Missing)
- R3: 물리 삭제 대신 톰스톤
- R4: 키 오름차순 순회
- R5: 근사 바이트 크기 추적

### 스타터 코드 작성

원본 JS skeleton을 참고하되, Go API로 재설계했다.

```bash
# problem/code/skiplist.skeleton.go 생성
```

스켈레톤 파일은 모든 메서드가 빈 상태로 `// TODO:` 주석만 달려 있다.
`ValueState` 상수, `Entry` 구조체, `SkipList` 타입과 `New()` 생성자, 그리고 `Put`, `Delete`, `Get`, `Entries`, `Size`, `ByteSize`, `Clear` 메서드 시그니처를 정의했다.

---

## Phase 2: 핵심 구현

### 파일 위치

구현 코드는 `internal/skiplist/skiplist.go` 한 파일에 모두 담았다.
`internal/` 하위에 둔 이유는 Go 컨벤션상 패키지 외부에서의 직접 import를 차단하기 위해서다. 이 SkipList는 MemTable 내부 구현이지, 외부 API가 아니다.

### 구현 순서

1. **상수 및 타입 정의**
   - `maxLevel = 16`: SkipList 최대 레벨. $\log_2(65536) = 16$이므로, 6만 개 수준의 키에서 $O(\log n)$ 보장.
   - `probability = 0.5`: 레벨 승격 확률.
   - `nodeOverhead = 64`: 노드당 근사 메모리 오버헤드(바이트).
   - `ValueState` enum: `Missing`, `Present`, `Tombstone`.
   - `Entry` struct: 순회 결과를 담는 DTO.
   - `node` struct: 키, 값 포인터, forward 슬라이스.

2. **`New()` 생성자**
   - 고정 시드(`seed=7`)로 `math/rand.Rand` 인스턴스 생성.
   - header 노드를 maxLevel 높이로 초기화.

3. **`put()` 내부 메서드** — 가장 핵심적인 로직
   - 탑-다운 탐색으로 각 레벨의 삽입 직전 노드를 `update[]`에 기록.
   - 기존 키가 있으면 값만 교체하고 byteSize 차이를 반영.
   - 새 키면 랜덤 레벨 생성 → 필요 시 SkipList 레벨 확장 → forward 포인터 연결.

4. **`Put()`, `Delete()`** — `put()`의 래퍼
   - `Put`: 값의 복사본을 만들어 포인터로 전달.
   - `Delete`: `nil` 포인터를 전달해 tombstone 생성.

5. **`Get()`**
   - 탑-다운 탐색 후 레벨 0에서 키 매칭.
   - 값 포인터가 `nil`이면 `Tombstone`, 노드가 없으면 `Missing`.

6. **`Entries()`**
   - 레벨 0 연결 리스트를 순차 순회하며 슬라이스로 수집.

7. **`Size()`, `ByteSize()`, `Clear()`**
   - 필드 반환 또는 초기화.

---

## Phase 3: 데모 CLI 작성

```bash
# cmd/skiplist-demo/main.go 생성
```

데모는 세 개의 키를 넣고, 하나를 삭제한 뒤, 전체를 순회하는 간단한 시나리오다.

### 실행

```bash
cd go/database-internals/01-memtable-skiplist
GOWORK=off go run ./cmd/skiplist-demo
```

### 예상 출력

```
ordered entries:
- apple => green
- banana => <tombstone>
- carrot => orange
size=3 byteSize=...
```

banana가 tombstone으로 표시되면서도 순회 결과에 포함되는 것이 핵심 확인 포인트다.

---

## Phase 4: 테스트 작성 및 검증

### 테스트 파일 위치

`tests/skiplist_test.go` — 프로젝트 루트의 `tests/` 디렉터리에 별도 패키지(`package tests`)로 분리했다.
`internal/skiplist` 패키지의 공개 API만으로 테스트하므로, black-box 스타일이다.

### 테스트 실행

```bash
cd go/database-internals/01-memtable-skiplist
GOWORK=off go test ./...
```

### 개별 테스트 실행 (디버깅 시)

```bash
GOWORK=off go test ./tests/ -run TestDeleteProducesTombstone -v
```

### 테스트 케이스 목록

| 테스트명 | 검증 대상 |
|----------|----------|
| `TestPutAndGet` | 기본 삽입 후 조회 |
| `TestMissingKey` | 존재하지 않는 키 조회 시 Missing 상태 |
| `TestUpdateKeepsLogicalSize` | 같은 키 갱신 시 Size()가 증가하지 않음 |
| `TestManyInserts` | 1000개 삽입 후 중간 키 존재 확인 |
| `TestDeleteProducesTombstone` | 삭제 후 Tombstone 상태, Size 유지 |
| `TestEntriesStaySorted` | 삽입 순서와 무관하게 오름차순 정렬 |
| `TestEntriesIncludeTombstones` | 톰스톤이 Entries에 포함됨 |
| `TestByteSizeTracking` | 빈 상태 0, 삽입 후 양수 |
| `TestClear` | Clear 후 Size, ByteSize, Get 모두 초기화 |

---

## Phase 5: 개념 문서 작성

### docs/concepts/skiplist-invariants.md

SkipList의 핵심 불변량 세 가지를 정리:
- 레벨 0은 전체 키셋의 오름차순 연결 리스트
- 상위 레벨은 레벨 0의 부분집합 숏컷
- 톰스톤이 키 순서를 깨지 않음

### docs/references/README.md

참고 자료 목록:
- 레거시 프로젝트 경로
- *Database Internals*, Chapter 3

---

## 사용한 도구 요약

| 도구 | 용도 |
|------|------|
| Go 1.26.0 | 언어 런타임 및 빌드 |
| `go mod init` | 모듈 초기화 |
| `go work use` | workspace에 모듈 등록 |
| `go test ./...` | 테스트 실행 |
| `go run ./cmd/skiplist-demo` | 데모 실행 |
| `GOWORK=off` | 모듈 독립 빌드/테스트 시 workspace 격리 |

외부 패키지 의존성: **없음** (표준 라이브러리 `math/rand`만 사용)
