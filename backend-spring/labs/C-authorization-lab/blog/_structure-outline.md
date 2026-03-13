# C-authorization-lab structure outline

## 글 목표

- authorization을 membership lifecycle 중심 문제로 복원한다.
- macOS + VSCode 통합 터미널에서 재현 가능한 검증 흐름을 남긴다.

## 글 순서

1. invite와 role change 시나리오를 먼저 고정한 단계
2. owner, pending, member 전이를 서비스 코드에 둔 단계
3. method security를 미룬 이유를 닫는 단계

## 반드시 넣을 코드 앵커

- `AuthorizationApiTest.inviteAcceptAndRoleChangeFlowWork()`
- `AuthorizationDemoService.invite()`
- `AuthorizationDemoService.accept()`

## 반드시 넣을 CLI

```bash
cd spring
make test
make smoke
docker compose up --build
```

## 핵심 개념

- authorization의 중심은 role 이름보다 membership lifecycle이다.
- service logic으로 먼저 규칙을 고정해야 다음 단계가 선명해진다.
