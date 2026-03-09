# 04 Selector Baseline And Reranking

## Purpose

baseline selector와 signal-based reranker를 단계적으로 구현한다.

## Capstone Connection

- `08-capstone-submission/v0-initial-demo/node/src/services/recommendation-service.ts`
- `08-capstone-submission/v1-ranking-hardening/node/src/services/rerank-service.ts`
- `08-capstone-submission/v1-ranking-hardening/node/src/services/compare-service.ts`

## Main Outputs

- weighted baseline
- reranker
- compare runner

## Implementation Pointers

- `08-capstone-submission/v1-ranking-hardening/node/tests/rerank-service.test.ts`

## Status

- implemented across v0 and v1; v2 reuses the same compare core
