# 04 baseline selector와 reranking 문제 정의

## 문제 해석

baseline selector를 먼저 세우고 reranker와 compare runner를 더해 추천 로직 개선을 설명 가능한 형태로 만드는 단계다.

## 입력

- 루트 `README.md`와 `../../docs/`에 정리된 트랙 해석
- 아래 capstone 연결 경로에 있는 실제 구현과 증빙 파일

## 기대 산출물

- weighted baseline
- signal-based reranker
- compare runner

## 완료 기준

- 추천 로직이 단계적으로 진화했다는 점을 버전별로 설명할 수 있다.
- 학생이 baseline과 candidate를 분리해 개선 증빙 구조를 만들 수 있다.
- compare 결과가 다음 stage의 로그/지표 설계와 자연스럽게 이어진다.

## capstone 연결 증거

- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/src/services/recommendation-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/services/rerank-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/services/compare-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/tests/rerank-service.test.ts`

## 범위 메모

- 이 단계는 '더 똑똑한 추천'을 만들었다는 주장보다, 왜 그렇게 판단할 수 있는지의 근거를 정리한다.
