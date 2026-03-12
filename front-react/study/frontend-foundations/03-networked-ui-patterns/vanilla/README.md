# Vanilla 구현

상태: `verified`

## 이 구현이 답하는 범위

- mock directory service
- loading, empty, error, retry
- abort and stale request protection
- query-param navigation and detail selection

## 핵심 파일

- `src/service.ts`: latency, failure, abort simulation
- `src/state.ts`: URL state와 request token helper
- `src/app.ts`: list/detail 분리 로딩과 stale response 무시

## 실행과 검증

```bash
cd study
npm run build --workspace @front-react/networked-ui-patterns
npm run verify --workspace @front-react/networked-ui-patterns
```

## 현재 한계

- 실제 서버 캐시나 인증은 없다.
- detail failure와 list failure의 backoff 정책은 최소 범위로만 다룬다.
- keyboard flow는 smoke 수준으로 유지한다.
