# BOJ 15649 — 개발 타임라인

## Phase 1: 프로젝트 구조 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/04-recursion-backtracking/silver-15649 study/Core-04-Recursion-Backtracking/15649
```

## Phase 2: 백트래킹 구현

```bash
vi python/src/solution.py
```

구현 순서:
1. `used` 배열 + `seq` 리스트 초기화
2. `backtrack(depth)` 재귀 함수 작성
3. 기저 조건: `depth == m`이면 결과 수집
4. 선택 → 재귀 → 되돌림 3단계 패턴
5. 출력 최적화

## Phase 3: 테스트

```bash
make -C problem test
make -C problem run-py
```

fixture 테스트 결과: PASS

## Phase 4: 문서화

```bash
vi docs/concepts/backtracking-concept.md
```

## 사용 도구

- Python 3
- GNU Make (테스트 자동화)
