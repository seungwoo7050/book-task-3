# 문제 프레이밍

> 프로젝트: 스택
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 문제를 처음 읽었을 때

BOJ 10828은 스택을 직접 구현하는 문제다. push, pop, size, empty, top 다섯 가지 명령을 처리해야 한다.
Python에서는 리스트가 이미 스택의 모든 기능을 갖고 있으므로, 이 문제의 진짜 가치는 "스택의 인터페이스를 명시적으로 정의해 보는 것"에 있다.

## 문제의 핵심 구조

- **입력**: 명령 수 $N$ ($\le 10\,000$), 각 줄에 명령 하나
- **출력**: pop, top, size, empty에 대한 결과를 줄 단위로 출력
- **빈 스택 처리**: pop/top에서 빈 스택이면 `-1` 출력

"빈 스택에서 -1을 출력한다"는 규칙은 문제 고유의 약속이다. 일반적인 스택은 예외를 발생시킨다.

## 왜 이 문제를 골랐는가

Core-02-Stack-Queue의 첫 문제로, 스택 인터페이스를 직접 체험하는 것이 목적이다.
Python list의 `append()`/`pop()`이 스택 연산과 정확히 대응한다는 걸 직접 확인한다.
CLRS Ch 10.1(스택과 큐)에 직접 해당한다.

## 지금 이 프로젝트에서 먼저 고정할 것

- `스택`에서 실제로 확인하려는 학습 목표는 `명령 기반 자료구조 문제를 상태 전이 규칙으로 정리하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`stack-concept.md`](../docs/concepts/stack-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 다음 프로젝트: [`../../2164/README.md`](../../2164/README.md) (카드2)
