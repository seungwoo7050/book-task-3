# 07 운영자 대시보드와 실험 콘솔 디버그 기록

## 먼저 확인할 명령

```bash
pnpm install
cp .env.example .env
pnpm db:up
pnpm migrate
pnpm seed
pnpm eval
pnpm compatibility rc-release-check-bot-1-5-0
pnpm release:gate rc-release-check-bot-1-5-0
pnpm artifact:export rc-release-check-bot-1-5-0
pnpm capture:presentation
pnpm test
pnpm e2e
```

## 다시 막히기 쉬운 지점

- 상위 `README.md`, `problem/README.md`, `docs/README.md`, 연결된 capstone 경로 설명이 서로 어긋나지 않는지 먼저 확인한다.
- `v2-submission-polish`가 아니라 다른 버전의 코드를 보고 있으면 stage 목적이 흐려질 수 있다.
- 이 단계는 UI 컴포넌트 목록보다, 운영자가 무엇을 보고 어떤 결정을 내리는지에 초점을 둔다.

## 현재 상태 메모

- 운영 콘솔은 `v1`에서 시작해 `v2`에서 제출용 시연 화면으로 정리된다.
- 이 stage는 추천 품질 실험과 운영 작업을 한 화면 구조로 묶는 이유를 설명한다.

## 재현 실패 시 다시 볼 경로

- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/components/mcp-dashboard.tsx`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/react/components/mcp-dashboard.tsx`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/tests/e2e/recommendation.spec.ts`
