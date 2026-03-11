# 알고리즘 학습 아카이브

이 저장소는 알고리즘 문제 풀이를 정답 모음으로 쌓아 두는 대신, 문제 자료와 구현, 공개 해설, 장문 학습 노트를 분리해 읽을 수 있는 학습 아카이브로 다시 정리한 레포다.
목표는 "이 문제를 풀었다"에서 멈추지 않고, **왜 이런 구조로 공부했는지**까지 다른 사람이 따라올 수 있게 만드는 것이다.

## 이 레포로 배우는 것

- 문제 원문, 구현, 공개 문서를 한 저장소 안에서 어떻게 분리해야 하는지
- 작은 문제부터 그래프 후반부, CLRS 심화까지 어떤 순서로 밟으면 좋은지
- 학습 레포를 읽는 사람이 자신의 공개 포트폴리오 레포를 어떻게 더 잘 설계할 수 있는지

## 누가 읽으면 좋은가

- 백준과 CLRS를 함께 공부하면서, 문제 풀이 기록을 구조적으로 남기고 싶은 학생
- 정답 코드만 나열된 레포가 아니라 "문제 자료 / 구현 / 해설 / 장문 노트"가 분리된 학습 레포를 만들고 싶은 사람
- 나중에 자신의 포트폴리오 레포를 공개할 때 무엇을 남기고 무엇을 숨길지 기준이 필요한 사람

## 추천 읽기 순서

1. [docs/legacy-audit.md](docs/legacy-audit.md)에서 현재 기준선과 provenance 규칙을 본다.
2. [docs/curriculum-map.md](docs/curriculum-map.md)에서 트랙 순서와 브리지 프로젝트 이유를 본다.
3. [study/README.md](study/README.md)에서 전체 학습 트리를 훑는다.
4. [study/Core-00-Basics/10988/README.md](study/Core-00-Basics/10988/README.md) 같은 작은 프로젝트 하나를 끝까지 읽는다.
5. 익숙해지면 같은 형식을 자기 레포에 그대로 옮겨 본다.

## 학습 경로 한눈에 보기

- 필수 코스: `Core-00-Basics` -> `Core-01-Array-List` -> `Core-02-Stack-Queue` -> `Core-03-BFS-DFS` -> `Core-04-Recursion-Backtracking` -> `Core-05-Simulation` -> `Core-06-Sorting` -> `Core-07-Binary-Search-Hash` -> `Core-08-DP` -> `Core-09-Greedy` -> `Core-0A-Priority-Queue` -> `Core-0B-Graph-Tree` -> `Core-0C-Shortest-Path` -> `Core-Bridges` -> `Core-0D-MST-Topo`
- 심화 코스: `Advanced-CLRS`
- `Core-Bridges`는 선택 보강이 아니라 `Core-0D-MST-Topo` 전에 두는 필수 브리지로 읽는 편이 좋다.

## 필수 코스 트랙

- [Core-00-Basics](study/Core-00-Basics/README.md): 입출력, 문자열, 배열, 가장 짧은 DP 브리지를 통해 이후 모든 트랙에서 필요한 기본 구현 습관을 잡는 출발점이다.
- [Core-01-Array-List](study/Core-01-Array-List/README.md): 배열 순회와 편집기 시뮬레이션을 묶어, 자료구조 선택이 성능과 구현 난이도에 어떤 차이를 만드는지 체감하게 한다.
- [Core-02-Stack-Queue](study/Core-02-Stack-Queue/README.md): LIFO/FIFO/덱의 차이를 문제 규칙과 연결해, 자료구조 이름이 아니라 동작 모델로 이해하게 하는 트랙이다.
- [Core-03-BFS-DFS](study/Core-03-BFS-DFS/README.md): 정점 방문 순서, 그래프 표현, 격자 탐색을 묶어 BFS/DFS의 기본기를 고정하는 트랙이다.
- [Core-04-Recursion-Backtracking](study/Core-04-Recursion-Backtracking/README.md): 재귀 호출의 구조를 이해하고, 상태 복원과 가지치기를 작은 문제에서 큰 문제로 확장해 보는 트랙이다.
- [Core-05-Simulation](study/Core-05-Simulation/README.md): 문제 설명을 상태 전이 규칙으로 번역하는 힘을 키우는 트랙이다. 구현은 길어도 논리는 짧게 정리하는 연습이 핵심이다.
- [Core-06-Sorting](study/Core-06-Sorting/README.md): 기본 정렬부터 다중 기준 정렬, 정렬 후 스위프 라인까지 자연스럽게 확장되는 트랙이다.
- [Core-07-Binary-Search-Hash](study/Core-07-Binary-Search-Hash/README.md): 탐색 문제를 선형 탐색으로 버티지 않고, 집합/카운터/매개변수 탐색으로 재구성하는 방법을 익히는 트랙이다.
- [Core-08-DP](study/Core-08-DP/README.md): 점화식, 상태 정의, 전이 방향을 가장 기본적인 형태부터 차근차근 고정하는 트랙이다.
- [Core-09-Greedy](study/Core-09-Greedy/README.md): 매 단계에서 가장 좋아 보이는 선택이 전체 최적과 맞물리는 조건을 사례 중심으로 익히는 트랙이다.
- [Core-0A-Priority-Queue](study/Core-0A-Priority-Queue/README.md): 힙을 직접 구현하기보다, 힙이 필요한 문제 구조를 구분하는 감각을 키우는 트랙이다.
- [Core-0B-Graph-Tree](study/Core-0B-Graph-Tree/README.md): 트리 구조를 별도 자료형으로 다루며, 부모 찾기, 순회, 지름 계산 같은 대표 패턴을 익히는 트랙이다.
- [Core-0C-Shortest-Path](study/Core-0C-Shortest-Path/README.md): 가중치 조건에 따라 Dijkstra와 Bellman-Ford를 고르는 기준을 실전 문제로 익히는 트랙이다.
- [Core-Bridges](study/Core-Bridges/README.md): 정규 트랙 사이의 학습 공백을 메우는 보강 프로젝트 모음이다. 지금은 union-find를 독립적으로 다룬다.
- [Core-0D-MST-Topo](study/Core-0D-MST-Topo/README.md): 그래프 학습 후반부에서 가장 자주 다시 만나는 두 패턴인 최소 스패닝 트리와 선행관계 정렬을 묶은 트랙이다.

## 심화 코스 트랙

- [Advanced-CLRS](study/Advanced-CLRS/README.md): Core를 지나 CLRS의 고급 주제를 직접 구현 가능한 작은 실험으로 바꿔 보는 심화 트랙이다.

## 이 레포를 자기 포트폴리오로 옮길 때의 기준

- `problem/`, 구현 디렉터리, 공개 문서, 장문 노트를 섞지 않는다.
- README는 "문제 설명 복붙"이 아니라 "어떻게 읽고 어떻게 검증하는가"를 안내해야 한다.
- `make test` 같은 재현 명령이 없다면, 설명이 좋아 보여도 학습 기록으로서 신뢰도가 떨어진다.
- 빠른 검증 명령은 `docs/references/reproducibility.md`에, 전체 재현 흐름은 `notion/05-development-timeline.md`에 나눠 두면 학습자가 따라오기 쉽다.
- 장문 노트는 공개용 `notion/`과 보관용 `notion-archive/`로 나눠 버전을 관리한다.

## 현재 워크스페이스 기준 메모

- 총 프로젝트 수: 53
- 자동 검증 통과: 53/53 (`make -C problem test` 기준)
- 트랙 수: 16
- 현재 작업 트리에는 `legacy/` 디렉터리가 없으므로, 문서에서는 legacy를 필수 경로가 아니라 선택적 provenance 자료로만 다룬다.
