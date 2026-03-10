# BOJ 11279 — 개발 타임라인

## Phase 1: 프로젝트 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/0A-priority-queue/bronze-11279 study/Core-0A-Priority-Queue/11279
```

## Phase 2: Python 구현

`heapq` + 부호 반전 패턴.

## Phase 3: 테스트

```bash
make -C problem test
```

PASS.

## 사용 도구

- Python 3
- GNU Make
