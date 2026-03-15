# 10-shippable-backend-service structure plan

이 문서는 `09`의 덩치를 키운 후속편처럼 보이면 안 된다. 핵심은 "서비스 표면과 운영 실패 모드를 어디까지 코드로 끌어올렸는가"다. 읽기 축은 `bootstrap/init -> Redis policy -> infra-backed verification -> startup risk`로 잡는다.

## 읽기 구조

1. `configureApp`, `AppModule`, migration, seed로 실행 표면을 먼저 설명한다.
2. `AuthRateLimitService`와 `BooksService`가 Redis를 어떻게 정책으로 쓰는지 잇는다.
3. unit/e2e와 수동 `curl`/`redis-cli` 재실행으로 검증 루프를 닫는다.
4. `StructuredLoggingInterceptor`와 `RedisService`를 통해 로그 왜곡과 startup hang 리스크를 마지막에 남긴다.

## 반드시 남길 근거

- `app.bootstrap.ts`
- `app.module.ts`
- `health.controller.ts`
- `request-id.middleware.ts`
- migration file
- `seed-data.ts`
- `AuthController`
- `AuthRateLimitService`
- `AuthService.login`
- `BooksService`
- `StructuredLoggingInterceptor`
- `RedisService`
- unit 12개
- e2e 16개
- 수동 `/health`, `/docs`, throttle, cache, invalid Redis 부팅 실험

## 리라이트 톤

- 기능 홍보문처럼 쓰지 않는다.
- "실행 절차가 어떻게 제품의 일부가 되었는가"가 먼저 보이게 쓴다.
- 성공 검증과 함께 현재 운영상 거친 부분을 같은 비중으로 남긴다.
