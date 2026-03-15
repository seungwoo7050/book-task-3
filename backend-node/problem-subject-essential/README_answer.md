# backend-node 서버 개발 필수 답안지

이 문서는 Node 트랙에서 서버 공통성이 가장 직접적인 `08-production-readiness`를 실제 NestJS 소스 기준으로 정리한 답안지다. 핵심은 기능 API를 더 만드는 것이 아니라, bootstrap 단계에서 runtime config를 읽고, health/readiness와 structured logging을 HTTP 표면으로 고정하고, 같은 검증을 CI까지 밀어 넣는 데 있다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [08-production-readiness-nestjs](08-production-readiness-nestjs_answer.md) | 시작 위치의 구현을 완성해 health/live와 health/ready를 분리할 것, config loader와 structured logging을 문서화할 것, 테스트와 Docker/CI 예시를 함께 제공할 것을 한 흐름으로 설명하고 검증한다. 핵심은 AppModule와 HealthController, bootstrap 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/applied/08-production-readiness/nestjs && npm run test -- --run` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
