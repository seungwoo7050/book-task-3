# 09-platform-capstone structure plan

이 문서는 "큰 프로젝트 하나를 더 만들었다"보다 "이전 단계 규약을 한 앱으로 조합했다"는 인상이 먼저 남아야 한다. 읽는 축은 `module composition -> cross-cutting contract -> end-to-end user flow`로 잡는다.

## 읽기 구조

1. auth/books/events를 왜 다시 쓰지 않고 조합했는지 보여 준다.
2. 공통 filter/logging/event listener가 통합 단계에서 왜 더 중요해졌는지 잇는다.
3. 관리자/일반 사용자/public read 흐름을 e2e로 묶는 장면으로 닫는다.

## 반드시 남길 근거

- `AuthService`
- `BooksService`
- `HttpExceptionFilter`
- `LoggingInterceptor`
- `AppEventListener`
- auth unit test
- capstone e2e

## 리라이트 톤

- capstone을 과장하지 않는다.
- "새로 쓰기"보다 "조합하면서 지켜 낸 규약"이 먼저 보이게 쓴다.
