# 06 release compatibility와 quality gate

## 이 stage의 문제

semver/compatibility gate와 release gate를 deterministic rule로 구현해 추천 시스템의 배포 판단을 설명한다.

## 입력/제약

- 입력: release candidate, compatibility rule, quality threshold, artifact export 규칙
- 제약: 같은 입력이면 같은 gate 결과가 나와야 한다.

## 이 stage의 답

- compatibility와 quality gate를 분리해 배포 전 판단 기준을 명확히 한다.
- artifact export까지 포함해 제출용 proof를 재생성 가능하게 만든다.

## capstone 연결 증거

- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/compatibility-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/release-gate-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/artifact-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/tests/compatibility-service.test.ts`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/tests/release-gate-service.test.ts`

## 검증 명령

- 별도 stage-local 실행 명령은 없다.
- 공식 답 `v2-submission-polish`에서 `pnpm compatibility ...`, `pnpm release:gate ...`가 이 stage의 기준 명령이 된다.

## 현재 한계

- self-hosted auth/job 운영은 아직 포함하지 않는다.
- production release governance 전체를 모델링하지는 않는다.
