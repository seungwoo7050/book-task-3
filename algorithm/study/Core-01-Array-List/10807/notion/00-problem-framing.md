# 문제 프레이밍

> 프로젝트: 개수 세기
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 문제를 처음 읽었을 때

BOJ 10807은 정수 배열에서 특정 값이 몇 번 나오는지 세는 문제다.
이게 문제라고 할 수 있나 싶을 정도로 단순하다. Python에서는 `arr.count(v)` 한 줄이면 끝이니까.

하지만 이 문제를 Core-01-Array-List의 첫 번째로 배치한 이유가 있다.
배열이라는 자료 구조에서 "선형 탐색"이 무엇을 의미하는지, 왜 O(n)인지를 처음 체감하게 만드는 문제이기 때문이다.

## 문제의 핵심 구조

- **입력**: 정수 $N$ ($\le 100$), $N$개의 정수 ($-100 \le A_i \le 100$), 찾을 값 $v$
- **출력**: 배열에서 $v$가 나타나는 횟수
- **제약**: 너무 작아서 어떤 방법이든 통과

## 왜 이 문제를 골랐는가

Array-List 트랙의 워밍업이다.
배열을 입력받고, 순회하고, 조건에 맞는 원소를 세는 "가장 기본적인 루프 패턴"을 여기서 확인한다.
CLRS Ch 10.2(연결 리스트 기본)와 연결되지만, 실제로 이 문제는 배열만으로 충분하다.

## 지금 이 프로젝트에서 먼저 고정할 것

- `개수 세기`에서 실제로 확인하려는 학습 목표는 `순차 자료구조를 선택하고 편집 연산의 비용 모델을 설명하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`array-concept.md`](../docs/concepts/array-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 다음 프로젝트: [`../../5397/README.md`](../../5397/README.md) (키로거)
