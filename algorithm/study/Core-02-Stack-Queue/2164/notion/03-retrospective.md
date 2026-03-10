# 회고

> 프로젝트: 카드2
> 아래 내용은 `notion-archive/03-retrospective.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 이 문제가 남긴 것

### collections.deque의 존재를 알게 됨
Python의 `deque`는 양쪽 끝에서 O(1) 삽입/삭제가 가능한 자료 구조다.
이 문제 이전까지는 리스트만 사용했는데, 앞쪽에서 빼는 연산이 잦을 때 deque가 필수라는 걸 여기서 배웠다.

### 시뮬레이션 = 적절한 자료 구조 선택
문제가 "앞에서 빼고 뒤에 넣는" 행동을 반복하라고 하면, 그건 큐다.
이 인식이 자연스럽게 나오려면 연습이 필요하고, 이 문제가 그 연습의 시작이었다.

## 다음에 적용할 것
- 앞뒤 양방향 삽입/삭제가 필요하면 deque 사용

## 이번 프로젝트가 남긴 기준

- `카드2`를 통해 `명령 기반 자료구조 문제를 상태 전이 규칙으로 정리하는 연습`를 코드와 문장으로 같이 설명하는 감각을 다시 확인했다.
- 짧은 정답 코드보다, 왜 이 선택이 안전했는지 적어 둔 문장이 나중에 더 오래 남는다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.

## 다음 프로젝트로 가져갈 것

- 구현을 시작하기 전에 핵심 상태와 종료 조건을 먼저 적는다.
- 자동 검증이 통과한 뒤에야 문서 문장을 확정한다.
- 포트폴리오용 README로 옮길 때는 "선택 이유"와 "실수 포인트"를 먼저 보여 준다.
- `05-development-timeline.md`처럼 실행 순서와 검증 순서를 남기면, 시간이 지난 뒤에도 학습 과정을 다시 밟기 쉬워진다.

## 트랙 안에서 이어지는 연결

- 앞 프로젝트: [`../../10828/README.md`](../../10828/README.md) (스택)
- 다음 프로젝트: [`../../5430/README.md`](../../5430/README.md) (AC)
- 현재 프로젝트를 다시 설명할 때는 같은 트랙의 앞뒤 프로젝트와 무엇이 달라졌는지 한 문장으로 비교해 두는 편이 좋다.

## 다시 확인할 경로

- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`queue-concept.md`](../docs/concepts/queue-concept.md)
