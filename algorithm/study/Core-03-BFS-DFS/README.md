# Core-03-BFS-DFS

## 트랙 한 줄 질문

그래프 표현과 방문 순서를 어떻게 고정할까?

## 왜 이 순서인가

그래프 탐색은 이후 트리, 최단 경로, 위상 정렬의 기반이다. 방문 처리와 큐/스택 규칙을 여기서 확실히 잡아야 뒤가 편해진다.

## 프로젝트 카탈로그

| 순서 | 프로젝트 | 문제가 뭐였나 | 이 레포의 답 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | [1260](1260/README.md) | `DFS와 BFS` | `python/src/` | `make -C study/Core-03-BFS-DFS/1260/problem test` | `verified` |
| 2 | [24479](24479/README.md) | `알고리즘 수업 - 깊이 우선 탐색 1` | `python/src/` | `make -C study/Core-03-BFS-DFS/24479/problem test` | `verified` |
| 3 | [7576](7576/README.md) | `토마토` | `python/src/`, `cpp/src/` | `make -C study/Core-03-BFS-DFS/7576/problem test` | `verified` |

## 공통 읽기 순서

1. [../README.md](../README.md)에서 전체 트랙 인덱스를 확인한다.
2. [../../docs/curriculum-map.md](../../docs/curriculum-map.md)에서 이 트랙이 놓인 이유를 본다.
3. 원하는 프로젝트 README에서 6문답을 먼저 읽고 `problem/ -> 구현 -> docs/ -> notion/` 순서로 내려간다.

## 포트폴리오 관점 메모

탐색 문제는 정답 코드보다도 '방문 처리 시점'을 설명하는 문장이 중요하다. 그 한 줄이 있으면 문서 품질이 크게 좋아진다.
