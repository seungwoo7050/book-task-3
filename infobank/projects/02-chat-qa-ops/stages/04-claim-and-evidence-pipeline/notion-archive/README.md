> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# 04-claim-and-evidence-pipeline Notion 문서 안내

이 폴더는 **Claim & Evidence Pipeline** 단계의 개발 과정과 의사결정을 기록한 블로그형 에세이 모음입니다.

## 어떤 문서를 먼저 읽을까?

| 목적 | 문서 |
|------|------|
| 왜 claim 단위로 근거를 추적해야 하는지 알고 싶다 | [00-problem-framing.md](./00-problem-framing.md) |
| claim extraction과 verification을 왜 분리했는지 궁금하다 | [01-approach-log.md](./01-approach-log.md) |
| 근거 없는 claim이 사라지는 버그를 보고 싶다 | [02-debug-log.md](./02-debug-log.md) |
| 이 stage의 한계와 향후 방향을 알고 싶다 | [03-retrospective.md](./03-retrospective.md) |
| groundedness, retrieval trace 개념을 정리하고 싶다 | [04-knowledge-index.md](./04-knowledge-index.md) |
| 파일 생성과 CLI 순서를 따라가고 싶다 | [05-development-timeline.md](./05-development-timeline.md) |

## 이 문서들과 소스코드의 관계

소스코드(`pipeline.py`)는 claim extraction과 verification 로직을 보여줍니다.
이 문서들은 **왜 `not_found` verdict를 결과에서 제거하지 않는지**, **retrieval trace가 왜 필요한지** 등 소스코드에 담기지 않는 설계 이유를 설명합니다.

## 관련 stage

- **이전**: [03-rule-and-guardrail-engine](../../03-rule-and-guardrail-engine/notion/) — 안전 규칙 엔진
- **다음**: [05-judge-and-score-merge](../../05-judge-and-score-merge/notion/) — 판정과 점수 통합
