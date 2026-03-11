# 05 로그, 지표, 피드백 루프 문제 정의

## 이 stage가 맡는 문제

usage event, feedback record, experiment metadata를 DB와 API로 연결해 추천 품질 개선의 운영 루프를 설명하는 단계다.

## 현재 기준 성공 조건

- 추천 품질 개선이 일회성 실험이 아니라 운영 루프로 설명된다.
- 학생이 자기 프로젝트에서 어떤 운영 지표를 남겨야 할지 감을 잡는다.
- 후속 release gate와 operator console 단계로 자연스럽게 이어진다.

## 먼저 알고 있으면 좋은 것

- 상위 `README.md`, `problem/README.md`, `docs/README.md`를 먼저 읽어 stage 목적을 고정한다.
- 실제 구현 확인은 `v1-ranking-hardening` 기준으로 내려가야 한다.
- 이 단계는 추천 품질을 '사용 이후'까지 추적하는 구조를 다룬다.

## 확인할 증거

- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/db/schema.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/repositories/catalog-repository.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/app.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/components/mcp-dashboard.tsx`

## 아직 남아 있는 불확실성

- 이 단계는 추천 품질을 '사용 이후'까지 추적하는 구조를 다룬다.
