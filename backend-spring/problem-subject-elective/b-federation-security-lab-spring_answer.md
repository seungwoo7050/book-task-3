# b-federation-security-lab-spring 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 source, trace, fixture, 검증 스크립트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 Google OAuth2 authorize/callback 형태를 설명할 수 있는 federation flow가 존재한다, TOTP setup/verify와 recovery code 사고방식을 같은 랩에서 다룬다, audit 기록이 왜 필요한지 API와 문서 수준에서 설명할 수 있다를 한 흐름으로 설명하고 검증한다.

## 이 문제의 목표 구조

- Google OAuth2 authorize/callback 형태를 설명할 수 있는 federation flow가 존재한다.
- TOTP setup/verify와 recovery code 사고방식을 같은 랩에서 다룬다.
- audit 기록이 왜 필요한지 API와 문서 수준에서 설명할 수 있다.
- 근거 파일은 `../labs/B-federation-security-lab/spring/src/main/resources/application.yml` 등처럼 실제 trace/fixture/스크립트로 고정한다.

## 단계별 풀이

1. `../labs/B-federation-security-lab/spring/src/main/resources/application.yml`를 먼저 열어 어떤 입력과 근거 파일이 이 lab의 사실 원천인지 고정한다.
2. `../labs/B-federation-security-lab/spring/src/main/resources/application.yml`와 `../labs/B-federation-security-lab/spring/src/test/resources/application.yml`에서 요구하는 값과 근거를 한 항목씩 대응시킨다.
3. `cd /Users/woopinbell/work/book-task-3/backend-spring/labs/B-federation-security-lab/spring && ./gradlew test`를 사용해 빠진 근거와 누락된 항목이 없는지 마지막에 다시 잠근다.

## 흔한 오답과 보완

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `../labs/B-federation-security-lab/spring/src/main/resources/application.yml` 등 fixture/trace를 읽지 않고 동작을 추측하지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/backend-spring/labs/B-federation-security-lab/spring && ./gradlew test`로 회귀를 조기에 잡는다.

## 검증 기준

```bash
cd /Users/woopinbell/work/book-task-3/backend-spring/labs/B-federation-security-lab/spring && ./gradlew test
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-spring/labs/B-federation-security-lab/spring test
```

## 왜 이것이 정답인가

- 문제 원문이 요구한 질문이나 산출물 계약이 실제 trace, fixture, 검증 스크립트와 일대일로 연결되면 답안이 임의 설명이 아니라 근거 기반 결과가 된다.
- `cd /Users/woopinbell/work/book-task-3/backend-spring/labs/B-federation-security-lab/spring && ./gradlew test`가 통과하면 누락된 질문, 빠진 산출물, 형식 오류가 없는 상태를 재현할 수 있다.

## 소스 근거

- `../labs/B-federation-security-lab/spring/src/main/resources/application.yml`
- `../labs/B-federation-security-lab/spring/src/test/resources/application.yml`
- `../labs/B-federation-security-lab/spring/bin/main/application.yml`
- `../labs/B-federation-security-lab/spring/bin/test/application.yml`
- `../labs/B-federation-security-lab/spring/build.gradle.kts`
- `../labs/B-federation-security-lab/spring/Makefile`
