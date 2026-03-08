# Architecture Summary

## 서비스 목표

이 프로젝트는 `09-platform-capstone`의 통합 구조를 유지하면서,
채용 제출 관점에서 바로 읽히는 운영 인터페이스와 재현 절차를 추가한 NestJS 서비스다.

## 모듈 구성

- `AuthModule`
  - 회원 등록과 JWT 발급
  - Redis 기반 로그인 실패 throttling
- `BooksModule`
  - public 조회와 admin 쓰기 분리
  - Redis 응답 캐시와 write 후 invalidation
- `EventsModule`
  - `book.created`, `book.updated`, `book.deleted`, `user.registered` 이벤트 로깅
- `RuntimeModule`
  - env 검증
  - Redis 연결
  - structured logging 설정

## 요청 흐름

1. `RequestIdMiddleware`가 `x-request-id`를 보장한다.
2. `ValidationPipe`가 payload 형식을 검증한다.
3. `JwtAuthGuard`와 `RolesGuard`가 보호 라우트를 제한한다.
4. controller와 service가 비즈니스 로직을 수행한다.
5. TypeORM repository가 Postgres에 접근한다.
6. Redis는 cache와 throttling 상태를 관리한다.
7. `TransformInterceptor`와 `HttpExceptionFilter`가 응답 형식을 통일한다.
8. `StructuredLoggingInterceptor`가 JSON 로그를 남긴다.

## 왜 09를 수정하지 않았는가

- `09`는 학습용 통합 capstone으로 충분하다.
- `10`은 채용 제출용 보강 과제이므로 평가 기준이 다르다.
- 두 프로젝트를 분리해야 “학습용 통합”과 “실무형 패키징”을 각각 설명할 수 있다.
