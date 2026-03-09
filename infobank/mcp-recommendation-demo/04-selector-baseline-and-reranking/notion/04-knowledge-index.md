# Selector Baseline & Reranking — 지식 인덱스

## 핵심 개념

| 개념 | 설명 | 관련 파일 |
|------|------|-----------|
| baseline selector | 키워드 매칭 + 정적 가중치 기반 추천. v0에서 동작 | `recommendation-service.ts` |
| reranker | baseline 결과를 추가 signal로 재정렬하는 모듈. v1에서 추가 | `rerank-service.ts` |
| signal | reranker가 사용하는 추가 정보: usage_count, avg_feedback, days_since_update, compat_score | `rerank-service.ts` |
| compare runner | baseline과 reranker 결과를 같은 eval case로 비교하는 도구 | `compare-service.ts` |
| min-max 정규화 | signal 값을 0~1 범위로 변환. `(value - min) / (max - min)` | `rerank-service.ts` |
| score composition | `finalScore = baselineScore * 0.6 + signals * 0.4` | `rerank-service.ts` |

## 구현 위치

| 기능 | capstone 버전 | 파일 |
|------|--------------|------|
| baseline selector | v0 | `node/src/services/recommendation-service.ts` |
| reranker | v1 | `node/src/services/rerank-service.ts` |
| compare service | v1 | `node/src/services/compare-service.ts` |
| reranker test | v1 | `node/tests/rerank-service.test.ts` |

## 다음 단계 연결

- **stage 05**: usage event와 feedback을 DB에 기록 → reranker signal의 실제 데이터
- **stage 06**: reranker + compatibility signal → compatibility gate
