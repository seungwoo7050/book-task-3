# 프로젝트 카탈로그

`2026-03-11` 기준 전체 53개 프로젝트를 `문제 | 답 | 검증 | 상태` 관점으로 묶은 색인이다.

## Core-00-Basics

| 트랙 | 프로젝트 | 문제가 뭐였나 | 이 레포의 답 | 구현 경로 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Core-00-Basics` | [10988](../study/Core-00-Basics/10988/README.md) | `팰린드롬인지 확인하기` | `양끝 포인터(two pointers)로 좌우 문자를 동시에 비교` | `study/Core-00-Basics/10988/python/src` | `make -C study/Core-00-Basics/10988/problem test` | `verified` |
| `Core-00-Basics` | [11053](../study/Core-00-Basics/11053/README.md) | `가장 긴 증가하는 부분 수열` | `1차원 DP로 각 위치에서 끝나는 LIS 길이를 누적 계산` | `study/Core-00-Basics/11053/python/src`, `study/Core-00-Basics/11053/cpp/src` | `make -C study/Core-00-Basics/11053/problem test` | `verified` |
| `Core-00-Basics` | [16926](../study/Core-00-Basics/16926/README.md) | `배열 돌리기 1` | `레이어 분해(layer decomposition) 후 각 테두리를 독립적으로 회전` | `study/Core-00-Basics/16926/python/src` | `make -C study/Core-00-Basics/16926/problem test` | `verified` |

## Core-01-Array-List

| 트랙 | 프로젝트 | 문제가 뭐였나 | 이 레포의 답 | 구현 경로 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Core-01-Array-List` | [10807](../study/Core-01-Array-List/10807/README.md) | `개수 세기` | `단일 선형 스캔으로 목표 값 v의 출현 횟수를 집계` | `study/Core-01-Array-List/10807/python/src` | `make -C study/Core-01-Array-List/10807/problem test` | `verified` |
| `Core-01-Array-List` | [5397](../study/Core-01-Array-List/5397/README.md) | `키로거` | `키 입력 문자열을 좌/우 버퍼로 시뮬레이션하는 keylogger 처리` | `study/Core-01-Array-List/5397/python/src`, `study/Core-01-Array-List/5397/cpp/src` | `make -C study/Core-01-Array-List/5397/problem test` | `verified` |
| `Core-01-Array-List` | [1406](../study/Core-01-Array-List/1406/README.md) | `에디터` | `커서를 기준으로 좌/우 스택(또는 리스트) 두 개를 유지하는 editor simulation` | `study/Core-01-Array-List/1406/python/src` | `make -C study/Core-01-Array-List/1406/problem test` | `verified` |

## Core-02-Stack-Queue

| 트랙 | 프로젝트 | 문제가 뭐였나 | 이 레포의 답 | 구현 경로 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Core-02-Stack-Queue` | [10828](../study/Core-02-Stack-Queue/10828/README.md) | `스택` | `명령형 스택 연산을 조건 분기와 리스트 push/pop으로 구현` | `study/Core-02-Stack-Queue/10828/python/src` | `make -C study/Core-02-Stack-Queue/10828/problem test` | `verified` |
| `Core-02-Stack-Queue` | [2164](../study/Core-02-Stack-Queue/2164/README.md) | `카드2` | `큐에서 앞 원소 제거 후 다음 원소를 뒤로 보내는 카드 시뮬레이션` | `study/Core-02-Stack-Queue/2164/python/src` | `make -C study/Core-02-Stack-Queue/2164/problem test` | `verified` |
| `Core-02-Stack-Queue` | [5430](../study/Core-02-Stack-Queue/5430/README.md) | `AC` | `함수 문자열을 reverse flag + deque 양끝 제거로 lazy evaluation` | `study/Core-02-Stack-Queue/5430/python/src`, `study/Core-02-Stack-Queue/5430/cpp/src` | `make -C study/Core-02-Stack-Queue/5430/problem test` | `verified` |

## Core-03-BFS-DFS

| 트랙 | 프로젝트 | 문제가 뭐였나 | 이 레포의 답 | 구현 경로 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Core-03-BFS-DFS` | [1260](../study/Core-03-BFS-DFS/1260/README.md) | `DFS와 BFS` | `동일 그래프에서 DFS와 BFS를 각각 수행해 방문 순서를 출력` | `study/Core-03-BFS-DFS/1260/python/src` | `make -C study/Core-03-BFS-DFS/1260/problem test` | `verified` |
| `Core-03-BFS-DFS` | [24479](../study/Core-03-BFS-DFS/24479/README.md) | `알고리즘 수업 - 깊이 우선 탐색 1` | `정점 번호 오름차순 인접 리스트를 이용한 DFS 방문 순서 기록` | `study/Core-03-BFS-DFS/24479/python/src` | `make -C study/Core-03-BFS-DFS/24479/problem test` | `verified` |
| `Core-03-BFS-DFS` | [7576](../study/Core-03-BFS-DFS/7576/README.md) | `토마토` | `다중 시작점(multi-source) BFS로 토마토 익는 날짜를 레벨 단위 전파` | `study/Core-03-BFS-DFS/7576/python/src`, `study/Core-03-BFS-DFS/7576/cpp/src` | `make -C study/Core-03-BFS-DFS/7576/problem test` | `verified` |

## Core-04-Recursion-Backtracking

| 트랙 | 프로젝트 | 문제가 뭐였나 | 이 레포의 답 | 구현 경로 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Core-04-Recursion-Backtracking` | [10872](../study/Core-04-Recursion-Backtracking/10872/README.md) | `팩토리얼` | `재귀 또는 반복으로 N!을 누적 계산하는 기본 recursion` | `study/Core-04-Recursion-Backtracking/10872/python/src` | `make -C study/Core-04-Recursion-Backtracking/10872/problem test` | `verified` |
| `Core-04-Recursion-Backtracking` | [15649](../study/Core-04-Recursion-Backtracking/15649/README.md) | `N과 M (1)` | `방문 배열과 경로 배열을 사용하는 백트래킹(permutation generation)` | `study/Core-04-Recursion-Backtracking/15649/python/src` | `make -C study/Core-04-Recursion-Backtracking/15649/problem test` | `verified` |
| `Core-04-Recursion-Backtracking` | [9663](../study/Core-04-Recursion-Backtracking/9663/README.md) | `N-Queen` | `열/대각선 점유 배열을 이용한 N-Queen backtracking` | `study/Core-04-Recursion-Backtracking/9663/python/src`, `study/Core-04-Recursion-Backtracking/9663/cpp/src` | `make -C study/Core-04-Recursion-Backtracking/9663/problem test` | `verified` |

## Core-05-Simulation

| 트랙 | 프로젝트 | 문제가 뭐였나 | 이 레포의 답 | 구현 경로 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Core-05-Simulation` | [2920](../study/Core-05-Simulation/2920/README.md) | `음계` | `인접 음계 차이를 검사해 ascending/descending/mixed 판정` | `study/Core-05-Simulation/2920/python/src` | `make -C study/Core-05-Simulation/2920/problem test` | `verified` |
| `Core-05-Simulation` | [14503](../study/Core-05-Simulation/14503/README.md) | `로봇 청소기` | `현재 방향 기준으로 좌회전 탐색을 반복하는 로봇 청소 시뮬레이션` | `study/Core-05-Simulation/14503/python/src`, `study/Core-05-Simulation/14503/cpp/src` | `make -C study/Core-05-Simulation/14503/problem test` | `verified` |
| `Core-05-Simulation` | [14891](../study/Core-05-Simulation/14891/README.md) | `톱니바퀴` | `기어 맞물림 방향 전파를 먼저 계산한 뒤 동시 회전 적용` | `study/Core-05-Simulation/14891/python/src` | `make -C study/Core-05-Simulation/14891/problem test` | `verified` |

## Core-06-Sorting

| 트랙 | 프로젝트 | 문제가 뭐였나 | 이 레포의 답 | 구현 경로 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Core-06-Sorting` | [2750](../study/Core-06-Sorting/2750/README.md) | `수 정렬하기` | `입력 수열을 정렬해 오름차순으로 출력하는 기본 sorting` | `study/Core-06-Sorting/2750/python/src` | `make -C study/Core-06-Sorting/2750/problem test` | `verified` |
| `Core-06-Sorting` | [1181](../study/Core-06-Sorting/1181/README.md) | `단어 정렬` | `중복 제거 후 (길이, 사전순) 복합 키로 정렬` | `study/Core-06-Sorting/1181/python/src` | `make -C study/Core-06-Sorting/1181/problem test` | `verified` |
| `Core-06-Sorting` | [2170](../study/Core-06-Sorting/2170/README.md) | `선 긋기` | `구간을 시작점 기준 정렬 후 병합해 총 길이 계산` | `study/Core-06-Sorting/2170/python/src`, `study/Core-06-Sorting/2170/cpp/src` | `make -C study/Core-06-Sorting/2170/problem test` | `verified` |

## Core-07-Binary-Search-Hash

| 트랙 | 프로젝트 | 문제가 뭐였나 | 이 레포의 답 | 구현 경로 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Core-07-Binary-Search-Hash` | [1920](../study/Core-07-Binary-Search-Hash/1920/README.md) | `수 찾기` | `정렬된 배열에서 각 질의를 이분 탐색(binary search)으로 판정` | `study/Core-07-Binary-Search-Hash/1920/python/src` | `make -C study/Core-07-Binary-Search-Hash/1920/problem test` | `verified` |
| `Core-07-Binary-Search-Hash` | [10816](../study/Core-07-Binary-Search-Hash/10816/README.md) | `숫자 카드 2` | `빈도 해시맵(counter)으로 카드 개수를 누적하고 질의별 출력` | `study/Core-07-Binary-Search-Hash/10816/python/src` | `make -C study/Core-07-Binary-Search-Hash/10816/problem test` | `verified` |
| `Core-07-Binary-Search-Hash` | [2110](../study/Core-07-Binary-Search-Hash/2110/README.md) | `공유기 설치` | `거리 D에 대한 가능성 판정을 이분 탐색하는 parametric search` | `study/Core-07-Binary-Search-Hash/2110/python/src`, `study/Core-07-Binary-Search-Hash/2110/cpp/src` | `make -C study/Core-07-Binary-Search-Hash/2110/problem test` | `verified` |

## Core-08-DP

| 트랙 | 프로젝트 | 문제가 뭐였나 | 이 레포의 답 | 구현 경로 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Core-08-DP` | [2748](../study/Core-08-DP/2748/README.md) | `피보나치 수 2` | `반복 DP로 피보나치 수를 하향식 없이 누적 계산` | `study/Core-08-DP/2748/python/src` | `make -C study/Core-08-DP/2748/problem test` | `verified` |
| `Core-08-DP` | [1149](../study/Core-08-DP/1149/README.md) | `RGB거리` | `집 i를 색 c로 칠할 때 최소 비용을 이전 색 전이로 누적하는 DP` | `study/Core-08-DP/1149/python/src` | `make -C study/Core-08-DP/1149/problem test` | `verified` |
| `Core-08-DP` | [12865](../study/Core-08-DP/12865/README.md) | `평범한 배낭` | `무게 한도 K에서 최대 가치를 누적하는 0/1 knapsack DP` | `study/Core-08-DP/12865/python/src`, `study/Core-08-DP/12865/cpp/src` | `make -C study/Core-08-DP/12865/problem test` | `verified` |

## Core-09-Greedy

| 트랙 | 프로젝트 | 문제가 뭐였나 | 이 레포의 답 | 구현 경로 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Core-09-Greedy` | [11047](../study/Core-09-Greedy/11047/README.md) | `동전 0` | `큰 동전부터 가능한 만큼 선택하는 greedy coin change` | `study/Core-09-Greedy/11047/python/src` | `make -C study/Core-09-Greedy/11047/problem test` | `verified` |
| `Core-09-Greedy` | [1931](../study/Core-09-Greedy/1931/README.md) | `회의실 배정` | `종료 시간 우선 정렬 후 가능한 회의를 순차 선택하는 activity selection` | `study/Core-09-Greedy/1931/python/src` | `make -C study/Core-09-Greedy/1931/problem test` | `verified` |
| `Core-09-Greedy` | [1744](../study/Core-09-Greedy/1744/README.md) | `수 묶기` | `양수/음수/1/0을 분리해 곱셈 이득이 큰 쌍을 우선 결합` | `study/Core-09-Greedy/1744/python/src`, `study/Core-09-Greedy/1744/cpp/src` | `make -C study/Core-09-Greedy/1744/problem test` | `verified` |

## Core-0A-Priority-Queue

| 트랙 | 프로젝트 | 문제가 뭐였나 | 이 레포의 답 | 구현 경로 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Core-0A-Priority-Queue` | [11279](../study/Core-0A-Priority-Queue/11279/README.md) | `최대 힙` | `최대 힙(max-heap)에 삽입/삭제 연산을 매 명령마다 처리` | `study/Core-0A-Priority-Queue/11279/python/src` | `make -C study/Core-0A-Priority-Queue/11279/problem test` | `verified` |
| `Core-0A-Priority-Queue` | [1927](../study/Core-0A-Priority-Queue/1927/README.md) | `최소 힙` | `최소 힙(min-heap)으로 0 명령 시 최솟값을 추출` | `study/Core-0A-Priority-Queue/1927/python/src` | `make -C study/Core-0A-Priority-Queue/1927/problem test` | `verified` |
| `Core-0A-Priority-Queue` | [1715](../study/Core-0A-Priority-Queue/1715/README.md) | `카드 정렬하기` | `가장 작은 두 묶음을 반복 병합하는 Huffman-style greedy` | `study/Core-0A-Priority-Queue/1715/python/src`, `study/Core-0A-Priority-Queue/1715/cpp/src` | `make -C study/Core-0A-Priority-Queue/1715/problem test` | `verified` |

## Core-0B-Graph-Tree

| 트랙 | 프로젝트 | 문제가 뭐였나 | 이 레포의 답 | 구현 경로 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Core-0B-Graph-Tree` | [11725](../study/Core-0B-Graph-Tree/11725/README.md) | `트리의 부모 찾기` | `루트 1에서 BFS/DFS로 각 노드의 부모를 기록` | `study/Core-0B-Graph-Tree/11725/python/src` | `make -C study/Core-0B-Graph-Tree/11725/problem test` | `verified` |
| `Core-0B-Graph-Tree` | [1991](../study/Core-0B-Graph-Tree/1991/README.md) | `트리 순회` | `이진 트리 노드 맵을 구성하고 preorder/inorder/postorder 재귀 순회` | `study/Core-0B-Graph-Tree/1991/python/src` | `make -C study/Core-0B-Graph-Tree/1991/problem test` | `verified` |
| `Core-0B-Graph-Tree` | [1167](../study/Core-0B-Graph-Tree/1167/README.md) | `트리의 지름` | `임의 정점에서 최원점 탐색 후 한 번 더 탐색하는 트리 지름(two-pass)` | `study/Core-0B-Graph-Tree/1167/python/src`, `study/Core-0B-Graph-Tree/1167/cpp/src` | `make -C study/Core-0B-Graph-Tree/1167/problem test` | `verified` |

## Core-0C-Shortest-Path

| 트랙 | 프로젝트 | 문제가 뭐였나 | 이 레포의 답 | 구현 경로 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Core-0C-Shortest-Path` | [1916](../study/Core-0C-Shortest-Path/1916/README.md) | `최소비용 구하기` | `우선순위 큐 기반 Dijkstra로 시작-도착 최소 비용 계산` | `study/Core-0C-Shortest-Path/1916/python/src` | `make -C study/Core-0C-Shortest-Path/1916/problem test` | `verified` |
| `Core-0C-Shortest-Path` | [1753](../study/Core-0C-Shortest-Path/1753/README.md) | `최단경로` | `단일 시작점에서 모든 정점까지 Dijkstra 최단거리 계산` | `study/Core-0C-Shortest-Path/1753/python/src`, `study/Core-0C-Shortest-Path/1753/cpp/src` | `make -C study/Core-0C-Shortest-Path/1753/problem test` | `verified` |
| `Core-0C-Shortest-Path` | [11657](../study/Core-0C-Shortest-Path/11657/README.md) | `타임머신` | `N-1회 완화 + 추가 1회 검사로 음수 사이클을 판정하는 Bellman-Ford` | `study/Core-0C-Shortest-Path/11657/python/src`, `study/Core-0C-Shortest-Path/11657/cpp/src` | `make -C study/Core-0C-Shortest-Path/11657/problem test` | `verified` |

## Core-Bridges

| 트랙 | 프로젝트 | 문제가 뭐였나 | 이 레포의 답 | 구현 경로 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Core-Bridges` | [1717](../study/Core-Bridges/1717/README.md) | `집합의 표현` | `다음 트랙에서 필요한 선행 개념을 별도 실습으로 고정하는 연습` | `study/Core-Bridges/1717/python/src` | `make -C study/Core-Bridges/1717/problem test` | `verified` |

## Core-0D-MST-Topo

| 트랙 | 프로젝트 | 문제가 뭐였나 | 이 레포의 답 | 구현 경로 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Core-0D-MST-Topo` | [9372](../study/Core-0D-MST-Topo/9372/README.md) | `상근이의 여행` | `연결 그래프에서 최소 비행기 수는 항상 N-1임을 이용한 단순 출력` | `study/Core-0D-MST-Topo/9372/python/src` | `make -C study/Core-0D-MST-Topo/9372/problem test` | `verified` |
| `Core-0D-MST-Topo` | [2252](../study/Core-0D-MST-Topo/2252/README.md) | `줄 세우기` | `진입차수(indegree) 기반 Kahn 알고리즘으로 위상정렬 수행` | `study/Core-0D-MST-Topo/2252/python/src`, `study/Core-0D-MST-Topo/2252/cpp/src` | `make -C study/Core-0D-MST-Topo/2252/problem test` | `verified` |
| `Core-0D-MST-Topo` | [1197](../study/Core-0D-MST-Topo/1197/README.md) | `최소 스패닝 트리` | `간선 가중치 정렬 + 유니온파인드로 MST를 구성하는 Kruskal` | `study/Core-0D-MST-Topo/1197/python/src`, `study/Core-0D-MST-Topo/1197/cpp/src` | `make -C study/Core-0D-MST-Topo/1197/problem test` | `verified` |

## Advanced-CLRS

| 트랙 | 프로젝트 | 문제가 뭐였나 | 이 레포의 답 | 구현 경로 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Advanced-CLRS` | [0x10-strassen-matrix](../study/Advanced-CLRS/0x10-strassen-matrix/README.md) | `Strassen 행렬 곱셈` | `python/src/solution.py`에서 `Strassen 행렬 곱셈` 핵심 절차를 실행 가능한 실험으로 재현 | `study/Advanced-CLRS/0x10-strassen-matrix/python/src` | `make -C study/Advanced-CLRS/0x10-strassen-matrix/problem test` | `verified` |
| `Advanced-CLRS` | [0x11-amortized-analysis-lab](../study/Advanced-CLRS/0x11-amortized-analysis-lab/README.md) | `상각 분석 실습` | `python/src/solution.py`에서 `상각 분석 실습` 핵심 절차를 실행 가능한 실험으로 재현 | `study/Advanced-CLRS/0x11-amortized-analysis-lab/python/src` | `make -C study/Advanced-CLRS/0x11-amortized-analysis-lab/problem test` | `verified` |
| `Advanced-CLRS` | [0x12-red-black-tree](../study/Advanced-CLRS/0x12-red-black-tree/README.md) | `레드-블랙 트리 삽입과 검증` | `python/src/solution.py`에서 `레드-블랙 트리 삽입과 검증` 핵심 절차를 실행 가능한 실험으로 재현 | `study/Advanced-CLRS/0x12-red-black-tree/python/src` | `make -C study/Advanced-CLRS/0x12-red-black-tree/problem test` | `verified` |
| `Advanced-CLRS` | [0x13-meldable-heap](../study/Advanced-CLRS/0x13-meldable-heap/README.md) | `합칠 수 있는 힙 브리지` | `python/src/solution.py`에서 `합칠 수 있는 힙 브리지` 핵심 절차를 실행 가능한 실험으로 재현 | `study/Advanced-CLRS/0x13-meldable-heap/python/src` | `make -C study/Advanced-CLRS/0x13-meldable-heap/problem test` | `verified` |
| `Advanced-CLRS` | [0x14-network-flow](../study/Advanced-CLRS/0x14-network-flow/README.md) | `네트워크 플로우` | `python/src/solution.py`에서 `네트워크 플로우` 핵심 절차를 실행 가능한 실험으로 재현 | `study/Advanced-CLRS/0x14-network-flow/python/src` | `make -C study/Advanced-CLRS/0x14-network-flow/problem test` | `verified` |
| `Advanced-CLRS` | [0x15-string-matching](../study/Advanced-CLRS/0x15-string-matching/README.md) | `고급 문자열 매칭` | `python/src/solution.py`에서 `고급 문자열 매칭` 핵심 절차를 실행 가능한 실험으로 재현 | `study/Advanced-CLRS/0x15-string-matching/python/src` | `make -C study/Advanced-CLRS/0x15-string-matching/problem test` | `verified` |
| `Advanced-CLRS` | [0x16-computational-geometry](../study/Advanced-CLRS/0x16-computational-geometry/README.md) | `계산 기하 실습` | `python/src/solution.py`에서 `계산 기하 실습` 핵심 절차를 실행 가능한 실험으로 재현 | `study/Advanced-CLRS/0x16-computational-geometry/python/src` | `make -C study/Advanced-CLRS/0x16-computational-geometry/problem test` | `verified` |
| `Advanced-CLRS` | [0x17-number-theory-lab](../study/Advanced-CLRS/0x17-number-theory-lab/README.md) | `정수론 실습` | `python/src/solution.py`에서 `정수론 실습` 핵심 절차를 실행 가능한 실험으로 재현 | `study/Advanced-CLRS/0x17-number-theory-lab/python/src` | `make -C study/Advanced-CLRS/0x17-number-theory-lab/problem test` | `verified` |
| `Advanced-CLRS` | [0x18-np-completeness-lab](../study/Advanced-CLRS/0x18-np-completeness-lab/README.md) | `NP-완전성 실습` | `python/src/solution.py`에서 `NP-완전성 실습` 핵심 절차를 실행 가능한 실험으로 재현 | `study/Advanced-CLRS/0x18-np-completeness-lab/python/src` | `make -C study/Advanced-CLRS/0x18-np-completeness-lab/problem test` | `verified` |
| `Advanced-CLRS` | [0x19-approximation-lab](../study/Advanced-CLRS/0x19-approximation-lab/README.md) | `근사 알고리즘 실습` | `python/src/solution.py`에서 `근사 알고리즘 실습` 핵심 절차를 실행 가능한 실험으로 재현 | `study/Advanced-CLRS/0x19-approximation-lab/python/src` | `make -C study/Advanced-CLRS/0x19-approximation-lab/problem test` | `verified` |
