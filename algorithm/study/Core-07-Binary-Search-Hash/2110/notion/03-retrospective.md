# 회고

> 프로젝트: 공유기 설치
> 아래 내용은 `notion-archive/03-retrospective.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 배운 것

매개변수 이진 탐색(Parametric Search)은 최적화 문제를 결정 문제로 변환하는 강력한 기법이다. "최솟값을 최대화하라" → "이 최솟값이 가능한가?"로 바꾸면 이진 탐색이 적용 가능하다.

## 패턴의 범용성

이 패턴이 적용되는 문제 유형:
- "최대 중 최소" 또는 "최소 중 최대"
- 답이 단조 증가/감소 조건을 만족
- 판별 함수가 $O(N)$ 이하로 구현 가능

## 판별 함수와 그리디의 결합

`feasible(d)` 내부에서 탐욕적 설치를 하는 것이 핵심. 매개변수 탐색의 판별 함수는 그 자체가 또 다른 알고리즘(여기서는 그리디)을 포함한다.

## 이번 프로젝트가 남긴 기준

- `공유기 설치`를 통해 `탐색 대상을 재정의하고 자료구조 또는 매개변수 탐색으로 문제를 다시 보는 연습`를 코드와 문장으로 같이 설명하는 감각을 다시 확인했다.
- 짧은 정답 코드보다, 왜 이 선택이 안전했는지 적어 둔 문장이 나중에 더 오래 남는다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.

## 다음 프로젝트로 가져갈 것

- 구현을 시작하기 전에 핵심 상태와 종료 조건을 먼저 적는다.
- 자동 검증이 통과한 뒤에야 문서 문장을 확정한다.
- 포트폴리오용 README로 옮길 때는 "선택 이유"와 "실수 포인트"를 먼저 보여 준다.
- `05-development-timeline.md`처럼 실행 순서와 검증 순서를 남기면, 시간이 지난 뒤에도 학습 과정을 다시 밟기 쉬워진다.

## 트랙 안에서 이어지는 연결

- 앞 프로젝트: [`../../10816/README.md`](../../10816/README.md) (숫자 카드 2)
- 현재 프로젝트를 다시 설명할 때는 같은 트랙의 앞뒤 프로젝트와 무엇이 달라졌는지 한 문장으로 비교해 두는 편이 좋다.

## 다시 확인할 경로

- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`parametric-search-concept.md`](../docs/concepts/parametric-search-concept.md)
