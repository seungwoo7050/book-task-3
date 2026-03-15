# d-data-jpa-lab-spring 문제지

## 왜 중요한가

JPA를 "그냥 돌아가는 CRUD"가 아니라, 데이터 경계와 persistence 선택을 설명하는 도구로 다루는 Spring 랩을 만든다.

## 목표

시작 위치의 구현을 완성해 Flyway와 JPA entity/repository/service 경계가 같이 보인다, pagination과 optimistic locking 같은 persistence 고민이 코드에 드러난다, Querydsl을 왜 지금은 얕게 두는지 설명할 수 있다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../labs/D-data-jpa-lab/spring/src/main/resources/application.yml`
- `../labs/D-data-jpa-lab/spring/src/test/resources/application.yml`
- `../labs/D-data-jpa-lab/spring/bin/main/application.yml`
- `../labs/D-data-jpa-lab/spring/build.gradle.kts`
- `../labs/D-data-jpa-lab/spring/Makefile`

## starter code / 입력 계약

- `../labs/D-data-jpa-lab/spring/src/main/resources/application.yml`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- Flyway와 JPA entity/repository/service 경계가 같이 보인다.
- pagination과 optimistic locking 같은 persistence 고민이 코드에 드러난다.
- Querydsl을 왜 지금은 얕게 두는지 설명할 수 있다.

## 제외 범위

- `../labs/D-data-jpa-lab/spring/src/main/resources/application.yml` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- `../labs/D-data-jpa-lab/spring/src/main/resources/application.yml` 등 fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/backend-spring/labs/D-data-jpa-lab/spring && ./gradlew test`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-spring/labs/D-data-jpa-lab/spring && ./gradlew test
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-spring/labs/D-data-jpa-lab/spring test
```

- Spring/Java 계열 검증은 `JDK/JRE`가 현재 머신에 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`d-data-jpa-lab-spring_answer.md`](d-data-jpa-lab-spring_answer.md)에서 확인한다.
