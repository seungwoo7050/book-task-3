# 지식 인덱스

> 프로젝트: 수 묶기
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 알고리즘

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| 그리디 | Ch 16 | 케이스 분류 후 각 그룹 최적 매칭 |
| 정렬 기반 그리디 | Ch 16.1 | 정렬 후 양 끝부터 2개씩 묶기 |

## 시간 복잡도

- $O(N \log N)$ (정렬 지배)

## 연결 문제

- **BOJ 11047** (Core-09): 동전 0 — 단순 그리디
- **BOJ 1931** (Core-09): 회의실 배정 — 정렬 기반 그리디
- **BOJ 2212**: 센서 — 정렬 + 그리디

## 다시 연결해 볼 질문

- `수 묶기`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `탐욕 선택의 기준을 말로 설명하고 반례 가능성을 점검하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `수 묶기`를 다시 설명할 때는 문제 이름보다 `탐욕 선택의 기준을 말로 설명하고 반례 가능성을 점검하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 앞 프로젝트: [`../../1931/README.md`](../../1931/README.md) (회의실 배정)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`bundling-greedy-concept.md`](../docs/concepts/bundling-greedy-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
