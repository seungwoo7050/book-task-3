# backend-spring 서버 캡스톤 문제지

`backend-spring`의 capstone은 개별 랩에서 나눠 다룬 인증, 데이터, 이벤트, 캐시, 운영성 문제를 하나의 커머스 도메인으로 다시 조합하게 만드는 종합 과제입니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [commerce-backend-spring](commerce-backend-spring.md) | 시작 위치의 구현을 완성해 하나의 modular monolith 안에서 커머스 기본 흐름이 연결된다, 랩 학습을 통합했을 때 어떤 경계가 남는지 설명할 수 있다, 이후 commerce-backend-v2가 왜 필요한지 비교 기준이 된다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-spring/capstone/commerce-backend/spring && ./gradlew test` |
| [commerce-backend-v2-spring](commerce-backend-v2-spring.md) | 시작 위치의 구현을 완성해 persisted local auth와 mocked Google account linking이 존재한다, JPA + Flyway + PostgreSQL로 catalog, order, payment, notification 경계를 설명할 수 있다, Redis와 Kafka가 cart, throttling, outbox handoff 같은 구체적 문제에 연결된다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-spring/capstone/commerce-backend-v2/spring && ./gradlew test` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
