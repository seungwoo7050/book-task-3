# 디버그 로그

## 1. copied 설정에서 `access_token_ttl_seconds`가 빠져 있었다

- 증상: `workspace-service` 통합 테스트가 `Settings`에 `access_token_ttl_seconds`가 없다고 실패했다.
- 원인: v2 구조를 랩으로 복사하는 과정에서 `workspace-service` 설정 파일이 일부 누락된 상태였다.
- 수정: `app/core/config.py`에 `access_token_ttl_seconds` 기본값을 다시 추가했다.
- 검증: `services/workspace-service/tests/integration/test_workspace_service.py`가 통과했다.

## 2. 테스트 토큰의 `sub`가 UUID 형식이 아니었다

- 증상: 워크스페이스 생성 시 SQLAlchemy가 UUID primary key를 처리하는 단계에서 `badly formed hexadecimal UUID string` 오류가 났다.
- 원인: copied 테스트가 `user-owner`, `user-collab` 같은 문자열을 그대로 `sub` claim에 넣고 있었다.
- 수정: 테스트 토큰의 `sub`를 실제 UUID 문자열로 바꿨다.
- 검증: 워크스페이스 생성, invite 수락, comment 생성 흐름이 다시 정상 동작했다.

## 3. 컨테이너 실행에서는 `argon2`가 없어서 앱이 죽었다

- 증상: 로컬 테스트는 통과했지만 Compose로 올린 `workspace-service`가 `ModuleNotFoundError: No module named 'argon2'`로 시작하지 못했다.
- 원인: 루트 가상환경에는 `argon2-cffi`가 이미 있어서 가려졌지만, 서비스별 `pyproject.toml` 의존성에는 빠져 있었다.
- 수정: `workspace-service` 패키지 의존성에 `argon2-cffi`를 추가했다.
- 검증: `pytest tests/test_system.py -q`와 `python -m tests.smoke`가 Compose에서 통과했다.

## 4. Compose project name 충돌이 새 랩들에서 반복됐다

- 증상: timestamp 기반 project name이 초 단위라 병렬 실행 시 이미지 이름 충돌이 발생했다.
- 원인: copied `compose_harness.py`가 같은 prefix와 초 단위 timestamp만 사용했다.
- 수정: UUID 기반 project name과 cleanup timeout을 도입했다.
- 검증: H 랩 system test가 고유한 Compose project로 안정적으로 종료됐다.
