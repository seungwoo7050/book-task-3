# 지식 인덱스

> 프로젝트: 최소 스패닝 트리
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 알고리즘

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| 크루스칼 | Ch 23.2 | 간선 정렬 + Union-Find |
| Union-Find | Ch 21 | 경로 압축 + 랭크 |
| 컷 속성 | Ch 23.1 | 최소 가중 교차 간선 ∈ MST |

## 시간 복잡도

- $O(E \log E)$

## 연결 문제

- **BOJ 9372** (Core-0D): 상근이의 여행 — 스패닝 트리 간선 수
- **BOJ 2252** (Core-0D): 줄 세우기 — 위상 정렬
- **BOJ 1717** (Core-Bridges): 집합의 표현 — Union-Find 전용

## 다시 연결해 볼 질문

- `최소 스패닝 트리`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `그래프 전체 구조를 만들거나 순서를 고정하는 규칙을 설명하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `최소 스패닝 트리`를 다시 설명할 때는 문제 이름보다 `그래프 전체 구조를 만들거나 순서를 고정하는 규칙을 설명하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 앞 프로젝트: [`../../2252/README.md`](../../2252/README.md) (줄 세우기)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`kruskal-concept.md`](../docs/concepts/kruskal-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
