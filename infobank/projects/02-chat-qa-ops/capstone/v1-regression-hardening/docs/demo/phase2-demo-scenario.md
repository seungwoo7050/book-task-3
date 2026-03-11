# Phase 2 데모 시나리오

## 목적

개선 루프(가산점)가 동작함을 시연한다.

## 시나리오

1. baseline 결과 조회 (`v1.0`)
- Overview와 `version-compare`의 baseline 기준값 확인

2. 개선 반영 (`v1.1`)
- 프롬프트/규칙/KB 일부 보강 버전 가정

3. 동일 Golden Set 재평가

```bash
qualbot compare --baseline v1.0 --candidate v1.1
```

필요 시 assertion 포함 재실행:

```bash
curl -X POST http://localhost:8000/api/golden-set/run -H 'content-type: application/json' -d '{"prompt_version":"v1.1"}'
```

4. 결과 비교 제시
- `FORBIDDEN_PROMISE` 감소
- 평균 점수 상승
- CRITICAL 감소
- `pass_count` 증가, `assertion_failures` 감소

## 기대 결과

- baseline 대비 candidate 개선 수치가 명시됨
- 개선 항목이 failure type과 연결됨
- assertion 기준에서도 개선이 확인됨

## 시연 모드 A: UI 차이 있음

- `Overview`의 Compare Hook 출력 또는 별도 버전 비교 패널 활용
- baseline/candidate 점수와 delta를 화면에서 직접 비교

## 시연 모드 B: UI 차이 없음

UI가 동일해도 아래 내부 지표로 Phase2 차이를 증명한다.

- `/api/system/pipeline-stats`
- `/api/dashboard/version-compare`

필수 지표:
- `eval_total_ms`
- `judge_ms`
- `retrieval_hit_at_k`
- `critical_short_circuit_rate`
- `cache_hit_rate`
- `version_compare_job_ms`
