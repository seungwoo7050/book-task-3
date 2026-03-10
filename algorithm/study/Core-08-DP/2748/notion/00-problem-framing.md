# 문제 프레이밍

> 프로젝트: 피보나치 수 2
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

$n$번째 피보나치 수를 구하는 문제. 재귀로 풀면 $O(2^n)$이지만, 반복문(bottom-up DP)으로 풀면 $O(n)$이다. 10872(팩토리얼)가 재귀의 시작이었다면, 이 문제는 **메모이제이션/DP**의 시작이다.

## 문제 구조

- $0 \leq n \leq 90$
- $F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2)$
- $F(90) \approx 2.88 \times 10^{18}$ — 64비트 정수 범위 (Python은 bigint이므로 무관)

## 왜 이 문제를 선택했는가

CLRS Ch 15의 DP 개념을 가장 순수하게 보여주는 문제. "중복 부분 문제"와 "최적 부분 구조"라는 DP의 두 핵심을 피보나치에서 확인한다.

## 난이도 평가

Bronze 등급. 변수 두 개로 공간 $O(1)$까지 최적화 가능.

## 지금 이 프로젝트에서 먼저 고정할 것

- `피보나치 수 2`에서 실제로 확인하려는 학습 목표는 `상태와 전이를 명시적으로 정의하고 표나 배열 의미를 끝까지 유지하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`dp-fib-concept.md`](../docs/concepts/dp-fib-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 다음 프로젝트: [`../../1149/README.md`](../../1149/README.md) (RGB거리)
