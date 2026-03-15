# 01-selection-rubric-and-eval-contract 문제지

## 왜 중요한가

추천 품질을 어떤 rubric과 offline eval contract로 판정할지 먼저 고정하는 단계다.

## 목표

시작 위치의 구현을 완성해 어떤 추천이 pass인지 fail인지 문서만으로 설명할 수 있다, 후속 버전 비교가 같은 기준을 사용한다는 점이 분명해진다, 학생이 자기 프로젝트에 맞는 rubric을 설계할 출발점을 얻는다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/src/services/eval-service.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/contracts.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/eval.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/tests/manifest-validation.test.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/tests/recommendation-service.test.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/package.json`
- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/package.json`

## starter code / 입력 계약

- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/src/services/eval-service.ts`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 어떤 추천이 pass인지 fail인지 문서만으로 설명할 수 있다.
- 후속 버전 비교가 같은 기준을 사용한다는 점이 분명해진다.
- 학생이 자기 프로젝트에 맞는 rubric을 설계할 출발점을 얻는다.

## 제외 범위

- 이 단계는 '어떻게 구현했는가'보다 '무엇을 좋은 추천으로 볼 것인가'를 먼저 설명한다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `evaluateOfflineCases`와 `toolCategorySchema`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `manifest validation`와 `rejects incomplete manifests`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node && npm test -- tests/manifest-validation.test.ts tests/recommendation-service.test.ts`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node && npm test -- tests/manifest-validation.test.ts tests/recommendation-service.test.ts
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`01-selection-rubric-and-eval-contract_answer.md`](01-selection-rubric-and-eval-contract_answer.md)에서 확인한다.
