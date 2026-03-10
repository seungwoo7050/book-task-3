# Phase 1 데모 시나리오 (v1.6, KR)

## 목적

필수 범위(품질 정의 + 자동평가 + 가시화)가 완성되었음을 시연한다.
실사용자 입력 기반 전체 시나리오는 `phase1-e2e-user-scenarios-ko.md`(v1.6 기준)를 따른다.

## 준비물

1. 백엔드 실행: `make run-backend`
2. 프론트 실행: `make run-frontend`
3. 시드 데이터: `make init-db && make seed-demo`
4. Golden Set: 30건(`backend/golden_set/phase1_seed.yaml`)
5. 실연동 모드 환경 변수:
   - `QUALBOT_EVAL_MODE=llm`
   - `QUALBOT_RETRIEVAL_BACKEND=chroma`
   - `QUALBOT_ENABLE_OLLAMA=1`
   - `QUALBOT_ENABLE_CHROMA=1`
   - `QUALBOT_OLLAMA_JUDGE_MODEL`, `QUALBOT_OLLAMA_CLAIM_MODEL`, `QUALBOT_OLLAMA_EVIDENCE_MODEL`
6. 사전 점검: `make preflight`

## 실행 순서

1. CLI 배치평가 실행

```bash
make evaluate-golden
```

2. 대시보드 개요 확인 (`/`)
- 평균 점수
- 실패율
- CRITICAL 건수
- Failure Top
 - dependency 상태(`dependency_fail_count`)

3. 실패 분석 페이지 확인 (`/failures`)
- `FORBIDDEN_PROMISE`, `PII_EXPOSURE`, `MISSING_MANDATORY_STEP` 집계 확인

4. 세션 리뷰 페이지 확인 (`/sessions`)
- 대화 원문
- 턴별 grade/score/failure types
- CRITICAL 샘플 1건 열람

5. CLI 리포트 출력

```bash
make report
```

6. Golden assertion 결과 확인
- `pass_count`, `fail_count`, `assertion_failures` 확인
- 실패 케이스에서 `reason_codes` 확인

## 기대 결과

- 평균 점수, 등급 분포, 실패 Top 유형 표시
- CRITICAL 케이스 1건 이상 확인
- CLI 리포트와 대시보드 집계가 정합
- Golden assertion에서 케이스별 pass/fail이 구조화되어 반환
- 캡처 증빙: `docs/demo/scenario-artifacts/*.png`

## 발표 멘트 키포인트

- "이 실패는 고객 피해 가능성이 있어 CRITICAL로 즉시 분류됩니다."
- "이 건은 `forbid-discount-promise` 규칙이 탐지해 자동 차단합니다."
- "점수보다 실패 유형 분해가 실제 개선 포인트를 제공합니다."
- "v1.6에서는 strict 모드에서 자동 fallback 없이 503으로 명시합니다."
