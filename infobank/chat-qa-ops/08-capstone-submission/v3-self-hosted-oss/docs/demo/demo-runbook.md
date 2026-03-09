# Demo Runbook (10~12분 + Q&A 3분)

## 0:00 ~ 1:00 환경 확인

```bash
make backend-install
make init-db
make seed-demo
make preflight
export QUALBOT_EVAL_MODE=llm
export QUALBOT_RETRIEVAL_BACKEND=chroma
export QUALBOT_ENABLE_OLLAMA=1
export QUALBOT_ENABLE_CHROMA=1
export QUALBOT_OLLAMA_JUDGE_MODEL=<judge-model>
export QUALBOT_OLLAMA_CLAIM_MODEL=<claim-model>
export QUALBOT_OLLAMA_EVIDENCE_MODEL=<evidence-model>
make run-backend
# 별도 터미널
make frontend-install
make run-frontend
```

성공 기준:
- `GET /healthz` = `{"status":"ok"}`
- `GET /api/system/dependency-health`가 200
- 프론트 진입 가능

## 1:00 ~ 4:00 Phase1 핵심 시연

1. CLI 배치 평가

```bash
make evaluate-golden
```

2. Overview에서 평균 점수/실패율/CRITICAL 확인
3. Failures에서 Top 실패 유형 확인
4. Session Review에서 CRITICAL 세션 1건 상세 확인
5. CLI 리포트 출력

```bash
make report
```

6. assertion 요약 확인
- `pass_count`, `fail_count`, `assertion_failures`

성공 기준:
- 대시보드/CLI 결과 정합
- CRITICAL 탐지 근거 제시 가능

## 4:00 ~ 8:00 Phase2 훅 시연

1. 버전 비교 API 호출(또는 Overview Compare Hook)

```bash
qualbot compare --baseline v1.0 --candidate v1.1
```

2. 개선 수치 제시
- score delta
- forbidden promise 감소
- critical 감소

3. UI 차이가 작으면 내부 통계로 보강

```bash
curl http://localhost:8000/api/system/pipeline-stats
```

성공 기준:
- baseline 대비 candidate 개선 수치 제시
- 내부 지표 최소 3개 설명 가능

## 8:00 ~ 9:00 장애 명시 계약 확인

1. Ollama 또는 Chroma 비가동 상태 1회 시연
2. 평가 API `503 + DEPENDENCY_UNAVAILABLE` 확인
3. fallback 문서(`demo-fallbacks.md`) 기준으로 운영자 비상 전환 절차 설명

## 8:00 ~ 10:00 마무리

- "Phase1은 운영 필수, Phase2는 개선 루프"로 결론 정리
- 실패 유형 기반 개선 액션 제시

## 10:00 ~ 13:00 Q&A 스크립트

예상 질문 1: "UI 차이가 작은데 뭐가 달라졌나?"
- 답변: version compare 수치 + pipeline stats로 차이 증명

예상 질문 2: "왜 Rule->Evidence->Judge 순서인가?"
- 답변: Critical short-circuit로 비용 절감 + 판정 정확도 향상

예상 질문 3: "실패 원인을 어떻게 고치나?"
- 답변: failure taxonomy를 개선 대상(prompt/KB/retrieval/rule)로 매핑

예상 질문 4: "Ollama/Chroma가 죽으면 어떻게 되나?"
- 답변: v1.5는 조용한 대체 대신 `503 DEPENDENCY_UNAVAILABLE`를 명시해 운영자가 상태를 즉시 파악한다.
