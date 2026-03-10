# 지식 인덱스

> 프로젝트: 팩토리얼
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 알고리즘

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| 재귀 | Ch 4 | 기저 조건 + 재귀 단계 구조 |
| 분할 정복 | Ch 4 | 재귀의 일반화 — $T(n) = aT(n/b) + f(n)$ |

## 시간 복잡도

- $T(n) = T(n-1) + O(1)$ → $O(n)$
- 공간: 호출 스택 $O(n)$

## 연결 문제

- **BOJ 15649** (Core-04): N과 M — 재귀 + 백트래킹
- **BOJ 9663** (Core-04): N-Queen — 백트래킹의 정석
- **BOJ 2748** (Core-08): 피보나치 — 재귀 + 메모이제이션으로 DP 전환

## Python 특이사항

- `sys.setrecursionlimit`: 이 문제에서는 불필요 ($N \leq 12$)
- Python 정수는 자동 bigint이므로 오버플로우 없음

## 다시 연결해 볼 질문

- `팩토리얼`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `호출 구조를 추적하고 상태 복원 규칙을 설명하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `팩토리얼`를 다시 설명할 때는 문제 이름보다 `호출 구조를 추적하고 상태 복원 규칙을 설명하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 다음 프로젝트: [`../../15649/README.md`](../../15649/README.md) (N과 M (1))
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`recursion-concept.md`](../docs/concepts/recursion-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
