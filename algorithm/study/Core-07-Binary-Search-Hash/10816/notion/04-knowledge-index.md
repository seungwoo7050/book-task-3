# 지식 인덱스

> 프로젝트: 숫자 카드 2
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 알고리즘

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| 해시 맵 (Counter) | Ch 11 | 빈도 카운팅, $O(1)$ 평균 쿼리 |
| lower/upper bound | Ch 12.3 | 이진 탐색으로 범위 크기 |

## 연결 문제

- **BOJ 1920** (Core-07): 수 찾기 — 존재 여부 (set)
- **BOJ 2110** (Core-07): 공유기 설치 — 매개변수 이진 탐색

## 다시 연결해 볼 질문

- `숫자 카드 2`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `탐색 대상을 재정의하고 자료구조 또는 매개변수 탐색으로 문제를 다시 보는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `숫자 카드 2`를 다시 설명할 때는 문제 이름보다 `탐색 대상을 재정의하고 자료구조 또는 매개변수 탐색으로 문제를 다시 보는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 앞 프로젝트: [`../../1920/README.md`](../../1920/README.md) (수 찾기)
- 다음 프로젝트: [`../../2110/README.md`](../../2110/README.md) (공유기 설치)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`counter-concept.md`](../docs/concepts/counter-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
