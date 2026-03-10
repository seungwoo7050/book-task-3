# 지식 인덱스

> 프로젝트: 카드 정렬하기
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 알고리즘

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| 허프만 코딩 | Ch 16.3 | 최소 빈도 두 노드 합치기 |
| 우선순위 큐 | Ch 6 | 최솟값 추출 $O(\log N)$ |
| heapify | Ch 6.3 | 배열 → 힙 $O(N)$ |

## 시간 복잡도

- $O(N \log N)$

## 연결 문제

- **BOJ 11279** (Core-0A): 최대 힙 — 기본 힙 연산
- **BOJ 1927** (Core-0A): 최소 힙 — 기본 힙 연산
- **BOJ 13975**: 파일 합치기 3 — 동일 문제 대규모

## 다시 연결해 볼 질문

- `카드 정렬하기`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `우선순위 큐가 필요한 상황을 식별하고 비교 기준을 일관되게 유지하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `카드 정렬하기`를 다시 설명할 때는 문제 이름보다 `우선순위 큐가 필요한 상황을 식별하고 비교 기준을 일관되게 유지하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 앞 프로젝트: [`../../1927/README.md`](../../1927/README.md) (최소 힙)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`huffman-concept.md`](../docs/concepts/huffman-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
