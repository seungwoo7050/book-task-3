# BOJ 14891 — 개발 타임라인

## Phase 1: 프로젝트 구조 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/05-simulation/silver-14891 study/Core-05-Simulation/14891
```

## Phase 2: 구현

```bash
vi python/src/solution.py
```

구현 순서:
1. 톱니바퀴를 deque로 읽기
2. 전파 방향 결정 (왼쪽/오른쪽)
3. 회전 적용
4. 점수 계산

## Phase 3: 테스트

```bash
make -C problem test
make -C problem run-py
```

PASS.

## 사용 도구

- Python 3, `collections.deque`
- GNU Make
