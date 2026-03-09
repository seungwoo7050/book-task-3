# BOJ 2252 — 개발 타임라인

## Phase 1: 프로젝트 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/0D-mst-topo/gold-2252 study/Core-0D-MST-Topo/2252
```

Gold → `cpp/` 포함.

## Phase 2: Python 구현

Kahn's Algorithm (BFS 위상 정렬).

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
