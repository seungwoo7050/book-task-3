# BOJ 1181 — 개발 타임라인

## Phase 1: 프로젝트 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/06-sorting/silver-1181 study/Core-06-Sorting/1181
```

## Phase 2: 구현 및 테스트

```bash
vi python/src/solution.py
make -C problem test
```

`set` + `sorted(key=lambda)` 패턴. PASS.

## 사용 도구
- Python 3, `set`, `sorted(key=...)`
- GNU Make
