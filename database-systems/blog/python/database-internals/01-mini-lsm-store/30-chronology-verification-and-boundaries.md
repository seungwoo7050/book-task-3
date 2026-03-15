# 30 다시 돌려 보기: 이 프로젝트가 실제로 보장하는 것과 아직 비워 둔 것

마지막으로 남는 질문은 간단하다. 방금 읽은 invariant가 실제로 어떤 검증 신호로 묶여 있고, 어디서 멈추는가? 작은 프로젝트일수록 이 마지막 정리가 중요하다. 구현이 짧아서 "다 된 것처럼" 보이기 쉽기 때문이다.

## Phase 3-1. pytest는 공개 계약을 꽤 넓게 잡고 있다

이번 재실행에서 pytest는 `9 passed, 1 warning in 0.03s`였다. 경고는 `pytest_asyncio` deprecation이라 프로젝트 자체의 invariant와는 무관했다. 중요한 건 9개 테스트가 잡는 표면이다.

- 기본 put/get
- missing key
- update overwrite
- delete tombstone
- threshold 기반 flush
- force flush 이후 read
- memtable 우선권
- tombstone across levels
- close/reopen persistence

즉 이 프로젝트는 toy API 수준에서 멈추지 않는다. read visibility와 persistence까지 이미 공개적으로 약속한다. 특히 `test_memtable_wins_over_sstable`와 `test_tombstone_across_levels`는 이후 LSM 계열 프로젝트에서 계속 반복될 ordering 규칙을 여기서 먼저 못 박는다.

## Phase 3-2. demo는 "최신 값이 먼저 보인다"는 최소 표면만 밖으로 보여 준다

demo entry point는 아주 얇다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/01-mini-lsm-store
PYTHONPATH=src python3 -m mini_lsm_store
```

출력:

```text
{'key': 'alpha', 'found': True, 'value': '3', 'sstables': 1}
```

이 한 줄이 보여 주는 건 많지 않지만 핵심은 선명하다. 한 번 flush된 old value `1`보다, 이후 memtable에 쓴 new value `3`가 먼저 읽혀야 한다는 점이다. demo는 바로 그 "newest-first visibility"를 밖으로 노출하는 최소 표면이다.

테스트가 전체 계약을 지키는 장치라면, demo는 그중 무엇을 처음 보여 줄지를 고른다. 이 프로젝트는 flush count나 byte size보다 "최신 값이 stale SSTable보다 먼저 보인다"는 메시지를 택한 셈이다.

## Phase 3-3. 이번 보조 재실행이 드러낸 경계

추가로 한 번 더 돌려 보면서 현재 경계도 확인했다.

- `close()`는 active memtable만 flush한다
- reopen 후 파일 순서는 `000002.sst`, `000001.sst`
- tombstone은 reopen 뒤에도 `(None, True)` 형태로 유지된다

즉 현재 구현은 단일 프로세스, 단일 writer, 동기 flush 전제에선 꽤 일관적이다. 하지만 동시에 빠진 것도 분명하다.

- WAL이 없다. flush 전에 프로세스가 죽으면 active memtable의 write는 사라진다.
- compaction이 없다. SSTable은 계속 쌓이기만 한다.
- range query가 없다.
- bloom filter나 sparse index가 없어서 lookup cost는 table 수에 비례해 늘어난다.
- immutable memtable은 개념적으로는 분리돼 있지만, 현재 구현에선 동기 flush 안에서 곧바로 비워진다.

이 한계들은 결함이라기보다 다음 슬롯의 이유에 가깝다. `02 WAL Recovery`, `03 Index Filter` 같은 뒤 프로젝트가 왜 필요한지가 바로 여기서 보인다.

그래서 이 마지막 글의 결론은 단순하다. `01 Mini LSM Store`는 production storage engine이 아니다. 대신 이후 모든 확장이 기대는 바닥, 즉 flush lifecycle, tombstone visibility, newest-first read ordering, reopen sequence reconstruction을 아주 작고 선명한 형태로 먼저 고정하는 슬롯이다.
