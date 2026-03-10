# 01 추천 품질 기준과 평가 계약

추천 품질을 어떤 rubric과 offline eval contract로 판정할지 먼저 고정하는 단계다.

## 이 단계에서 배우는 것

- 좋은 추천을 설명할 때 필요한 평가 축과 acceptance threshold
- runtime 로직과 독립된 offline eval contract 설계
- 비교 가능한 개선 실험을 위해 score vocabulary를 먼저 정하는 법

## 먼저 읽을 순서

- `problem/README.md`
- `docs/README.md`
- `08-capstone-submission/v0-initial-demo/shared/src/contracts.ts`
- `08-capstone-submission/v0-initial-demo/shared/src/eval.ts`
- `08-capstone-submission/v0-initial-demo/node/src/services/eval-service.ts`

## 현재 상태

- 실제 계약은 `v0`의 shared contract와 eval service에 반영돼 있다.
- 이 stage는 별도 구현보다 평가 기준을 stable index로 남기는 역할을 맡는다.

## 포트폴리오로 가져갈 것

- 추천 품질 rubric과 acceptance threshold를 문서화하는 방식
- offline eval contract를 제품 설명과 연결하는 구조
