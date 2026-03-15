# 05-auth-and-authorization structure plan

이 문서는 JWT 기능 소개보다 `401`과 `403`을 어디서 갈라 놓았는지, 그리고 그 경계와 별개로 무엇이 아직 비어 있는지 먼저 읽혀야 한다. 서사의 중심은 `auth service claim 구성 -> Express/Nest 요청 경계 -> 실제 응답 body -> validation 공백`이다.

## 읽기 구조

1. 왜 auth service가 middleware/guard보다 먼저 읽혀야 하는지부터 잡는다.
2. Express `authmiddleware`, `requireRole`, `book.router.ts`로 `401 -> 403` 순서를 보여 준다.
3. NestJS `JwtStrategy`, `JwtAuthGuard`, `RolesGuard`, `BooksController`로 같은 경계를 어떻게 프레임워크 안으로 옮기는지 잇는다.
4. 상태코드뿐 아니라 실제 응답 body 차이를 짚어 이전 request-pipeline의 envelope가 여기선 유지되지 않는다는 점을 적는다.
5. 마지막에는 두 레인 모두 빈 credential 등록을 허용하는 validation 공백을 남긴다.

## 반드시 남길 근거

- Express `src/services/auth.service.ts`
- Express `src/middleware/auth.middleware.ts`
- Express `src/middleware/role.middleware.ts`
- Express `src/routes/book.router.ts`
- Express `401/403` 직접 재실행 결과
- Express 빈 register 직접 재실행 결과
- NestJS `src/auth/auth.module.ts`
- NestJS `src/auth/auth.service.ts`
- NestJS `src/auth/guards/jwt-auth.guard.ts`
- NestJS `src/auth/guards/roles.guard.ts`
- NestJS `src/auth/strategies/jwt.strategy.ts`
- NestJS `src/books/books.controller.ts`
- NestJS `401/403` 직접 재실행 결과
- NestJS 빈 register 직접 재실행 결과

## 리라이트 톤

- 보안 일반론이나 교과서 설명보다, 현재 소스가 실제로 만드는 경계와 한계를 중심으로 쓴다.
- "이전 lab 위에 자연스럽게 확장됐다"는 서술을 자동으로 받아들이지 않는다.
- role 경계의 성과와 validation 공백을 동시에 드러낸다.
