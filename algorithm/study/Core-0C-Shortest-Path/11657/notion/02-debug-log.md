# 디버그 로그

> 프로젝트: 타임머신
> 아래 내용은 `notion-archive/02-debug-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 함정 1: V번째 반복 위치

**증상**: 음의 사이클을 탐지 못함

**원인**: `i == n - 1` 검사를 루프 밖에서 하면 놓침

**해결**: relaxation 내부에서 `if i == n - 1: print(-1); return`

## 함정 2: INF에서 출발하는 relaxation

**증상**: INF + 음수값이 유한한 값이 됨

**원인**: `dist[a] = INF`인데 `dist[a] + c`를 계산

**해결**: `if dist[a] != INF` 조건 추가

## 함정 3: 도달 불가 정점

최단 경로가 없는 정점은 `-1` 출력 (음의 사이클의 `-1`과 구분).

## 확인 과정

```bash
make -C problem test
make -C problem run-cpp
```

PASS.

## 왜 이 디버그 메모가 중요한가

- `타임머신`는 `가중치 조건과 그래프 특성에 맞는 최단 경로 알고리즘을 선택하는 연습`를 연습하는 프로젝트라서, 작은 경계 조건 하나가 전체 상태 전이를 망가뜨릴 수 있다.
- 그래서 이 문서는 "무엇이 틀렸는가"보다 "어떤 징후를 보면 같은 실수를 다시 알아차릴 수 있는가"를 남기는 데 의미가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 재현 경로가 필요할 때는 `05-development-timeline.md`의 단계 순서와 이 디버그 로그를 같이 보면, 어느 시점에 어떤 실패를 확인해야 하는지 더 선명해진다.

## 다음 수정 때 다시 볼 체크리스트

- 가장 작은 입력과 대표 경계 입력을 먼저 다시 실행했는가?
- 상태를 갱신하는 순서가 문제 규칙과 정확히 같은가?
- `make -C problem test` 결과와 문서 설명이 서로 어긋나지 않는가?

## 같이 점검할 문서

- [`bellman-ford-concept.md`](../docs/concepts/bellman-ford-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
