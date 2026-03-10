# 문제 프레이밍

> 프로젝트: 회의실 배정
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

CLRS Ch 16.1의 **활동 선택 문제**(Activity Selection Problem) 그 자체. $N$개의 회의 중 겹치지 않는 최대 개수를 고르는 전형적인 그리디. "종료 시간 기준 정렬" 전략의 정당성을 배우기 최적의 문제.

## 문제 구조

- $N$개의 회의, 각각 시작 시간과 종료 시간
- 한 회의가 끝나는 시각에 다른 회의가 시작 가능 (경계 포함)
- 최대 비겹치는 회의 수 출력

## 왜 이 문제를 선택했는가

그리디 정당성 증명의 교과서적 예제. "왜 종료 시간이 빠른 것부터?"에 대해 교환 논증(exchange argument)으로 증명할 수 있다.

## 난이도 평가

Silver. 정렬 한 번 + 선형 스캔.

## 지금 이 프로젝트에서 먼저 고정할 것

- `회의실 배정`에서 실제로 확인하려는 학습 목표는 `탐욕 선택의 기준을 말로 설명하고 반례 가능성을 점검하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`activity-selection-concept.md`](../docs/concepts/activity-selection-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 앞 프로젝트: [`../../11047/README.md`](../../11047/README.md) (동전 0)
