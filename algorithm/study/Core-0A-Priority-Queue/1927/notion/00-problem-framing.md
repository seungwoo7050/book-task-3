# 문제 프레이밍

> 프로젝트: 최소 힙
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

11279(최대 힙)의 쌍둥이. 삽입과 최솟값 추출을 지원하는 최소 힙. Python `heapq`가 기본적으로 최소 힙이므로 부호 반전 없이 직접 사용 가능.

## 문제 구조

- $N$개의 연산
- $x > 0$: 삽입
- $x = 0$: 최솟값 추출 (비어있으면 0 출력)

## 왜 이 문제를 선택했는가

11279와 쌍으로, 최소/최대 힙 양쪽을 모두 구현해보는 훈련.

## 난이도 평가

Silver. `heapq` 그대로 사용.

## 지금 이 프로젝트에서 먼저 고정할 것

- `최소 힙`에서 실제로 확인하려는 학습 목표는 `우선순위 큐가 필요한 상황을 식별하고 비교 기준을 일관되게 유지하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`minheap-concept.md`](../docs/concepts/minheap-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 앞 프로젝트: [`../../11279/README.md`](../../11279/README.md) (최대 힙)
