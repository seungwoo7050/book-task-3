# 지식 인덱스

> 프로젝트: 스택
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 개념

### 스택 (Stack)
LIFO(Last In, First Out) 자료 구조. push/pop/top/size/empty 연산 모두 O(1).
Python에서는 list의 `append()`/`pop()` = push/pop, `[-1]` = top.

## 연결되는 문제들

| 개념 | 관련 |
|------|------|
| 스택 활용 | 괄호 검사, DFS, 후위 표기법 계산 |
| Two-Stack | BOJ 1406, 5397 (에디터/키로거) |

## CLRS 매핑
| Ch 10.1 | 스택과 큐의 기본 인터페이스와 배열 구현 |

## 다시 연결해 볼 질문

- `스택`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `명령 기반 자료구조 문제를 상태 전이 규칙으로 정리하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `스택`를 다시 설명할 때는 문제 이름보다 `명령 기반 자료구조 문제를 상태 전이 규칙으로 정리하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 다음 프로젝트: [`../../2164/README.md`](../../2164/README.md) (카드2)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`stack-concept.md`](../docs/concepts/stack-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
