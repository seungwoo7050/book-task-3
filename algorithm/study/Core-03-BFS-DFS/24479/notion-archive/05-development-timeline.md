# BOJ 24479 — 개발 타임라인

## Phase 1: 프로젝트 구조 생성

```bash
python3 tools/migrate_legacy_to_study.py legacy/core/03-bfs-dfs/bronze-24479 study/Core-03-BFS-DFS/24479
tree study/Core-03-BFS-DFS/24479/
```

생성된 구조: `problem/`, `python/`, `docs/`, `notion/`

## Phase 2: 1260 코드 기반 수정

```bash
# 1260 풀이를 참고하여 변형
cp ../1260/python/src/solution.py python/src/solution.py
vi python/src/solution.py
```

변경 사항:
1. BFS 부분 제거 (DFS만 필요)
2. `dfs_order` 리스트 대신 `result` 배열 + `order` 카운터
3. `setrecursionlimit` 200000으로 상향
4. 출력을 `'\n'.join`으로 변경

## Phase 3: 테스트 및 검증

```bash
make -C problem test
make -C problem run-py
```

fixture 테스트 결과: PASS

## Phase 4: 문서화

```bash
vi docs/concepts/dfs-visit-order.md
vi docs/concepts/edge-cases.md
```

## 사용 도구

- Python 3, `sys.setrecursionlimit`
- GNU Make (테스트 자동화)
- 1260 풀이를 기반으로 변형 (코드 재사용)
