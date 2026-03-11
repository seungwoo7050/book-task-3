# 01 추천 품질 기준과 평가 계약 문제 정의

## 문제 해석

추천 품질을 어떤 rubric과 offline eval contract로 판정할지 먼저 고정하는 단계다.

## 입력

- 루트 `README.md`와 `../../docs/`에 정리된 트랙 해석
- 아래 capstone 연결 경로에 있는 실제 구현과 증빙 파일

## 기대 산출물

- selection rubric
- offline eval contract
- acceptance threshold 설명

## 완료 기준

- 어떤 추천이 pass인지 fail인지 문서만으로 설명할 수 있다.
- 후속 버전 비교가 같은 기준을 사용한다는 점이 분명해진다.
- 학생이 자기 프로젝트에 맞는 rubric을 설계할 출발점을 얻는다.

## capstone 연결 증거

- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/contracts.ts`
- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/eval.ts`
- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/src/services/eval-service.ts`

## 범위 메모

- 이 단계는 '어떻게 구현했는가'보다 '무엇을 좋은 추천으로 볼 것인가'를 먼저 설명한다.
