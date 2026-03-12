# 문제 정의

프로비넌스: `authored`

## 문제

`Client Onboarding Portal`은 SaaS 고객이 첫 로그인 이후 workspace profile을 채우고, 팀원을 초대하고, 최종 제출까지 마치는 onboarding 앱이다. 이 문제의 핵심은 session gate, validation, draft restore, retry를 포함한 multi-step flow를 자연스럽게 연결하는 것이다.

## 제공 자산

- 이 문서: 제품 정의와 서비스 경계
- `data/`: 별도 외부 fixture 없이 프로젝트 내부 mock data를 쓰기 위한 placeholder
- `script/`: 공통 디렉터리 shape를 유지하기 위한 placeholder

## 제약

- 실제 auth backend, server database, email delivery 없이 완결된 데모여야 한다.
- route guard와 validation 실패 상태가 화면 흐름으로 드러나야 한다.
- draft restore와 submit retry가 검증 가능한 시나리오여야 한다.

## 포함 범위

- sign-in / session gate
- onboarding wizard
- workspace profile/settings
- member invite
- review and submit
- draft save and restore
- submit failure and retry

## 제외 범위

- 실제 auth backend
- 실제 DB와 email delivery
- organization admin 전반
- 멀티유저 협업

## 요구 산출물

- `next/`에 실행 가능한 onboarding 포털 구현
- route와 validation 흐름을 설명하는 공개 문서와 발표 자료
- `typecheck`, unit, integration, E2E를 포함한 검증 체계

## Canonical Verification

```bash
cd study
npm run verify --workspace @front-react/client-onboarding-portal
```

- `typecheck`: Next.js 앱 타입 검사
- `vitest`: schema validation, storage, route guard, integration 흐름 확인
- `playwright`: sign-in, validation, draft restore, retry, success 흐름 확인
