# b-federation-security-lab-spring 문제지

## 왜 중요한가

로컬 계정 인증 이후에 federation, 2FA, audit 같은 인증 강화 요소가 설계를 어떻게 바꾸는지 보여주는 Spring 랩을 만든다.

## 목표

시작 위치의 구현을 완성해 Google OAuth2 authorize/callback 형태를 설명할 수 있는 federation flow가 존재한다, TOTP setup/verify와 recovery code 사고방식을 같은 랩에서 다룬다, audit 기록이 왜 필요한지 API와 문서 수준에서 설명할 수 있다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../labs/B-federation-security-lab/spring/src/main/resources/application.yml`
- `../labs/B-federation-security-lab/spring/src/test/resources/application.yml`
- `../labs/B-federation-security-lab/spring/bin/main/application.yml`
- `../labs/B-federation-security-lab/spring/build.gradle.kts`
- `../labs/B-federation-security-lab/spring/Makefile`

## starter code / 입력 계약

- `../labs/B-federation-security-lab/spring/src/main/resources/application.yml`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- Google OAuth2 authorize/callback 형태를 설명할 수 있는 federation flow가 존재한다.
- TOTP setup/verify와 recovery code 사고방식을 같은 랩에서 다룬다.
- audit 기록이 왜 필요한지 API와 문서 수준에서 설명할 수 있다.

## 제외 범위

- `../labs/B-federation-security-lab/spring/src/main/resources/application.yml` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- `../labs/B-federation-security-lab/spring/src/main/resources/application.yml` 등 fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/backend-spring/labs/B-federation-security-lab/spring && ./gradlew test`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-spring/labs/B-federation-security-lab/spring && ./gradlew test
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-spring/labs/B-federation-security-lab/spring test
```

- Spring/Java 계열 검증은 `JDK/JRE`가 현재 머신에 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`b-federation-security-lab-spring_answer.md`](b-federation-security-lab-spring_answer.md)에서 확인한다.
