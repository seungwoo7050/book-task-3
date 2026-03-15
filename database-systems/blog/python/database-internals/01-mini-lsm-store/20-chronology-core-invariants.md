# 20 핵심 invariant 붙잡기: flush, tombstone, sequence ordering

범위를 다시 잡고 나면, 실제로 중요한 건 함수 몇 개로 빠르게 좁혀진다. 이 프로젝트에서는 `force_flush`, `get`, `open`, `_replace_memtable_value` 네 군데가 거의 모든 약속을 만든다. 각 함수가 작아서 오히려 더 조심해서 읽어야 했다. 한 줄의 선택이 공개 semantics가 되기 때문이다.

## Phase 2-1. `force_flush()`가 active와 immutable의 경계를 고정한다

`force_flush()`는 이 프로젝트의 write path를 가장 선명하게 보여 주는 함수다. memtable이 비어 있지 않으면 먼저 현재 memtable을 immutable snapshot으로 복사하고, active memtable은 바로 비우며 `_byte_size`를 0으로 되돌린다. 그 다음 sorted records를 새 `SSTable` 파일로 쓰고, `self.sstables`의 맨 앞에 insert 한다.

이 순서가 중요한 이유는 두 가지다.

1. 새 write를 받을 active 구조는 즉시 비워 둔다.
2. 방금 만든 SSTable이 read path에서 가장 먼저 보이도록 newest 위치에 들어간다.

코드가 보여 주는 핵심은 "background flush를 구현하지 않아도 immutable snapshot 개념은 이미 있다"는 점이다. 지금은 동기 flush지만, 상태 분리는 이후 async flush 모델과 같은 vocabulary를 유지한다.

## Phase 2-2. tombstone은 `None` 하나로 level을 건너간다

이 프로젝트의 delete는 별도 tombstone 타입이 아니라 `None` 값으로 구현된다. `delete()`는 결국 `_replace_memtable_value(key, None)`을 부르고, `get()`은 key가 memtable이나 immutable memtable에 있으면 value가 `None`이어도 `found=True`로 바로 반환한다. SSTable에서도 마찬가지다. `SSTable.get()`은 key가 index에 있으면 저장된 값이 `None`이더라도 `found=True`다.

이게 중요한 이유는 tombstone semantics가 "삭제된 key는 없다"가 아니라 "삭제 기록이 있다"라는 뜻이기 때문이다. 그래서 cross-level read에서도 older SSTable의 이전 값을 다시 꺼내지 않는다. 테스트 `test_tombstone_across_levels`가 바로 그 약속을 고정한다.

이번 보조 재실행에서도 같은 흐름을 다시 확인했다.

```text
preclose ('3', True) (None, True) 1 {'a': '3', 'b': None} None
reopen ('3', True) (None, True) ['000002.sst', '000001.sst']
```

여기서 `b`가 reopen 뒤에도 `(None, True)`라는 점이 tombstone persistence를 그대로 보여 준다.

## Phase 2-3. `open()`이 sequence ordering을 다시 세운다

reopen path에서 진짜 중요한 건 파일을 읽는 것 자체보다, 어떤 순서로 읽을 것인가다. `open()`은 `*.sst`를 파일명 순으로 정렬해서 순회하고, 각 파일을 load한 뒤 `self.sstables`에 append 한다. 그 다음 `self.sstables.reverse()`를 한 번 호출한다. 결과적으로 리스트는 newest-first가 된다.

보조 재실행에서 reopen 뒤 파일 순서가 `['000002.sst', '000001.sst']`였던 이유가 바로 이 reverse다. 이 선택이 없으면 read path는 older table을 먼저 보고 stale value를 다시 노출할 수 있다.

여기서 같이 보이는 seam도 하나 있다. `_next_sequence`는 reopen 시 현재 파일 stem의 최댓값에서 `+1`로 다시 잡힌다. 즉 manifest나 별도 metadata 파일 없이도 sequence continuity는 파일명만으로 유지된다. 단순하지만 현재 범위에서는 꽤 효과적이다.

## Phase 2-4. `_replace_memtable_value()`는 flush trigger를 byte 기준으로 만든다

이 프로젝트에서 threshold는 entry count가 아니라 byte size다. `_replace_memtable_value()`는 key와 value 길이를 더하고, 같은 key를 덮어쓸 때는 이전 길이를 먼저 빼 준다. tombstone인 `None`은 value length를 더하지 않는다. 그래서 flush는 "몇 개를 썼는가"가 아니라 "현재 memtable이 얼마나 커졌는가"에 따라 결정된다.

이 구현은 교육용으로 꽤 좋다. 아주 단순한 상태만으로도 LSM write path의 진짜 trigger가 record count보다 data size에 더 가깝다는 감각을 만든다. 동시에 한계도 분명하다. Python dict 자체의 메모리 비용은 계산하지 않고, 직렬화 오버헤드도 고려하지 않는다. 지금은 conceptual byte budget만 잡는 셈이다.

여기까지 따라오면 이 프로젝트의 invariant는 꽤 선명해진다.

- active memtable만 write를 받는다
- flush는 immutable snapshot을 거쳐 newest SSTable을 만든다
- tombstone `None`은 삭제 기록으로 남는다
- reopen은 SSTable sequence ordering을 다시 세운다

이 네 가지가 이후 슬롯들에서 계속 확장될 바닥이다.
