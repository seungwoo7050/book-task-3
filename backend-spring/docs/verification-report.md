# backend-spring 검증 기록

- 점검 날짜: `2026-03-09`
- 범위: 7개 Spring 랩과 2개 커머스 캡스톤

## 다시 실행한 명령

각 `spring/` 워크스페이스에서 문서화된 검증 명령을 다시 실행했습니다.

- `./gradlew spotlessApply test --no-daemon`
- `make test`
- `make lint`
- `make smoke`

Compose 기반 확인도 다시 수행해 각 스택이 부팅되고 `/api/v1/health/live`, `/api/v1/health/ready`에 응답하는지 점검했습니다.

`capstone/commerce-backend-v2/spring`에서는 아래도 별도로 확인했습니다.

- `./gradlew testClasses --no-daemon`
- `make lint`
- `make test`
- `make smoke`
- Compose 부팅 후 health endpoint 확인

## 결과 요약

- `A-auth-lab`: lint, test, smoke, Compose health 확인 통과
- `B-federation-security-lab`: lint, test, smoke, Compose health 확인 통과
- `C-authorization-lab`: lint, test, smoke, Compose health 확인 통과
- `D-data-jpa-lab`: lint, test, smoke, Compose health 확인 통과
- `E-event-messaging-lab`: lint, test, smoke, Compose health 확인 통과
- `F-cache-concurrency-lab`: test 시 로컬 in-memory `CacheManager`를 사용하도록 한 뒤 통과
- `G-ops-observability-lab`: lint, test, smoke, Compose health 확인 통과
- `commerce-backend`: lint, test, smoke, Compose health 확인 통과
- `commerce-backend-v2`: lint, test, smoke, 전체 JUnit suite, Testcontainers messaging test, Compose health 확인 통과

## 이 기록이 증명하는 것

- 각 Spring 워크스페이스가 문서화된 lint/test/smoke 흐름을 다시 통과했다
- 로컬 테스트 설정에서 H2 기반 부팅이 가능하다
- Docker Compose 스택이 health endpoint에 응답한다

## 아직 증명하지 않은 것

- 모든 워크스페이스의 `make run` 장시간 foreground 실행
- 실제 Google OAuth console integration
- 장기 운영 환경에서의 Kafka runtime behavior
- 실제 결제 provider integration
- 실제 AWS 배포 성공

이 레포의 목표는 production claim이 아니라, 다시 실행 가능하고 설명 가능한 Spring 학습 결과물을 남기는 것입니다.
