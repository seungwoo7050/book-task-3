# Core Invariants

## 1. flush는 active를 immutable로 바꾸고 새 active를 즉시 연다

`flush()`의 첫 두 줄이 가장 중요하다.

```go
store.ImmutableMemtable = store.Memtable
store.Memtable = skiplist.New()
```

이 순서 때문에 flush 도중에도 write를 받을 새 active memtable 자리가 즉시 생긴다. 지금 구현은 동기 flush라 실제 병행 write는 없지만, 상태 분리는 async flush 모델과 같은 방향을 유지한다. docs의 [`flush-lifecycle.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/03-mini-lsm-store/docs/concepts/flush-lifecycle.md)가 말하는 핵심이 바로 이 구분이다.

## 2. lookup은 active -> immutable -> newest SSTable 순서를 절대 바꾸지 않는다

`Get()`의 read path는 고정돼 있다.

1. active memtable
2. immutable memtable
3. `SSTables` slice 순서대로

그리고 `Open()`은 disk에서 `.sst` 파일을 오름차순으로 읽은 뒤 `reverseTables()`로 뒤집는다. flush는 새 table을 `append([]*sstable.SSTable{table}, store.SSTables...)`로 맨 앞에 넣는다. 결과적으로 `SSTables`는 언제나 newest-first를 유지한다.

이 우선순위 덕분에 더 최신의 tombstone이나 overwrite가 오래된 SSTable 값을 가릴 수 있다.

## 3. tombstone은 cross-level에서도 "found but nil"로 끝나야 한다

`Get()`은 memtable과 immutable memtable에서 `state != Missing`이면 즉시 반환한다. tombstone도 여기에 포함된다. SSTable lookup도 `found == true`면 `value`가 `nil`이어도 바로 반환한다.

즉 이 store에서 delete는 "missing"이 아니라 "삭제 표지가 최신 레벨에 존재함"이다. 바로 이 semantics가 `TestTombstoneAcrossLevels`와 demo의 `apple => <tombstone>`을 설명한다.

## 4. flush 파일 이름과 reopen 순서는 sequence로 복원된다

`flush()`는 `sstable.FileName(store.DataDir, store.nextSequence)`를 사용하고, flush 성공 뒤 `nextSequence++`를 한다. `Open()`은 디렉터리의 `.sst` 파일 이름을 읽어 sequence를 다시 계산하고, 가장 큰 번호 다음 값으로 `nextSequence`를 잡는다.

즉 manifest는 없지만, 최소한 파일 이름 규칙만으로 다음 SSTable sequence를 이어갈 수 있다. 추가 재실행에서 `000002.sst`가 newest로 유지된 것도 이 규칙 덕분이다.

## 5. 현재 flush는 atomic swap 이후 write 실패를 되돌리지 않는다

소스만 읽으면 보이는 중요한 경계도 있다. `flush()`는 먼저 `ImmutableMemtable = Memtable`, `Memtable = New()`를 수행한 뒤 SSTable `Write()`를 호출한다. 만약 `Write()`가 실패하면 그 시점엔 이미 active memtable은 교체된 상태다. 테스트는 이 실패 경로를 다루지 않지만, 현재 구현은 flush failure rollback을 별도로 제공하지 않는다.

이건 production-grade WAL/manifest 설계가 아직 없는 현재 범위의 한계로 보는 편이 정확하다.
