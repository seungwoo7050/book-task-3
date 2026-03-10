# 지식 인덱스

> 프로젝트: 공유기 설치
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 알고리즘

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| 매개변수 이진 탐색 | Ch 12.3 확장 | 답의 범위에서 이진 탐색 |
| 탐욕적 판별 | Ch 16 | feasible 함수 내부의 그리디 배치 |

## 시간 복잡도

- $O(N \log N + N \log(\text{max\_coord}))$

## 연결 문제

- **BOJ 1920** (Core-07): 기본 이진 탐색
- **BOJ 10816** (Core-07): 빈도 세기
- **BOJ 2805**: 나무 자르기 — 매개변수 탐색 변형
- **BOJ 1654**: 랜선 자르기 — 매개변수 탐색 변형

## 다시 연결해 볼 질문

- `공유기 설치`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `탐색 대상을 재정의하고 자료구조 또는 매개변수 탐색으로 문제를 다시 보는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `공유기 설치`를 다시 설명할 때는 문제 이름보다 `탐색 대상을 재정의하고 자료구조 또는 매개변수 탐색으로 문제를 다시 보는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 앞 프로젝트: [`../../10816/README.md`](../../10816/README.md) (숫자 카드 2)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`parametric-search-concept.md`](../docs/concepts/parametric-search-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
