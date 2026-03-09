# BOJ 1931 — 개발 타임라인

## Phase 1: 프로젝트 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/09-greedy/silver-1931 study/Core-09-Greedy/1931
```

Silver → C++ 미포함.

## Phase 2: Python 구현

`(end, start)` 복합 키 정렬 + 선형 스캔.

## Phase 3: 테스트

```bash
make -C problem test
```

PASS.

## 사용 도구

- Python 3
- GNU Make
