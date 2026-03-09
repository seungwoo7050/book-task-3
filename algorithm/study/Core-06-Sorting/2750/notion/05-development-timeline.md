# BOJ 2750 — 개발 타임라인

## Phase 1: 프로젝트 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/06-sorting/bronze-2750 study/Core-06-Sorting/2750
```

## Phase 2: 구현 및 테스트

```bash
vi python/src/solution.py
make -C problem test
```

3줄 구현. PASS.

## 사용 도구
- Python 3, 내장 `sort()`
- GNU Make
