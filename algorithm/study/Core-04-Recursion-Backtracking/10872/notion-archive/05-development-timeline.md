# BOJ 10872 — 개발 타임라인

## Phase 1: 프로젝트 구조 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/04-recursion-backtracking/bronze-10872 study/Core-04-Recursion-Backtracking/10872
tree study/Core-04-Recursion-Backtracking/10872/
```

## Phase 2: 구현

```bash
vi python/src/solution.py
```

5줄 구현: 재귀 함수 + 기저 조건 + 입력/출력

## Phase 3: 테스트

```bash
make -C problem test
make -C problem run-py
```

fixture 테스트 결과: PASS. $N = 0$ 엣지 케이스 포함.

## Phase 4: 문서화

```bash
vi docs/concepts/recursion-concept.md
```

## 사용 도구

- Python 3
- GNU Make (테스트 자동화)
