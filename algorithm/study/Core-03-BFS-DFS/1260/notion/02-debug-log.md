# 디버그 로그

> 프로젝트: DFS와 BFS
> 아래 내용은 `notion-archive/02-debug-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 함정 1: 인접 리스트 정렬 누락

**증상**: DFS 방문 순서가 예제와 다르게 출력됨

**원인**: 간선 입력 순서대로 인접 리스트가 구성되므로, 정렬하지 않으면 "번호가 작은 정점 먼저" 조건을 위반한다.

**해결**: 입력 완료 후 `adj[i].sort()`를 모든 정점에 대해 수행. 이 정렬은 DFS와 BFS 양쪽에 영향을 미치므로 한 번만 하면 된다.

## 함정 2: visited 배열 공유

**증상**: BFS 출력에서 정점 수가 예상보다 적음

**원인**: DFS에서 사용한 visited 배열을 BFS에서 초기화 없이 재사용. DFS가 이미 모든 정점을 방문한 상태여서 BFS가 탐색할 정점이 없었다.

**해결**: BFS 시작 전 `visited = [False] * (n + 1)`로 새 배열 생성.

## 함정 3: 재귀 한도

**증상**: $N = 1000$인 체인 그래프에서 RecursionError 발생

**원인**: Python 기본 재귀 한도는 1000. 최악의 경우 DFS가 1000 깊이까지 들어간다.

**해결**: `sys.setrecursionlimit(10000)` 설정. 문제 제약이 $N \leq 1000$이므로 10000이면 충분하다.

## 확인 과정

`make -C problem test`로 제공된 fixture 테스트 통과 확인. 연결 그래프와 비연결 그래프 케이스 모두 검증.

## 왜 이 디버그 메모가 중요한가

- `DFS와 BFS`는 `그래프 표현을 고르고 방문 순서를 안정적으로 제어하는 연습`를 연습하는 프로젝트라서, 작은 경계 조건 하나가 전체 상태 전이를 망가뜨릴 수 있다.
- 그래서 이 문서는 "무엇이 틀렸는가"보다 "어떤 징후를 보면 같은 실수를 다시 알아차릴 수 있는가"를 남기는 데 의미가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 재현 경로가 필요할 때는 `05-development-timeline.md`의 단계 순서와 이 디버그 로그를 같이 보면, 어느 시점에 어떤 실패를 확인해야 하는지 더 선명해진다.

## 다음 수정 때 다시 볼 체크리스트

- 가장 작은 입력과 대표 경계 입력을 먼저 다시 실행했는가?
- 상태를 갱신하는 순서가 문제 규칙과 정확히 같은가?
- `make -C problem test` 결과와 문서 설명이 서로 어긋나지 않는가?

## 같이 점검할 문서

- [`dfs-bfs-concept.md`](../docs/concepts/dfs-bfs-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
