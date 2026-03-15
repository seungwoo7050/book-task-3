# Verification And Boundaries

## 1. 자동 검증은 LSM의 핵심 계약을 넓게 덮는다

2026-03-14 기준 재실행 명령은 아래와 같다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/03-mini-lsm-store
GOWORK=off go test ./...
```

결과는 아래처럼 통과했다.

```text
ok  	study.local/go/database-internals/projects/03-mini-lsm-store/tests	(cached)
```

테스트가 잡는 항목은 다음과 같다.

- put/get
- missing key
- update
- delete tombstone
- threshold-triggered flush
- force flush 뒤 read
- memtable precedence over SSTable
- tombstone across levels
- close/reopen persistence

즉 작은 프로젝트지만, 현재 범위 안에서 중요한 read precedence와 persistence는 꽤 촘촘히 덮는다.

## 2. demo와 추가 재실행이 보여 준 관찰값

demo 출력:

```text
apple => <tombstone>
banana => ripe
missing => <missing>
```

추가 재실행 출력:

```text
sstables_after_flush 2 000002.sst
beta_active_wins 3
alpha_tombstone true
reopened_sstables 2 000002.sst
reopened_beta 3
reopened_alpha_tombstone true
```

이 값들을 합치면 현재 구현은 아래 사실을 만족한다.

- 새 write는 기존 SSTable보다 우선한다
- tombstone은 디스크의 오래된 live value를 가린다
- reopen 뒤에도 newest SSTable 순서와 최신 lookup semantics가 유지된다

## 3. 현재 구현이 일부러 다루지 않는 것

이 랩을 production LSM engine으로 읽으면 안 되는 이유도 분명하다.

- WAL이 없다
- background compaction이 없다
- concurrent flush가 없다
- range scan과 compression이 없다
- flush failure rollback이나 manifest recovery가 없다

즉 orchestration은 있지만 durability story는 아직 얕다.

## 4. 이 문서에서 피한 과장

이번 재작성에서는 아래 같은 표현을 쓰지 않았다.

- "LSM storage engine을 완성했다"
- "crash-safe flush를 구현했다"
- "production-ready read/write path를 제공한다"

현재 소스와 테스트가 실제로 보여 주는 것은 active/immutable/SSTable의 우선순위와 reopen 뒤 index 재적재까지다. 그보다 큰 durability claim은 근거가 없다.
