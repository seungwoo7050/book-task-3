# 문제 프레이밍

> 프로젝트: 단어 정렬
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

단어들을 "길이순, 같으면 사전순"으로 정렬하는 문제. 2750의 기본 정렬에서 **정렬 키(key)**를 커스터마이징하는 단계로 넘어간다. Python의 `sorted(key=...)`가 빛나는 문제.

## 문제 구조

- $N$개의 소문자 영단어 ($N \leq 20,000$, 길이 $\leq 50$)
- 길이가 짧은 것 먼저, 같으면 사전순
- **중복 제거** 후 출력

## 왜 이 문제를 선택했는가

다중 키 정렬과 중복 제거를 동시에 훈련. `set`으로 중복을 제거하고, `sorted(key=lambda)`로 다중 키를 지정하는 Python 관용 패턴을 확인한다.

## 난이도 평가

Silver 등급. Python에서는 `set` + `sorted` 두 줄이면 해결되지만, 정렬 안정성(stability)과 키 함수의 개념을 이해해야 한다.

## 지금 이 프로젝트에서 먼저 고정할 것

- `단어 정렬`에서 실제로 확인하려는 학습 목표는 `정렬 기준을 설계하고, 정렬 이후의 후처리 로직을 분리해 설명하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`multikey-sort-concept.md`](../docs/concepts/multikey-sort-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 앞 프로젝트: [`../../2750/README.md`](../../2750/README.md) (수 정렬하기)
