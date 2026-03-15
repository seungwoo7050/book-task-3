# Scope, Election Surface, And First Leader

## 1. 문제 범위는 Raft minimum viable semantics에만 집중한다

[`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/04-raft-lite/problem/README.md) 는 leader election, up-to-date vote rule, AppendEntries consistency, majority commit, higher-term step-down을 요구한다. persistence, membership change, snapshotting, real transport는 뺀다.

즉 이 랩은 production Raft library가 아니라, term과 log 규칙이 어떤 안전성/진행성을 보장하는지 보여 주는 학습용 시뮬레이터다.

## 2. 코드 표면은 Node와 Cluster 두 층으로 나뉜다

핵심 구현은 [`raft.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/04-raft-lite/internal/raft/raft.go)에 있다.

- `Node`: state, term, votedFor, log, commit index, peer replication state
- `Cluster`: RPC delivery, ticking, leader lookup, node up/down

즉 protocol semantics는 node에 있고, 네트워크는 실제 socket이 아니라 `sendRPC` callback과 cluster `deliverRPC()`로 추상화된다.

## 3. demo는 선출과 commit의 가장 작은 happy path를 보여 준다

2026-03-14에 아래 명령을 다시 실행했다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/04-raft-lite
GOWORK=off go run ./cmd/raft-lite
```

출력은 아래였다.

```text
leader=n1 commit=0 log_len=1
```

이 출력은 세 가지를 보여 준다.

- 고정 election TTL 덕분에 `n1`이 먼저 leader가 된다
- client request 하나가 leader log에 append된다
- 그 entry는 majority replication 뒤 `commit=0`까지 올라간다

즉 현재 demo는 합의 전체보다 "선출된 leader가 current-term entry를 commit할 수 있다"는 최소 happy path를 보여 준다.

## 4. 추가 재실행으로 failover와 multi-entry commit을 고정했다

이번에 project root 내부 임시 Go 파일로 추가 재실행을 돌린 결과는 아래였다.

```text
first_leader n1 1
commit_after_repl 1 2
failover_leader n2 2
```

이 결과는 세 가지를 보여 준다.

- 첫 leader는 term 1에서 `n1`이다
- 두 개의 command를 append한 뒤 leader commit index는 `1`까지 오른다
- 첫 leader를 down시키면 term 2에서 `n2`가 새 leader가 된다

즉 단일 leader 보장과 higher term 기반 교체가 실제로 관찰된다.
