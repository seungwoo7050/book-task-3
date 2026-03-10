# 문제 프레이밍

> 프로젝트: 팩토리얼
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

팩토리얼은 재귀의 가장 기본적인 예시다. $N! = N \times (N-1)!$이라는 수학적 정의가 곧 코드가 된다. 이 문제가 Core-04의 첫 번째인 이유는, 백트래킹으로 가기 전에 "재귀 호출이 어떻게 동작하는가"를 확인하는 출발점이기 때문이다.

## 문제 구조 파악

- $0 \leq N \leq 12$
- $N!$ 계산 후 출력
- $0! = 1$이 정의

$N \leq 12$이므로 $12! = 479,001,600$으로 32비트 정수 범위 안에 있다. 오버플로우 걱정이 없다.

## 왜 이 문제를 선택했는가

재귀의 기본 구조 — 기저 조건(base case)과 재귀 단계(recursive step) — 를 가장 순수하게 보여주는 문제. 15649(순열)과 9663(N-Queen)에서 사용할 백트래킹 패턴의 뼈대가 된다.

## 난이도 평가

Bronze 등급. 구현 자체는 5줄이면 충분하지만, "재귀가 왜 동작하는가"를 이해하는 것이 핵심이다. 호출 스택의 push/pop을 머릿속으로 따라가는 연습.

## 지금 이 프로젝트에서 먼저 고정할 것

- `팩토리얼`에서 실제로 확인하려는 학습 목표는 `호출 구조를 추적하고 상태 복원 규칙을 설명하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`recursion-concept.md`](../docs/concepts/recursion-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 다음 프로젝트: [`../../15649/README.md`](../../15649/README.md) (N과 M (1))
