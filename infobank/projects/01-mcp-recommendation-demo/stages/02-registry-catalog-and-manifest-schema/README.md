# 02 registry catalog와 manifest schema

## 이 stage의 문제

catalog seed와 manifest schema를 하나의 데이터 계약으로 묶어 추천 시스템의 입력 경계를 고정한다.

## 입력/제약

- 입력: catalog seed, manifest schema, validation route
- 제약: 데모용 데이터셋이 버전이 달라져도 재현 가능해야 한다.

## 이 stage의 답

- schema-first로 catalog와 manifest를 설명하는 구조를 제시한다.
- seed data와 validation을 같은 계약 아래에서 읽게 만든다.

## capstone 연결 증거

- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/contracts.ts`
- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/catalog.ts`
- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/src/scripts/seed.ts`
- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/tests/manifest-validation.test.ts`

## 검증 명령

- 별도 stage-local 실행 명령은 없다.
- capstone `v0` seed와 validation 테스트 포인터가 문서의 데이터 경계 설명과 일치하는지 확인한다.

## 현재 한계

- 실제 운영 registry sync는 범위 밖이다.
- 추천 로직 개선과 실험 비교는 아직 포함하지 않는다.
