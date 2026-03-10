# 지식 인덱스

> 프로젝트: 트리의 지름
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 알고리즘

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| 트리의 지름 | Ch 22 | 최장 경로의 두 끝점 |
| BFS | Ch 22.2 | 가중치 트리에서 거리 계산 |
| 두 번 BFS | — | 임의 점 → 최원점 → 최원점 = 지름 |

## 시간 복잡도

- $O(V)$ — BFS 2회

## 연결 문제

- **BOJ 11725** (Core-0B): 트리 부모 — BFS 기초
- **BOJ 1991** (Core-0B): 트리 순회 — 전위/중위/후위
- **BOJ 1967**: 트리의 지름 — 같은 알고리즘, 다른 입력

## 다시 연결해 볼 질문

- `트리의 지름`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `트리 구조의 성질을 이용해 탐색과 누적 계산을 재구성하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `트리의 지름`를 다시 설명할 때는 문제 이름보다 `트리 구조의 성질을 이용해 탐색과 누적 계산을 재구성하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 앞 프로젝트: [`../../1991/README.md`](../../1991/README.md) (트리 순회)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`tree-diameter-concept.md`](../docs/concepts/tree-diameter-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
