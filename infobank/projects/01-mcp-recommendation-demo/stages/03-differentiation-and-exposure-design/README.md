# 03 차별화 포인트와 노출 설계

## 이 stage의 문제

한국어 추천 문구와 differentiation point를 설계해 사용자가 추천 이유를 바로 이해하게 만든다.

## 입력/제약

- 입력: catalog metadata, recommendation result, 한국어 노출 문구
- 제약: 점수만 보여 주지 않고 사람에게 읽히는 이유 문장을 남겨야 한다.

## 이 stage의 답

- recommendation copy와 reason template을 별도 학습 포인트로 분리한다.
- 사용자-facing 문구와 운영 콘솔 설명 구조를 같은 축으로 맞춘다.

## capstone 연결 증거

- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/catalog.ts`
- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/src/services/recommendation-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/react/components/mcp-dashboard.tsx`

## 검증 명령

- 별도 stage-local 실행 명령은 없다.
- capstone `v0` 추천 결과와 UI 노출 문구가 문서에 적은 reason template 설명과 일치하는지 확인한다.

## 현재 한계

- 추천 설명 문구의 품질 측정은 후속 compare 단계에서 다룬다.
- 다국어 전략은 범위 밖이다.
