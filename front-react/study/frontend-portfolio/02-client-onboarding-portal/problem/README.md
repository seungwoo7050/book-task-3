# Product Brief

프로비넌스: `authored`

## 제품 정의

`Client Onboarding Portal`은 SaaS 고객이 첫 로그인 이후 workspace profile을 채우고, 팀원을 초대하고, 최종 제출까지 마치는 onboarding 앱이다.

## 핵심 화면

- sign-in / session gate
- onboarding wizard
- workspace profile/settings
- member invite
- review and submit

## 서비스 경계

- `getSession()`
- `signIn(credentials)`
- `signOut()`
- `getWorkspaceProfile()`
- `saveWorkspaceProfile(patch)`
- `listInvites()`
- `createInvite(input)`
- `listChecklistItems()`
- `completeChecklistItem(id)`
- `submitOnboarding()`

## 품질 목표

- field validation
- draft save
- route guard
- loading/pending/success/failure states
- server-like error handling
