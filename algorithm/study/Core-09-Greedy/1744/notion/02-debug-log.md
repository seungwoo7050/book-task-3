# 디버그 로그

> 프로젝트: 수 묶기
> 아래 내용은 `notion-archive/02-debug-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 함정 1: 1을 양수 그룹에 넣으면 안 된다

**증상**: 1과 다른 양수를 묶어서 결과가 작아짐

**예시**: [1, 5] → 묶으면 5, 안 묶으면 6

**해결**: 1은 별도 카운트, 항상 그냥 더함

## 함정 2: 음수 홀수 개 + 0 존재

**증상**: 남은 음수를 그냥 더하면 합이 줄어듦

**원인**: 0과 묶으면 곱이 0이 되어 음수보다 이득

**해결**: `zeros > 0`이면 남은 음수를 버림 (0과 묶어 상쇄)

## 함정 3: 양수 2개인데 묶으면 손해?

양수가 모두 1보다 클 때 곱이 더 크다: $a \times b > a + b$ (단, $a,b > 1$). 맞다. 하지만 $a=2, b=2$이면 $2 \times 2 = 4 = 2+2$로 같다. $a=2, b=3$이면 $6 > 5$. 문제없음.

## 확인 과정

```bash
make -C problem test
make -C problem run-cpp
```

PASS.

## 왜 이 디버그 메모가 중요한가

- `수 묶기`는 `탐욕 선택의 기준을 말로 설명하고 반례 가능성을 점검하는 연습`를 연습하는 프로젝트라서, 작은 경계 조건 하나가 전체 상태 전이를 망가뜨릴 수 있다.
- 그래서 이 문서는 "무엇이 틀렸는가"보다 "어떤 징후를 보면 같은 실수를 다시 알아차릴 수 있는가"를 남기는 데 의미가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 재현 경로가 필요할 때는 `05-development-timeline.md`의 단계 순서와 이 디버그 로그를 같이 보면, 어느 시점에 어떤 실패를 확인해야 하는지 더 선명해진다.

## 다음 수정 때 다시 볼 체크리스트

- 가장 작은 입력과 대표 경계 입력을 먼저 다시 실행했는가?
- 상태를 갱신하는 순서가 문제 규칙과 정확히 같은가?
- `make -C problem test` 결과와 문서 설명이 서로 어긋나지 않는가?

## 같이 점검할 문서

- [`bundling-greedy-concept.md`](../docs/concepts/bundling-greedy-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
