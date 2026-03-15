# f-cache-concurrency-lab-spring 문제지

## 왜 중요한가

캐시 무효화, 중복 요청, 재고 경합 문제를 inventory 시나리오 하나로 묶어 구체화하는 Spring 랩을 만든다.

## 목표

시작 위치의 구현을 완성해 inventory 조회와 reservation 흐름에서 cacheable read path와 idempotency key 처리가 보인다, 같은 JVM 안에서의 동시성 제어가 재고 차감 문제와 연결된다, Redis나 분산 락을 왜 다음 단계로 남겼는지 설명할 수 있다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../labs/F-cache-concurrency-lab/spring/src/main/resources/application.yml`
- `../labs/F-cache-concurrency-lab/spring/src/test/resources/application.yml`
- `../labs/F-cache-concurrency-lab/spring/bin/main/application.yml`
- `../labs/F-cache-concurrency-lab/spring/build.gradle.kts`
- `../labs/F-cache-concurrency-lab/spring/Makefile`

## starter code / 입력 계약

- `../labs/F-cache-concurrency-lab/spring/src/main/resources/application.yml`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- inventory 조회와 reservation 흐름에서 cacheable read path와 idempotency key 처리가 보인다.
- 같은 JVM 안에서의 동시성 제어가 재고 차감 문제와 연결된다.
- Redis나 분산 락을 왜 다음 단계로 남겼는지 설명할 수 있다.

## 제외 범위

- `../labs/F-cache-concurrency-lab/spring/src/main/resources/application.yml` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- `../labs/F-cache-concurrency-lab/spring/src/main/resources/application.yml` 등 fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/backend-spring/labs/F-cache-concurrency-lab/spring && ./gradlew test`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-spring/labs/F-cache-concurrency-lab/spring && ./gradlew test
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-spring/labs/F-cache-concurrency-lab/spring test
```

- Spring/Java 계열 검증은 `JDK/JRE`가 현재 머신에 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`f-cache-concurrency-lab-spring_answer.md`](f-cache-concurrency-lab-spring_answer.md)에서 확인한다.
