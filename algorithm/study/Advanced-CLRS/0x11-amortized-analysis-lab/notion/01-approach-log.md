# 접근 로그

> 프로젝트: 상각 분석 실습
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## Stack MULTIPOP

- PUSH: 비용 1
- POP: 비용 1
- MULTIPOP(k): min(k, size)개 pop, 비용 = pop 횟수

총 비용이 $O(n)$임을 보이는 것이 핵심 (각 원소는 최대 한 번 push, 한 번 pop).

## Binary Counter

- INC: value + 1, 비용 = 변경된 비트 수 (XOR의 popcount)

총 비용이 $O(n)$임을 보이는 것이 핵심 (각 비트 위치 $i$는 $n/2^i$번 변경).

## 구현

```python
cost += (value ^ nxt).bit_count()
```

XOR로 변경된 비트 수를 직접 세는 우아한 방법.

## 이 접근에서 꼭 기억할 선택

- `상각 분석 실습`에서 중심이 된 판단은 `상각 분석 실습의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- CLRS Ch 17의 핵심 아이디어를 입출력과 자동 검증이 가능한 작은 실험으로 바꾸는 과정이 중요했다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`amortized-concept.md`](../docs/concepts/amortized-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
