# BOJ 7576 — 개발 타임라인

## Phase 1: 프로젝트 구조 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/03-bfs-dfs/gold-7576 study/Core-03-BFS-DFS/7576
tree study/Core-03-BFS-DFS/7576/
```

생성된 구조: `problem/`, `python/`, `cpp/`, `docs/`, `notion/`
- Gold 등급이므로 C++ 비교 구현 디렉토리도 포함

## Phase 2: Python 구현

```bash
vi python/src/solution.py
```

구현 순서:
1. 격자 입력 + 초기 소스 수집
2. 방향 벡터 기반 BFS 루프
3. 최대 일수 추적
4. 불가능 판별 로직

## Phase 3: C++ 비교 구현

```bash
vi cpp/src/solution.cpp
# 컴파일 및 테스트
g++-14 -std=c++17 -O2 -Wall -o cpp/build/solution cpp/src/solution.cpp
```

C++ 구현 시 주의점:
- `queue<tuple<int,int,int>>` 사용
- structured binding은 C++17 필수
- `ios_base::sync_with_stdio(false)` + `cin.tie(nullptr)`

## Phase 4: 테스트 및 검증

```bash
make -C problem test        # Python fixture PASS
make -C problem run-py      # 수동 확인
make -C problem run-cpp     # C++ 비교 확인
```

Python과 C++ 결과 일치 확인.

## Phase 5: 문서화

```bash
vi docs/concepts/multi-source-bfs-concept.md
vi docs/concepts/edge-cases.md
```

다중 소스 BFS 개념과 CLRS Ch 22.2 연결 정리.

## 사용 도구

- Python 3, `collections.deque`
- g++-14 (`-std=c++17 -O2 -Wall`)
- GNU Make (테스트 자동화)
