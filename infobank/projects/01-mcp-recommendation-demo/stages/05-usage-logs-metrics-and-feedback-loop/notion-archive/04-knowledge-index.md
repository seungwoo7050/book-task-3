> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Usage Logs, Metrics & Feedback Loop — 지식 인덱스

## 핵심 개념

| 개념 | 설명 | 관련 파일 |
|------|------|-----------|
| usage event | 도구 선택/실행/해제 기록. toolId, action, recommendationId 포함 | `schema.ts → usageEvents` |
| feedback record | 도구 사용 후 만족도 (1~5점) + 코멘트 | `schema.ts → feedbackRecords` |
| experiment | A/B 테스트 메타데이터. selector type, status, 기간 | `schema.ts → experiments` |
| feedback loop | usage → feedback → reranker signal → 개선된 추천 → usage ... 순환 | 전체 파이프라인 |
| catalog CRUD | 대시보드에서 도구를 추가/수정/삭제하는 API | `catalog-repository.ts` |

## DB 테이블

| 테이블 | 주요 컬럼 | 관계 |
|--------|-----------|------|
| usage_events | tool_id, recommendation_id, experiment_id, action | → catalog |
| feedback_records | tool_id, usage_event_id, score, comment | → usage_events |
| experiments | id, name, selector_type, status | → usage_events |

## API 엔드포인트

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/api/usage-events` | POST | usage event 기록 |
| `/api/feedback` | POST | feedback 기록 |
| `/api/experiments` | GET/POST | 실험 목록/생성 |
| `/api/experiments/:id` | PATCH | 실험 상태 변경 |
| `/api/metrics/tool/:id` | GET | 도구별 요약 |

## 구현 위치

| 기능 | capstone 버전 | 파일 |
|------|--------------|------|
| DB schema | v1 | `node/src/db/schema.ts` |
| catalog CRUD | v1 | `node/src/repositories/catalog-repository.ts` |
| API routes | v1 | `node/src/app.ts` |
| dashboard CRUD UI | v1 | `react/components/mcp-dashboard.tsx` |

## 다음 단계 연결

- **stage 06**: usage 데이터가 release gate 판정 시 참고됨
- **stage 07**: 대시보드에서 experiment 관리 + metrics 시각화
