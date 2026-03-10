# 회고

> 프로젝트: 계산 기하 실습
> 아래 내용은 `notion-archive/03-retrospective.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 배운 것

- 외적 하나로 방향, 넓이, 교차 판정 모두 가능
- Andrew's Monotone Chain이 Graham Scan보다 구현 단순 (atan2 불필요)
- 정수 좌표면 부동소수점 오차 없이 정확한 판정 가능

## 주의

실수 좌표에서는 epsilon 비교 필요. 이 프로젝트는 정수 좌표 전제.

## 이번 프로젝트가 남긴 기준

- `계산 기하 실습`를 통해 `계산 기하 실습의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 코드와 문장으로 같이 설명하는 감각을 다시 확인했다.
- 짧은 정답 코드보다, 왜 이 선택이 안전했는지 적어 둔 문장이 나중에 더 오래 남는다.
- CLRS Ch 33의 핵심 아이디어를 입출력과 자동 검증이 가능한 작은 실험으로 바꾸는 과정이 중요했다.

## 다음 프로젝트로 가져갈 것

- 구현을 시작하기 전에 핵심 상태와 종료 조건을 먼저 적는다.
- 자동 검증이 통과한 뒤에야 문서 문장을 확정한다.
- 포트폴리오용 README로 옮길 때는 "선택 이유"와 "실수 포인트"를 먼저 보여 준다.
- `05-development-timeline.md`처럼 실행 순서와 검증 순서를 남기면, 시간이 지난 뒤에도 학습 과정을 다시 밟기 쉬워진다.

## 트랙 안에서 이어지는 연결

- 앞 프로젝트: [`../../0x15-string-matching/README.md`](../../0x15-string-matching/README.md) (고급 문자열 매칭)
- 다음 프로젝트: [`../../0x17-number-theory-lab/README.md`](../../0x17-number-theory-lab/README.md) (정수론 실습)
- 현재 프로젝트를 다시 설명할 때는 같은 트랙의 앞뒤 프로젝트와 무엇이 달라졌는지 한 문장으로 비교해 두는 편이 좋다.

## 다시 확인할 경로

- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`geometry-primitives.md`](../docs/concepts/geometry-primitives.md)
