# 문제 프레이밍

> 프로젝트: N과 M (1)
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

$\{1, 2, \ldots, N\}$에서 $M$개를 **중복 없이** 고르는 순열을 사전순으로 출력하는 문제. 수학적으로는 $P(N, M) = \frac{N!}{(N-M)!}$개의 결과를 생성해야 한다. 10872에서 재귀를 배웠다면, 이 문제에서는 "선택 → 재귀 → 되돌림"이라는 **백트래킹** 패턴을 처음 만난다.

## 문제 구조 파악

- $1 \leq M \leq N \leq 8$
- 중복 없는 순열을 사전순으로 출력
- 한 줄에 하나의 순열, 숫자는 공백으로 구분

$N \leq 8$이므로 최대 $P(8, 8) = 40320$개. 완전 탐색이 충분히 가능한 범위.

## 왜 이 문제를 선택했는가

백트래킹의 가장 순수한 형태를 보여주는 문제. `used` 배열로 선택 여부를 관리하고, 재귀 호출 후 **되돌리는** 패턴이 명확하다. 이 패턴이 9663(N-Queen)에서 3차원으로 확장된다.

## 난이도 평가

Silver 등급. 알고리즘은 직관적이지만, 백트래킹의 "상태 복원"을 처음 구현할 때 실수하기 쉽다.

## 지금 이 프로젝트에서 먼저 고정할 것

- `N과 M (1)`에서 실제로 확인하려는 학습 목표는 `호출 구조를 추적하고 상태 복원 규칙을 설명하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`backtracking-concept.md`](../docs/concepts/backtracking-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 앞 프로젝트: [`../../10872/README.md`](../../10872/README.md) (팩토리얼)
