# 05 MVCC 시리즈 맵

이 프로젝트는 Python `database-internals` 트랙의 마지막 저장 엔진 슬롯으로, 이제 write/read 비용이 아니라 visibility 규칙 자체를 다룬다. 읽을 때도 "트랜잭션 기능 추가"로 보기보다 `snapshot watermark`, `read-your-own-write`, `first-committer-wins`, `cleanup/gc`가 어떻게 맞물리는지 먼저 붙드는 편이 맞다.

## 먼저 보고 갈 질문

- transaction이 시작할 때 어떤 committed watermark를 snapshot으로 잡는가?
- 왜 자기 자신의 uncommitted write만 예외적으로 snapshot 규칙을 건너뛰어 읽게 되는가?
- write-write conflict와 aborted cleanup은 version chain을 어떻게 바꾸는가?

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md)
   테스트와 문제 정의를 다시 보며 이 슬롯의 중심이 SQL 기능이 아니라 version visibility 규칙이라는 점을 먼저 잡는다.
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md)
   `VersionStore`, `TransactionManager.begin/read/commit/abort/gc()`가 실제로 어떤 상태 전이를 고정하는지 본다.
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md)
   pytest, demo, 보조 재실행으로 snapshot read, conflict cleanup, GC가 실제로 어떤 chain 모양을 남기는지 정리한다.

## 재검증 명령

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/05-mvcc
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m mvcc_lab
```

## 이번 시리즈의 근거

- `database-systems/python/database-internals/projects/05-mvcc/README.md`
- `database-systems/python/database-internals/projects/05-mvcc/problem/README.md`
- `database-systems/python/database-internals/projects/05-mvcc/docs/README.md`
- `database-systems/python/database-internals/projects/05-mvcc/docs/concepts/snapshot-visibility.md`
- `database-systems/python/database-internals/projects/05-mvcc/docs/concepts/write-conflict.md`
- `database-systems/python/database-internals/projects/05-mvcc/src/mvcc_lab/core.py`
- `database-systems/python/database-internals/projects/05-mvcc/src/mvcc_lab/__main__.py`
- `database-systems/python/database-internals/projects/05-mvcc/tests/test_mvcc.py`

## 보조 메모

작업 메모는 [_evidence-ledger.md](_evidence-ledger.md)와 [_structure-outline.md](_structure-outline.md)에 남긴다. 공개 시리즈는 `00 -> 10 -> 20 -> 30`만 읽어도 충분하다.
