# BOJ 9663 — 개발 타임라인

## Phase 1: 프로젝트 구조 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/04-recursion-backtracking/gold-9663 study/Core-04-Recursion-Backtracking/9663
tree study/Core-04-Recursion-Backtracking/9663/
```

Gold 등급이므로 `cpp/` 디렉토리 포함.

## Phase 2: Python 구현

```bash
vi python/src/solution.py
```

구현 순서:
1. 대각선 인코딩 설계 (`row - col + n - 1`, `row + col`)
2. `place(row)` 백트래킹 함수 작성
3. `nonlocal count` 카운터 관리

## Phase 3: C++ 비교 구현

```bash
vi cpp/src/solution.cpp
g++-14 -std=c++17 -O2 -Wall -o cpp/build/solution cpp/src/solution.cpp
```

전역 배열로 간결하게 구현. `place(row)` 재귀 구조는 Python과 동일.

## Phase 4: 성능 비교

```bash
echo "15" | python3 python/src/solution.py   # ~10초
echo "15" | ./cpp/build/solution              # <1초
```

C++이 약 10배 이상 빠름 확인.

## Phase 5: 테스트 및 문서화

```bash
make -C problem test
make -C problem run-cpp
vi docs/concepts/backtracking-pruning-concept.md
```

## 사용 도구

- Python 3, `nonlocal` 키워드
- g++-14 (`-std=c++17 -O2 -Wall`)
- GNU Make (테스트 자동화)
- 시간 측정: `time` 명령어
