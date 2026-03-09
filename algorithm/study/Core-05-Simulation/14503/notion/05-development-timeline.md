# BOJ 14503 — 개발 타임라인

## Phase 1: 프로젝트 구조 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/05-simulation/gold-14503 study/Core-05-Simulation/14503
```

Gold 등급이므로 `cpp/` 디렉토리 포함.

## Phase 2: 규칙 분석

문제 원문에서 로봇의 동작 규칙을 단계별로 정리:
1. 현재 칸 청소
2. 왼쪽 회전 → 전진 (4방향 탐색)
3. 막히면 후진 또는 종료

## Phase 3: Python 구현

```bash
vi python/src/solution.py
```

방향 벡터 + while 루프 + cleaned 배열 분리

## Phase 4: C++ 비교 구현

```bash
vi cpp/src/solution.cpp
g++-14 -std=c++17 -O2 -Wall -o cpp/build/solution cpp/src/solution.cpp
```

## Phase 5: 테스트

```bash
make -C problem test
make -C problem run-py
make -C problem run-cpp
```

PASS. Python과 C++ 결과 일치.

## 사용 도구

- Python 3
- g++-14 (`-std=c++17 -O2`)
- GNU Make
