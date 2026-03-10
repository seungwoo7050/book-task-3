# 문제 프레이밍

> 프로젝트: 카드 정렬하기
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

$N$개의 카드 묶음을 하나로 합칠 때 최소 비교 횟수를 구하는 문제. 두 묶음을 합치면 비교 횟수 = 두 묶음 크기의 합. 이것은 **허프만 코딩**과 동일한 구조: 항상 가장 작은 두 묶음을 합치는 것이 최적.

## 문제 구조

- $N$개 묶음, 각 크기 주어짐
- 두 묶음 합치기: 비용 = 합
- 전체를 하나로 합칠 때의 최소 총 비용

## 왜 이 문제를 선택했는가

Core-0A의 Gold 문제로, 우선순위 큐의 실전 응용. 단순 정렬로는 안 되고, 합친 결과를 다시 큐에 넣어야 하므로 힙이 필수.

## 난이도 평가

Gold. 허프만 코딩과의 연결을 아느냐가 핵심.

## 지금 이 프로젝트에서 먼저 고정할 것

- `카드 정렬하기`에서 실제로 확인하려는 학습 목표는 `우선순위 큐가 필요한 상황을 식별하고 비교 기준을 일관되게 유지하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`huffman-concept.md`](../docs/concepts/huffman-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 앞 프로젝트: [`../../1927/README.md`](../../1927/README.md) (최소 힙)
