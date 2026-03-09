# BOJ 2170 — 개발 타임라인

## Phase 1: 프로젝트 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/06-sorting/gold-2170 study/Core-06-Sorting/2170
```

Gold 등급 → `cpp/` 포함.

## Phase 2: Python 구현

```bash
vi python/src/solution.py
```

구간 합치기 알고리즘: 정렬 → 스위프 → 확장/확정

## Phase 3: C++ 비교 구현

```bash
vi cpp/src/solution.cpp
g++-14 -std=c++17 -O2 -Wall -o cpp/build/solution cpp/src/solution.cpp
```

## Phase 4: 테스트

```bash
make -C problem test
make -C problem run-cpp
```

PASS.

## 사용 도구

- Python 3, `sys.stdin.readline`
- g++-14
- GNU Make
