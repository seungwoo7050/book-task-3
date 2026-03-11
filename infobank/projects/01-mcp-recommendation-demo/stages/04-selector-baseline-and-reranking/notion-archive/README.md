> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Stage 04 — Selector Baseline & Reranking 노트 가이드

이 폴더는 mcp-recommendation-demo의 다섯 번째 stage인 **Selector Baseline & Reranking**의 설계 과정을 담고 있다.

## 문서 읽는 순서

| 순서 | 파일 | 내용 |
|------|------|------|
| 1 | [00-problem-framing.md](./00-problem-framing.md) | 왜 baseline selector와 reranker를 분리하는지 |
| 2 | [01-approach-log.md](./01-approach-log.md) | weighted baseline 구현, signal-based reranker 설계, compare runner |
| 3 | [02-debug-log.md](./02-debug-log.md) | 가중치 튜닝, reranker 신호 중복, compare 결과 해석 문제 |
| 4 | [03-retrospective.md](./03-retrospective.md) | baseline → reranker 전환의 효과 |
| 5 | [04-knowledge-index.md](./04-knowledge-index.md) | selector, reranker, compare, signal 개념 정리 |
| 6 | [05-development-timeline.md](./05-development-timeline.md) | recommendation-service, rerank-service, compare-service 구현 순서 |

## 관련 stage

- **이전**: [03-differentiation-and-exposure](../../03-differentiation-and-exposure-design/notion/) — 추천 결과에 포함할 노출 정보
- **다음**: [05-usage-logs](../../05-usage-logs-metrics-and-feedback-loop/notion/) — 추천 결과의 사용 로그와 피드백
