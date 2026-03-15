# Scope, Flush Surface, And First Reads

## 1. 문제는 LSM의 모든 기능이 아니라 최소 orchestration이다

[`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/03-mini-lsm-store/problem/README.md)는 active memtable threshold, immutable swap 후 flush, newest-first read path, tombstone across levels, close/reopen persistence를 요구한다. 반대로 background compaction, concurrent flush, range query, compression은 빼 둔다.

즉 이 프로젝트는 LSM tree 완성본이 아니라, "memtable과 SSTable을 어떤 순서로 엮어야 올바른 lookup semantics가 나오는가"를 검증하는 단계다.

## 2. 코드 표면은 놀랄 만큼 단순하다

핵심 구현은 [`store.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/03-mini-lsm-store/internal/lsmstore/store.go) 한 파일에 모여 있다.

- `Open()`
- `Put()` / `Delete()`
- `Get()`
- `ForceFlush()`
- `Close()`

구조체 필드도 설계 의도를 그대로 드러낸다.

- `Memtable`
- `ImmutableMemtable`
- `SSTables []*sstable.SSTable`
- `nextSequence`

이 네 필드만으로도 현재 LSM lifecycle이 읽힌다. write는 active memtable로 들어가고, flush 중에는 immutable snapshot이 따로 잡히며, 디스크에 내려간 table은 newest-first slice에 등록되고, reopen 뒤 sequence는 파일 이름 기준으로 재계산된다.

## 3. demo는 cross-level 상태를 아주 짧게 보여 준다

2026-03-14에 아래 명령을 다시 실행했다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/03-mini-lsm-store
GOWORK=off go run ./cmd/mini-lsm-store
```

출력은 아래와 같았다.

```text
apple => <tombstone>
banana => ripe
missing => <missing>
```

demo 흐름은 의외로 밀도가 높다.

1. `apple=green`, `banana=yellow`를 active memtable에 넣는다.
2. `ForceFlush()`로 이를 SSTable로 내린다.
3. `banana=ripe`를 새 active memtable에 다시 쓴다.
4. `apple`은 active memtable에서 tombstone으로 지운다.

그래서 lookup 결과는 곧바로 현재 우선순위를 보여 준다. `banana`는 디스크의 old value가 아니라 active memtable의 new value를 읽고, `apple`은 SSTable의 old value가 남아 있어도 active tombstone이 먼저 이긴다.

## 4. 추가 재실행으로 flush와 reopen 관찰값을 고정했다

이번에 프로젝트 루트 내부 임시 Go 파일로 짧은 검증을 더 돌렸다. 결과는 아래였다.

```text
sstables_after_flush 2 000002.sst
beta_active_wins 3
alpha_tombstone true
reopened_sstables 2 000002.sst
reopened_beta 3
reopened_alpha_tombstone true
```

여기서 보이는 핵심은 두 가지다.

- flush 이후 새 table은 slice 앞쪽, 즉 newest 위치에 `000002.sst`로 들어온다.
- reopen 뒤에도 SSTable 등록 순서는 newest-first로 복원되고, latest value와 tombstone semantics가 그대로 유지된다.
