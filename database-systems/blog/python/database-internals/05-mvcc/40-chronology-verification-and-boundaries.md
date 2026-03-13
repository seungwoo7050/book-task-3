# 40 Verification And Boundaries

## Day 1
### Session 6

최종 검증은 visibility/conflict/gc를 각각 확인하는 쪽으로 했다.

CLI:

```bash
cd python/database-internals/projects/05-mvcc
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m mvcc_lab
```

검증 신호:

- `7 passed`
- demo: `{'tx': 1, 'read_your_own_write': 10}`

demo는 read-your-own-write 하나만 보여 주지만, 테스트가 나머지 경계를 채운다.

- `test_snapshot_isolation`: 시작 시점 snapshot 고정
- `test_write_write_conflict`: first-committer-wins
- `test_gc`: 오래된 버전 정리 후에도 최신 가시성 유지

GC 기준은 아래 코드에서 확인한다.

```python
min_snapshot = self.next_tx_id
for tx in self.transactions.values():
    if tx.status == "active" and tx.snapshot < min_snapshot:
        min_snapshot = tx.snapshot
self.version_store.gc(min_snapshot)
```

active tx 중 가장 오래된 snapshot을 기준으로 지울 수 있는 버전만 정리한다. 즉 gc는 aggressive cleanup이 아니라 visibility safety를 우선한다.

이 단계의 boundary:

- 다루는 것:
  - snapshot visibility
  - read-your-own-write
  - write-write conflict + abort
  - min-snapshot 기반 gc
- 다루지 않는 것:
  - serializable isolation
  - predicate lock / range conflict
  - distributed commit protocol

다음 질문:

- key-version MVCC를 page/WAL 기반 엔진에 붙일 때 flush order 제약은 무엇인가
- read-heavy 환경에서 gc 주기와 chain length를 어떻게 제어할까