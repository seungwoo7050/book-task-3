# 디버그 로그

## 실패 사례

Compose health check가 너무 빨리 실행되어 API가 준비되기 전에 `unhealthy`로 보이거나, `@lru_cache`로 감싼 설정이 테스트 간에 남아 잘못된 환경 변수를 읽는 문제가 있었다.

## 원인

- health check의 `start_period`가 느린 환경 기준으로 넉넉하지 않았다.
- 설정 객체는 환경 변수에 의존하는데, 캐시는 테스트 격리를 보장하지 않는다.

## 수정

- Compose health check에 충분한 `start_period`와 재시도 여유를 두었다.
- 테스트에서는 `get_settings.cache_clear()` 패턴으로 설정 캐시를 비우는 규칙을 유지했다.

## 검증 근거

- 이 실패는 운영 문제의 상당수가 비즈니스 로직보다 실행 환경과 설정 캐시에서 먼저 드러난다는 점을 보여 준다.
- 마지막 기록된 검증은 [../../../docs/verification-report.md](../../../docs/verification-report.md)를 따른다.

## 남은 메모

readiness는 DB 엔진이나 외부 의존성의 특성에 따라 실패 양상이 달라질 수 있으므로, 문서에서 그 한계를 숨기지 않는 편이 좋다.
