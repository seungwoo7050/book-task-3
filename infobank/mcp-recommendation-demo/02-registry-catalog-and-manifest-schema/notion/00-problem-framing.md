# 02 registry catalog와 manifest schema 문제 정의

## 이 stage가 맡는 문제

catalog seed와 manifest schema를 하나의 데이터 계약으로 묶어 추천 시스템의 입력 경계를 고정하는 단계다.

## 현재 기준 성공 조건

- catalog 데이터와 manifest 형식이 한 묶음의 계약으로 이해된다.
- 학생이 자기 프로젝트에서 seed data와 validation을 같이 설명할 수 있다.
- 후속 추천 로직이 어떤 입력 위에서 동작하는지 추적 가능하다.

## 먼저 알고 있으면 좋은 것

- 상위 `README.md`, `problem/README.md`, `docs/README.md`를 먼저 읽어 stage 목적을 고정한다.
- 실제 구현 확인은 `v0-initial-demo` 기준으로 내려가야 한다.
- 여기서는 추천 알고리즘보다 입력 데이터의 안정성과 검증 가능성을 먼저 설명한다.

## 확인할 증거

- `08-capstone-submission/v0-initial-demo/shared/src/contracts.ts`
- `08-capstone-submission/v0-initial-demo/shared/src/catalog.ts`
- `08-capstone-submission/v0-initial-demo/node/src/scripts/seed.ts`
- `08-capstone-submission/v0-initial-demo/node/tests/manifest-validation.test.ts`

## 아직 남아 있는 불확실성

- 여기서는 추천 알고리즘보다 입력 데이터의 안정성과 검증 가능성을 먼저 설명한다.
