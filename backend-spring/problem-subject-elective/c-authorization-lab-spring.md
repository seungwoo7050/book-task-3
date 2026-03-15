# c-authorization-lab-spring 문제지

## 왜 중요한가

인증 문제와 분리된 authorization 랩을 만들어 role, membership, ownership 규칙을 명시적으로 다룬다.

## 목표

시작 위치의 구현을 완성해 organization 생성, invite 발급/수락, role 변경 흐름이 존재한다, 누가 어떤 조직/상점 리소스를 수정할 수 있는지 service logic 수준에서 설명 가능하다, 인증 랩의 문제와 authorization 랩의 문제가 문서와 코드에서 섞이지 않는다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../labs/C-authorization-lab/spring/src/main/resources/application.yml`
- `../labs/C-authorization-lab/spring/src/test/resources/application.yml`
- `../labs/C-authorization-lab/spring/bin/main/application.yml`
- `../labs/C-authorization-lab/spring/build.gradle.kts`
- `../labs/C-authorization-lab/spring/Makefile`

## starter code / 입력 계약

- `../labs/C-authorization-lab/spring/src/main/resources/application.yml`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- organization 생성, invite 발급/수락, role 변경 흐름이 존재한다.
- 누가 어떤 조직/상점 리소스를 수정할 수 있는지 service logic 수준에서 설명 가능하다.
- 인증 랩의 문제와 authorization 랩의 문제가 문서와 코드에서 섞이지 않는다.

## 제외 범위

- `../labs/C-authorization-lab/spring/src/main/resources/application.yml` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- `../labs/C-authorization-lab/spring/src/main/resources/application.yml` 등 fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/backend-spring/labs/C-authorization-lab/spring && ./gradlew test`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-spring/labs/C-authorization-lab/spring && ./gradlew test
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-spring/labs/C-authorization-lab/spring test
```

- Spring/Java 계열 검증은 `JDK/JRE`가 현재 머신에 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`c-authorization-lab-spring_answer.md`](c-authorization-lab-spring_answer.md)에서 확인한다.
