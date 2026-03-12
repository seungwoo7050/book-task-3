# 문제 정의

프로비넌스: `authored`

## 문제

`Ops Triage Console`은 여러 채널에서 들어오는 이슈를 한 명의 운영자가 빠르게 정리하고 우선순위를 지정하며 적절한 팀으로 라우팅하는 콘솔이다. 이 문제의 핵심은 data-heavy queue에서도 읽기 흐름, bulk 작업, failure recovery가 무너지지 않게 만드는 것이다.

## 제공 자산

- 이 문서: 제품 정의와 품질 목표
- `data/`: 별도 외부 fixture 없이 프로젝트 내부 mock data를 쓰기 위한 placeholder
- `script/`: 공통 디렉터리 shape를 유지하기 위한 placeholder

## 제약

- 실제 인증, 실제 DB, 실제 백엔드 API 없이 완결된 데모여야 한다.
- 단일 운영자 시나리오를 기준으로 한다.
- 실패 시 retry와 undo가 가능해야 하며, keyboard-only 주요 흐름도 지원해야 한다.

## 포함 범위

- dashboard summary
- searchable triage queue
- faceted filters
- saved views
- bulk actions
- issue detail panel
- operator note
- demo reset
- chaos/failure simulation

## 제외 범위

- 실제 인증
- 실제 DB
- 멀티유저 실시간 협업
- 실제 백엔드 API

## 요구 산출물

- `next/`에 실행 가능한 운영 콘솔 구현
- 제품 판단과 UX 흐름을 설명하는 공개 문서와 발표 자료
- `typecheck`, unit, integration, E2E를 포함한 검증 체계

## Canonical Verification

```bash
cd study
npm run verify --workspace @front-react/ops-triage-console
```

- `typecheck`: Next.js 앱 타입 검사
- `vitest`: query/filter/sort, optimistic update, integration 흐름 확인
- `playwright`: dashboard, queue, detail, retry, keyboard flow 확인
