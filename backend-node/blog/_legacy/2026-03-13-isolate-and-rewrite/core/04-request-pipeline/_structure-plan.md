# 04-request-pipeline structure plan

## 중심 질문

- CRUD보다 앞서 왜 request pipeline 규약을 먼저 세웠는가
- Express middleware 순서와 NestJS global pipe/filter/interceptor는 어떻게 대응되는가
- e2e 로그와 응답 envelope가 이 프로젝트의 핵심 증거가 되는 이유는 무엇인가

## 10-development-timeline.md

- 오프닝: 이 프로젝트가 "기능 추가"가 아니라 "공통 요청 규약 고정"이라는 점을 먼저 밝힌다.
- Phase 1: Express middleware chain에서 validation, response wrapping, error handling 순서를 결정한 장면.
- Phase 2: NestJS main bootstrap에서 같은 규약을 global primitives로 올린 장면.
- Phase 3: e2e가 응답 envelope와 로그를 실제 신호로 남기는 장면.
- 강조 포인트: 이후 auth, persistence, events는 모두 이 pipeline 위에 올라간다는 점.
