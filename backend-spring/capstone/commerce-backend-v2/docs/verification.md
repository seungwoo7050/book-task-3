# commerce-backend-v2 검증 메모

- 점검 날짜: `2026-03-09`
- 실행 워크스페이스: [../spring/README.md](../spring/README.md)

## 다시 실행한 명령

- `./gradlew testClasses --no-daemon`
- `make lint`
- `make test`
- `make smoke`
- Compose 부팅 후 `/api/v1/health/live`, `/api/v1/health/ready` 확인

## 통과한 것

- MockMvc 테스트와 Testcontainers-backed messaging test를 포함한 전체 JUnit suite
- formatting과 checkstyle
- smoke 테스트
- Docker image build와 Compose health 확인

## 아직 의도적으로 남긴 것

- Google OAuth는 callback contract 수준의 mock이다
- payment provider integration은 mock-only다
- AWS deployment는 문서화된 방향이지 live provisioning은 아니다
