# 03 Networked UI Patterns

상태: `verified`

## 무슨 문제인가

비동기 UI의 핵심 문제는 데이터를 불러오는 것 자체보다 loading, empty, error, retry, abort, navigation state가 한 화면에서 어떻게 엮이는가에 있다. 이 프로젝트는 directory/explorer UI를 통해 request lifecycle을 제품처럼 다루는 문제를 푼다.

## 왜 필요한가

프론트 업무의 많은 문제는 순수 렌더링보다 네트워크와 비동기 상태에서 생긴다. 이 단계는 실제 서버 없이도 서버처럼 보이는 UX를 설계하고 설명하는 능력을 만드는 마지막 vanilla 단계다.

## 내가 만든 답

mock API latency, request race 보호, loading/error/empty state, query-param driven navigation을 갖춘 explorer 앱을 `vanilla/`로 구현했다.

- 문제 정의: [problem/README.md](problem/README.md)
- 구현 상세: [vanilla/README.md](vanilla/README.md)
- 공개 문서: [docs/README.md](docs/README.md)

## 핵심 구현 포인트

- `vanilla/src/service.ts`에서 latency, failure, abort를 시뮬레이션한다.
- `vanilla/src/state.ts`에서 URL state와 race-aware request token helper를 제공한다.
- `vanilla/src/app.ts`에서 list/detail 요청을 분리하고 stale response를 무시한다.

## 검증

```bash
cd study
npm run dev --workspace @front-react/networked-ui-patterns
npm run verify --workspace @front-react/networked-ui-patterns
```

- 검증 기준일: 2026-03-08
- `vitest`: service, state, explorer logic `4`개 테스트 통과
- `playwright`: retry와 query-driven navigation `2`개 시나리오 통과

## 읽기 순서

1. [problem/README.md](problem/README.md)
2. [vanilla/README.md](vanilla/README.md)
3. [docs/README.md](docs/README.md)

## 한계

- 실제 서버 캐시, 인증, SSR은 다루지 않는다.
- keyboard flow는 smoke 수준으로만 유지한다.
- 다음 단계는 `react-internals` 트랙에서 컴포넌트 추상화와 rendering model을 직접 구현하는 것이다.
