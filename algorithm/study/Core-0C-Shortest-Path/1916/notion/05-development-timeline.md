# BOJ 1916 — 개발 타임라인

## Phase 1: 프로젝트 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/0C-shortest-path/bronze-1916 study/Core-0C-Shortest-Path/1916
```

## Phase 2: Python 구현

다익스트라 + lazy deletion.

## Phase 3: 테스트

```bash
make -C problem test
```

PASS.

## 사용 도구

- Python 3
- GNU Make
