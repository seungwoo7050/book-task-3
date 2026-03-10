# 지식 인덱스

> 프로젝트: 피보나치 수 2
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 알고리즘

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| 동적 프로그래밍 | Ch 15 | 중복 부분문제 + 최적 부분구조 |
| Bottom-Up DP | Ch 15.3 | 반복문으로 테이블 채우기 |
| 공간 최적화 | — | 이전 상태만 유지하는 슬라이딩 윈도우 |

## 연결 문제

- **BOJ 10872** (Core-04): 팩토리얼 재귀 → DP로의 전환점
- **BOJ 1149** (Core-08): RGB 거리 — 3-상태 DP
- **BOJ 12865** (Core-08): 배낭 — 2차원 DP → 1차원 최적화

## 다시 연결해 볼 질문

- `피보나치 수 2`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `상태와 전이를 명시적으로 정의하고 표나 배열 의미를 끝까지 유지하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `피보나치 수 2`를 다시 설명할 때는 문제 이름보다 `상태와 전이를 명시적으로 정의하고 표나 배열 의미를 끝까지 유지하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 다음 프로젝트: [`../../1149/README.md`](../../1149/README.md) (RGB거리)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`dp-fib-concept.md`](../docs/concepts/dp-fib-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
