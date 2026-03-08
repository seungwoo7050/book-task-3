# Checked Sources

- NestJS Fundamentals: Interceptors
  - checked: 2026-03-07
  - why: 요청당 structured log를 남기는 가장 작은 확장 지점을 다시 확인했다.
  - learned: 운영성 기능은 controller 안에 섞기보다 interceptor나 middleware로 빼야 재사용이 쉽다.
- Node.js API: `process.env`
  - checked: 2026-03-07
  - why: 런타임 설정 로더의 입력 계약을 단순하게 유지하기 위해 재확인했다.
  - learned: config loader는 "읽기"보다 "검증 실패를 빨리 드러내기"가 더 중요하다.
