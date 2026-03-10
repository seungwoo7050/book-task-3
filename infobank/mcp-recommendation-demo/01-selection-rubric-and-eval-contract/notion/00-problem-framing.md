# 01 추천 품질 기준과 평가 계약 문제 정의

## 이 stage가 맡는 문제

추천 품질을 어떤 rubric과 offline eval contract로 판정할지 먼저 고정하는 단계다.

## 현재 기준 성공 조건

- 어떤 추천이 pass인지 fail인지 문서만으로 설명할 수 있다.
- 후속 버전 비교가 같은 기준을 사용한다는 점이 분명해진다.
- 학생이 자기 프로젝트에 맞는 rubric을 설계할 출발점을 얻는다.

## 먼저 알고 있으면 좋은 것

- 상위 `README.md`, `problem/README.md`, `docs/README.md`를 먼저 읽어 stage 목적을 고정한다.
- 실제 구현 확인은 `v0-initial-demo` 기준으로 내려가야 한다.
- 이 단계는 '어떻게 구현했는가'보다 '무엇을 좋은 추천으로 볼 것인가'를 먼저 설명한다.

## 확인할 증거

- `08-capstone-submission/v0-initial-demo/shared/src/contracts.ts`
- `08-capstone-submission/v0-initial-demo/shared/src/eval.ts`
- `08-capstone-submission/v0-initial-demo/node/src/services/eval-service.ts`

## 아직 남아 있는 불확실성

- 이 단계는 '어떻게 구현했는가'보다 '무엇을 좋은 추천으로 볼 것인가'를 먼저 설명한다.
