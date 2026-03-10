# 디버그 로그

## 1. 어떤 포트를 Compose probe 기준으로 삼을지 먼저 고정해야 했다

- 증상: 다중 서비스 구조에서는 “어느 포트가 최종 readiness인가”가 모호해졌다.
- 판단: 외부 기준은 gateway public health이고, 내부 서비스는 각자 own ready를 따로 봐야 한다.
- 수정: Compose health matrix와 top-level smoke를 gateway 기준으로 두고, 각 서비스 ready는 개별 healthcheck로 유지했다.
- 검증: K 랩 system test와 smoke가 gateway 기준으로 안정적으로 통과했다.

## 2. gateway와 workspace-service의 컨테이너 의존성이 로컬 테스트에 가려졌다

- 증상: 로컬 unit test는 통과했지만 Compose에서는 `argon2` import 에러가 발생할 수 있었다.
- 원인: 루트 가상환경 패키지가 컨테이너 의존성 누락을 가려 주고 있었다.
- 수정: `gateway`와 `workspace-service`의 `pyproject.toml`에 `argon2-cffi`를 추가했다.
- 검증: K 랩 Compose 기반 system test가 전체 스택에서 통과했다.

## 3. cleanup 단계가 system test 종료를 늦췄다

- 증상: 테스트 본문은 끝났는데 `docker compose down`이 cleanup에서 오래 걸렸다.
- 수정: `compose_harness.py` teardown에 timeout과 예외 무시를 넣었다.
- 검증: K 랩 검증이 cleanup 때문에 실패하지 않고 종료됐다.

## 4. project name 충돌은 운영성 랩에서도 그대로 나타났다

- 증상: MSA 랩을 병렬로 검증하면 Compose project name 충돌이 생겼다.
- 수정: UUID suffix와 소문자 prefix를 사용하는 project name 규칙으로 통일했다.
- 검증: K 랩 system test와 smoke가 고유 project name으로 각각 실행됐다.
