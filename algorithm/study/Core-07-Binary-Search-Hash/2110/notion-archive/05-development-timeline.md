# BOJ 2110 — 개발 타임라인

## Phase 1: 프로젝트 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/07-binary-search-hash/gold-2110 study/Core-07-Binary-Search-Hash/2110
```

Gold → `cpp/` 포함.

## Phase 2: Python 구현

```bash
vi python/src/solution.py
```

정렬 → 매개변수 이진 탐색 → 탐욕 판별 함수

## Phase 3: C++ 비교 구현 및 테스트

```bash
vi cpp/src/solution.cpp
g++-14 -std=c++17 -O2 -Wall -o cpp/build/solution cpp/src/solution.cpp
make -C problem test
```

PASS.

## 사용 도구
- Python 3, `sorted()`
- g++-14
- GNU Make
