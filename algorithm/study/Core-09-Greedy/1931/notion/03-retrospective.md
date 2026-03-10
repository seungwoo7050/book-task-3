# 회고

> 프로젝트: 회의실 배정
> 아래 내용은 `notion-archive/03-retrospective.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 배운 것

Activity Selection은 그리디의 정전(正典). 교환 논증으로 정당성을 증명하는 패턴을 체화했다. "최적해에 첫 번째 그리디 선택이 포함되지 않는다면 → 교체해도 해가 나빠지지 않으므로 → 포함시켜도 된다."

## 정렬 키의 중요성

$(end, start)$ 복합 키를 쓰지 않으면 틀릴 수 있다. "동률(tie-breaking)"을 어떻게 처리하는지가 정렬 기반 그리디의 반복적인 함정.

## Core-09 트랙 종합

11047(동전 0) → 1931(회의실) → 1744(수 묶기) 순서로, 그리디의 난이도가 "단순 탐욕 → 정렬+탐욕 → 분류+탐욕"으로 올라간다.

## 이번 프로젝트가 남긴 기준

- `회의실 배정`를 통해 `탐욕 선택의 기준을 말로 설명하고 반례 가능성을 점검하는 연습`를 코드와 문장으로 같이 설명하는 감각을 다시 확인했다.
- 짧은 정답 코드보다, 왜 이 선택이 안전했는지 적어 둔 문장이 나중에 더 오래 남는다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.

## 다음 프로젝트로 가져갈 것

- 구현을 시작하기 전에 핵심 상태와 종료 조건을 먼저 적는다.
- 자동 검증이 통과한 뒤에야 문서 문장을 확정한다.
- 포트폴리오용 README로 옮길 때는 "선택 이유"와 "실수 포인트"를 먼저 보여 준다.
- `05-development-timeline.md`처럼 실행 순서와 검증 순서를 남기면, 시간이 지난 뒤에도 학습 과정을 다시 밟기 쉬워진다.

## 트랙 안에서 이어지는 연결

- 앞 프로젝트: [`../../11047/README.md`](../../11047/README.md) (동전 0)
- 다음 프로젝트: [`../../1744/README.md`](../../1744/README.md) (수 묶기)
- 현재 프로젝트를 다시 설명할 때는 같은 트랙의 앞뒤 프로젝트와 무엇이 달라졌는지 한 문장으로 비교해 두는 편이 좋다.

## 다시 확인할 경로

- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
- [`activity-selection-concept.md`](../docs/concepts/activity-selection-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
