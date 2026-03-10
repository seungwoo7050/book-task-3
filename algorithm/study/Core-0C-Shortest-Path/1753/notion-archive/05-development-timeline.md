# BOJ 1753 — 개발 타임라인

## Phase 1: 프로젝트 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/0C-shortest-path/silver-1753 study/Core-0C-Shortest-Path/1753
```

Silver, 다만 `cpp/` 포함 (비교 구현).

## Phase 2: Python 구현

다익스트라 + lazy deletion 패턴.

## Phase 3: C++ 비교 구현 및 테스트

```bash
make -C problem test
make -C problem run-cpp
```

PASS.

## 사용 도구

- Python 3
- g++-14
- GNU Make
