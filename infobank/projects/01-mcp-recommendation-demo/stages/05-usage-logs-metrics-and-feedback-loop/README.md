# 05 로그, 지표, 피드백 루프

## 이 stage의 문제

usage event, feedback record, experiment metadata를 연결해 추천 품질 개선의 운영 루프를 설명한다.

## 입력/제약

- 입력: usage event, feedback record, experiment metadata, dashboard 조회 API
- 제약: 로그는 다음 실험과 compare 판단으로 다시 이어져야 한다.

## 이 stage의 답

- 사용 로그와 피드백을 DB schema와 repository 단위로 정리한다.
- 운영 콘솔에서 실험 메타데이터를 다시 읽을 수 있는 구조를 마련한다.

## capstone 연결 증거

- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/db/schema.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/repositories/catalog-repository.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/app.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/components/mcp-dashboard.tsx`

## 검증 명령

- 별도 stage-local 실행 명령은 없다.
- `v1-ranking-hardening`의 schema, repository, dashboard 포인터가 feedback loop 설명과 맞는지 확인한다.

## 현재 한계

- release gate와 artifact export는 아직 포함하지 않는다.
- 실제 장기 운영 metric tuning은 범위 밖이다.
