# 문제 프레이밍

> 프로젝트: 계산 기하 실습
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

CLRS Ch 33 계산 기하. Cross product, Convex Hull (Andrew's Monotone Chain), Segment Intersection 세 가지 핵심 연산.

## 프로젝트 구조

HULL 모드: 점 집합 → 볼록 껍질 꼭짓점. INTERSECT 모드: 두 선분의 교차 판정.

## 왜 이 프로젝트인가

기하 알고리즘은 게임, CAD, GIS, 로보틱스의 기초. 외적 기반 방향 판정이 모든 기하 알고리즘의 빌딩 블록.

## 지금 이 프로젝트에서 먼저 고정할 것

- `계산 기하 실습`에서 실제로 확인하려는 학습 목표는 `계산 기하 실습의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- CLRS Ch 33의 핵심 아이디어를 입출력과 자동 검증이 가능한 작은 실험으로 바꾸는 과정이 중요했다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`geometry-primitives.md`](../docs/concepts/geometry-primitives.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 앞 프로젝트: [`../../0x15-string-matching/README.md`](../../0x15-string-matching/README.md) (고급 문자열 매칭)
