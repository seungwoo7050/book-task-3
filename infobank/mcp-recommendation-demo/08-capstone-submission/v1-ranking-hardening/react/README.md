# v1 React 대시보드

이 디렉터리는 `v1-ranking-hardening`의 Next.js 대시보드다. `v0` 화면 위에 baseline/candidate 비교, usage feedback, experiment console을 추가해 운영형 추천 콘솔의 형태를 만든다.

## 현재 범위

- baseline/candidate recommendation 실행
- compare snapshot 표시
- usage totals와 피드백 입력
- experiment 생성과 목록 표시
- catalog 확장 엔트리 확인

## 자주 쓰는 명령

```bash
pnpm dev
pnpm build
pnpm start
pnpm test
```

기본 Web 포트는 `3001`이다.

## 현재 상태

- 구현 상태: 완료
- 검증 경로: `pnpm test`, 상위 버전 README의 `pnpm e2e`
- 핵심 컴포넌트: `components/mcp-dashboard.tsx`

## 아직 없는 것

- release candidate와 compatibility summary
- release gate와 artifact preview
- 로그인, 역할 구분, background job 상태

## 읽을 때 보면 좋은 파일

- `app/page.tsx`
- `components/mcp-dashboard.tsx`
- `components/mcp-dashboard.test.tsx`
- `app/globals.css`
