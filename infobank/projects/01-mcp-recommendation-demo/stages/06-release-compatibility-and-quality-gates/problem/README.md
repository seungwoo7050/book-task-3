# 06 release compatibility와 quality gate 문제 정의

## 문제 해석

semver/compatibility gate와 release gate를 deterministic rule로 구현해 추천 시스템의 배포 판단을 설명하는 단계다.

## 입력

- 루트 `README.md`와 `../../docs/`에 정리된 트랙 해석
- 아래 capstone 연결 경로에 있는 실제 구현과 증빙 파일

## 기대 산출물

- release candidate model
- compatibility report
- release gate report
- artifact export

## 완료 기준

- 추천 시스템의 품질 개선을 배포 준비 상태와 연결해 설명할 수 있다.
- 학생이 자기 프로젝트에서 release gate 문서를 설계할 기준을 얻는다.
- 최종 제출물의 proof artifact 재생성 경로가 분명해진다.

## capstone 연결 증거

- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/compatibility-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/release-gate-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/artifact-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/tests/compatibility-service.test.ts`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/tests/release-gate-service.test.ts`

## 범위 메모

- 이 단계는 추천 결과를 보여 주는 데서 끝나지 않고, 배포 판단과 제출 산출물까지 연결한다.
