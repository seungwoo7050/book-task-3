# BOJ 1927 — 개발 타임라인

## Phase 1: 프로젝트 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/0A-priority-queue/silver-1927 study/Core-0A-Priority-Queue/1927
```

## Phase 2: Python 구현

`heapq` 직접 사용 (최소 힙).

## Phase 3: 테스트

```bash
make -C problem test
```

PASS.

## 사용 도구

- Python 3
- GNU Make
