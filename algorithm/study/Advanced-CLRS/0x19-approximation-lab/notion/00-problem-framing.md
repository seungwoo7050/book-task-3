# 문제 프레이밍

> 프로젝트: 근사 알고리즘 실습
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

CLRS Ch 35 근사 알고리즘. NP-hard 문제에 대한 현실적 해법. Greedy Set Cover + 2-Approximation Vertex Cover.

## 프로젝트 구조

`SET_COVER` 모드: 탐욕 집합 덮개. `VERTEX_COVER` 모드: 2-근사 꼭짓점 덮개.

## 왜 이 프로젝트인가

최적해를 보장할 수 없지만, 근사 비율이 증명된 알고리즘. 실무에서 NP-hard 문제를 만났을 때의 첫 번째 선택지.

## 지금 이 프로젝트에서 먼저 고정할 것

- `근사 알고리즘 실습`에서 실제로 확인하려는 학습 목표는 `근사 알고리즘 실습의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- CLRS Ch 35의 핵심 아이디어를 입출력과 자동 검증이 가능한 작은 실험으로 바꾸는 과정이 중요했다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`approximation-concept.md`](../docs/concepts/approximation-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 앞 프로젝트: [`../../0x18-np-completeness-lab/README.md`](../../0x18-np-completeness-lab/README.md) (NP-완전성 실습)
