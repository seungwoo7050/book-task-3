# BOJ 1991 — 개발 타임라인

## Phase 1: 프로젝트 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/0B-graph-tree/silver-1991 study/Core-0B-Graph-Tree/1991
```

## Phase 2: Python 구현

딕셔너리 기반 트리 + 재귀 순회 3종.

## Phase 3: 테스트

```bash
make -C problem test
```

PASS.

## 사용 도구

- Python 3
- GNU Make
