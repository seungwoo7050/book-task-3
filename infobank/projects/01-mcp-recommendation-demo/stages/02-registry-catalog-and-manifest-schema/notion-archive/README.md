> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Stage 02 — Registry Catalog & Manifest Schema 노트 가이드

이 폴더는 mcp-recommendation-demo의 세 번째 stage인 **Registry Catalog & Manifest Schema**의 설계 과정을 담고 있다.

## 문서 읽는 순서

| 순서 | 파일 | 내용 |
|------|------|------|
| 1 | [00-problem-framing.md](./00-problem-framing.md) | catalog과 manifest를 왜 단일 계약으로 고정해야 하는지 |
| 2 | [01-approach-log.md](./01-approach-log.md) | Zod manifest contract, seed catalog, manifest validation 설계 |
| 3 | [02-debug-log.md](./02-debug-log.md) | manifest validation 실패 케이스, seed 스크립트 문제 |
| 4 | [03-retrospective.md](./03-retrospective.md) | schema-first 접근의 장단점 |
| 5 | [04-knowledge-index.md](./04-knowledge-index.md) | manifest schema, catalog entry, seed, validation 개념 정리 |
| 6 | [05-development-timeline.md](./05-development-timeline.md) | contracts.ts, catalog.ts, seed.ts, test 작성 순서 |

## 관련 stage

- **이전**: [01-selection-rubric](../../01-selection-rubric-and-eval-contract/notion/) — eval contract의 대상이 되는 catalog
- **다음**: [03-differentiation-and-exposure](../../03-differentiation-and-exposure-design/notion/) — catalog에 한국어 노출 필드 설계
