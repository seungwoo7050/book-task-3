# 05-auth-and-authorization

- 그룹: `Core`
- 상태: `verified`
- 공개 답안 레인: `express/`, `nestjs/`
- 성격: 초기 원본 이관 + 재검증

## 한 줄 문제

JWT 인증과 RBAC 인가를 Express middleware chain과 NestJS guard chain으로 비교하는 보안 기초 문제다.

## 성공 기준

- `401`과 `403` 경계를 설명하고 구현할 수 있다.
- Express middleware chain과 NestJS guard chain의 차이를 비교할 수 있다.
- JWT 발급, 검증, 권한 체크를 테스트로 고정할 수 있다.

## 내가 만든 답

- 두 레인 모두 로그인과 보호된 Books 쓰기 경로를 구현하고 테스트로 검증했다.
- request pipeline 위에 auth 규칙을 올려 어떤 시점에 인증/인가가 개입하는지 비교하게 했다.
- `notion/`에는 이후 capstone에서 재사용되는 JWT/RBAC 관점을 연결해 두었다.

## 제공 자료

- `problem/README.md`와 starter code
- `express/`
- `nestjs/`
- `docs/`
- `notion/`

## 실행과 검증

### Express 레인
- 작업 디렉터리: `express/`
- install: `pnpm install`
- verify: `pnpm run build && pnpm run test`
- run: `pnpm run dev`

### NestJS 레인
- 작업 디렉터리: `nestjs/`
- install: `pnpm install`
- verify: `pnpm run build && pnpm run test`
- run: `pnpm run start:dev`

## 왜 다음 단계로 이어지는가

- `06-persistence-and-repositories`에서 메모리 저장소를 영속 계층으로 교체하며 API 계약을 유지한다.
- canonical problem statement는 [problem/README.md](problem/README.md)에서, 구현별 실행 메모는 [express/README.md](express/README.md), [nestjs/README.md](nestjs/README.md)에서 확인한다.
