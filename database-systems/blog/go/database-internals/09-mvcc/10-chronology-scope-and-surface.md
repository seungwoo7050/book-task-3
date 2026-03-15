# Scope, Transaction Surface, And First Snapshot

## 1. 문제 범위는 snapshot isolation의 최소 규칙에만 집중한다

[`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/09-mvcc/problem/README.md)는 snapshot visibility, read-your-own-write, first-committer-wins, abort cleanup, GC를 요구한다. predicate locking, phantom read 제어, distributed transaction, full SQL transaction manager는 뺀다.

즉 이 랩은 MVCC 일반론보다 "version chain과 transaction metadata만으로 어떤 읽기/쓰기 규칙을 만들 수 있는가"를 작게 보여 주는 단계다.

## 2. 코드 표면은 VersionStore와 TransactionManager 두 층으로 나뉜다

핵심 구현은 [`mvcc.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/09-mvcc/internal/mvcc/mvcc.go)에 있다.

- `VersionStore`: key별 version chain을 들고 append/remove/gc를 담당한다.
- `TransactionManager`: snapshot 부여, read/write/delete, commit/abort, committed set 관리를 담당한다.

이 분리 덕분에 "어떤 version들이 존재하는가"와 "그중 어떤 version이 visible한가"를 따로 읽을 수 있다.

## 3. demo는 snapshot visibility를 한 줄로 보여 준다

2026-03-14에 아래 명령을 다시 실행했다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/09-mvcc
GOWORK=off go run ./cmd/mvcc
```

출력은 아래였다.

```text
t2 sees x=v1
```

demo 흐름은 단순하다.

1. `t1`이 `x=v1`을 commit한다.
2. `t2`가 begin해서 snapshot을 잡는다.
3. `t3`가 `x=v2`를 commit한다.
4. `t2`는 여전히 `v1`을 본다.

즉 later commit이 있어도 transaction 시작 시점 snapshot이 그대로 읽기 경계를 만든다.

## 4. 추가 재실행으로 conflict와 GC도 고정했다

이번에 project root 내부 임시 Go 파일로 추가 재실행을 돌린 결과는 아래였다.

```text
snapshot_read v1
conflict_error true
chain_after_conflict 1
gc_chain_len 1
```

이 결과는 네 가지를 보여 준다.

- snapshot visibility는 demo와 같은 방식으로 유지된다
- 같은 key에 대한 늦은 commit은 conflict로 실패한다
- conflict로 abort된 tx의 version은 chain에서 제거된다
- GC 뒤에는 오래된 version chain이 길게 남지 않는다
