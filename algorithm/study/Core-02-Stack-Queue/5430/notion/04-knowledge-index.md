# 지식 인덱스

> 프로젝트: AC
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 개념

### 논리적 뒤집기 (Lazy Reverse)
실제로 배열을 뒤집지 않고 방향 플래그만 토글. D 연산 시 방향에 따라 popleft/pop 선택.

### deque의 양방향 O(1) 삭제
`popleft()`와 `pop()` 모두 O(1). 방향 플래그와 결합하면 논리적 뒤집기를 구현할 수 있다.

### 문자열 기반 배열 파싱
`[x1,x2,...,xn]` 형태를 `s[1:-1].split(',')` 로 파싱. 빈 배열(`n=0`)은 별도 처리.

## 연결되는 문제들
| 개념 | 관련 |
|------|------|
| Lazy 처리 | 세그먼트 트리의 lazy propagation |
| deque | BOJ 2164 (카드2), BFS 0-1 |
| 파싱 | 복잡한 입력 형식의 문제 전반 |

## CLRS 매핑
| Ch 10.1 | 큐/deque 인터페이스 |

## 다시 연결해 볼 질문

- `AC`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `명령 기반 자료구조 문제를 상태 전이 규칙으로 정리하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `AC`를 다시 설명할 때는 문제 이름보다 `명령 기반 자료구조 문제를 상태 전이 규칙으로 정리하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 앞 프로젝트: [`../../2164/README.md`](../../2164/README.md) (카드2)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`deque-lazy-concept.md`](../docs/concepts/deque-lazy-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
