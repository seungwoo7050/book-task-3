# 02 registry catalog와 manifest schema 문제 정의

## 문제 해석

catalog seed와 manifest schema를 하나의 데이터 계약으로 묶어 추천 시스템의 입력 경계를 고정하는 단계다.

## 입력

- 루트 `README.md`와 `../../docs/`에 정리된 트랙 해석
- 아래 capstone 연결 경로에 있는 실제 구현과 증빙 파일

## 기대 산출물

- Zod manifest contract
- seed catalog
- manifest validation route 설명

## 완료 기준

- catalog 데이터와 manifest 형식이 한 묶음의 계약으로 이해된다.
- 학생이 자기 프로젝트에서 seed data와 validation을 같이 설명할 수 있다.
- 후속 추천 로직이 어떤 입력 위에서 동작하는지 추적 가능하다.

## capstone 연결 증거

- `08-capstone-submission/v0-initial-demo/shared/src/contracts.ts`
- `08-capstone-submission/v0-initial-demo/shared/src/catalog.ts`
- `08-capstone-submission/v0-initial-demo/node/src/scripts/seed.ts`
- `08-capstone-submission/v0-initial-demo/node/tests/manifest-validation.test.ts`

## 범위 메모

- 여기서는 추천 알고리즘보다 입력 데이터의 안정성과 검증 가능성을 먼저 설명한다.
