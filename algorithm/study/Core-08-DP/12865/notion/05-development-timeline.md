# BOJ 12865 — 개발 타임라인

## Phase 1: 프로젝트 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/08-dp/gold-12865 study/Core-08-DP/12865
```

Gold → `cpp/` 포함.

## Phase 2: Python 구현

1D 배열 역순 순회 패턴 구현.

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
