# 06 release compatibility와 quality gate 문제 정의

## 이 stage가 맡는 문제

semver/compatibility gate와 release gate를 deterministic rule로 구현해 추천 시스템의 배포 판단을 설명하는 단계다.

## 현재 기준 성공 조건

- 추천 시스템의 품질 개선을 배포 준비 상태와 연결해 설명할 수 있다.
- 학생이 자기 프로젝트에서 release gate 문서를 설계할 기준을 얻는다.
- 최종 제출물의 proof artifact 재생성 경로가 분명해진다.

## 먼저 알고 있으면 좋은 것

- 상위 `README.md`, `problem/README.md`, `docs/README.md`를 먼저 읽어 stage 목적을 고정한다.
- 실제 구현 확인은 `v2-submission-polish` 기준으로 내려가야 한다.
- 이 단계는 추천 결과를 보여 주는 데서 끝나지 않고, 배포 판단과 제출 산출물까지 연결한다.

## 확인할 증거

- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/compatibility-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/release-gate-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/artifact-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/tests/compatibility-service.test.ts`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/tests/release-gate-service.test.ts`

## 아직 남아 있는 불확실성

- 이 단계는 추천 결과를 보여 주는 데서 끝나지 않고, 배포 판단과 제출 산출물까지 연결한다.
