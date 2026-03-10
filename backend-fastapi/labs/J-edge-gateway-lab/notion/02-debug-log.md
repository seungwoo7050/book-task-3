# 디버그 로그

## 1. gateway client 오류가 500으로 흘러가면 edge 의미가 약해졌다

- 증상: 내부 서비스 연결 실패가 generic 500으로 보이면 upstream 문제인지 gateway 코드 문제인지 구분하기 어려웠다.
- 수정: gateway client에서 `httpx.RequestError`를 잡아 503 `UPSTREAM_UNAVAILABLE`로 번역했다.
- 검증: notification-service 중단 뒤 drain 호출 시 503이 반환되고, 복구 후 재시도는 다시 성공했다.

## 2. Compose 컨테이너에서 gateway가 `argon2` import 에러로 죽었다

- 증상: 로컬 gateway 테스트는 통과했지만 Compose로 올린 gateway는 `ModuleNotFoundError: No module named 'argon2'`로 시작하지 못했다.
- 원인: 루트 가상환경 패키지가 로컬 실행을 가려 주고 있었고, gateway의 `pyproject.toml`에는 `argon2-cffi`가 빠져 있었다.
- 수정: gateway 패키지 의존성에 `argon2-cffi`를 추가했다.
- 검증: J 랩 system test와 smoke가 Compose에서 통과했다.

## 3. Compose teardown이 cleanup 단계에서 오래 걸렸다

- 증상: 테스트 본문은 끝났는데 `docker compose down`이 cleanup에서 오래 매달려 전체 검증이 느리게 끝났다.
- 수정: `compose_harness.py`에 timeout과 teardown 예외 무시를 추가했다.
- 검증: J 랩 system test가 cleanup 때문에 실패하지 않고 종료됐다.

## 4. project name 충돌이 병렬 검증에서 드러났다

- 증상: 초 단위 timestamp project name이 다른 MSA 랩과 겹치며 이미지 이름 충돌을 만들었다.
- 수정: UUID suffix 기반 project name으로 바꾸고 prefix를 소문자로 정규화했다.
- 검증: J 랩 Compose system test가 고유 project name으로 실행됐다.
