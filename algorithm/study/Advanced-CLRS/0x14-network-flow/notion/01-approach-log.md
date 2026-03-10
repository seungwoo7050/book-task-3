# 접근 로그

> 프로젝트: 네트워크 플로우
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## Edmonds-Karp: BFS 기반 증가 경로

1. BFS로 $s \to t$ 경로 탐색 (잔여 용량 > 0인 간선만)
2. 경로 상 최소 잔여 용량 = bottleneck
3. 경로 상 모든 간선: 순방향 용량 감소, 역방향 용량 증가
4. 반복 — BFS 실패 시 종료

```python
cap[u][v] -= bn
cap[v][u] += bn
```

## 용량 행렬 vs 인접 리스트

`cap[][]`로 잔여 용량 관리, `adj[]`로 BFS 탐색. 역간선은 입력 시 양방향으로 adj에 추가.

## 최대 유량 정리

max-flow = min-cut (Ford-Fulkerson 정리).

## 이 접근에서 꼭 기억할 선택

- `네트워크 플로우`에서 중심이 된 판단은 `네트워크 플로우의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- CLRS Ch 26의 핵심 아이디어를 입출력과 자동 검증이 가능한 작은 실험으로 바꾸는 과정이 중요했다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`residual-graph-concept.md`](../docs/concepts/residual-graph-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
