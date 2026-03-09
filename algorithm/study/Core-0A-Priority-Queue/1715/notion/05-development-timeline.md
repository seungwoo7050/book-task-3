# BOJ 1715 — 개발 타임라인

## Phase 1: 프로젝트 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/0A-priority-queue/gold-1715 study/Core-0A-Priority-Queue/1715
```

Gold → `cpp/` 포함.

## Phase 2: Python 구현

`heapify` + 반복 pop-pop-push 패턴.

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
