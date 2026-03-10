# 지식 인덱스

> 프로젝트: 평범한 배낭
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 알고리즘

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| 0/1 배낭 | Ch 15 | $\textrm{dp}[i][j] = \max(\textrm{dp}[i-1][j], \textrm{dp}[i-1][j-w]+v)$ |
| 1D 최적화 | — | 역순 순회로 2D → 1D |
| 완전 배낭 | — | 순방향 순회 (각 아이템 무한 사용) |

## 시간 복잡도

- $O(NK)$ 시간, $O(K)$ 공간

## 연결 문제

- **BOJ 2748** (Core-08): 피보나치 — 기초 DP
- **BOJ 1149** (Core-08): RGB 거리 — 상태 DP
- **BOJ 2629**: 양팔 저울 — 배낭 변형
- **BOJ 9251**: LCS — 2D DP 최적화

## 다시 연결해 볼 질문

- `평범한 배낭`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `상태와 전이를 명시적으로 정의하고 표나 배열 의미를 끝까지 유지하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `평범한 배낭`를 다시 설명할 때는 문제 이름보다 `상태와 전이를 명시적으로 정의하고 표나 배열 의미를 끝까지 유지하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 앞 프로젝트: [`../../1149/README.md`](../../1149/README.md) (RGB거리)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`knapsack-concept.md`](../docs/concepts/knapsack-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
