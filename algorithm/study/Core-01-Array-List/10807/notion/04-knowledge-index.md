# 지식 인덱스

> 프로젝트: 개수 세기
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 개념

### 선형 탐색 (Linear Search)
배열을 처음부터 끝까지 순회하면서 조건에 맞는 원소를 찾거나 세는 O(n) 연산.
가장 단순하지만 정렬되지 않은 데이터에서는 이것이 최선이다.

### Python list.count()
내장 메서드로, C 레벨에서 선형 탐색을 수행한다.
직접 루프를 짜는 것보다 빠르지만 복잡도는 동일하게 O(n).

## 연결되는 문제들

| 개념 | 관련 |
|------|------|
| 빈도수 세기 | Counter, 해시맵 기반 빈도 테이블 (Core-07) |
| 배열 순회 | 거의 모든 문제의 기본 |

## 다시 연결해 볼 질문

- `개수 세기`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `순차 자료구조를 선택하고 편집 연산의 비용 모델을 설명하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `개수 세기`를 다시 설명할 때는 문제 이름보다 `순차 자료구조를 선택하고 편집 연산의 비용 모델을 설명하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 다음 프로젝트: [`../../5397/README.md`](../../5397/README.md) (키로거)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`array-concept.md`](../docs/concepts/array-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
