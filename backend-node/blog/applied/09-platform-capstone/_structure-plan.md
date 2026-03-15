# 09-platform-capstone structure plan

이 문서는 "기능이 많아진 통합판"보다 "이전 장의 계약을 단일 NestJS 앱으로 다시 고정하는 과정"이 먼저 보이게 써야 한다. 읽기 축은 `앱 껍질 -> auth/books 책임 -> 공통 HTTP 표면 -> e2e와 수동 검증`으로 잡는다.

## 읽기 구조

1. `AppModule`과 `main.ts`로 통합 껍질을 먼저 설명한다.
2. `AuthService`와 `BooksService`가 이전 장 책임을 어떻게 유지하는지 잇는다.
3. `TransformInterceptor`와 `HttpExceptionFilter`로 응답 계약을 정리한다.
4. `LoggingInterceptor`와 `AppEventListener`를 통해 통합 후 남는 운영 seam과 공백을 적는다.
5. `capstone.e2e.test.ts`와 수동 `curl` 재실행으로 실제 사용자 흐름을 닫는다.

## 반드시 남길 근거

- `app.module.ts`
- `main.ts`
- `AuthService`
- `BooksController`
- `BooksService`
- `HttpExceptionFilter`
- `TransformInterceptor`
- `LoggingInterceptor`
- `AppEventListener`
- `test/unit/auth.service.test.ts`
- `test/unit/books.service.test.ts`
- `test/e2e/capstone.e2e.test.ts`

## 리라이트 톤

- capstone을 "완성형 제품"처럼 과장하지 않는다.
- `token` 필드명, 공개 read vs 관리자 write, 성공 요청 위주 로그 같은 실제 구현 디테일을 숨기지 않는다.
- 테스트가 덮는 영역과 아직 덮지 못한 로그 계약을 분리해서 쓴다.
