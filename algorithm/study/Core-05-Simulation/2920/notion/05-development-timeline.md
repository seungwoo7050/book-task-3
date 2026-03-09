# BOJ 2920 — 개발 타임라인

## Phase 1: 프로젝트 구조 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/05-simulation/bronze-2920 study/Core-05-Simulation/2920
```

## Phase 2: 구현

```bash
vi python/src/solution.py
```

3줄 조건문으로 완성.

## Phase 3: 테스트

```bash
make -C problem test
```

PASS.

## 사용 도구

- Python 3
- GNU Make
