# commerce-backend-v2-spring 문제지

## 왜 중요한가

Spring 랩들의 학습을 하나의 커머스 도메인으로 다시 조합하되, junior backend interview에서 방어 가능한 깊이까지 끌어올린 대표 capstone을 만든다.

## 목표

시작 위치의 구현을 완성해 persisted local auth와 mocked Google account linking이 존재한다, JPA + Flyway + PostgreSQL로 catalog, order, payment, notification 경계를 설명할 수 있다, Redis와 Kafka가 cart, throttling, outbox handoff 같은 구체적 문제에 연결된다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../capstone/commerce-backend-v2/spring/src/main/resources/application.yml`
- `../capstone/commerce-backend-v2/spring/src/test/resources/application.yml`
- `../capstone/commerce-backend-v2/spring/bin/main/application.yml`
- `../capstone/commerce-backend-v2/spring/build.gradle.kts`
- `../capstone/commerce-backend-v2/spring/Makefile`

## starter code / 입력 계약

- `../capstone/commerce-backend-v2/spring/src/main/resources/application.yml`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- persisted local auth와 mocked Google account linking이 존재한다.
- JPA + Flyway + PostgreSQL로 catalog, order, payment, notification 경계를 설명할 수 있다.
- Redis와 Kafka가 cart, throttling, outbox handoff 같은 구체적 문제에 연결된다.
- Docker Compose, health/readiness, metrics, 테스트, 배포 메모가 함께 남는다.

## 제외 범위

- `../capstone/commerce-backend-v2/spring/src/main/resources/application.yml` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- `../capstone/commerce-backend-v2/spring/src/main/resources/application.yml` 등 fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/backend-spring/capstone/commerce-backend-v2/spring && ./gradlew test`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-spring/capstone/commerce-backend-v2/spring && ./gradlew test
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-spring/capstone/commerce-backend-v2/spring test
```

- Spring/Java 계열 검증은 `JDK/JRE`가 현재 머신에 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`commerce-backend-v2-spring_answer.md`](commerce-backend-v2-spring_answer.md)에서 확인한다.
