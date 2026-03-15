# Scope, Ordered Log Surface, And First Sync

## 1. 문제 범위는 replication minimum viable path에만 집중한다

[`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication/problem/README.md)는 sequential offset log, put/delete replication, follower watermark 기반 incremental sync, idempotent replay를 요구한다. election, consensus, quorum write, multi-leader는 뺀다.

즉 이 랩은 장애 조치까지 포함한 replication system이 아니라, ordered mutation stream을 follower가 어디까지 따라왔는지 설명하는 가장 작은 모델이다.

## 2. 코드 표면은 log, leader, follower 세 층이면 끝난다

핵심 구현은 [`replication.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication/internal/replication/replication.go)에 모여 있다.

- `ReplicationLog`
- `Leader`
- `Follower`
- `ReplicateOnce()`

여기서 진짜 network protocol은 `leader.LogFrom(follower.Watermark() + 1)` 한 줄로 요약된다. 즉 follower는 leader 상태 전체를 받지 않고, 자기 watermark 이후의 mutation batch만 받는다.

## 3. demo는 delete propagation과 watermark를 함께 보여 준다

2026-03-14에 아래 명령을 다시 실행했다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication
GOWORK=off go run ./cmd/replication
```

출력은 아래였다.

```text
alpha deleted
beta=2 watermark=2
```

이 출력만으로도 세 가지를 확인할 수 있다.

- delete는 follower에서 실제로 key를 숨긴다
- `beta`는 latest replicated value를 가진다
- follower watermark는 현재 offset `2`까지 적용됐음을 나타낸다

## 4. 추가 재실행으로 replay semantics를 고정했다

이번에 project root 내부 임시 Go 파일로 추가 재실행을 돌린 결과는 아래였다.

```text
initial_apply 2 1
duplicate_apply 0 1
incremental_apply 2 3
a_deleted true
b_value 3
```

이 결과는 핵심을 아주 선명하게 보여 준다.

- 첫 sync는 2개 entry를 적용해 watermark를 `1`로 올린다
- 같은 batch를 다시 적용하면 `0`개만 적용한다
- 이후 delete와 overwrite를 추가한 incremental batch는 다시 2개만 적용된다

즉 replay safety는 별도 dedupe map이 아니라 offset 비교만으로 성립한다.
