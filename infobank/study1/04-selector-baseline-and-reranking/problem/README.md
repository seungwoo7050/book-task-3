# 04 Selector Baseline And Reranking Problem

## Inputs

- reference docs and track-level requirements under `study1/`
- deterministic MCP catalog and eval fixtures from the capstone workspace

## Outputs

- weighted baseline
- reranker
- compare runner

## Acceptance Criteria

- tracked documents explain the scope without relying on private notes
- the capstone file mapping is explicit
- implementation claims point to runnable code or tests

## Implemented In Capstone

- `08-capstone-submission/v0-initial-demo/node/src/services/recommendation-service.ts`
- `08-capstone-submission/v1-ranking-hardening/node/src/services/rerank-service.ts`
- `08-capstone-submission/v1-ranking-hardening/node/src/services/compare-service.ts`
- `08-capstone-submission/v1-ranking-hardening/node/tests/rerank-service.test.ts`
