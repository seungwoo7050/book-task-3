# 05-auth-and-authorization structure plan

## 중심 질문

- request pipeline 위에 JWT와 RBAC를 어디에 끼워 넣었는가
- Express middleware chain과 Nest guard chain은 어떻게 대응되는가
- `401`과 `403` 경계가 왜 이 프로젝트의 핵심 개념인가

## 10-development-timeline.md

- 오프닝: auth 프로젝트의 주제가 "로그인 기능 추가"가 아니라 "보호 경로의 경계 재정의"라는 점을 먼저 세운다.
- Phase 1: Express에서 `req.user`를 붙이는 인증 middleware와 role middleware를 분리한 장면.
- Phase 2: NestJS에서 `AuthService`, JWT strategy, `RolesGuard`로 같은 규칙을 guard chain에 올린 장면.
- Phase 3: e2e가 public/401/403/admin happy path를 모두 검증하는 장면.
- 강조 포인트: 이후 persistence와 events는 이 auth 경계를 유지한 채 확장된다는 점.
