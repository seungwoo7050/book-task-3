# 문제 프레이밍

> 프로젝트: 숫자 카드 2
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

1920이 "존재 여부"를 묻는다면, 10816은 "몇 개 있는지"를 묻는다. `set`에서 `Counter`로의 자연스러운 확장.

## 문제 구조

- $N$개의 카드 ($N \leq 500,000$), $M$개의 쿼리
- 각 쿼리의 숫자가 몇 장 있는지 출력

## 왜 이 문제를 선택했는가

해시 맵(딕셔너리)의 활용과 `Counter` 클래스의 실전 사용을 훈련. 이진 탐색으로도 풀 수 있어 `bisect_left`/`bisect_right`의 활용법도 확인한다.

## 난이도 평가

Silver 등급. `Counter`를 알면 2줄이지만, 이진 탐색으로 구간 길이를 구하는 방식도 학습 가치가 높다.

## 지금 이 프로젝트에서 먼저 고정할 것

- `숫자 카드 2`에서 실제로 확인하려는 학습 목표는 `탐색 대상을 재정의하고 자료구조 또는 매개변수 탐색으로 문제를 다시 보는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`counter-concept.md`](../docs/concepts/counter-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 앞 프로젝트: [`../../1920/README.md`](../../1920/README.md) (수 찾기)
