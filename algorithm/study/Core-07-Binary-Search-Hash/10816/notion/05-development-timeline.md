# BOJ 10816 — 개발 타임라인

## Phase 1: 프로젝트 생성 및 구현

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/07-binary-search-hash/silver-10816 study/Core-07-Binary-Search-Hash/10816
vi python/src/solution.py
make -C problem test
```

`Counter` 사용. PASS.

## 사용 도구
- Python 3, `collections.Counter`
- GNU Make
