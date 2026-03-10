# 06 release compatibility와 quality gate

semver/compatibility gate와 release gate를 deterministic rule로 구현해 추천 시스템의 배포 판단을 설명하는 단계다.

## 이 단계에서 배우는 것

- 추천 결과를 release candidate 판단으로 연결하는 법
- compatibility와 quality gate를 별도 개념으로 다루는 방식
- 제출용 artifact export를 재생성 가능하게 유지하는 법

## 먼저 읽을 순서

- `problem/README.md`
- `docs/README.md`
- `08-capstone-submission/v2-submission-polish/node/src/services/compatibility-service.ts`
- `08-capstone-submission/v2-submission-polish/node/src/services/release-gate-service.ts`
- `08-capstone-submission/v2-submission-polish/node/src/services/artifact-service.ts`
- `08-capstone-submission/v2-submission-polish/node/tests/compatibility-service.test.ts`
- `08-capstone-submission/v2-submission-polish/node/tests/release-gate-service.test.ts`

## 현재 상태

- compatibility, release gate, artifact export는 `v2`에서 구현돼 최종 제출 proof의 핵심이 된다.
- 이 stage는 운영형 추천 시스템이 '배포 가능한가'를 어떻게 판단하는지 설명한다.

## 포트폴리오로 가져갈 것

- release gate와 artifact export를 문서화하는 방식
- 배포 전 품질 점검을 추천 시스템 서사에 연결하는 방법
