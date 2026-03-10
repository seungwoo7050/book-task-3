# 지식 인덱스

> 프로젝트: N과 M (1)
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 알고리즘

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| 백트래킹 | Ch 4 | 탐색 트리에서 유망하지 않은 가지를 잘라내는 전략 |
| 순열 생성 | — | $P(N, M)$개의 결과를 DFS로 열거 |

## 자료구조 사용

- **used 배열**: 선택 여부 관리, $O(N)$ 공간
- **seq 리스트**: 현재까지의 선택 기록, 스택처럼 append/pop

## 시간 복잡도

- $O(P(N, M)) = O(\frac{N!}{(N-M)!})$ — 모든 순열 열거
- 각 리프에서 $O(M)$ 출력 → 전체 $O(M \cdot P(N, M))$

## 연결 문제

- **BOJ 10872** (Core-04): 팩토리얼 — 재귀의 기초
- **BOJ 9663** (Core-04): N-Queen — 백트래킹 + 가지치기
- **BOJ 15650**: N과 M (2) — 조합 변형
- **BOJ 15651**: N과 M (3) — 중복 순열 변형

## Python 특이사항

- 출력 최적화: `out` 리스트에 모아서 `'\n'.join`
- `used` 배열의 1-indexed 접근: `[False] * (n + 1)`

## 다시 연결해 볼 질문

- `N과 M (1)`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `호출 구조를 추적하고 상태 복원 규칙을 설명하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `N과 M (1)`를 다시 설명할 때는 문제 이름보다 `호출 구조를 추적하고 상태 복원 규칙을 설명하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 앞 프로젝트: [`../../10872/README.md`](../../10872/README.md) (팩토리얼)
- 다음 프로젝트: [`../../9663/README.md`](../../9663/README.md) (N-Queen)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`backtracking-concept.md`](../docs/concepts/backtracking-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
