# BOJ 1167 — 개발 타임라인

## Phase 1: 프로젝트 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/0B-graph-tree/gold-1167 study/Core-0B-Graph-Tree/1167
```

Gold → `cpp/` 포함.

## Phase 2: Python 구현

BFS 두 번 패턴. `deque` 사용.

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
