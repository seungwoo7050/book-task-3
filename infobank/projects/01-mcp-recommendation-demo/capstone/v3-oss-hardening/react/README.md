# v3 React 운영 콘솔

이 디렉터리는 `v3-oss-hardening`의 Next.js 운영 콘솔이다. `v2`의 제출 대시보드를 self-hosted 콘솔로 확장해 로그인, 역할 구분, job activity, audit log, artifact preview까지 보여 준다.

## 현재 범위

- 로그인 화면과 세션 기반 진입
- role-aware recommendation / compare / gate 화면
- experiment, release candidate, catalog 운영 UI
- job activity와 audit log 표시
- latest artifact preview와 운영 요약 카드

## 자주 쓰는 명령

```bash
pnpm dev
pnpm build
pnpm start
pnpm test
```

기본 Web 포트는 `3003`이다.

## 현재 상태

- 구현 상태: 완료
- 검증 경로: `pnpm test`, 상위 버전 README의 `pnpm e2e`
- 핵심 컴포넌트: `components/mcp-dashboard.tsx`

## 범위 밖

- multi-workspace UI
- SSO/OAuth 연동 화면
- 외부 조직 관리와 billing 화면

## 읽을 때 보면 좋은 파일

- `app/page.tsx`
- `components/mcp-dashboard.tsx`
- `components/mcp-dashboard.test.tsx`
- `app/globals.css`
