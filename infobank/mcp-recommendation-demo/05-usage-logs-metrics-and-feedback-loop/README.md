# 05 로그, 지표, 피드백 루프

usage event, feedback record, experiment metadata를 DB와 API로 연결해 추천 품질 개선의 운영 루프를 설명하는 단계다.

## 이 단계에서 배우는 것

- 추천 서비스에서 어떤 로그와 피드백을 남겨야 하는지
- 실험 메타데이터를 운영자 콘솔과 연결하는 법
- 사용 로그를 다음 실험 설계와 품질 개선으로 잇는 방식

## 먼저 읽을 순서

- `problem/README.md`
- `docs/README.md`
- `08-capstone-submission/v1-ranking-hardening/node/src/db/schema.ts`
- `08-capstone-submission/v1-ranking-hardening/node/src/repositories/catalog-repository.ts`
- `08-capstone-submission/v1-ranking-hardening/node/src/app.ts`
- `08-capstone-submission/v1-ranking-hardening/react/components/mcp-dashboard.tsx`

## 현재 상태

- usage event와 feedback loop는 `v1`에서 구현되고 `v2`가 이를 바탕으로 제출 산출물을 만든다.
- 이 stage는 운영형 추천 시스템으로 넘어가는 지점을 설명한다.

## 포트폴리오로 가져갈 것

- 피드백 루프와 실험 메타데이터 설계
- 운영 로그를 제품 품질 개선 서사로 묶는 방식
