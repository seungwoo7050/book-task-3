# 지식 인덱스

> 프로젝트: 카드2
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 개념

### 큐 (Queue)
FIFO(First In, First Out) 자료 구조. `popleft()`/`append()` 패턴.

### collections.deque
Python 표준 라이브러리의 양방향 큐. 양쪽 끝에서 O(1) 삽입/삭제.
일반 list의 `pop(0)`은 O(n)이므로, 큐 용도로는 반드시 deque를 사용해야 한다.

## 연결되는 문제들
| 개념 | 관련 |
|------|------|
| 큐 시뮬레이션 | 요세푸스(1158), BFS 전반 |
| deque 활용 | BOJ 5430 (AC), 슬라이딩 윈도우 |

## CLRS 매핑
| Ch 10.1 | 큐의 배열 구현 |

## 다시 연결해 볼 질문

- `카드2`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `명령 기반 자료구조 문제를 상태 전이 규칙으로 정리하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `카드2`를 다시 설명할 때는 문제 이름보다 `명령 기반 자료구조 문제를 상태 전이 규칙으로 정리하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 앞 프로젝트: [`../../10828/README.md`](../../10828/README.md) (스택)
- 다음 프로젝트: [`../../5430/README.md`](../../5430/README.md) (AC)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`queue-concept.md`](../docs/concepts/queue-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
