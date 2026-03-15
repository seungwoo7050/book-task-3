# algorithm 핵심 문제지

여기서 `essential`은 서버 공통 필수라는 뜻이 아니라, 알고리즘 학습에서 가장 먼저 읽어야 하는 핵심 트랙이라는 뜻입니다. 이 저장소는 개별 문제 53개를 다시 leaf 문제지로 만들지 않고, 트랙 인덱스를 기준으로 읽는 편이 더 자연스럽습니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [core-00-basics-python](core-00-basics-python.md) | 시작 위치의 구현을 완성해 주제: 가장 긴 증가하는 부분 수열, 학습 초점: 작은 입력을 안정적으로 읽고, 조건 분기를 코드와 문서로 함께 정리하는 감각, canonical fixture는 data/input*.txt, data/output*.txt에 둔다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/algorithm/study/Core-00-Basics/11053/problem test` |
| [core-01-array-list-python](core-01-array-list-python.md) | 시작 위치의 구현을 완성해 주제: 개수 세기, 학습 초점: 순차 자료구조를 선택하고 편집 연산의 비용 모델을 설명하는 연습, canonical fixture는 data/input*.txt, data/output*.txt에 둔다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/algorithm/study/Core-01-Array-List/10807/problem test` |
| [core-02-stack-queue-python](core-02-stack-queue-python.md) | 시작 위치의 구현을 완성해 주제: 스택, 학습 초점: 명령 기반 자료구조 문제를 상태 전이 규칙으로 정리하는 연습, canonical fixture는 data/input*.txt, data/output*.txt에 둔다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/algorithm/study/Core-02-Stack-Queue/10828/problem test` |
| [core-03-bfs-dfs-python](core-03-bfs-dfs-python.md) | 시작 위치의 구현을 완성해 주제: 알고리즘 수업 - 깊이 우선 탐색 1, 학습 초점: 그래프 표현을 고르고 방문 순서를 안정적으로 제어하는 연습, canonical fixture는 data/input*.txt, data/output*.txt에 둔다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/algorithm/study/Core-03-BFS-DFS/24479/problem test` |
| [core-04-recursion-backtracking-python](core-04-recursion-backtracking-python.md) | 시작 위치의 구현을 완성해 주제: 팩토리얼, 학습 초점: 호출 구조를 추적하고 상태 복원 규칙을 설명하는 연습, canonical fixture는 data/input*.txt, data/output*.txt에 둔다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/algorithm/study/Core-04-Recursion-Backtracking/10872/problem test` |
| [core-05-simulation-python](core-05-simulation-python.md) | 시작 위치의 구현을 완성해 주제: 로봇 청소기, 학습 초점: 복잡한 설명을 작은 상태 전이 규칙으로 나누어 구현하는 연습, canonical fixture는 data/input*.txt, data/output*.txt에 둔다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/algorithm/study/Core-05-Simulation/14503/problem test` |
| [core-06-sorting-python](core-06-sorting-python.md) | 시작 위치의 구현을 완성해 주제: 수 정렬하기, 학습 초점: 정렬 기준을 설계하고, 정렬 이후의 후처리 로직을 분리해 설명하는 연습, canonical fixture는 data/input*.txt, data/output*.txt에 둔다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/algorithm/study/Core-06-Sorting/2750/problem test` |
| [core-07-binary-search-hash-python](core-07-binary-search-hash-python.md) | 시작 위치의 구현을 완성해 주제: 수 찾기, 학습 초점: 탐색 대상을 재정의하고 자료구조 또는 매개변수 탐색으로 문제를 다시 보는 연습, canonical fixture는 data/input*.txt, data/output*.txt에 둔다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/algorithm/study/Core-07-Binary-Search-Hash/1920/problem test` |
| [core-08-dp-python](core-08-dp-python.md) | 시작 위치의 구현을 완성해 주제: RGB거리, 학습 초점: 상태와 전이를 명시적으로 정의하고 표나 배열 의미를 끝까지 유지하는 연습, canonical fixture는 data/input*.txt, data/output*.txt에 둔다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/algorithm/study/Core-08-DP/1149/problem test` |
| [core-09-greedy-python](core-09-greedy-python.md) | 시작 위치의 구현을 완성해 주제: 수 묶기, 학습 초점: 탐욕 선택의 기준을 말로 설명하고 반례 가능성을 점검하는 연습, canonical fixture는 data/input*.txt, data/output*.txt에 둔다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/algorithm/study/Core-09-Greedy/1744/problem test` |
| [core-0a-priority-queue-python](core-0a-priority-queue-python.md) | 시작 위치의 구현을 완성해 주제: 최소 힙, 학습 초점: 우선순위 큐가 필요한 상황을 식별하고 비교 기준을 일관되게 유지하는 연습, canonical fixture는 data/input*.txt, data/output*.txt에 둔다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/algorithm/study/Core-0A-Priority-Queue/1927/problem test` |
| [core-0b-graph-tree-python](core-0b-graph-tree-python.md) | 시작 위치의 구현을 완성해 주제: 트리의 부모 찾기, 학습 초점: 트리 구조의 성질을 이용해 탐색과 누적 계산을 재구성하는 연습, canonical fixture는 data/input*.txt, data/output*.txt에 둔다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/algorithm/study/Core-0B-Graph-Tree/11725/problem test` |
| [core-0c-shortest-path-python](core-0c-shortest-path-python.md) | 시작 위치의 구현을 완성해 주제: 타임머신, 학습 초점: 가중치 조건과 그래프 특성에 맞는 최단 경로 알고리즘을 선택하는 연습, canonical fixture는 data/input*.txt, data/output*.txt에 둔다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/algorithm/study/Core-0C-Shortest-Path/11657/problem test` |
| [core-0d-mst-topo-python](core-0d-mst-topo-python.md) | 시작 위치의 구현을 완성해 주제: 최소 스패닝 트리, 학습 초점: 그래프 전체 구조를 만들거나 순서를 고정하는 규칙을 설명하는 연습, canonical fixture는 data/input*.txt, data/output*.txt에 둔다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/algorithm/study/Core-0D-MST-Topo/1197/problem test` |
| [core-bridges-python](core-bridges-python.md) | 시작 위치의 구현을 완성해 주제: 집합의 표현, 학습 초점: 다음 트랙에서 필요한 선행 개념을 별도 실습으로 고정하는 연습, canonical fixture는 data/input*.txt, data/output*.txt에 둔다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/algorithm/study/Core-Bridges/1717/problem test` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
