# BOJ 11047 — 개발 타임라인

## Phase 1: 프로젝트 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/09-greedy/bronze-11047 study/Core-09-Greedy/11047
```

Bronze → C++ 미포함.

## Phase 2: Python 구현

`reversed` + 나눗셈/나머지 패턴.

## Phase 3: 테스트

```bash
make -C problem test
```

PASS.

## 사용 도구

- Python 3
- GNU Make
