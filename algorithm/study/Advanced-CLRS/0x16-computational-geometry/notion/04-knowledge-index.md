# 지식 인덱스

> 프로젝트: 계산 기하 실습
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| 외적 (cross product) | Ch 33.1 | 방향 판정의 기본 도구 |
| CCW / CW | Ch 33.1 | 반시계 / 시계 방향 |
| 볼록 껍질 (convex hull) | Ch 33.3 | 점 집합의 최외곽 볼록 다각형 |
| Andrew's Monotone Chain | — | 정렬 기반 hull, $O(n \log n)$ |
| 선분 교차 | Ch 33.1 | 두 선분의 교차 여부 판정 |
| on_segment | Ch 33.1 | collinear 점의 선분 위 포함 검사 |

## 다시 연결해 볼 질문

- `계산 기하 실습`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `계산 기하 실습의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `계산 기하 실습`를 다시 설명할 때는 문제 이름보다 `계산 기하 실습의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 앞 프로젝트: [`../../0x15-string-matching/README.md`](../../0x15-string-matching/README.md) (고급 문자열 매칭)
- 다음 프로젝트: [`../../0x17-number-theory-lab/README.md`](../../0x17-number-theory-lab/README.md) (정수론 실습)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`geometry-primitives.md`](../docs/concepts/geometry-primitives.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
