# BOJ 1260 — 개발 타임라인

## Phase 1: 프로젝트 구조 생성

```bash
# legacy에서 study 구조로 마이그레이션
python3 tools/migrate_legacy_to_study.py legacy/core/03-bfs-dfs/silver-1260 study/Core-03-BFS-DFS/1260

# 디렉토리 구조 확인
tree study/Core-03-BFS-DFS/1260/
```

생성된 구조: `problem/`, `python/`, `docs/`, `notion/`

## Phase 2: 문제 분석 및 구현

```bash
# 문제 원문 확인
cat problem/README.md

# Python 풀이 작성
vi python/src/solution.py
```

구현 순서:
1. 인접 리스트 구성 + 정렬
2. 재귀 DFS 구현
3. deque BFS 구현
4. 출력 포맷팅

## Phase 3: 테스트 및 검증

```bash
# fixture 테스트 실행
make -C problem test

# 대표 입력으로 수동 확인
make -C problem run-py
```

fixture 테스트 결과: PASS

## Phase 4: 문서화

```bash
# 개념 문서 작성
vi docs/concepts/dfs-bfs-concept.md
vi docs/concepts/edge-cases.md
```

개념 정리: DFS/BFS 의사코드, 자료구조, 시간 복잡도 비교

## 사용 도구

- Python 3, `collections.deque`
- GNU Make (테스트 자동화)
- `sys.setrecursionlimit` (재귀 한도 조정)
