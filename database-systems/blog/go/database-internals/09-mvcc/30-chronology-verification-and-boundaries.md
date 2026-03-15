# Verification And Boundaries

## 1. 자동 검증은 visibility, conflict, abort, GC를 넓게 덮는다

2026-03-14 기준 재실행 명령은 아래와 같다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/09-mvcc
GOWORK=off go test ./...
```

결과는 아래처럼 통과했다.

```text
ok  	study.local/go/database-internals/projects/09-mvcc/tests	(cached)
```

테스트가 잡는 항목은 다음과 같다.

- basic read/write와 read-your-own-write
- snapshot isolation
- latest committed value
- write-write conflict
- different-key no-conflict
- abort cleanup과 delete
- stale version GC

즉 현재 범위 안에서 MVCC 핵심 규칙은 비교적 넓게 덮인다.

## 2. demo와 추가 재실행 관찰값

demo 출력:

```text
t2 sees x=v1
```

추가 재실행 출력:

```text
snapshot_read v1
conflict_error true
chain_after_conflict 1
gc_chain_len 1
```

이 결과를 합치면 현재 구현은 아래 사실을 만족한다.

- later commit이 있어도 old snapshot은 기존 committed value를 본다
- write-write conflict가 나면 늦은 tx는 실패한다
- abort된 tx의 version은 chain에 남지 않는다
- GC는 stale version chain을 실제로 줄인다

## 3. 현재 구현이 일부러 다루지 않는 것

이 랩을 full database transaction manager로 읽으면 안 된다.

- predicate locking이 없다
- phantom read 제어가 없다
- distributed transaction이 없다
- lock table과 deadlock handling이 없다
- SQL statement execution과 직접 연결돼 있지 않다

즉 snapshot isolation의 핵심 규칙만 따로 떼어 구현한 학습용 MVCC다.

## 4. 이 문서에서 피한 과장

이번 재작성에서는 아래 같은 표현을 쓰지 않았다.

- "완전한 MVCC DB를 구현했다"
- "모든 격리 수준을 다 지원한다"
- "phantom read까지 해결했다"

현재 소스와 테스트가 실제로 보여 주는 것은 snapshot watermark, read-your-own-write, first-committer-wins, abort cleanup, GC trimming까지다. 그보다 큰 transaction engine claim은 근거가 없다.
