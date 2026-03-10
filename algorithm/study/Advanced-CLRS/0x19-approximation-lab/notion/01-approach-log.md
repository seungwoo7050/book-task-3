# 접근 로그

> 프로젝트: 근사 알고리즘 실습
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## Greedy Set Cover

1. 미커버 원소 집합 유지
2. 매 단계, 가장 많은 미커버 원소를 포함하는 집합 선택 (동률 시 결정적 타이브레이킹)
3. 선택된 집합의 원소를 커버 처리
4. 전체 커버될 때까지 반복

근사 비율: $O(\ln n)$ — 최적의 $\ln n$ 배 이내.

## 2-Approximation Vertex Cover

1. 미커버 간선 중 하나 선택 $(u, v)$
2. $u$와 $v$ 모두 커버에 추가
3. $u$ 또는 $v$에 인접한 모든 간선 제거
4. 반복

근사 비율: 2 — 최적의 2배 이내.

```python
while uncovered_edges:
    u, v = pick_edge()  # deterministic tie-breaking
    cover.add(u)
    cover.add(v)
    remove edges incident to u or v
```

## 이 접근에서 꼭 기억할 선택

- `근사 알고리즘 실습`에서 중심이 된 판단은 `근사 알고리즘 실습의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- CLRS Ch 35의 핵심 아이디어를 입출력과 자동 검증이 가능한 작은 실험으로 바꾸는 과정이 중요했다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`approximation-concept.md`](../docs/concepts/approximation-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
