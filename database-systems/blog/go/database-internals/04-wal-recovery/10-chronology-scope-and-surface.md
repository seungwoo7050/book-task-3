# Scope, WAL Surface, And First Reopen

## 1. 문제 범위는 durability의 최소 경로에만 집중한다

[`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery/problem/README.md)는 네 가지를 요구한다. append-before-apply ordering, checksum이 붙은 WAL record format, 손상 지점에서 멈추는 replay, flush 이후 WAL rotation이다. 반대로 group commit, fsync batching, 압축 세그먼트, multi-writer, distributed recovery는 일부러 뺀다.

그래서 이 랩의 질문은 "완전한 durability 시스템인가"가 아니라, "acknowledged write를 잃지 않기 위한 최소한의 local write-ahead discipline이 있는가"에 가깝다.

## 2. 코드 표면은 WAL과 store 두 층으로 나뉜다

핵심 구현은 두 파일에 나뉜다.

- [`wal.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery/internal/wal/wal.go): append, recover, checksum verification
- [`store.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery/internal/store/store.go): WAL-integrated memtable/SSTable store

`DurableStore.Put()`과 `Delete()`는 먼저 WAL append를 호출하고, 그 다음 memtable을 갱신한다. `Open()`은 먼저 SSTable registry를 복원한 뒤 WAL을 recover해서 memtable을 재구성하고, 마지막으로 새 active WAL handle을 연다.

## 3. demo는 reopen recovery surface를 아주 단순하게 보여 준다

2026-03-14에 아래 명령을 다시 실행했다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery
GOWORK=off go run ./cmd/wal-recovery
```

출력은 아래와 같았다.

```text
name => Alice
city => Seoul
missing => <missing>
```

demo 흐름은 간단하지만 중요한 걸 확인시켜 준다.

1. store를 열고 `name`, `city`를 쓴다.
2. close한다.
3. 새 store 인스턴스로 reopen한다.
4. `Get()`이 WAL replay 결과를 그대로 보여 준다.

즉 이 프로젝트의 reopen recovery는 "flush된 SSTable만 읽는다"가 아니라, active WAL에 남아 있던 write까지 다시 memtable에 적용하는 흐름이다.

## 4. 추가 재실행으로 rotation과 tombstone도 고정했다

이번에 프로젝트 루트 내부 임시 Go 파일로 아래 관찰값을 추가로 확인했다.

```text
recovered_records 3 put delete beta
alpha_tombstone_after_reopen true
beta_after_reopen 2
wal_size_after_flush 0 sstables 1
```

이 결과는 네 가지를 함께 보여 준다.

- WAL replay는 `put`, `delete`, `put` 순서를 그대로 복원한다
- delete는 reopen 뒤에도 tombstone으로 유지된다
- flush 뒤 active WAL은 크기 0의 새 파일로 회전된다
- flush된 데이터는 SSTable 1개로 남아 reopen에서도 읽힌다
