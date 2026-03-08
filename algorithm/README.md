# Algorithm Study Archive

이 저장소는 `legacy/`의 알고리즘 풀이 트리를 읽기 전용 참조로 보존하면서, 새 학습용 구조를 `study/`에 다시 세운다. 목표는 정답 묶음이 아니라 재실행 가능한 학습 아카이브를 만드는 것이다.

## Repository Roles

- `legacy/`: 원본 참조 트리. 수정하지 않는다.
- `study/`: 현재 학습과 마이그레이션의 기준 구조
- `docs/`: 저장소 수준 감사 문서와 커리큘럼 문서
- `.gitignore`: local-only 노트와 빌드 산출물 무시 규칙

## Current State

- Legacy core backlog preserved: 42 problems
- Bridge project added: `study/Core-Bridges/1717`
- Advanced backlog documented under `study/Advanced-CLRS/README.md`

## Study Tracks

- [Core-00-Basics](study/Core-00-Basics/README.md): 기초 입출력, 문자열 순회, 배열 회전, LIS 입문을 통해 이후 전 트랙의 구현 기반을 만든다.
- [Core-01-Array-List](study/Core-01-Array-List/README.md): 배열 순회와 편집기/키로거 문제로 자료구조 선택의 비용 모델을 익힌다.
- [Core-02-Stack-Queue](study/Core-02-Stack-Queue/README.md): LIFO/FIFO/양방향 큐를 문제 규칙에 맞게 구현하는 감각을 만든다.
- [Core-03-BFS-DFS](study/Core-03-BFS-DFS/README.md): 정점 방문 순서, 그래프 표현, 격자 탐색의 기본기를 고정한다.
- [Core-04-Recursion-Backtracking](study/Core-04-Recursion-Backtracking/README.md): 재귀 호출 구조, 상태 복원, 탐색 가지치기를 작은 문제부터 누적한다.
- [Core-05-Simulation](study/Core-05-Simulation/README.md): 문제 설명을 상태 전이와 방향 규칙으로 번역하는 연습을 한다.
- [Core-06-Sorting](study/Core-06-Sorting/README.md): 기본 정렬, 복합 정렬 조건, 정렬 후 스위프라인으로 이어지는 패턴을 다룬다.
- [Core-07-Binary-Search-Hash](study/Core-07-Binary-Search-Hash/README.md): 검색 문제를 집합/카운터/매개변수 탐색으로 나누어 푼다.
- [Core-08-DP](study/Core-08-DP/README.md): 점화식 설계, 상태 정의, 1차원과 2차원 DP의 기초를 고정한다.
- [Core-09-Greedy](study/Core-09-Greedy/README.md): 그리디 선택 조건이 성립하는 경우와 아닌 경우를 사례로 구분한다.
- [Core-0A-Priority-Queue](study/Core-0A-Priority-Queue/README.md): 최소/최대 힙 조작과 힙 기반 그리디를 연결한다.
- [Core-0B-Graph-Tree](study/Core-0B-Graph-Tree/README.md): 트리 부모 찾기, 순회, 지름 문제로 그래프 후반부의 기반을 다진다.
- [Core-0C-Shortest-Path](study/Core-0C-Shortest-Path/README.md): Dijkstra와 Bellman-Ford를 문제 조건에 맞게 선택하는 법을 익힌다.
- [Core-0D-MST-Topo](study/Core-0D-MST-Topo/README.md): MST와 DAG 선행관계 문제를 그래프 학습의 마무리로 묶는다.
- [Core-Bridges](study/Core-Bridges/README.md): 그래프 후반부 전에 필요한 bridge 프로젝트
- [Advanced-CLRS](study/Advanced-CLRS/README.md): core 이후에 여는 심화 백로그

## Start Here

1. `docs/legacy-audit.md`에서 현재 기준선과 legacy 제약을 확인한다.
2. `docs/curriculum-map.md`에서 트랙 순서와 bridge rationale을 본다.
3. `study/Core-00-Basics/10988/README.md`로 파일럿 구조를 확인한다.
