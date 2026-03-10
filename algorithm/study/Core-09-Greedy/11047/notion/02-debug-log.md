# 디버그 로그

> 프로젝트: 동전 0
> 아래 내용은 `notion-archive/02-debug-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 특이사항

Bronze 난이도라 치명적 버그는 없었다. 다만 주의할 점:

## 주의점 1: reversed vs 역순 슬라이스

`reversed(coins)` vs `coins[::-1]` — 전자가 메모리 효율적이지만 이 규모에서는 무관.

## 주의점 2: K=0 조기 종료

`K`가 0이 된 후에도 루프가 계속 돌지만, `K // coin = 0`이므로 논리적 오류는 없다. 조기 종료 조건을 넣을 수도 있지만 필요 없다.

## 확인 과정

```bash
make -C problem test
```

PASS.

## 왜 이 디버그 메모가 중요한가

- `동전 0`는 `탐욕 선택의 기준을 말로 설명하고 반례 가능성을 점검하는 연습`를 연습하는 프로젝트라서, 작은 경계 조건 하나가 전체 상태 전이를 망가뜨릴 수 있다.
- 그래서 이 문서는 "무엇이 틀렸는가"보다 "어떤 징후를 보면 같은 실수를 다시 알아차릴 수 있는가"를 남기는 데 의미가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 재현 경로가 필요할 때는 `05-development-timeline.md`의 단계 순서와 이 디버그 로그를 같이 보면, 어느 시점에 어떤 실패를 확인해야 하는지 더 선명해진다.

## 다음 수정 때 다시 볼 체크리스트

- 가장 작은 입력과 대표 경계 입력을 먼저 다시 실행했는가?
- 상태를 갱신하는 순서가 문제 규칙과 정확히 같은가?
- `make -C problem test` 결과와 문서 설명이 서로 어긋나지 않는가?

## 같이 점검할 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`greedy-coin-concept.md`](../docs/concepts/greedy-coin-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
