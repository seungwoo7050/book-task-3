# BOJ 11657 — 개발 타임라인

## Phase 1: 프로젝트 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/0C-shortest-path/gold-11657 study/Core-0C-Shortest-Path/11657
```

Gold → `cpp/` 포함.

## Phase 2: Python 구현

간선 리스트 + 벨만-포드 + 음의 사이클 탐지.

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
