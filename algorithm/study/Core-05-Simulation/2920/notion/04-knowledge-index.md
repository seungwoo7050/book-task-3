# 지식 인덱스

> 프로젝트: 음계
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 개념

| 개념 | 설명 |
|------|------|
| 시뮬레이션 | 주어진 규칙을 그대로 구현 |
| 패턴 매칭 | 고정된 패턴과의 직접 비교 |

## 시간 복잡도

- $O(N)$ — 배열 비교 ($N = 8$ 고정)

## 연결 문제

- **BOJ 14891** (Core-05): 톱니바퀴 — 회전 시뮬레이션
- **BOJ 14503** (Core-05): 로봇 청소기 — 이동 시뮬레이션

## 다시 연결해 볼 질문

- `음계`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `복잡한 설명을 작은 상태 전이 규칙으로 나누어 구현하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `음계`를 다시 설명할 때는 문제 이름보다 `복잡한 설명을 작은 상태 전이 규칙으로 나누어 구현하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 다음 프로젝트: [`../../14503/README.md`](../../14503/README.md) (로봇 청소기)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`simulation-concept.md`](../docs/concepts/simulation-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
