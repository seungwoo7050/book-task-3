# Usage Logs, Metrics & Feedback Loop — 디버그 기록

## usage event 중복 기록 문제

### 상황

프론트엔드에서 "도구 선택" 버튼을 빠르게 두 번 클릭하면
같은 usage event가 두 번 기록되었다.

### 해결

프론트엔드에서 debounce를 적용하고,
백엔드에서도 같은 toolId + recommendationId + action 조합이
최근 1초 이내에 있으면 무시하는 중복 방지 로직을 추가했다.

## feedback score 범위 검증

### 상황

UI에서 1~5점만 선택할 수 있지만,
API를 직접 호출하면 0이나 100 같은 값을 보낼 수 있다.

### 해결

Zod schema에서 범위 검증을 추가:

```typescript
score: z.number().int().min(1).max(5)
```

Fastify의 route handler에서 Zod parse를 먼저 실행하고,
유효하지 않으면 400을 반환한다.

## experiment 상태 전이 제어

### 상황

completed 상태의 experiment를 다시 running으로 변경하는 API 호출이 가능했다.

### 해결

허용되는 상태 전이를 명시적으로 정의:
- draft → running: 허용
- running → completed: 허용
- completed → anything: 거부 (400)
- draft → completed: 거부 (running을 거쳐야 함)
