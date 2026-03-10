# 문제 프레이밍

> 프로젝트: 카드2
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 문제를 처음 읽었을 때

BOJ 2164는 카드 더미에서 "맨 위 카드 버리기 → 그다음 카드 맨 아래로 보내기"를 반복하여 마지막 카드를 찾는 문제다.
1부터 $N$까지의 카드가 순서대로 쌓여 있고, 위 과정을 카드 하나 남을 때까지 반복한다.

처음 읽으면 "그냥 시뮬레이션이네" 싶다.
맞다. 하지만 이 시뮬레이션이 **큐(Queue)**의 동작 그 자체라는 걸 알아채는 게 핵심이다.

## 문제의 핵심 구조

- **입력**: 정수 $N$ ($1 \le N \le 500\,000$)
- **출력**: 마지막으로 남는 카드 번호
- **핵심**: 앞에서 빼고(`popleft`) 뒤에 넣는(`append`) 연산 = 큐

## 왜 이 문제를 골랐는가

큐의 `popleft`/`append` 패턴을 체화하기 위한 문제다.
Python에서 `collections.deque`를 처음 사용하게 되는 계기이기도 하다.
일반 리스트의 `pop(0)`은 O(n)이므로, $N=500\,000$에서 시간 초과가 날 수 있다.

## 지금 이 프로젝트에서 먼저 고정할 것

- `카드2`에서 실제로 확인하려는 학습 목표는 `명령 기반 자료구조 문제를 상태 전이 규칙으로 정리하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`queue-concept.md`](../docs/concepts/queue-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 앞 프로젝트: [`../../10828/README.md`](../../10828/README.md) (스택)
