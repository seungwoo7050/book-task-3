# 01 Mini LSM Store — Series Map

`store.py` 한 파일에 memtable, immutable snapshot, SSTable이 전부 들어 있다. 처음엔 이게 정말 저장 엔진이라고 부를 수 있는 물건인지 의심스러웠다. 이 시리즈는 그 의심이 어떻게 풀렸는지, 그리고 어디서 새로운 의심이 생겼는지를 따라간다.

## 이 프로젝트가 답하는 질문

- `dict` 하나짜리 memtable이 flush와 reopen을 거치면서도 newest-first lookup을 유지할 수 있는가
- tombstone이 `None`일 뿐인데 삭제된 키가 SSTable에서 되살아나지 않는 이유는 무엇인가

## 읽는 순서

1. [10-chronology-setup-and-surface.md](10-chronology-setup-and-surface.md) — 파일 하나짜리 저장 엔진을 처음 열었을 때
2. [20-chronology-core-mechanics.md](20-chronology-core-mechanics.md) — `get`의 조회 순서가 전부였다는 깨달음
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md) — 9 passed, 그리고 WAL 없는 세계의 한계

## 참조한 실제 파일

- `python/database-internals/projects/01-mini-lsm-store/src/mini_lsm_store/store.py`
- `python/database-internals/projects/01-mini-lsm-store/tests/test_mini_lsm_store.py`
- `python/database-internals/projects/01-mini-lsm-store/src/mini_lsm_store/__main__.py`
- `python/database-internals/projects/01-mini-lsm-store/README.md`
- `python/database-internals/projects/01-mini-lsm-store/problem/README.md`
- `python/database-internals/projects/01-mini-lsm-store/pyproject.toml`

## 재검증 명령

```bash
cd python/database-internals/projects/01-mini-lsm-store
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m mini_lsm_store
```

## Git Anchor

- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
- `2026-03-11 74d5b11 feat: add new project in database-systems`
