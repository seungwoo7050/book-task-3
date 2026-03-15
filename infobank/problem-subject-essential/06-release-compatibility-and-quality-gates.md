# 06-release-compatibility-and-quality-gates 문제지

## 왜 중요한가

semver/compatibility gate와 release gate를 deterministic rule로 구현해 추천 시스템의 배포 판단을 설명하는 단계다.

## 목표

시작 위치의 구현을 완성해 추천 시스템의 품질 개선을 배포 준비 상태와 연결해 설명할 수 있다, 학생이 자기 프로젝트에서 release gate 문서를 설계할 기준을 얻는다, 최종 제출물의 proof artifact 재생성 경로가 분명해진다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/artifact-service.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/compatibility-service.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/release-gate-service.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/tests/compatibility-service.test.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/tests/manifest-validation.test.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/package.json`

## starter code / 입력 계약

- `../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node/src/services/artifact-service.ts`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 추천 시스템의 품질 개선을 배포 준비 상태와 연결해 설명할 수 있다.
- 학생이 자기 프로젝트에서 release gate 문서를 설계할 기준을 얻는다.
- 최종 제출물의 proof artifact 재생성 경로가 분명해진다.

## 제외 범위

- 이 단계는 추천 결과를 보여 주는 데서 끝나지 않고, 배포 판단과 제출 산출물까지 연결한다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `buildSubmissionArtifact`와 `buildCheck`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `releaseCheckBot`와 `runCompatibilityGate`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node && npm test -- tests/compatibility-service.test.ts tests/manifest-validation.test.ts tests/recommendation-service.test.ts tests/release-gate-service.test.ts tests/rerank-service.test.ts`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/node && npm test -- tests/compatibility-service.test.ts tests/manifest-validation.test.ts tests/recommendation-service.test.ts tests/release-gate-service.test.ts tests/rerank-service.test.ts
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`06-release-compatibility-and-quality-gates_answer.md`](06-release-compatibility-and-quality-gates_answer.md)에서 확인한다.
