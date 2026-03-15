# 10 범위를 다시 좁히기: 이 슬롯은 CRUD가 아니라 flush와 reopen까지 본다

이 트랙의 첫 프로젝트라서 처음엔 "작은 key-value store로 감을 익히는 단계"처럼 보였다. 그런데 실제로 파일 구조와 테스트 이름을 다시 훑어 보니, 이 슬롯은 생각보다 더 많은 경계를 한 번에 잡고 있었다. 단순 put/get이 아니라 flush, tombstone, reopen까지 이미 공개 계약에 들어와 있었다.

## Phase 1. 테스트 이름이 먼저 문제의 테두리를 보여 줬다

먼저 다시 본 것은 `tests/test_mini_lsm_store.py`였다. 이런 프로젝트는 구현이 작을수록 테스트 이름이 범위를 더 선명하게 드러내는 경우가 많다. 실제로 이 파일에는 `test_put_and_get`, `test_update`, `test_delete` 같은 표면 테스트뿐 아니라 `test_flush_creates_sstable`, `test_tombstone_across_levels`, `test_persistence_after_reopen`가 같이 있었다.

이 조합은 꽤 중요하다. 여기서부터 이미 이 프로젝트가 "메모리 map 위에 API 몇 개 얹기"가 아니라는 게 보인다. write path가 disk shape를 만들고, delete는 `None` tombstone으로 level을 건너가고, close 이후 reopen은 파일에서 상태를 다시 올려와야 한다는 뜻이기 때문이다.

이번 재실행에서 테스트 명령은 이렇게 확인했다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/01-mini-lsm-store
PYTHONPATH=src python3 -m pytest
```

결과:

```text
9 passed, 1 warning in 0.03s
```

pass 숫자보다 더 중요했던 건, 이 9개 테스트가 어떤 경계를 공개적으로 약속하는지였다.

## Phase 2. 파일 배치가 "한 슬롯에 여러 전제"를 압축했다는 걸 보여 줬다

소스 파일도 다시 정리해 보니 구조가 더 분명해졌다. `src/mini_lsm_store/store.py` 하나에 `SSTable`와 `MiniLSMStore`가 같이 있고, `__main__.py`는 demo entry point만 아주 얇게 붙는다. 즉 이 프로젝트는 memtable 전용 구현, SSTable 전용 구현, recovery 전용 구현으로 분리하지 않고, 첫 슬롯에서 저장 엔진의 최소 end-to-end를 압축해서 보여 준다.

`problem/README.md`도 같은 방향을 가리킨다. 원래는 더 잘게 나뉘어 있을 수 있었던 prerequisite를 Python 입문 트랙에서는 한 슬롯로 접어, 저장 엔진의 전체 흐름을 더 빨리 잡도록 재구성했다고 직접 적고 있다. 그래서 이 프로젝트는 "너무 이른 시점에 너무 많은 걸 한다"기보다, 이후 슬롯을 빠르게 읽기 위한 공통 언어를 먼저 깔아 주는 역할에 가깝다.

이 단계에서 `docs/concepts/flush-lifecycle.md`와 `docs/concepts/read-path.md`를 같이 보니, 이 프로젝트가 진짜로 고정하려는 문장이 딱 정리됐다.

- active memtable은 write를 받는 유일한 구조다
- threshold를 넘으면 immutable snapshot을 SSTable로 flush한다
- read path는 active -> immutable -> newest SSTable 순서다
- tombstone을 만나면 lookup은 즉시 삭제된 상태로 끝난다

즉 이 첫 글의 결론은 단순하다. 이 슬롯은 작은 구현처럼 보이지만, 이후의 WAL, filter, MVCC까지 계속 반복될 invariant vocabulary를 이미 여기서 다 깔아 둔다.
