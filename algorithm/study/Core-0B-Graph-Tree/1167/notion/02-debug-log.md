# 디버그 로그

> 프로젝트: 트리의 지름
> 아래 내용은 `notion-archive/02-debug-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 함정 1: 입력 파싱

**증상**: 인덱스 오류

**원인**: 각 줄이 `노드 이웃 가중치 이웃 가중치 ... -1` 형식으로, 2씩 건너뛰어야 함

**해결**: `while data[i] != -1: ... i += 2`

## 함정 2: 재귀 깊이 (DFS 사용시)

**증상**: RecursionError

**원인**: $V \leq 100,000$에서 DFS 재귀 시 스택 오버플로

**해결**: BFS(deque) 사용. 또는 `sys.setrecursionlimit` 설정 (코드에 200000으로 설정됨)

## 함정 3: 양방향 간선

무방향 트리이므로 `adj[node].append`와 `adj[neighbor].append` 둘 다 필요... 하지만 이 문제는 입력 자체가 각 노드 기준으로 모든 인접 점을 나열하므로 한 방향만 넣으면 됨.

## 확인 과정

```bash
make -C problem test
make -C problem run-cpp
```

PASS.

## 왜 이 디버그 메모가 중요한가

- `트리의 지름`는 `트리 구조의 성질을 이용해 탐색과 누적 계산을 재구성하는 연습`를 연습하는 프로젝트라서, 작은 경계 조건 하나가 전체 상태 전이를 망가뜨릴 수 있다.
- 그래서 이 문서는 "무엇이 틀렸는가"보다 "어떤 징후를 보면 같은 실수를 다시 알아차릴 수 있는가"를 남기는 데 의미가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 재현 경로가 필요할 때는 `05-development-timeline.md`의 단계 순서와 이 디버그 로그를 같이 보면, 어느 시점에 어떤 실패를 확인해야 하는지 더 선명해진다.

## 다음 수정 때 다시 볼 체크리스트

- 가장 작은 입력과 대표 경계 입력을 먼저 다시 실행했는가?
- 상태를 갱신하는 순서가 문제 규칙과 정확히 같은가?
- `make -C problem test` 결과와 문서 설명이 서로 어긋나지 않는가?

## 같이 점검할 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`tree-diameter-concept.md`](../docs/concepts/tree-diameter-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
