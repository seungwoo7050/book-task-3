# v2 React 대시보드

이 디렉터리는 `v2-submission-polish`의 Next.js 대시보드다. `v1`의 compare/feedback/experiment 화면 위에 release candidate, compatibility, release gate, artifact preview를 추가해 제출 시연 화면을 완성한다.

## 현재 범위

- recommendation과 compare snapshot
- feedback loop와 experiment console
- release candidate CRUD
- compatibility summary와 release gate 결과
- submission artifact preview

## 자주 쓰는 명령

```bash
pnpm dev
pnpm build
pnpm start
pnpm test
```

기본 Web 포트는 `3002`이다.

## 현재 상태

- 구현 상태: 완료
- 검증 경로: `pnpm test`, 상위 버전 README의 `pnpm e2e`
- 핵심 컴포넌트: `components/mcp-dashboard.tsx`

## 아직 없는 것

- 로그인, 역할별 UI 분기
- background job activity와 audit log
- self-hosted 운영용 설치 화면

## 읽을 때 보면 좋은 파일

- `app/page.tsx`
- `components/mcp-dashboard.tsx`
- `components/mcp-dashboard.test.tsx`
- `app/globals.css`
