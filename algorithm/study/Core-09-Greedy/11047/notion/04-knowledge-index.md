# 지식 인덱스

> 프로젝트: 동전 0
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 알고리즘

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| 그리디 알고리즘 | Ch 16 | 매 단계 최선의 선택 → 전체 최적 |
| 그리디 선택 속성 | Ch 16.2 | 지역 최적 선택이 전역 최적에 포함 |

## 시간 복잡도

- $O(N)$

## 연결 문제

- **BOJ 1931** (Core-09): 회의실 배정 — 그리디, 종료 시간 정렬
- **BOJ 1744** (Core-09): 수 묶기 — 분류 후 그리디
- **BOJ 2293**: 동전 1 — 배수 조건 없는 동전 → DP

## 다시 연결해 볼 질문

- `동전 0`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `탐욕 선택의 기준을 말로 설명하고 반례 가능성을 점검하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `동전 0`를 다시 설명할 때는 문제 이름보다 `탐욕 선택의 기준을 말로 설명하고 반례 가능성을 점검하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 다음 프로젝트: [`../../1931/README.md`](../../1931/README.md) (회의실 배정)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`greedy-coin-concept.md`](../docs/concepts/greedy-coin-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
