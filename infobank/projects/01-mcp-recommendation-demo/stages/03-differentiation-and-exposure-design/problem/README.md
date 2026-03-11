# 03 차별화 포인트와 노출 설계 문제 정의

## 문제 해석

한국어 추천 문구와 differentiation point를 설계해 사용자가 추천 이유를 바로 이해하도록 만드는 단계다.

## 입력

- 루트 `README.md`와 `../../docs/`에 정리된 트랙 해석
- 아래 capstone 연결 경로에 있는 실제 구현과 증빙 파일

## 기대 산출물

- korean exposure fields
- reason template
- operator-facing explanation rules

## 완료 기준

- 추천 결과를 한국어 문장으로 납득 가능하게 설명할 수 있다.
- 차별화 포인트가 catalog 데이터와 UI 설명에 함께 반영된다.
- 학생이 자기 서비스 소개 문구와 recommendation copy를 함께 설계할 힌트를 얻는다.

## capstone 연결 증거

- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/catalog.ts`
- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/src/services/recommendation-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/react/components/mcp-dashboard.tsx`

## 범위 메모

- 이 단계는 ranking 수치 자체보다, 추천 이유를 어떻게 표현할지를 다룬다.
