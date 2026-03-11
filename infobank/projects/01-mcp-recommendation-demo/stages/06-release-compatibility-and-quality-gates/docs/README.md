# 06 release compatibility와 quality gate 문서 안내

semver/compatibility gate와 release gate를 deterministic rule로 구현해 추천 시스템의 배포 판단을 설명하는 단계다.

## 오래 남길 개념

- 추천 결과를 release candidate 판단으로 연결하는 법
- compatibility와 quality gate를 별도 개념으로 다루는 방식
- 제출용 artifact export를 재생성 가능하게 유지하는 법

## 같이 볼 파일

- `../README.md`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/compatibility-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/release-gate-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/artifact-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/tests/compatibility-service.test.ts`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/tests/release-gate-service.test.ts`

## 이 단계를 문서로 남기는 이유

- 이 stage는 capstone 구현을 읽기 위한 기준 문장과 개념 인덱스를 맡는다.
- 빠르게 현재 상태를 파악할 수 있어야 하므로 장문의 시행착오는 `notion/`으로 분리한다.
- 이 단계는 추천 결과를 보여 주는 데서 끝나지 않고, 배포 판단과 제출 산출물까지 연결한다.

## notion과의 관계

- `notion/`은 판단 과정, 실패 기록, 회고를 담는 공개 백업 문서다.
- 새 버전으로 다시 정리할 때는 기존 노트를 `notion-archive/`로 옮겨 보존한다.

## 학생이 이 문서 묶음에서 바로 가져갈 것

- `README.md`, `problem/README.md`, `docs/README.md`, `notion/05-development-timeline.md`를 서로 다른 공개 역할로 나누는 방식
- 현재 단계의 검증 명령과 acceptance 기준을 짧은 공개 문서로 남기는 방식
- 장문 시행착오는 `notion/`으로 보내고, 오래 남길 개념과 증빙만 tracked docs에 남기는 방식

## notion과 05 타임라인을 읽는 법

- 빠른 현재 상태는 tracked docs에서 먼저 확인한다.
- 같은 결과를 다시 재현하려면 `../notion/05-development-timeline.md`를 따라 읽고 실행한다.
- 새 기준으로 다시 쓰고 싶다면 기존 `notion/`을 `../notion-archive/`로 옮긴 뒤 새 `notion/`을 만든다.
