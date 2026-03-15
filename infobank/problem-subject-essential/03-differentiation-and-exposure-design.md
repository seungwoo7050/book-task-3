# 03-differentiation-and-exposure-design 문제지

## 왜 중요한가

한국어 추천 문구와 differentiation point를 설계해 사용자가 추천 이유를 바로 이해하도록 만드는 단계다.

## 목표

시작 위치의 구현을 완성해 추천 결과를 한국어 문장으로 납득 가능하게 설명할 수 있다, 차별화 포인트가 catalog 데이터와 UI 설명에 함께 반영된다, 학생이 자기 서비스 소개 문구와 recommendation copy를 함께 설계할 힌트를 얻는다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/src/services/recommendation-service.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/react/components/mcp-dashboard.tsx`
- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/catalog.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/tests/manifest-validation.test.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/tests/recommendation-service.test.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/package.json`
- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/react/package.json`

## starter code / 입력 계약

- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/src/services/recommendation-service.ts`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 추천 결과를 한국어 문장으로 납득 가능하게 설명할 수 있다.
- 차별화 포인트가 catalog 데이터와 UI 설명에 함께 반영된다.
- 학생이 자기 서비스 소개 문구와 recommendation copy를 함께 설계할 힌트를 얻는다.

## 제외 범위

- 이 단계는 ranking 수치 자체보다, 추천 이유를 어떻게 표현할지를 다룬다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `tokenize`와 `unique`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `manifest validation`와 `rejects incomplete manifests`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node && npm test -- tests/manifest-validation.test.ts tests/recommendation-service.test.ts`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node && npm test -- tests/manifest-validation.test.ts tests/recommendation-service.test.ts
```

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/react && npm run test
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`03-differentiation-and-exposure-design_answer.md`](03-differentiation-and-exposure-design_answer.md)에서 확인한다.
