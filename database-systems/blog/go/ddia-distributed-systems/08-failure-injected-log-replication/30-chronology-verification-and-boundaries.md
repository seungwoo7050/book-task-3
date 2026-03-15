# 30 검증과 경계: failure를 견디지만 consensus는 아니다

이번 Todo에서는 failure 종류를 설명하는 데서 멈추지 않고, 실제 출력이 어떤 경계를 보여 주는지 다시 정리했다. 이 project는 retry와 idempotency를 잘 보여 주지만, full replication protocol이라고 부르기엔 일부러 생략한 것이 많다.

## Session 1 — 재실행 결과

```bash
$ GOWORK=off go test ./...
?   	study.local/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/cmd/failure-replication	[no test files]
?   	study.local/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/internal/replication	[no test files]
ok  	study.local/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/tests	(cached)
```

```bash
$ GOWORK=off go run ./cmd/failure-replication
drop tick commit=0 node-2=-1 node-3=0
retry tick commit=0 node-2=0 node-3=0
duplicate tick commit=1 node-3-log=2 node-3-applied=2
pause tick commit=2 node-2=1 node-3=2
recover tick commit=2 node-2=2 node-3=2
```

이 출력이 바로 세 가지 장면을 보여 준다.

- drop: quorum commit은 되지만 한 follower는 lagging일 수 있다.
- duplicate: 같은 entry 재전달이 follower apply를 두 번 만들지 않는다.
- pause/recover: commit은 유지되지만 convergence는 나중에 따라온다.

## Session 2 — 추가로 확인한 pre-commit visibility 경계

임시 체크를 추가했다가 제거하면서 아래 결과를 확보했다.

```text
commit=-1 leader=true:1 node2=true:1 node3=true:1
```

양쪽 follower의 ack를 모두 drop해서 commit이 전혀 안 된 상황에서도 leader와 append를 받은 follower 둘 다 이미 새 값을 본다는 뜻이다. 이유는 leader `AppendPut()`이 append 즉시 local store를 갱신하고, follower `HandleAppend()`도 commit을 기다리지 않고 append 시점에 `apply()`를 호출하기 때문이다. 이건 source를 얼핏 보면 놓치기 쉬운 차이라서, 이번 문서에는 명시적으로 남겼다.

## Session 3 — 현재 한계

- term, vote, leader transfer가 없으므로 authority 교체는 다루지 않는다.
- persistent log/storage가 없어 restart recovery를 다룰 수 없다.
- out-of-order delivery, ack corruption, long-tail latency가 없다.
- cross-shard routing이나 membership reconfiguration이 없다.
- leader/follower local visibility와 committed visibility를 분리하지만, client-facing read rule은 정의하지 않는다.

그래서 이 project는 "failure-aware log replication path"로는 충분히 유익하지만, consensus protocol이나 production replication engine의 축약판으로 읽으면 과장된다. 정확한 역할은 retry, idempotency, quorum commit의 관계를 작은 하네스에서 투명하게 보여 주는 것이다.
