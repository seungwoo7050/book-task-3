> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Stage 05 — Usage Logs, Metrics & Feedback Loop 노트 가이드

이 폴더는 mcp-recommendation-demo의 여섯 번째 stage인 **Usage Logs, Metrics & Feedback Loop**의 설계 과정을 담고 있다.

## 문서 읽는 순서

| 순서 | 파일 | 내용 |
|------|------|------|
| 1 | [00-problem-framing.md](./00-problem-framing.md) | 왜 usage event와 feedback을 기록해야 하는지 |
| 2 | [01-approach-log.md](./01-approach-log.md) | DB 테이블 설계, API 구현, experiment 메타데이터 |
| 3 | [02-debug-log.md](./02-debug-log.md) | event 중복, feedback 유효성 검증, experiment 상태 관리 |
| 4 | [03-retrospective.md](./03-retrospective.md) | feedback loop의 효과와 한계 |
| 5 | [04-knowledge-index.md](./04-knowledge-index.md) | usage event, feedback, experiment, metrics 개념 정리 |
| 6 | [05-development-timeline.md](./05-development-timeline.md) | DB schema, API route, test 작성 순서 |

## 관련 stage

- **이전**: [04-selector-baseline](../../04-selector-baseline-and-reranking/notion/) — reranker의 signal 데이터를 기록하는 것이 이 stage
- **다음**: [06-release-compatibility](../../06-release-compatibility-and-quality-gates/notion/) — usage 데이터가 release gate 판정에 사용
