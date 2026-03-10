# 02 registry catalog와 manifest schema

catalog seed와 manifest schema를 하나의 데이터 계약으로 묶어 추천 시스템의 입력 경계를 고정하는 단계다.

## 이 단계에서 배우는 것

- schema-first로 catalog와 manifest를 설계하는 법
- seed data와 validation route를 같은 계약으로 설명하는 방식
- 데모용 데이터셋을 재현 가능하게 유지하는 법

## 먼저 읽을 순서

- `problem/README.md`
- `docs/README.md`
- `08-capstone-submission/v0-initial-demo/shared/src/contracts.ts`
- `08-capstone-submission/v0-initial-demo/shared/src/catalog.ts`
- `08-capstone-submission/v0-initial-demo/node/src/scripts/seed.ts`
- `08-capstone-submission/v0-initial-demo/node/tests/manifest-validation.test.ts`

## 현재 상태

- 실제 schema와 seed는 `v0`에 구현돼 있고, `v1`과 `v2`가 이를 확장해 재사용한다.
- 이 stage는 데이터를 어떻게 고정했는지 설명하는 문서 단계다.

## 포트폴리오로 가져갈 것

- schema-first 설계와 seed data 운영 방식
- validation route를 품질 증빙으로 활용하는 방식
