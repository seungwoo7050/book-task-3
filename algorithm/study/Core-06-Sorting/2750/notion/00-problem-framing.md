# 문제 프레이밍

> 프로젝트: 수 정렬하기
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

$N$개의 정수를 오름차순으로 정렬하는 가장 기본적인 문제. Python의 `sort()`를 호출하면 한 줄이지만, CLRS Ch 2의 삽입 정렬부터 Ch 8의 선형 시간 정렬까지의 이론적 기반을 확인하는 출발점이다.

## 문제 구조

- $1 \leq N \leq 1000$, 절대값 $\leq 1000$
- 중복 없음, 오름차순 정렬 후 한 줄씩 출력

## 왜 이 문제를 선택했는가

Core-06의 Bronze 문제로, 정렬 트랙을 시작하는 워밍업. 1181(단어 정렬)과 2170(선분 합치기)에서 정렬을 **도구**로 활용하기 전에 기본을 다진다.

## 난이도 평가

Bronze 등급. `sort()` 한 줄이면 되지만, $O(N \log N)$과 $O(N^2)$ 알고리즘의 차이를 이해하는 것이 학습 목적.

## 지금 이 프로젝트에서 먼저 고정할 것

- `수 정렬하기`에서 실제로 확인하려는 학습 목표는 `정렬 기준을 설계하고, 정렬 이후의 후처리 로직을 분리해 설명하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`sorting-concept.md`](../docs/concepts/sorting-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 다음 프로젝트: [`../../1181/README.md`](../../1181/README.md) (단어 정렬)
