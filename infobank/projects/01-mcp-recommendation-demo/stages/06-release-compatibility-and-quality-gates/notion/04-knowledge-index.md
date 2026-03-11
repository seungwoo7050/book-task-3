# 06 release compatibility와 quality gate 지식 인덱스

## 핵심 개념

- 추천 결과를 release candidate 판단으로 연결하는 법
- compatibility와 quality gate를 별도 개념으로 다루는 방식
- 제출용 artifact export를 재생성 가능하게 유지하는 법

## 다시 찾을 경로

- `README.md`
- `problem/README.md`
- `docs/README.md`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/compatibility-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/release-gate-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/artifact-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/tests/compatibility-service.test.ts`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/tests/release-gate-service.test.ts`

## 포트폴리오 메모

- release gate와 artifact export를 문서화하는 방식
- 배포 전 품질 점검을 추천 시스템 서사에 연결하는 방법
