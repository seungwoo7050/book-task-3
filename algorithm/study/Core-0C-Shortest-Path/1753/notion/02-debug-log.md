# 디버그 로그

> 프로젝트: 최단경로
> 아래 내용은 `notion-archive/02-debug-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 함정 1: 중복 간선

같은 $(u, v)$ 쌍에 여러 간선이 있을 수 있음. 인접 리스트에 모두 넣으면 자연스럽게 처리.

## 함정 2: Lazy deletion 빼먹기

`if d > dist[u]: continue`를 빼면 이미 확정된 노드를 다시 처리 → TLE.

## 주의점: INF 값

Python에서 `float('inf')` 사용. 출력 시 문자열 `'INF'`로 변환 필요.

## 확인 과정

```bash
make -C problem test
make -C problem run-cpp
```

PASS.

## 왜 이 디버그 메모가 중요한가

- `최단경로`는 `가중치 조건과 그래프 특성에 맞는 최단 경로 알고리즘을 선택하는 연습`를 연습하는 프로젝트라서, 작은 경계 조건 하나가 전체 상태 전이를 망가뜨릴 수 있다.
- 그래서 이 문서는 "무엇이 틀렸는가"보다 "어떤 징후를 보면 같은 실수를 다시 알아차릴 수 있는가"를 남기는 데 의미가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 재현 경로가 필요할 때는 `05-development-timeline.md`의 단계 순서와 이 디버그 로그를 같이 보면, 어느 시점에 어떤 실패를 확인해야 하는지 더 선명해진다.

## 다음 수정 때 다시 볼 체크리스트

- 가장 작은 입력과 대표 경계 입력을 먼저 다시 실행했는가?
- 상태를 갱신하는 순서가 문제 규칙과 정확히 같은가?
- `make -C problem test` 결과와 문서 설명이 서로 어긋나지 않는가?

## 같이 점검할 문서

- [`dijkstra-all-concept.md`](../docs/concepts/dijkstra-all-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
