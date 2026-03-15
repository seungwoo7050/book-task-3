# backend-node 서버 캡스톤 문제지

`backend-node`의 capstone은 Books API 학습 단계에서 만든 규약을 한 서비스 표면으로 다시 조합하고, 그 위에 채용 제출용 포장을 더하는 종합 과제입니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [09-platform-capstone-nestjs](09-platform-capstone-nestjs.md) | 시작 위치의 구현을 완성해 auth, books, events, persistence, 운영성 규약이 한 서비스 안에서 함께 동작할 것, native SQLite 복구 절차를 포함해 재현 가능한 검증 명령을 남길 것, 단계별 학습 산출물이 capstone 안에서 어떻게 연결되는지 설명할 것을 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs && npm run test -- --run` |
| [10-shippable-backend-service-nestjs](10-shippable-backend-service-nestjs.md) | 시작 위치의 구현을 완성해 Postgres migration과 Redis 의존성을 포함한 로컬 실행 흐름을 제공할 것, Swagger, health endpoint, auth/books API를 한 서비스 표면으로 설명할 것, 학습용 capstone과 제출용 서비스의 차이를 문서화할 것을 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/applied/10-shippable-backend-service/nestjs && npm run test -- --run` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
