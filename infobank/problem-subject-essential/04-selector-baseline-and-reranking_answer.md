# 04-selector-baseline-and-reranking 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 추천 로직이 단계적으로 진화했다는 점을 버전별로 설명할 수 있다, 학생이 baseline과 candidate를 분리해 개선 증빙 구조를 만들 수 있다, compare 결과가 다음 stage의 로그/지표 설계와 자연스럽게 이어진다를 한 흐름으로 설명하고 검증한다. 핵심은 `tokenize`와 `unique`, `getKeywords` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 추천 로직이 단계적으로 진화했다는 점을 버전별로 설명할 수 있다.
- 학생이 baseline과 candidate를 분리해 개선 증빙 구조를 만들 수 있다.
- compare 결과가 다음 stage의 로그/지표 설계와 자연스럽게 이어진다.
- 첫 진입점은 `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/src/services/recommendation-service.ts`이고, 여기서 `tokenize`와 `unique` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/src/services/recommendation-service.ts`: `tokenize`, `unique`, `getKeywords`, `calculateIntentScore`가 핵심 흐름과 상태 전이를 묶는다.
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/services/compare-service.ts`: `dcg`, `ndcgAt3`, `runCompare`가 핵심 흐름과 상태 전이를 묶는다.
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/services/rerank-service.ts`: `aggregateSignals`, `rerankCatalog`가 핵심 흐름과 상태 전이를 묶는다.
- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/tests/manifest-validation.test.ts`: `manifest validation`, `rejects incomplete manifests`가 통과 조건과 회귀 포인트를 잠근다.
- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/tests/recommendation-service.test.ts`: `recommendation service`, `prioritizes release MCPs for release queries`, `keeps explanation within capability, differentiation, compatibility axes`가 통과 조건과 회귀 포인트를 잠근다.
- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/tests/routes.integration.test.ts`: `route contracts`, `returns seeded catalog and evaluation summary when DB is prepared`가 통과 조건과 회귀 포인트를 잠근다.
- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/package.json`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/package.json`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.

## 정답을 재구성하는 절차

1. `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/src/services/recommendation-service.ts`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `manifest validation` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node && npm test -- tests/manifest-validation.test.ts tests/recommendation-service.test.ts`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node && npm test -- tests/manifest-validation.test.ts tests/recommendation-service.test.ts
```

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node && npm test -- tests/manifest-validation.test.ts tests/recommendation-service.test.ts tests/rerank-service.test.ts
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `manifest validation`와 `rejects incomplete manifests`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node && npm test -- tests/manifest-validation.test.ts tests/recommendation-service.test.ts`로 회귀를 조기에 잡는다.

## 소스 근거

- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/src/services/recommendation-service.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/services/compare-service.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/services/rerank-service.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/tests/manifest-validation.test.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/tests/recommendation-service.test.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/tests/routes.integration.test.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/package.json`
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/package.json`
