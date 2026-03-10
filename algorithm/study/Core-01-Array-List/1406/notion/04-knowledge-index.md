# 지식 인덱스

> 프로젝트: 에디터
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 개념

### Two-Stack 모델
커서 왼쪽과 오른쪽을 각각 스택으로 관리하여, 커서 위치에서의 삽입/삭제/이동을 O(1)로 수행하는 기법.
연결 리스트의 대안으로 Python에서 특히 유효하다.

### 배열 insert/pop(i)의 비용
Python list의 `insert(i, x)`와 `pop(i)`는 O(n). 끝에서의 `append()`와 `pop()`만 amortized O(1).

## 연결되는 문제들

| 개념 | 관련 |
|------|------|
| Two-Stack | BOJ 5397 (키로거) — 거의 동일한 패턴 |
| 커서 이동 시뮬레이션 | 텍스트 에디터 구현 전반 |
| 연결 리스트 vs 스택 | CLRS Ch 10.2 |

## CLRS 매핑

| 챕터 | 연관성 |
|------|--------|
| Ch 10.2 | 연결 리스트와 그 대안 |
| Ch 17 | 동적 배열의 amortized 분석 |

## 다시 연결해 볼 질문

- `에디터`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `순차 자료구조를 선택하고 편집 연산의 비용 모델을 설명하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `에디터`를 다시 설명할 때는 문제 이름보다 `순차 자료구조를 선택하고 편집 연산의 비용 모델을 설명하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 앞 프로젝트: [`../../5397/README.md`](../../5397/README.md) (키로거)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`editor-concept.md`](../docs/concepts/editor-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
