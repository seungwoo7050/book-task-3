# 03 차별화 포인트와 노출 설계 문제 정의

## 이 stage가 맡는 문제

한국어 추천 문구와 differentiation point를 설계해 사용자가 추천 이유를 바로 이해하도록 만드는 단계다.

## 현재 기준 성공 조건

- 추천 결과를 한국어 문장으로 납득 가능하게 설명할 수 있다.
- 차별화 포인트가 catalog 데이터와 UI 설명에 함께 반영된다.
- 학생이 자기 서비스 소개 문구와 recommendation copy를 함께 설계할 힌트를 얻는다.

## 먼저 알고 있으면 좋은 것

- 상위 `README.md`, `problem/README.md`, `docs/README.md`를 먼저 읽어 stage 목적을 고정한다.
- 실제 구현 확인은 `v0-initial-demo` 기준으로 내려가야 한다.
- 이 단계는 ranking 수치 자체보다, 추천 이유를 어떻게 표현할지를 다룬다.

## 확인할 증거

- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/catalog.ts`
- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/src/services/recommendation-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/react/components/mcp-dashboard.tsx`

## 아직 남아 있는 불확실성

- 이 단계는 ranking 수치 자체보다, 추천 이유를 어떻게 표현할지를 다룬다.
