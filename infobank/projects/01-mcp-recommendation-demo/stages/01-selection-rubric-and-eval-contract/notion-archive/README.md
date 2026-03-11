> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Stage 01 — Selection Rubric & Eval Contract 노트 가이드

이 폴더는 mcp-recommendation-demo의 두 번째 stage인 **Selection Rubric & Eval Contract**의 설계 과정을 담고 있다.

## 문서 읽는 순서

| 순서 | 파일 | 내용 |
|------|------|------|
| 1 | [00-problem-framing.md](./00-problem-framing.md) | 추천 품질을 어떤 기준으로 판정할지 |
| 2 | [01-approach-log.md](./01-approach-log.md) | rubric 축 결정, offline eval contract 설계 |
| 3 | [02-debug-log.md](./02-debug-log.md) | eval 점수 계산, threshold 조정 문제 |
| 4 | [03-retrospective.md](./03-retrospective.md) | rubric 기반 평가의 효과와 한계 |
| 5 | [04-knowledge-index.md](./04-knowledge-index.md) | rubric, eval contract, threshold 개념 정리 |
| 6 | [05-development-timeline.md](./05-development-timeline.md) | contracts.ts schema, eval-service.ts, test 작성 순서 |

## 관련 stage

- **이전**: [00-source-brief](../../00-source-brief/notion/) — catalog와 eval fixture 정의
- **다음**: [02-registry-catalog](../../02-registry-catalog-and-manifest-schema/notion/) — rubric을 적용할 catalog와 manifest schema 확정
