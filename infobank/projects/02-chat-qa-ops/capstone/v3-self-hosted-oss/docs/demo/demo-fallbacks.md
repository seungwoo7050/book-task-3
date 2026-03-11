# 데모 fallback 안내

## 1) Ollama/Chroma 장애 시

증상:
- LLM 응답 지연/실패
- 근거 검증 응답 없음

대응:
1. `qualbot preflight`로 strict 의존성 상태를 먼저 확인
2. 기본 모드에서는 API가 `503 DEPENDENCY_UNAVAILABLE`를 반환하는지 확인
3. `GET /api/system/dependency-health`로 실패 component를 확인
4. 운영자가 명시적으로 비상 전환:
   - `QUALBOT_EVAL_MODE=heuristic`
   - `QUALBOT_RETRIEVAL_BACKEND=keyword`
   - `QUALBOT_ENABLE_OLLAMA=0`
   - `QUALBOT_ENABLE_CHROMA=0`
5. 동일 시나리오를 비상 모드로 재시연

주의:
- strict 모드에서는 자동 fallback이 동작하지 않는다.

## 2) 시간 부족 시 5분 축약 경로

1. `make evaluate-golden`
2. Overview 숫자 설명
3. Failures Top 3만 설명
4. `qualbot compare --baseline v1.0 --candidate v1.1`
5. 내부 지표 2개(`critical_short_circuit_rate`, `cache_hit_rate`)만 제시

## 3) 네트워크/성능 이슈 시

1. 사전 캡처 JSON 사용
- `/api/dashboard/overview` 결과 저장본
- `/api/dashboard/version-compare` 결과 저장본

2. 발표 중에는 저장본을 근거로 설명하고,
3. 질의응답에서 로컬 재실행 가능 경로를 안내

## 4) 실패 판정 기준

다음 조건이면 즉시 fallback 전환:
- API 호출 2회 연속 타임아웃
- Ollama 응답 30초 초과
- `503 DEPENDENCY_UNAVAILABLE`가 2회 연속 발생
- 프론트 빌드/로딩 실패

전환 후 목표:
- 시연 메시지의 핵심(Phase1 vs Phase2 차이)을 유지한 채 5분 내 완료
