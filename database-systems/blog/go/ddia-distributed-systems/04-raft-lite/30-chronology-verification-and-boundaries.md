# Verification And Boundaries

## 1. 자동 검증은 선출, failover, log replication, step-down을 함께 덮는다

2026-03-14 기준 재실행 명령은 아래와 같다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/04-raft-lite
GOWORK=off go test ./...
```

결과는 아래처럼 통과했다.

```text
ok  	study.local/go/ddia-distributed-systems/projects/04-raft-lite/tests	(cached)
```

테스트가 잡는 항목은 다음과 같다.

- leader election
- single leader guarantee
- leader failover
- log replication and commit
- higher-term step-down

즉 현재 범위의 핵심 Raft 규칙은 꽤 직접적으로 테스트된다.

## 2. demo와 추가 재실행 관찰값

demo 출력:

```text
leader=n1 commit=0 log_len=1
```

추가 재실행 출력:

```text
first_leader n1 1
commit_after_repl 1 2
failover_leader n2 2
```

이 결과를 합치면 현재 구현은 아래 사실을 만족한다.

- fixed TTL 환경에서도 leader는 결정적으로 하나만 선출된다
- leader의 current-term entries는 majority replication 뒤 commit index를 올린다
- leader down 이후 higher term의 새 leader가 선출된다

## 3. 현재 구현이 일부러 다루지 않는 것

이 랩을 production Raft implementation으로 읽으면 안 된다.

- persistent log가 없다
- restart recovery가 없다
- membership change가 없다
- snapshotting과 InstallSnapshot이 없다
- real network transport와 retry가 없다

즉 consensus semantics를 보여 주는 synchronous in-memory simulator다.

## 4. 이 문서에서 피한 과장

이번 재작성에서는 아래 같은 표현을 쓰지 않았다.

- "Raft를 완전히 구현했다"
- "crash-safe consensus를 달성했다"
- "실전 분산 로그 복제를 바로 쓸 수 있다"

현재 소스와 테스트가 실제로 보여 주는 것은 election, vote rule, append consistency, current-term majority commit, higher-term step-down까지다. 그보다 큰 consensus claim은 근거가 없다.
