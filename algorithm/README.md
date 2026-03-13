# 알고리즘 학습 아카이브

이 저장소는 알고리즘 문제 풀이 코드를 쌓아 두는 저장소가 아니라 `문제 -> 이 레포의 답 -> 검증 -> 학습 노트` 계약으로 읽히는 study-first 아카이브다. GitHub 첫 화면에서 무엇을 풀었고, 공개 답안이 어디 있으며, 어떤 명령으로 다시 검증하는지 바로 찾을 수 있게 표면을 다시 고정한다.

| 항목 | 내용 |
| :--- | :--- |
| 트랙 수 | `16` |
| 프로젝트 수 | `53` |
| 현재 상태 | `verified 53/53` |
| 최신 확인 | `2026-03-11` |

## 이 레포가 푸는 문제군
- 작은 BOJ 문제를 자료구조, 탐색, DP, greedy, 그래프 후반부까지 학습 순서로 다시 묶는 문제군
- 문제 원문과 풀이 코드를 분리하고, 공개 해설과 장문 노트까지 함께 보이게 만드는 학습 아카이브 설계 문제
- CLRS 고급 주제를 실행 가능한 입출력 실험으로 다시 쪼개는 심화 문제군

## 지금 바로 읽는 순서
1. [docs/readme-contract.md](docs/readme-contract.md)에서 공개 표면 계약을 먼저 본다.
2. [study/README.md](study/README.md)에서 16개 트랙 인덱스와 대표 문제를 고른다.
3. [docs/project-catalog.md](docs/project-catalog.md)에서 `문제 | 답 | 검증 | 상태` 전체 색인을 확인한다.
4. 선택한 프로젝트 README에서 6문답 구조를 따라 `problem/ -> 구현 -> docs/ -> notion/` 순서로 내려간다.

## 검증 빠른 시작
- [docs/verification-matrix.md](docs/verification-matrix.md): 53개 전 프로젝트의 canonical verify command와 최신 확인일
- `make -C study/Core-00-Basics/10988/problem test`
- `make -C study/Core-03-BFS-DFS/7576/problem test`
- `make -C study/Core-0C-Shortest-Path/1753/problem test`
- `make -C study/Advanced-CLRS/0x14-network-flow/problem test`

## 트랙 인덱스
| 트랙 | 핵심 질문 | 대표 문제 | 답 위치 | 대표 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [Core-00-Basics](study/Core-00-Basics/README.md) | 작은 입력과 조건 분기를 어떻게 안정적으로 구현하고 검증할까? | [팰린드롬인지 확인하기](study/Core-00-Basics/10988/README.md) | `study/Core-00-Basics/*/python/src/` + `study/Core-00-Basics/*/cpp/src/` | `make -C study/Core-00-Basics/10988/problem test` | `verified` |
| [Core-01-Array-List](study/Core-01-Array-List/README.md) | 순차 자료구조 선택이 편집과 이동 비용을 어떻게 바꾸는가? | [개수 세기](study/Core-01-Array-List/10807/README.md) | `study/Core-01-Array-List/*/python/src/` + `study/Core-01-Array-List/*/cpp/src/` | `make -C study/Core-01-Array-List/10807/problem test` | `verified` |
| [Core-02-Stack-Queue](study/Core-02-Stack-Queue/README.md) | 명령 규칙을 LIFO/FIFO/덱 모델로 어떻게 옮길까? | [스택](study/Core-02-Stack-Queue/10828/README.md) | `study/Core-02-Stack-Queue/*/python/src/` + `study/Core-02-Stack-Queue/*/cpp/src/` | `make -C study/Core-02-Stack-Queue/10828/problem test` | `verified` |
| [Core-03-BFS-DFS](study/Core-03-BFS-DFS/README.md) | 그래프 표현과 방문 순서를 어떻게 고정할까? | [DFS와 BFS](study/Core-03-BFS-DFS/1260/README.md) | `study/Core-03-BFS-DFS/*/python/src/` + `study/Core-03-BFS-DFS/*/cpp/src/` | `make -C study/Core-03-BFS-DFS/1260/problem test` | `verified` |
| [Core-04-Recursion-Backtracking](study/Core-04-Recursion-Backtracking/README.md) | 재귀 호출 구조와 상태 복원을 어디까지 명시해야 할까? | [팩토리얼](study/Core-04-Recursion-Backtracking/10872/README.md) | `study/Core-04-Recursion-Backtracking/*/python/src/` + `study/Core-04-Recursion-Backtracking/*/cpp/src/` | `make -C study/Core-04-Recursion-Backtracking/10872/problem test` | `verified` |
| [Core-05-Simulation](study/Core-05-Simulation/README.md) | 긴 문제 설명을 작은 상태 전이 규칙으로 어떻게 쪼갤까? | [음계](study/Core-05-Simulation/2920/README.md) | `study/Core-05-Simulation/*/python/src/` + `study/Core-05-Simulation/*/cpp/src/` | `make -C study/Core-05-Simulation/2920/problem test` | `verified` |
| [Core-06-Sorting](study/Core-06-Sorting/README.md) | 정렬 기준과 정렬 후 후처리를 어떻게 분리할까? | [수 정렬하기](study/Core-06-Sorting/2750/README.md) | `study/Core-06-Sorting/*/python/src/` + `study/Core-06-Sorting/*/cpp/src/` | `make -C study/Core-06-Sorting/2750/problem test` | `verified` |
| [Core-07-Binary-Search-Hash](study/Core-07-Binary-Search-Hash/README.md) | 탐색 대상을 어떻게 재정의해 선형 탐색을 벗어날까? | [수 찾기](study/Core-07-Binary-Search-Hash/1920/README.md) | `study/Core-07-Binary-Search-Hash/*/python/src/` + `study/Core-07-Binary-Search-Hash/*/cpp/src/` | `make -C study/Core-07-Binary-Search-Hash/1920/problem test` | `verified` |
| [Core-08-DP](study/Core-08-DP/README.md) | 상태와 전이를 표의 의미로 끝까지 유지하려면 무엇을 고정해야 할까? | [피보나치 수 2](study/Core-08-DP/2748/README.md) | `study/Core-08-DP/*/python/src/` + `study/Core-08-DP/*/cpp/src/` | `make -C study/Core-08-DP/2748/problem test` | `verified` |
| [Core-09-Greedy](study/Core-09-Greedy/README.md) | 탐욕 선택이 전체 최적과 맞는 이유를 어떻게 설명할까? | [동전 0](study/Core-09-Greedy/11047/README.md) | `study/Core-09-Greedy/*/python/src/` + `study/Core-09-Greedy/*/cpp/src/` | `make -C study/Core-09-Greedy/11047/problem test` | `verified` |
| [Core-0A-Priority-Queue](study/Core-0A-Priority-Queue/README.md) | 힙이 필요한 문제 구조를 어떻게 구분할까? | [최대 힙](study/Core-0A-Priority-Queue/11279/README.md) | `study/Core-0A-Priority-Queue/*/python/src/` + `study/Core-0A-Priority-Queue/*/cpp/src/` | `make -C study/Core-0A-Priority-Queue/11279/problem test` | `verified` |
| [Core-0B-Graph-Tree](study/Core-0B-Graph-Tree/README.md) | 트리 성질을 이용해 탐색과 누적 계산을 어떻게 단순화할까? | [트리의 부모 찾기](study/Core-0B-Graph-Tree/11725/README.md) | `study/Core-0B-Graph-Tree/*/python/src/` + `study/Core-0B-Graph-Tree/*/cpp/src/` | `make -C study/Core-0B-Graph-Tree/11725/problem test` | `verified` |
| [Core-0C-Shortest-Path](study/Core-0C-Shortest-Path/README.md) | 가중치 조건에 따라 어떤 최단 경로 알고리즘을 골라야 할까? | [최소비용 구하기](study/Core-0C-Shortest-Path/1916/README.md) | `study/Core-0C-Shortest-Path/*/python/src/` + `study/Core-0C-Shortest-Path/*/cpp/src/` | `make -C study/Core-0C-Shortest-Path/1916/problem test` | `verified` |
| [Core-Bridges](study/Core-Bridges/README.md) | 다음 트랙 전에 어떤 선행 개념을 별도 실습으로 고정할까? | [집합의 표현](study/Core-Bridges/1717/README.md) | `study/Core-Bridges/*/python/src/` | `make -C study/Core-Bridges/1717/problem test` | `verified` |
| [Core-0D-MST-Topo](study/Core-0D-MST-Topo/README.md) | 그래프 전체 구조나 순서를 만드는 규칙을 어떻게 설명할까? | [상근이의 여행](study/Core-0D-MST-Topo/9372/README.md) | `study/Core-0D-MST-Topo/*/python/src/` + `study/Core-0D-MST-Topo/*/cpp/src/` | `make -C study/Core-0D-MST-Topo/9372/problem test` | `verified` |
| [Advanced-CLRS](study/Advanced-CLRS/README.md) | proof-heavy 주제를 실행 가능한 실험으로 어떻게 바꿀까? | [Strassen 행렬 곱셈](study/Advanced-CLRS/0x10-strassen-matrix/README.md) | `study/Advanced-CLRS/*/python/src/` | `make -C study/Advanced-CLRS/0x10-strassen-matrix/problem test` | `verified` |

## 문서 지도
- [docs/readme-contract.md](docs/readme-contract.md): 루트, 트랙, 프로젝트, 하위 README가 각각 답해야 할 질문
- [docs/project-catalog.md](docs/project-catalog.md): 53개 프로젝트 전체 카탈로그
- [docs/verification-matrix.md](docs/verification-matrix.md): canonical verify command와 최신 확인일
- [docs/curriculum-map.md](docs/curriculum-map.md): 왜 이 순서로 문제를 배치했는지 설명하는 커리큘럼 맵
- [study/blog/README.md](study/blog/README.md): Gold 14개 프로젝트의 code-first blog series 인덱스
- [docs/migration-template.md](docs/migration-template.md): 새 프로젝트나 재정리 라운드에 쓰는 질문형 템플릿
