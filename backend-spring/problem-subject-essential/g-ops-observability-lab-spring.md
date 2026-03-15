# g-ops-observability-lab-spring 문제지

## 왜 중요한가

운영성을 capstone의 부록이 아니라 독립 학습 주제로 분리해, 백엔드가 스스로를 관찰 가능하게 만드는 최소 기준을 다룬다.

## 목표

시작 위치의 구현을 완성해 health/readiness, JSON logging, trace ID, Prometheus scrape target이 존재한다, Compose와 CI가 "운영 기본기"로서 어떤 역할을 하는지 설명할 수 있다, 현재 증명한 범위와 아직 미완인 운영 영역이 문서에 분리되어 있다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../labs/G-ops-observability-lab/spring/src/main/resources/application.yml`
- `../labs/G-ops-observability-lab/spring/src/test/resources/application.yml`
- `../labs/G-ops-observability-lab/spring/bin/main/application.yml`
- `../labs/G-ops-observability-lab/spring/build.gradle.kts`
- `../labs/G-ops-observability-lab/spring/Makefile`

## starter code / 입력 계약

- `../labs/G-ops-observability-lab/spring/src/main/resources/application.yml`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- health/readiness, JSON logging, trace ID, Prometheus scrape target이 존재한다.
- Compose와 CI가 "운영 기본기"로서 어떤 역할을 하는지 설명할 수 있다.
- 현재 증명한 범위와 아직 미완인 운영 영역이 문서에 분리되어 있다.

## 제외 범위

- `../labs/G-ops-observability-lab/spring/src/main/resources/application.yml` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- `../labs/G-ops-observability-lab/spring/src/main/resources/application.yml` 등 fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/backend-spring/labs/G-ops-observability-lab/spring && ./gradlew test`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-spring/labs/G-ops-observability-lab/spring && ./gradlew test
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-spring/labs/G-ops-observability-lab/spring test
```

- Spring/Java 계열 검증은 `JDK/JRE`가 현재 머신에 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`g-ops-observability-lab-spring_answer.md`](g-ops-observability-lab-spring_answer.md)에서 확인한다.
