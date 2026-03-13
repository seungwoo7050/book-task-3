# 04-request-pipeline structure plan

이 문서는 CRUD를 더 많이 설명하는 글이 아니라, validation·error handling·response envelope가 왜 별도 계층이 돼야 하는지 보여 주는 글이어야 한다. 읽는 리듬은 `validation -> response/error -> Nest global pipeline`이 좋다.

## 읽기 구조

1. handler 안의 조건문을 밖으로 뺀 이유를 먼저 잡는다.
2. success/error envelope가 왜 이후 프로젝트의 공통 표면이 되는지 설명한다.
3. 같은 규약을 NestJS에서 어떻게 다시 구성했는지 잇는다.

## 반드시 남길 근거

- Express `validate`
- Express `responseWrapper`
- Express `errorHandler`
- Nest `HttpExceptionFilter`
- Nest `TransformInterceptor`
- Express/Nest e2e 결과

## 리라이트 톤

- middleware/filter/interceptor를 기능 나열처럼 쓰지 않는다.
- "순서가 바뀌면 왜 곤란해지는가"가 드러나게 쓴다.
