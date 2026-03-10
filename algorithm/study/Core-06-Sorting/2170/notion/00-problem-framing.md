# 문제 프레이밍

> 프로젝트: 선 긋기
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

수직선 위에 $N$개의 선분이 주어지고, 겹치는 부분을 한 번만 세서 총 길이를 구하는 문제. "정렬 후 스위프(sweep)"라는 강력한 패턴을 처음 만나는 문제다. 정렬이 단순히 데이터를 정리하는 것이 아니라, **알고리즘의 핵심 전처리**로 기능하는 경우.

## 문제 구조

- $N$개의 선분 ($N \leq 1,000,000$), 각 선분은 (시작점, 끝점)
- 좌표 범위: $-10^9 \sim 10^9$
- 겹치는 부분은 한 번만 계산
- 총 덮인 길이 출력

## 왜 이 문제를 선택했는가

Core-06의 Gold 문제로, "정렬이 알고리즘의 전처리가 되는" 고전적 패턴을 보여준다. 구간 합치기(interval merging)는 스케줄링, 기하 알고리즘 등에서 반복 등장하는 핵심 기법이다.

## 난이도 평가

Gold 등급. $N \leq 10^6$이므로 $O(N \log N)$ 풀이가 필수. Python으로는 I/O가 빡빡하고 C++ 구현이 필요할 수 있다.

## 지금 이 프로젝트에서 먼저 고정할 것

- `선 긋기`에서 실제로 확인하려는 학습 목표는 `정렬 기준을 설계하고, 정렬 이후의 후처리 로직을 분리해 설명하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`interval-merge-concept.md`](../docs/concepts/interval-merge-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 앞 프로젝트: [`../../1181/README.md`](../../1181/README.md) (단어 정렬)
