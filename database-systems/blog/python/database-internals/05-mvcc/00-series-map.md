# 05 MVCC — Series Map

이 시리즈는 MVCC를 거대한 DB 이론이 아니라 작은 파이썬 자료구조로 내려다본다. 핵심은 "최신값"이 아니라 "내 snapshot에서 보이는 최신값"이었다.

## 이 프로젝트가 답하는 질문

- `tx.snapshot`, `committed`, `version chain` 세 가지로 visibility를 어디까지 표현할 수 있는가
- write-write conflict를 commit 시점에 모으는 선택이 어떤 실패/정리 경계를 만드는가

## 읽는 순서

1. [10-chronology-setup-and-surface.md](10-chronology-setup-and-surface.md)
2. [20-chronology-core-mechanics.md](20-chronology-core-mechanics.md)
3. [30-chronology-integration-and-tradeoffs.md](30-chronology-integration-and-tradeoffs.md)
4. [40-chronology-verification-and-boundaries.md](40-chronology-verification-and-boundaries.md)

## 참조한 실제 파일

- `python/database-internals/projects/05-mvcc/src/mvcc_lab/core.py`
- `python/database-internals/projects/05-mvcc/src/mvcc_lab/__main__.py`
- `python/database-internals/projects/05-mvcc/tests/test_mvcc.py`
- `python/database-internals/projects/05-mvcc/README.md`
- `python/database-internals/projects/05-mvcc/problem/README.md`
- `python/database-internals/projects/05-mvcc/docs/concepts/snapshot-visibility.md`
- `python/database-internals/projects/05-mvcc/docs/concepts/write-conflict.md`
- `python/database-internals/projects/05-mvcc/pyproject.toml`

## 재검증 명령

```bash
cd python/database-internals/projects/05-mvcc
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m mvcc_lab
```

## Git Anchor

- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
- `2026-03-11 74d5b11 feat: add new project in database-systems`
