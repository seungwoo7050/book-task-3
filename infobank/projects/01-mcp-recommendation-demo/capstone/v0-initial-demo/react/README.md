# v0 React 대시보드

이 디렉터리는 `v0-initial-demo`의 Next.js 대시보드다. catalog 샘플, baseline recommendation 결과, offline eval 요약을 한 화면에서 빠르게 보여 준다.

## 현재 범위

- seeded catalog 목록과 상세 표시
- recommendation 실행과 결과 카드
- 한국어 explanation panel
- offline eval 결과 요약

## 자주 쓰는 명령

```bash
pnpm dev
pnpm build
pnpm start
pnpm test
```

기본 Web 포트는 `3000`이다.

## 현재 상태

- 구현 상태: 완료
- 검증 경로: `pnpm test`, 상위 버전 README의 `pnpm e2e`
- 연동 패키지: `@study1-v0/shared`

## 아직 없는 것

- baseline/candidate compare 화면
- feedback loop와 experiment console
- release gate와 artifact preview
- 로그인, 권한, background jobs

## 읽을 때 보면 좋은 파일

- `app/page.tsx`
- `components/mcp-dashboard.tsx`
- `components/mcp-dashboard.test.tsx`
- `app/globals.css`
