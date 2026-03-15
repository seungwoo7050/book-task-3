# Verification And Boundaries

## 1. 자동 검증은 offset, idempotency, delete propagation을 함께 덮는다

2026-03-14 기준 재실행 명령은 아래와 같다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication
GOWORK=off go test ./...
```

결과는 아래처럼 통과했다.

```text
ok  	study.local/go/ddia-distributed-systems/projects/02-leader-follower-replication/tests	(cached)
```

테스트가 잡는 항목은 다음과 같다.

- sequential offsets
- follower idempotent apply
- incremental replicate-once
- delete propagation

즉 이 랩의 핵심 contract는 비교적 빠짐없이 테스트에 들어 있다.

## 2. demo와 추가 재실행 관찰값

demo 출력:

```text
alpha deleted
beta=2 watermark=2
```

추가 재실행 출력:

```text
initial_apply 2 1
duplicate_apply 0 1
incremental_apply 2 3
a_deleted true
b_value 3
```

이 결과를 합치면 현재 구현은 아래 사실을 만족한다.

- follower는 자기 watermark 이후 mutation만 적용한다
- duplicate replay는 applied count를 늘리지 않는다
- delete와 overwrite가 incremental batch 안에서도 정상적으로 반영된다

## 3. 현재 구현이 일부러 다루지 않는 것

이 랩을 full replication system으로 읽으면 안 된다.

- leader election이 없다
- quorum write/read가 없다
- log truncation이나 snapshot install이 없다
- network partition과 split brain이 없다
- lag metric과 health reporting이 없다

즉 ordered mutation stream replication minimum viable path만 다룬다.

## 4. 이 문서에서 피한 과장

이번 재작성에서는 아래 같은 표현을 쓰지 않았다.

- "실전 leader-follower cluster를 구현했다"
- "장애 상황에서도 안전하다"
- "consensus 없이도 production replication이 가능하다"

현재 소스와 테스트가 실제로 보여 주는 것은 sequential offset log, watermark fetch, idempotent replay, delete propagation까지다. 그보다 큰 replication claim은 근거가 없다.
