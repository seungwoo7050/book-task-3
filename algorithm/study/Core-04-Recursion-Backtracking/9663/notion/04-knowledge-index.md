# 지식 인덱스

> 프로젝트: N-Queen
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 알고리즘

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| 백트래킹 | Ch 4 | 탐색 트리에서 유망하지 않은 가지 제거 |
| 가지치기 (Pruning) | — | 충돌 발생 시 해당 서브트리 전체 건너뜀 |
| N-Queen | — | 백트래킹의 대표 응용 문제 |

## 자료구조 사용

- **col 배열**: 열 사용 여부 $O(N)$
- **diag1 배열**: 좌상→우하 대각선 $O(2N)$
- **diag2 배열**: 우상→좌하 대각선 $O(2N)$

## 시간 복잡도

- 최악: $O(N!)$ — 가지치기 후 실제 탐색 노드
- $N = 15$일 때 약 2,279,184개 (정답)

## 연결 문제

- **BOJ 15649** (Core-04): 순열 생성 — 백트래킹 기초
- **BOJ 10872** (Core-04): 팩토리얼 — 재귀 기초
- **BOJ 1799**: 비숍 — 대각선만 고려하는 변형
- **BOJ 2580**: 스도쿠 — 행/열/박스 제약의 백트래킹

## 구현 비교 (Python vs C++)

| 항목 | Python | C++ |
|------|--------|-----|
| 카운터 관리 | `nonlocal count` | 전역 변수 |
| 배열 | `[False] * (2*n)` | `bool arr[30]` |
| 성능 ($N=15$) | ~10초 | <1초 |
| 다중 할당 | `a = b = c = True` | `a = b = c = true` |

## 다시 연결해 볼 질문

- `N-Queen`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `호출 구조를 추적하고 상태 복원 규칙을 설명하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `N-Queen`를 다시 설명할 때는 문제 이름보다 `호출 구조를 추적하고 상태 복원 규칙을 설명하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 앞 프로젝트: [`../../15649/README.md`](../../15649/README.md) (N과 M (1))
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`nqueen-concept.md`](../docs/concepts/nqueen-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
