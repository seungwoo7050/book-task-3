# 접근 로그

> 프로젝트: 카드2
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 전략

`deque(range(1, n+1))`로 카드 더미를 초기화하고, 두 단계를 반복:
1. `q.popleft()` — 맨 위 카드 버리기
2. `q.append(q.popleft())` — 그다음 카드를 맨 아래로 보내기

카드가 하나 남으면 `q[0]`이 답이다.

## 왜 deque인가

리스트의 `pop(0)`은 나머지 원소를 한 칸씩 앞으로 옮기므로 O(n).
반복이 약 $N$번이므로 총 O(n²) → $N=500\,000$이면 $2.5 \times 10^{11}$ 연산.
`deque.popleft()`는 O(1)이므로 총 O(n)으로 끝난다.

## 복잡도

| 항목 | 값 |
|------|-----|
| 시간 | O(N) |
| 공간 | O(N) |

## 이 접근에서 꼭 기억할 선택

- `카드2`에서 중심이 된 판단은 `명령 기반 자료구조 문제를 상태 전이 규칙으로 정리하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`queue-concept.md`](../docs/concepts/queue-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
