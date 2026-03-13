# 01 Mini LSM Store 시리즈 맵

Database Internals 트랙의 1번째 슬롯인 `01 Mini LSM Store`에서는 active memtable, immutable flush, newest-first read path를 연결해 최소 LSM store를 완성합니다. 이 시리즈는 결과 요약보다 실제 구현 순서가 어디서 선명해지는지 보여 주는 데 초점을 둔다.

## 먼저 보고 갈 질문

- active memtable이 threshold를 넘으면 immutable swap 후 SSTable로 flush해야 합니다.
- read path는 active memtable, immutable memtable, newest SSTable부터 순서대로 조회해야 합니다.

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md) — 테스트 이름과 파일 배치부터 훑으면서 문제의 테두리를 다시 좁히는 글
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md) — 핵심 함수와 상태 전이에서 invariant가 실제로 어디서 잠기는지 따라가는 글
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md) — 테스트와 demo를 다시 돌려 약속 범위와 남는 한계를 정리하는 글

## 재검증 명령

```bash
PYTHONPATH=src .venv/bin/python -m pytest
PYTHONPATH=src .venv/bin/python -m mini_lsm_store
```

## 이번 시리즈가 근거로 삼은 파일

- `database-systems/python/database-internals/projects/01-mini-lsm-store/src/mini_lsm_store/store.py`
- `database-systems/python/database-internals/projects/01-mini-lsm-store/tests/test_mini_lsm_store.py`
- `database-systems/python/database-internals/projects/01-mini-lsm-store/README.md`
- `database-systems/python/database-internals/projects/01-mini-lsm-store/problem/README.md`
- `database-systems/python/database-internals/projects/01-mini-lsm-store/docs/README.md`
- `database-systems/python/database-internals/projects/01-mini-lsm-store/src/mini_lsm_store/__main__.py`

## 보조 메모

작업 메모가 꼭 필요할 때만 [_evidence-ledger.md](_evidence-ledger.md)와 [_structure-outline.md](_structure-outline.md)를 보면 된다. 공개 시리즈는 `00 -> 10 -> 20 -> 30`만 따라가면 충분하다.

## Git Anchor

- `2026-03-13 abeead6 docs: TRACK 1 에대한 blog/ 작업 1차 완료`
- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
