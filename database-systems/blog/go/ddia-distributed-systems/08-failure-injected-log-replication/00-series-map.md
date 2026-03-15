# 08 Failure-Injected Log Replication 시리즈 맵

`08 Failure-Injected Log Replication`은 authority가 이미 leader에게 있다고 가정한 뒤, append/ack 복제 경로가 drop, duplicate, pause를 만나도 어떤 규칙까지는 유지하는지를 보는 lab이다. 이번 문서 묶음은 failure 종류를 소개하는 데서 멈추지 않고, quorum commit과 follower convergence, 그리고 commit 전 leader local visibility가 어떻게 갈라지는지까지 분리해 적는다.

## 이번 Todo에서 다시 잡은 질문

- leader는 언제 commit index를 올리고, 언제 follower lag를 그냥 남겨 두는가?
- duplicate append는 왜 follower state를 두 번 바꾸지 않는가?
- commit되지 않은 entry가 leader와 follower read에 언제 보이는가?

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md)
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md)
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md)

## 이번 재작성의 근거

- `database-systems/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/problem/README.md`
- `database-systems/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/README.md`
- `database-systems/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/docs/concepts/failure-injection-harness.md`
- `database-systems/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/docs/concepts/quorum-commit-and-retry.md`
- `database-systems/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/internal/replication/replication.go`
- `database-systems/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/tests/replication_test.go`
- `database-systems/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/cmd/failure-replication/main.go`

## 재검증 명령

```bash
GOWORK=off go test ./...
GOWORK=off go run ./cmd/failure-replication
```

## 보조 문서

- [_evidence-ledger.md](_evidence-ledger.md)
- [_structure-outline.md](_structure-outline.md)

## 이번에 명시적으로 남긴 경계

- commit quorum은 leader 자신을 포함한 majority 기준이다.
- follower convergence는 retry에 맡겨지고, commit과 동시에 일어나지 않는다.
- leader는 entry를 append하는 즉시 local store를 바꾸고, follower도 append를 받는 즉시 apply하므로 visibility가 commit보다 앞선다.
