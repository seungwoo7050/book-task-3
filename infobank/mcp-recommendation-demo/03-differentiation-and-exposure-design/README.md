# 03 차별화 포인트와 노출 설계

한국어 추천 문구와 differentiation point를 설계해 사용자가 추천 이유를 바로 이해하도록 만드는 단계다.

## 이 단계에서 배우는 것

- 추천 결과를 단순 점수가 아니라 설명 가능한 문장으로 바꾸는 법
- 한국어 시장 맥락에 맞는 노출 필드와 reason template 설계
- 운영자 화면과 사용자-facing 문구를 연결하는 방식

## 먼저 읽을 순서

- `problem/README.md`
- `docs/README.md`
- `08-capstone-submission/v0-initial-demo/shared/src/catalog.ts`
- `08-capstone-submission/v0-initial-demo/node/src/services/recommendation-service.ts`
- `08-capstone-submission/v0-initial-demo/react/components/mcp-dashboard.tsx`

## 현재 상태

- 실제 노출 문구와 reason template은 `v0`에서 구현되고 이후 버전이 그대로 재사용한다.
- 이 stage는 '왜 이 추천이 좋은가'를 말하는 문장을 정리하는 인덱스다.

## 포트폴리오로 가져갈 것

- 추천 로직과 설명 문구를 함께 설계하는 방식
- 한국어 사용자에게 보이는 exposure copy 정리법
