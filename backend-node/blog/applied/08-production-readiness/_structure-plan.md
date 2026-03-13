# 08-production-readiness structure plan

이 문서는 운영성 항목 체크리스트처럼 보이지 않게 해야 한다. 읽는 축은 `runtime config -> liveness/readiness -> structured logging`으로 잡고, 왜 이 순서가 필요한지 보여 주는 쪽이 좋다.

## 읽기 구조

1. env parsing이 왜 health endpoint보다 먼저 나오는지 설명한다.
2. `/health`와 `/ready`가 다른 질문에 답한다는 점을 분명히 한다.
3. request id 기반 structured logging으로 글을 닫는다.

## 반드시 남길 근거

- `loadRuntimeConfig`
- `RuntimeConfigService`
- `HealthController`
- `StructuredLoggingInterceptor`
- unit/e2e 테스트
- `build && test && test:e2e`

## 리라이트 톤

- 운영성 체크리스트 나열처럼 쓰지 않는다.
- "이 서비스가 언제 살아 있고 언제 준비됐다고 말할 수 있는가"라는 질문이 먼저 보이게 쓴다.
