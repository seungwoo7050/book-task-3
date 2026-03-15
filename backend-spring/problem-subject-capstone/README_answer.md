# backend-spring 서버 캡스톤 답안지

이 문서는 Spring 트랙의 capstone 두 개를 실제 통합 소스 기준으로 정리한 답안지다. 첫 capstone은 modular monolith 기준선으로 인증, 카탈로그, 장바구니, 주문을 하나의 커머스 흐름으로 묶고, 두 번째 capstone은 persisted auth, Redis, Kafka, idempotent payment, notification outbox까지 연결해 대표 결과물 수준으로 확장한다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [commerce-backend-spring](commerce-backend-spring_answer.md) | 시작 위치의 구현을 완성해 하나의 modular monolith 안에서 커머스 기본 흐름이 연결된다, 랩 학습을 통합했을 때 어떤 경계가 남는지 설명할 수 있다, 이후 commerce-backend-v2가 왜 필요한지 비교 기준이 된다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-spring/capstone/commerce-backend/spring && ./gradlew test` |
| [commerce-backend-v2-spring](commerce-backend-v2-spring_answer.md) | 시작 위치의 구현을 완성해 persisted local auth와 mocked Google account linking이 존재한다, JPA + Flyway + PostgreSQL로 catalog, order, payment, notification 경계를 설명할 수 있다, Redis와 Kafka가 cart, throttling, outbox handoff 같은 구체적 문제에 연결된다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-spring/capstone/commerce-backend-v2/spring && ./gradlew test` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
