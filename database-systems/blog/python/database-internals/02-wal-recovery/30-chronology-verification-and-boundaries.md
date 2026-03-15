# 30 다시 돌려 보기: recovery가 실제 파일 상태에서 어떻게 보이는가

마지막으로 남는 건 구현 설명이 아니라 검증 신호다. WAL은 메모리 상태만 보고 이해했다고 느끼기 쉬운데, 실제 파일 크기와 reopen 결과를 같이 봐야 현재 semantics가 더 정확하게 보인다.

## Phase 3-1. pytest는 이 슬롯의 계약을 꽤 선명하게 잠근다

이번 재실행에서 pytest는 `7 passed, 1 warning in 0.04s`였다. 경고는 앞 슬롯과 마찬가지로 `pytest_asyncio` deprecation이라 프로젝트 핵심과는 무관했다.

테스트가 잠그는 계약은 이렇다.

- put/delete record replay
- 500건 대량 replay
- corruption 이후 중단
- missing/truncated WAL 처리
- reopen 뒤 memtable 복원
- force flush 이후 WAL rotation

특히 `test_force_flush_rotates_wal`는 꽤 중요하다. 단순히 flush가 성공했다는 게 아니라, 이후 `active.wal`이 비어 있고 reopen이 SSTable에서 값을 읽어야 한다는 상태까지 함께 고정한다.

## Phase 3-2. demo는 "append된 write는 reopen 뒤 살아 있다"는 최소 표면을 보여 준다

demo entry point는 아주 간단하다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/02-wal-recovery
PYTHONPATH=src python3 -m wal_recovery
```

출력:

```text
{'recovered': True, 'value': '1'}
```

이 한 줄은 flush나 corruption까지는 보여 주지 않지만, acknowledged write가 close/reopen 뒤에도 살아 있어야 한다는 가장 중요한 메시지를 드러낸다. 즉 공개 표면은 "recovery exists"이고, 더 세밀한 정책은 테스트와 보조 재실행이 맡는다.

## Phase 3-3. 보조 재실행이 WAL rotation과 recovery prefix를 더 잘 보여 줬다

이번 Todo에서는 테스트 밖에서 한 번 더 파일 상태를 확인했다.

- flush 전 `active.wal` 크기: `37`
- flush 후 `active.wal` 크기: `0`
- 생성된 SSTable: `000001.sst`
- 그 뒤 새로 쓴 `gamma`만 WAL recovery 대상
- corruption 파일에 trailing garbage를 붙여도 앞의 두 record만 replay

이 결과를 보면 현재 경계가 꽤 분명하다.

1. flush는 memtable만 비우는 게 아니라 WAL lifecycle을 끊는다.
2. recovery는 tail salvage보다 valid prefix 복원을 택한다.
3. reopen은 active WAL과 SSTable을 동시에 읽지만, 각각 역할이 다르다.

## Phase 3-4. 지금 상태에서 비워 둔 것

이번 슬롯이 durable write path를 분명히 만들긴 했지만, production durability로 읽으면 과장이다.

- `fsync_enabled`는 실제 `os.fsync()`로 이어지지 않는다.
- segmented WAL이 없다.
- group commit이나 batching이 없다.
- flush 도중 crash recovery, partial SSTable cleanup 같은 더 거친 failure mode는 다루지 않는다.
- immutable memtable과 concurrent flush 모델은 여전히 없다.

그래도 이 프로젝트가 중요한 이유는 분명하다. 바로 앞 슬롯의 memtable/SSTable ordering 위에 "append-before-apply"와 "stop-on-corruption recovery"라는 두 번째 축을 얹어, 이제 write path를 단순 성능이 아니라 durability 문제로 다시 보게 만들기 때문이다.
