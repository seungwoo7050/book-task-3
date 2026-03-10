# 지식 인덱스

> 프로젝트: 키로거
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 개념

### Two-Stack 커서 모델 (재확인)
1406에서 배운 패턴의 재적용. 커서 왼쪽/오른쪽을 두 스택으로 관리.

### sys.stdout.write vs print
`print()`는 내부적으로 문자열 변환, 구분자 처리, 개행 추가 등의 오버헤드가 있다.
대량 출력 시 `sys.stdout.write()`가 더 빠르다.

## 연결되는 문제들

| 개념 | 관련 |
|------|------|
| Two-Stack | BOJ 1406 (에디터) — 원본 패턴 |
| 출력 최적화 | 대량 출력이 있는 모든 문제 |

## CLRS 매핑

| 챕터 | 연관성 |
|------|--------|
| Ch 10.1 | 스택 연산의 기본 |
| Ch 10.2 | 연결 리스트의 대안으로서의 스택 |

## 다시 연결해 볼 질문

- `키로거`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `순차 자료구조를 선택하고 편집 연산의 비용 모델을 설명하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `키로거`를 다시 설명할 때는 문제 이름보다 `순차 자료구조를 선택하고 편집 연산의 비용 모델을 설명하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 앞 프로젝트: [`../../10807/README.md`](../../10807/README.md) (개수 세기)
- 다음 프로젝트: [`../../1406/README.md`](../../1406/README.md) (에디터)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`keylogger-concept.md`](../docs/concepts/keylogger-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
