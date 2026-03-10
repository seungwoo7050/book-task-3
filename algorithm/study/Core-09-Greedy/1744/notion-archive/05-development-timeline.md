# BOJ 1744 — 개발 타임라인

## Phase 1: 프로젝트 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/09-greedy/gold-1744 study/Core-09-Greedy/1744
```

Gold → `cpp/` 포함.

## Phase 2: Python 구현

4-way 분류 (pos>1, ones, zeros, neg) 후 그리디 매칭.

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
