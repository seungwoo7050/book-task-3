# Phase1 vs Phase2 Diff Matrix

| 구분 축 | Phase 1 (필수) | Phase 2 (가산점) | 검증 방법 |
|---|---|---|---|
| 사용자 관점 (화면/동작) | Overview/Failures/SessionReview/EvalRunner 기본 운영 | 버전 비교 강조(또는 동일 UI 유지) | `/`, `/failures`, `/sessions`, compare 결과 |
| 품질 결과 관점 (점수/실패 유형) | 단일 버전 상태 품질 측정 + golden assertion pass/fail | baseline vs candidate 개선 수치 제시 | `/api/dashboard/version-compare`, `/api/golden-set/run` |
| 시스템 관점 (파이프라인/성능/처리) | Rule->Evidence->Judge->Scoring 단일 실행, dependency 실패 시 503 명시 | 개선 후 성능/정확도/캐시/short-circuit 차이 분석 | `/api/system/pipeline-stats` |

## 사용자 체감이 유사할 때 허용되는 내부 차이 지표

- `eval_total_ms`
- `judge_ms`
- `retrieval_hit_at_k`
- `critical_short_circuit_rate`
- `cache_hit_rate`
- `version_compare_job_ms`
- `dependency_fail_count`
- `retrieval_backend`
- `judge_model`, `claim_model`, `evidence_model`

## 최소 합격 기준

1. Phase1: 필수 파이프라인과 모니터링이 동작한다.
2. Phase2: 동일 golden set에서 baseline 대비 candidate 개선 근거가 수치로 제시된다.
3. UI 변화가 없더라도 내부 지표 차이로 Phase2 추가 가치를 증명한다.
