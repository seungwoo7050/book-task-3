# e-event-messaging-lab-spring 문제지

## 왜 중요한가

Spring 백엔드가 request-response만으로 끝나지 않고 이벤트 기반 처리로 넘어갈 때 어떤 경계가 필요한지 보여주는 랩을 만든다.

## 목표

시작 위치의 구현을 완성해 도메인 변경 사실을 outbox record로 남기는 흐름이 존재한다, "이벤트 생성"과 "브로커 publish"를 다른 문제로 나눠 설명할 수 있다, Kafka/Redpanda가 왜 필요한지 handoff boundary 관점에서 설명 가능하다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../labs/E-event-messaging-lab/spring/src/main/resources/application.yml`
- `../labs/E-event-messaging-lab/spring/src/test/resources/application.yml`
- `../labs/E-event-messaging-lab/spring/bin/main/application.yml`
- `../labs/E-event-messaging-lab/spring/build.gradle.kts`
- `../labs/E-event-messaging-lab/spring/Makefile`

## starter code / 입력 계약

- `../labs/E-event-messaging-lab/spring/src/main/resources/application.yml`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 도메인 변경 사실을 outbox record로 남기는 흐름이 존재한다.
- "이벤트 생성"과 "브로커 publish"를 다른 문제로 나눠 설명할 수 있다.
- Kafka/Redpanda가 왜 필요한지 handoff boundary 관점에서 설명 가능하다.

## 제외 범위

- `../labs/E-event-messaging-lab/spring/src/main/resources/application.yml` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- `../labs/E-event-messaging-lab/spring/src/main/resources/application.yml` 등 fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/backend-spring/labs/E-event-messaging-lab/spring && ./gradlew test`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-spring/labs/E-event-messaging-lab/spring && ./gradlew test
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-spring/labs/E-event-messaging-lab/spring test
```

- Spring/Java 계열 검증은 `JDK/JRE`가 현재 머신에 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`e-event-messaging-lab-spring_answer.md`](e-event-messaging-lab-spring_answer.md)에서 확인한다.
