> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Stage 07 — Operator Dashboard & Experiment Console 노트 가이드

이 폴더는 mcp-recommendation-demo의 여덟 번째 stage인 **Operator Dashboard & Experiment Console**의 설계 과정을 담고 있다.

## 문서 읽는 순서

| 순서 | 파일 | 내용 |
|------|------|------|
| 1 | [00-problem-framing.md](./00-problem-framing.md) | 왜 운영 콘솔이 필요한지, 대시보드가 커버하는 범위 |
| 2 | [01-approach-log.md](./01-approach-log.md) | MCP 대시보드 구조, experiment 콘솔, release candidate 뷰 설계 |
| 3 | [02-debug-log.md](./02-debug-log.md) | CRUD 상태 관리, e2e 테스트 안정성 문제 |
| 4 | [03-retrospective.md](./03-retrospective.md) | 단일 대시보드 컴포넌트 접근의 장단점 |
| 5 | [04-knowledge-index.md](./04-knowledge-index.md) | 대시보드 섹션, API 연결, e2e 테스트 개념 정리 |
| 6 | [05-development-timeline.md](./05-development-timeline.md) | React 컴포넌트, Playwright 테스트, 스타일 작업 순서 |

## 관련 stage

- **이전**: [06-release-compatibility](../../06-release-compatibility-and-quality-gates/notion/) — gate 결과를 대시보드에서 표시
- **다음**: [08-capstone-submission](../../08-capstone-submission/notion/) — 대시보드를 포함한 전체 시스템 통합
