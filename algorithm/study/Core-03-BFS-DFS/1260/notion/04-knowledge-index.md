# 지식 인덱스

> 프로젝트: DFS와 BFS
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 알고리즘

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| DFS (깊이 우선 탐색) | Ch 22.3 | 재귀/스택 기반, 간선 분류, 위상 정렬의 기반 |
| BFS (너비 우선 탐색) | Ch 22.2 | 큐 기반, 최단 거리 계산, 레벨 단위 탐색 |

## 자료구조 사용

- **인접 리스트**: 그래프 표현, $O(V + E)$ 공간
- **deque**: BFS의 FIFO 큐, $O(1)$ popleft
- **재귀 호출 스택**: DFS의 암묵적 스택

## 시간 복잡도

- DFS: $O(V + E)$ — 모든 정점과 간선을 한 번씩 방문
- BFS: $O(V + E)$ — 동일
- 인접 리스트 정렬: $O(V \cdot d \log d)$, $d$는 최대 차수

## 연결 문제

- **BOJ 24479** (Core-03): DFS 방문 순서 기록 — 이 문제의 DFS 부분을 확장
- **BOJ 7576** (Core-03): 다중 소스 BFS — BFS를 여러 시작점으로 확장
- **BOJ 2606** (바이러스): BFS/DFS로 연결 요소 크기 세기
- **BOJ 1012** (유기농 배추): 연결 요소 개수 세기

## Python 특이사항

- `sys.setrecursionlimit`: 깊은 재귀에 필수
- `collections.deque`: `list.pop(0)`은 $O(n)$이므로 반드시 deque 사용
- 1-indexed 정점: `adj = [[] for _ in range(n + 1)]`로 1번부터 사용

## 다시 연결해 볼 질문

- `DFS와 BFS`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `그래프 표현을 고르고 방문 순서를 안정적으로 제어하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `DFS와 BFS`를 다시 설명할 때는 문제 이름보다 `그래프 표현을 고르고 방문 순서를 안정적으로 제어하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 다음 프로젝트: [`../../24479/README.md`](../../24479/README.md) (알고리즘 수업 - 깊이 우선 탐색 1)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`dfs-bfs-concept.md`](../docs/concepts/dfs-bfs-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
