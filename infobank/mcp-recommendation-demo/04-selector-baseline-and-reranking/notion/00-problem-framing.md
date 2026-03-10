# 04 baseline selector와 reranking 문제 정의

## 이 stage가 맡는 문제

baseline selector를 먼저 세우고 reranker와 compare runner를 더해 추천 로직 개선을 설명 가능한 형태로 만드는 단계다.

## 현재 기준 성공 조건

- 추천 로직이 단계적으로 진화했다는 점을 버전별로 설명할 수 있다.
- 학생이 baseline과 candidate를 분리해 개선 증빙 구조를 만들 수 있다.
- compare 결과가 다음 stage의 로그/지표 설계와 자연스럽게 이어진다.

## 먼저 알고 있으면 좋은 것

- 상위 `README.md`, `problem/README.md`, `docs/README.md`를 먼저 읽어 stage 목적을 고정한다.
- 실제 구현 확인은 `v1-ranking-hardening` 기준으로 내려가야 한다.
- 이 단계는 '더 똑똑한 추천'을 만들었다는 주장보다, 왜 그렇게 판단할 수 있는지의 근거를 정리한다.

## 확인할 증거

- `08-capstone-submission/v0-initial-demo/node/src/services/recommendation-service.ts`
- `08-capstone-submission/v1-ranking-hardening/node/src/services/rerank-service.ts`
- `08-capstone-submission/v1-ranking-hardening/node/src/services/compare-service.ts`
- `08-capstone-submission/v1-ranking-hardening/node/tests/rerank-service.test.ts`

## 아직 남아 있는 불확실성

- 이 단계는 '더 똑똑한 추천'을 만들었다는 주장보다, 왜 그렇게 판단할 수 있는지의 근거를 정리한다.
