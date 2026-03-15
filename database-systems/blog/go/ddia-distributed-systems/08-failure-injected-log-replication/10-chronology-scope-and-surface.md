# 10 범위를 다시 좁히기: failure 종류보다 복제 경로를 먼저 보기

이 project를 다시 읽을 때 이름만 보면 네트워크 장애 시뮬레이터처럼 느껴질 수 있다. 하지만 문제 문서와 구현을 함께 보면 실제 중심은 failure catalog가 아니라 매우 작은 log replication path다. failure injection은 그 path를 흔들어 보는 도구일 뿐이다.

## Session 1 — problem 문서가 고정하는 핵심

[`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/problem/README.md)는 질문을 딱 다섯 개로 압축한다.

- single leader가 append-only log를 가진다.
- follower에게 `append`와 `ack`를 주고받는다.
- harness가 `drop`, `duplicate`, `pause`를 주입한다.
- lagging follower는 retry로 따라온다.
- commit index는 quorum ack 기준으로만 오른다.

그리고 범위 밖도 분명하다.

- full Raft term/vote
- dynamic membership
- snapshotting
- disk persistence
- cross-shard routing

즉 이 lab은 consensus가 아니라 "leader가 이미 있다고 할 때 replication path가 실패를 어떻게 견디는가"를 보는 단계다.

## Session 2 — 구현의 중심은 `Leader`, `Follower`, `NetworkHarness`

핵심 구현 [`internal/replication/replication.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/internal/replication/replication.go)는 세 덩어리로 나뉜다.

- `Leader`: log, local store, `nextIndex`, `matchIndex`, `commitIndex`
- `Follower`: log, local store, `appliedCount`
- `NetworkHarness`: pause, drop, duplicate rule

이 구조를 보면 failure injection이 replication logic 밖에 따로 붙어 있다는 점이 중요하다. 네트워크 하네스는 메시지를 흔들 뿐이고, state machine consistency는 leader/follower 코드가 책임진다. 그래서 문서도 failure 종류를 먼저 나열하기보다, append/ack 경로가 어떤 상태를 잡고 있는지 먼저 설명하는 편이 맞다.

## Session 3 — demo는 commit과 convergence를 서로 다른 장면으로 보여 준다

demo output은 짧지만 정보량이 높다.

```text
drop tick commit=0 node-2=-1 node-3=0
retry tick commit=0 node-2=0 node-3=0
duplicate tick commit=1 node-3-log=2 node-3-applied=2
pause tick commit=2 node-2=1 node-3=2
recover tick commit=2 node-2=2 node-3=2
```

첫 두 줄만 봐도 중요한 사실이 나온다. 첫 tick에서 `node-2`는 아직 못 받았지만 `commit=0`이다. 즉 quorum commit은 follower 전체 convergence와 같은 뜻이 아니다. 다음 글에서는 이 분리를 만드는 코드 경로를 직접 따라간다.
