# Vanilla Implementation

상태: `verified`

## problem scope covered

- mock directory service
- loading, empty, error, retry
- abort and stale request protection
- query-param navigation and detail selection

## build command

```bash
cd study
npm run build --workspace @front-react/networked-ui-patterns
```

## test command

```bash
cd study
npm run verify --workspace @front-react/networked-ui-patterns
```

## current status

- `verified`

## known gaps

- 실제 서버 캐시나 인증은 없다.
- detail failure와 list failure의 backoff 정책은 최소 범위로만 다룬다.
- keyboard flow는 smoke 수준으로 유지한다.

## implementation notes

- `vanilla/src/service.ts`가 latency, failure, abort를 시뮬레이션한다.
- `vanilla/src/state.ts`는 URL state와 race-aware request token helper를 제공한다.
- `vanilla/src/app.ts`는 list/detail을 분리 로딩하고 stale response를 무시한다.
