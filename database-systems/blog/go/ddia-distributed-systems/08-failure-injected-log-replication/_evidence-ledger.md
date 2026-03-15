# Evidence Ledger

## Source files used

- `problem/README.md`
  - 구현 범위와 제외 항목을 먼저 고정했다.
- `README.md`
  - 검증 명령과 공개 demo surface를 다시 확인했다.
- `docs/concepts/failure-injection-harness.md`
  - drop, duplicate, pause가 각각 어떤 질문을 만들기 위한 장치인지 확인했다.
- `docs/concepts/quorum-commit-and-retry.md`
  - commit과 convergence를 분리해서 읽어야 하는 이유를 확인했다.
- `internal/replication/replication.go`
  - `AppendPut`, `advanceCommit`, `HandleAppend`, `NetworkHarness.Route`를 직접 추적했다.
- `tests/replication_test.go`
  - drop retry, duplicate idempotency, paused follower recovery를 확인했다.
- `cmd/failure-replication/main.go`
  - 공개 데모가 어떤 시퀀스로 상태를 드러내는지 다시 확인했다.

## Commands rerun

```bash
GOWORK=off go test ./...
GOWORK=off go run ./cmd/failure-replication
```

## Key outputs

```text
ok  	study.local/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/tests	(cached)
drop tick commit=0 node-2=-1 node-3=0
retry tick commit=0 node-2=0 node-3=0
duplicate tick commit=1 node-3-log=2 node-3-applied=2
pause tick commit=2 node-2=1 node-3=2
recover tick commit=2 node-2=2 node-3=2
```

## Manual boundary check

임시 체크를 추가했다가 제거하고 아래를 기록했다.

```text
commit=-1 leader=true:1 node2=true:1 node3=true:1
```

이 결과는 leader local store뿐 아니라 append를 받은 follower store도 quorum commit보다 먼저 갱신된다는 점을 실행으로 확인한 것이다.

## Inferences called out explicitly

- client-visible committed read rule이 정의되지 않았다는 점은 leader/follower `Read` API와 commit 사용 위치를 함께 보고 판단했다.
- convergence가 background retry에 맡겨진다는 점은 `nextIndex`, `outgoingAppends`, demo 출력의 조합에서 읽었다.
