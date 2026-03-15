# 20 핵심 invariant 붙잡기: append-before-apply, stop-on-corruption, WAL rotation

범위를 다시 잡고 나면 핵심은 몇 군데로 빠르게 모인다. 이 프로젝트에서는 `WriteAheadLog._append_record()`, `recover()`, `DurableStore.open()`, `force_flush()`가 거의 모든 semantics를 만든다. 함수 수는 많지 않지만, 이 네 군데가 write acknowledgement의 의미를 완전히 다시 정의한다.

## Phase 2-1. `_append_record()`가 append-before-apply를 강제한다

`DurableStore.put()`와 `delete()`는 둘 다 memtable을 건드리기 전에 먼저 WAL append를 호출한다.

- `put()` -> `self._wal.append_put(key, value)` -> `_replace_memtable_value(key, value)`
- `delete()` -> `self._wal.append_delete(key)` -> `_replace_memtable_value(key, None)`

이 순서 때문에 이 프로젝트의 durable write path가 성립한다. memtable 업데이트보다 WAL append가 먼저 실패하면, acknowledged write가 되지 않는다. 반대로 append가 끝난 뒤에만 메모리 상태를 바꾸니 reopen 시 replay할 근거가 남는다.

레코드 형식도 여기서 같이 고정된다. `[crc32][type][keyLen][valLen][key][value]` 구조고, delete는 `valLen = 0xFFFFFFFF` sentinel을 쓴다. 즉 tombstone의 뜻은 앞 프로젝트처럼 `None`이지만, 디스크에선 sentinel 길이로 표현된다.

## Phase 2-2. `recover()`는 가능한 많이 살리지 않고, 확실한 prefix만 복원한다

`recover()`를 읽으면 이 프로젝트의 recovery policy가 분명해진다. 루프는 buffer offset을 따라가면서 header 길이, payload 길이, CRC를 차례로 확인한다. 셋 중 하나라도 어긋나면 바로 `break`하고 뒤는 버린다.

이 보수적 정책은 테스트와 보조 재실행이 둘 다 뒷받침한다.

- `test_stop_at_corrupted_record`는 뒤에 garbage를 덧붙여도 앞의 두 record만 복원되기를 요구한다.
- `test_recover_nonexistent_and_truncated`는 파일이 없거나 header가 너무 짧으면 빈 배열을 요구한다.

이번 보조 재실행에서도 결과는 이랬다.

```text
corrupt_replay [('put', 'good1', 'v1'), ('put', 'good2', 'v2')]
```

즉 손상 지점 이후는 살리지 않는다. recovery의 목적을 "최대 salvage"가 아니라 "신뢰 가능한 prefix 복원"으로 잡고 있는 셈이다.

## Phase 2-3. `open()`이 WAL replay를 memtable 복원으로 연결한다

`DurableStore.open()`은 SSTable 목록을 먼저 읽고 reverse해서 newest-first 순서를 복원한 다음, `WriteAheadLog(self.wal_path, False).recover()` 결과를 돌며 memtable을 다시 채운다. 이 시점에 눈여겨볼 점이 두 가지 있다.

1. recovery는 WAL record를 직접 apply하지 않고 `_replace_memtable_value()`를 통해 현재 memtable semantics로 다시 흘려보낸다.
2. recover용 `WriteAheadLog`는 `fsync_enabled=False`로 새로 만들지만, recover 자체는 append가 아니므로 이 값은 의미가 없다.

즉 reopen은 "WAL parser"와 "현재 memtable accounting"을 연결하는 지점이다. replay 결과도 결국 현재 store가 쓰는 byte threshold 계산과 tombstone semantics를 그대로 따른다.

## Phase 2-4. `force_flush()`는 SSTable만 만들지 않고 WAL 수명도 끊는다

이 함수가 이번 프로젝트를 앞 슬롯과 가장 다르게 만든다. memtable을 SSTable로 write한 뒤, `self._wal.close()`를 먼저 호출하고 기존 `active.wal`을 unlink한 다음, 새 `WriteAheadLog`를 다시 열어 빈 active WAL로 시작한다.

이번 보조 재실행이 바로 이 rotation을 보여 줬다.

```text
before_flush_wal_size 37
after_flush_wal_size 0 sstables ['000001.sst']
recovered_after_reopen [('put', 'gamma', '3')]
```

여기서 핵심은 flush 전에 WAL에 있던 `alpha`, `beta`가 SSTable로 내려간 뒤 active WAL에는 남지 않는다는 점이다. 이후 `gamma`만 새 active WAL에 남고, reopen replay도 그 record만 복원한다. 즉 flush는 disk table 생성과 WAL lifecycle cut-over를 동시에 수행한다.

## Phase 2-5. source-based limitation: `fsync_enabled`는 아직 durability syscall로 이어지지 않는다

코드를 다시 보면 `WriteAheadLog.__init__()`와 `DurableStore.__init__()`는 둘 다 `fsync_enabled`를 받지만, `_append_record()`는 실제로 `self._handle.flush()`만 호출하고 `os.fsync()`는 부르지 않는다. 즉 옵션 이름은 future seam처럼 보이지만, 현재 구현에서 durability barrier는 userspace flush 수준에 머문다.

이건 버그라기보다 다음 확장 지점에 가깝다. 지금 슬롯의 초점은 append-before-apply와 replay policy이지, storage device까지 내려가는 flush semantics는 아니다. 그래도 문서에는 분명히 남겨 둘 가치가 있다. 이름만 보고 실제 fsync가 있다고 착각하기 쉽기 때문이다.
