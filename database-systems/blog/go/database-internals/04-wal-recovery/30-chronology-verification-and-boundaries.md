# Verification And Boundaries

## 1. 자동 검증은 record format, replay, store integration을 넓게 덮는다

2026-03-14 기준 재실행 명령은 아래와 같다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery
GOWORK=off go test ./...
```

결과는 아래처럼 통과했다.

```text
ok  	study.local/go/database-internals/projects/04-wal-recovery/tests	(cached)
```

테스트가 잡는 항목은 아래와 같다.

- put record recovery
- delete record recovery
- 500 record recovery
- corruption 이후 stop
- missing/truncated WAL
- reopen 뒤 WAL-based recovery
- force flush 뒤 WAL rotation

즉 이 랩은 append-only file layer와 store integration을 둘 다 검증한다.

## 2. demo와 추가 재실행이 보여 준 관찰값

demo 출력:

```text
name => Alice
city => Seoul
missing => <missing>
```

추가 재실행 출력:

```text
recovered_records 3 put delete beta
alpha_tombstone_after_reopen true
beta_after_reopen 2
wal_size_after_flush 0 sstables 1
```

이 결과를 합치면 현재 구현은 아래를 만족한다.

- active WAL만으로도 reopen 뒤 최근 write를 복원한다
- delete는 tombstone 의미를 잃지 않는다
- flush 뒤 old WAL은 비워지고 SSTable이 새 durability surface가 된다

## 3. 하지만 durability를 과장하면 안 된다

현재 구현이 다루지 않는 항목도 분명하다.

- group commit과 batching
- multi-writer serialization
- distributed recovery
- segment rollover와 archive retention
- flush 중 crash consistency에 대한 manifest/atomicity

즉 local single-writer WAL discipline은 있지만, 완전한 운영용 durability stack은 아니다.

## 4. 이 문서에서 피한 과장

이번 재작성에서는 아래 같은 표현을 쓰지 않았다.

- "crash-safe storage engine을 완성했다"
- "corruption recovery를 포괄적으로 해결했다"
- "fsync 정책까지 검증했다"

현재 소스와 테스트가 실제로 보여 주는 것은 append-before-apply, replay stop policy, WAL rotation, reopen recovery까지다. 그보다 큰 durability claim은 근거가 없다.
