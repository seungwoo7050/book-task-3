# 디버그 포인트

이 파일은 “어떤 테스트가 왜 깨지는가”를 바로 재현하기 위한 메모입니다. 05번 문서답게, 각 항목은 가능한 한 한 줄 규칙과 한 개 테스트에 대응하도록 적었습니다.

## 1. snapshot이 future commit을 읽어 버리는 경우
- 의심 파일: `../src/mvcc_lab/core.py`
- 재현 명령:

```bash
cd python/database-internals/projects/05-mvcc
source .venv/bin/activate
PYTHONPATH=src python -m pytest tests/test_mvcc.py::test_snapshot_isolation -v
```

- 정상 기대: `t2`는 200이 아니라 100을 읽어야 합니다.
- 깨졌을 때 보이는 징후: `manager.read(t2, "x")`가 200을 반환합니다.
- 확인 테스트: `test_snapshot_isolation`
- 다시 볼 질문: `begin()`이 snapshot을 언제 잡고, `get_visible()`이 어떤 조건으로 visible version을 고르는가?

## 2. read-your-own-write가 안 보이는 경우
- 의심 파일: `../src/mvcc_lab/core.py`
- 재현 명령:

```bash
cd python/database-internals/projects/05-mvcc
source .venv/bin/activate
PYTHONPATH=src python -m pytest tests/test_mvcc.py::test_basic_read_write -v
PYTHONPATH=src python -m mvcc_lab
```

- 정상 기대:

```text
{'tx': 1, 'read_your_own_write': 10}
```

- 깨졌을 때 보이는 징후: 데모에서 `read_your_own_write`가 `None`으로 나오거나, 테스트에서 즉시 실패합니다.
- 확인 테스트: `test_basic_read_write`
- 다시 볼 질문: `read()`가 visible committed version을 찾기 전에 자신의 tx_id 버전을 먼저 확인하는가?

## 3. 동일 key write conflict를 놓치는 경우
- 의심 파일: `../src/mvcc_lab/core.py`
- 재현 명령:

```bash
cd python/database-internals/projects/05-mvcc
source .venv/bin/activate
PYTHONPATH=src python -m pytest tests/test_mvcc.py::test_write_write_conflict -v
```

- 정상 기대: 두 번째 commit에서 `write-write conflict` 예외가 나야 합니다.
- 깨졌을 때 보이는 징후: `t2`도 그대로 commit되거나, 반대로 다른 key까지 모두 충돌로 취급됩니다.
- 확인 테스트: `test_write_write_conflict`, `test_different_keys_no_conflict`
- 다시 볼 질문: `commit()`이 자신의 snapshot 이후에 commit된 같은 key의 version만 검사하는가?

## 4. abort나 GC 뒤에 version chain이 이상해지는 경우
- 의심 파일: `../src/mvcc_lab/core.py`
- 재현 명령:

```bash
cd python/database-internals/projects/05-mvcc
source .venv/bin/activate
PYTHONPATH=src python -m pytest tests/test_mvcc.py::test_abort_and_delete -v
PYTHONPATH=src python -m pytest tests/test_mvcc.py::test_gc -v
```

- 정상 기대:
  - abort된 write는 읽히지 않아야 합니다.
  - GC 뒤에도 최신 읽기 결과는 유지되어야 합니다.
  - `len(manager.version_store.store["x"]) <= 2`
- 깨졌을 때 보이는 징후: abort한 값이 남거나, GC 뒤에 최신 값까지 사라집니다.
- 확인 테스트: `test_abort_and_delete`, `test_gc`
- 다시 볼 질문: `remove_by_tx_id()`와 `gc()`가 “최신 old version 하나는 남긴다”는 규칙을 지키는가?
