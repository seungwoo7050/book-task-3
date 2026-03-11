# study/ 안내

`study/`는 이 저장소의 실제 학습 트리다. 각 트랙 README는 `왜 이 문제가 여기 있는가`, 각 프로젝트 README는 `내 답이 어디 있고 어떻게 다시 검증하는가`를 먼저 보여 주도록 맞춘다.

## 읽는 순서
1. 관심 트랙의 핵심 질문을 고른다.
2. 트랙 README의 프로젝트 카탈로그에서 문제와 답 위치를 고른다.
3. 프로젝트 README의 6문답 구조를 따라 `problem/ -> 구현 -> docs/ -> notion/` 순서로 내려간다.

## 트랙 인덱스
| 트랙 | 핵심 질문 | 대표 문제 | 답 위치 | 대표 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [Core-00-Basics](Core-00-Basics/README.md) | 작은 입력과 조건 분기를 어떻게 안정적으로 구현하고 검증할까? | [팰린드롬인지 확인하기](Core-00-Basics/10988/README.md) | `study/Core-00-Basics/*/python/src/` + `study/Core-00-Basics/*/cpp/src/` | `make -C study/Core-00-Basics/10988/problem test` | `verified` |
| [Core-01-Array-List](Core-01-Array-List/README.md) | 순차 자료구조 선택이 편집과 이동 비용을 어떻게 바꾸는가? | [개수 세기](Core-01-Array-List/10807/README.md) | `study/Core-01-Array-List/*/python/src/` + `study/Core-01-Array-List/*/cpp/src/` | `make -C study/Core-01-Array-List/10807/problem test` | `verified` |
| [Core-02-Stack-Queue](Core-02-Stack-Queue/README.md) | 명령 규칙을 LIFO/FIFO/덱 모델로 어떻게 옮길까? | [스택](Core-02-Stack-Queue/10828/README.md) | `study/Core-02-Stack-Queue/*/python/src/` + `study/Core-02-Stack-Queue/*/cpp/src/` | `make -C study/Core-02-Stack-Queue/10828/problem test` | `verified` |
| [Core-03-BFS-DFS](Core-03-BFS-DFS/README.md) | 그래프 표현과 방문 순서를 어떻게 고정할까? | [DFS와 BFS](Core-03-BFS-DFS/1260/README.md) | `study/Core-03-BFS-DFS/*/python/src/` + `study/Core-03-BFS-DFS/*/cpp/src/` | `make -C study/Core-03-BFS-DFS/1260/problem test` | `verified` |
| [Core-04-Recursion-Backtracking](Core-04-Recursion-Backtracking/README.md) | 재귀 호출 구조와 상태 복원을 어디까지 명시해야 할까? | [팩토리얼](Core-04-Recursion-Backtracking/10872/README.md) | `study/Core-04-Recursion-Backtracking/*/python/src/` + `study/Core-04-Recursion-Backtracking/*/cpp/src/` | `make -C study/Core-04-Recursion-Backtracking/10872/problem test` | `verified` |
| [Core-05-Simulation](Core-05-Simulation/README.md) | 긴 문제 설명을 작은 상태 전이 규칙으로 어떻게 쪼갤까? | [음계](Core-05-Simulation/2920/README.md) | `study/Core-05-Simulation/*/python/src/` + `study/Core-05-Simulation/*/cpp/src/` | `make -C study/Core-05-Simulation/2920/problem test` | `verified` |
| [Core-06-Sorting](Core-06-Sorting/README.md) | 정렬 기준과 정렬 후 후처리를 어떻게 분리할까? | [수 정렬하기](Core-06-Sorting/2750/README.md) | `study/Core-06-Sorting/*/python/src/` + `study/Core-06-Sorting/*/cpp/src/` | `make -C study/Core-06-Sorting/2750/problem test` | `verified` |
| [Core-07-Binary-Search-Hash](Core-07-Binary-Search-Hash/README.md) | 탐색 대상을 어떻게 재정의해 선형 탐색을 벗어날까? | [수 찾기](Core-07-Binary-Search-Hash/1920/README.md) | `study/Core-07-Binary-Search-Hash/*/python/src/` + `study/Core-07-Binary-Search-Hash/*/cpp/src/` | `make -C study/Core-07-Binary-Search-Hash/1920/problem test` | `verified` |
| [Core-08-DP](Core-08-DP/README.md) | 상태와 전이를 표의 의미로 끝까지 유지하려면 무엇을 고정해야 할까? | [피보나치 수 2](Core-08-DP/2748/README.md) | `study/Core-08-DP/*/python/src/` + `study/Core-08-DP/*/cpp/src/` | `make -C study/Core-08-DP/2748/problem test` | `verified` |
| [Core-09-Greedy](Core-09-Greedy/README.md) | 탐욕 선택이 전체 최적과 맞는 이유를 어떻게 설명할까? | [동전 0](Core-09-Greedy/11047/README.md) | `study/Core-09-Greedy/*/python/src/` + `study/Core-09-Greedy/*/cpp/src/` | `make -C study/Core-09-Greedy/11047/problem test` | `verified` |
| [Core-0A-Priority-Queue](Core-0A-Priority-Queue/README.md) | 힙이 필요한 문제 구조를 어떻게 구분할까? | [최대 힙](Core-0A-Priority-Queue/11279/README.md) | `study/Core-0A-Priority-Queue/*/python/src/` + `study/Core-0A-Priority-Queue/*/cpp/src/` | `make -C study/Core-0A-Priority-Queue/11279/problem test` | `verified` |
| [Core-0B-Graph-Tree](Core-0B-Graph-Tree/README.md) | 트리 성질을 이용해 탐색과 누적 계산을 어떻게 단순화할까? | [트리의 부모 찾기](Core-0B-Graph-Tree/11725/README.md) | `study/Core-0B-Graph-Tree/*/python/src/` + `study/Core-0B-Graph-Tree/*/cpp/src/` | `make -C study/Core-0B-Graph-Tree/11725/problem test` | `verified` |
| [Core-0C-Shortest-Path](Core-0C-Shortest-Path/README.md) | 가중치 조건에 따라 어떤 최단 경로 알고리즘을 골라야 할까? | [최소비용 구하기](Core-0C-Shortest-Path/1916/README.md) | `study/Core-0C-Shortest-Path/*/python/src/` + `study/Core-0C-Shortest-Path/*/cpp/src/` | `make -C study/Core-0C-Shortest-Path/1916/problem test` | `verified` |
| [Core-Bridges](Core-Bridges/README.md) | 다음 트랙 전에 어떤 선행 개념을 별도 실습으로 고정할까? | [집합의 표현](Core-Bridges/1717/README.md) | `study/Core-Bridges/*/python/src/` | `make -C study/Core-Bridges/1717/problem test` | `verified` |
| [Core-0D-MST-Topo](Core-0D-MST-Topo/README.md) | 그래프 전체 구조나 순서를 만드는 규칙을 어떻게 설명할까? | [상근이의 여행](Core-0D-MST-Topo/9372/README.md) | `study/Core-0D-MST-Topo/*/python/src/` + `study/Core-0D-MST-Topo/*/cpp/src/` | `make -C study/Core-0D-MST-Topo/9372/problem test` | `verified` |
| [Advanced-CLRS](Advanced-CLRS/README.md) | proof-heavy 주제를 실행 가능한 실험으로 어떻게 바꿀까? | [Strassen 행렬 곱셈](Advanced-CLRS/0x10-strassen-matrix/README.md) | `study/Advanced-CLRS/*/python/src/` | `make -C study/Advanced-CLRS/0x10-strassen-matrix/problem test` | `verified` |

## 함께 보는 문서
- [../docs/readme-contract.md](../docs/readme-contract.md)
- [../docs/project-catalog.md](../docs/project-catalog.md)
- [../docs/verification-matrix.md](../docs/verification-matrix.md)
- [../docs/curriculum-map.md](../docs/curriculum-map.md)
