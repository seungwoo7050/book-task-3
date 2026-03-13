# A-auth-lab structure outline

## 글 목표

- 로컬 계정 인증을 로그인 API가 아니라 lifecycle 전체로 복원한다.
- macOS + VSCode 통합 터미널에서 바로 따라갈 수 있는 흐름으로 정리한다.

## 글 순서

1. baseline auth 범위를 먼저 자른 단계
2. refresh rotation과 CSRF 경계를 코드로 고정한 단계
3. 문서와 검증 기록으로 현재 범위를 닫은 단계

## 반드시 넣을 코드 앵커

- `AuthFlowApiTest.registerLoginAndRefreshFlowWorks()`
- `AuthDemoService.refresh()`
- `AuthDemoService.requireSession()`

## 반드시 넣을 CLI

```bash
cd spring
make test
make smoke
docker compose up --build
```

## 핵심 개념

- refresh rotation은 단순 재발급이 아니라 세션 재생산 규칙이다.
- CSRF token이 있어야 cookie 기반 인증 경계를 설명할 수 있다.
