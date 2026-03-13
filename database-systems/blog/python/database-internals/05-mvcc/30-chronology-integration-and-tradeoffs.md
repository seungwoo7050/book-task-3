# 30 Integration And Tradeoffs

## Day 1
### Session 5

트랜잭션 수명주기를 한 번에 보면 아래 순서다.

1. `begin`에서 snapshot 고정
2. `write/delete`로 version chain에 provisional 버전 추가
3. `commit`에서 write-write conflict 검사
4. 통과하면 committed 표시, 실패하면 rollback

rollback은 `_abort_internal()`이 담당한다.

```python
for key in tx.write_set:
    self.version_store.remove_by_tx_id(key, tx_id)
tx.status = "aborted"
```

abort된 tx 버전은 체인에서 제거된다. 이 덕분에 이후 read path가 aborted 버전을 고려할 필요가 없다.

tradeoff도 분명하다.

- 장점:
  - 구현이 단순해 snapshot isolation 핵심을 읽기 좋다
  - conflict 정책이 명시적이고 테스트 가능하다
- 한계:
  - predicate conflict/phantom 방지 없음
  - lock manager/intent lock 없음
  - 분산 tx, commit timestamp ordering 없음

CLI:

```bash
cd python/database-internals/projects/05-mvcc
PYTHONPATH=src python3 -m pytest -q
```

테스트를 보면 경계가 명확하다.

- `test_different_keys_no_conflict`: key 분리 시 commit 가능
- `test_write_write_conflict`: 동일 key 경합 시 후행 tx abort
- `test_abort_and_delete`: abort semantics + tombstone visibility

다음 단계 연결:

Python 트랙은 여기서 끝나고 Go 심화로 넘어간다. 이 단계에서 확보한 건 "읽기 가시성"과 "쓰기 충돌"의 최소 규칙이다.