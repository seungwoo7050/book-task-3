# 지식 인덱스

> 프로젝트: 집합의 표현
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 알고리즘

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| Disjoint Set Union | Ch 21 | 합집합 + 집합 판별 |
| 경로 압축 | Ch 21.3 | find 시 트리 평탄화 |
| 유니온 바이 랭크 | Ch 21.3 | 작은 트리를 큰 트리 아래에 |

## 시간 복잡도

- $O(M \cdot \alpha(N))$ ≈ $O(M)$

## 연결 문제

- **BOJ 1197** (Core-0D): MST — Union-Find 활용
- **BOJ 4195**: 친구 네트워크 — Union-Find + 크기 관리

## 다시 연결해 볼 질문

- `집합의 표현`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `다음 트랙에서 필요한 선행 개념을 별도 실습으로 고정하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `집합의 표현`를 다시 설명할 때는 문제 이름보다 `다음 트랙에서 필요한 선행 개념을 별도 실습으로 고정하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 같은 트랙의 큰 흐름은 [`../../README.md`](../../README.md)에서 다시 확인한다.
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`disjoint-set-union.md`](../docs/concepts/disjoint-set-union.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
