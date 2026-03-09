# 디버그 기록 — Rate Limiter에서 만나는 함정들

## float64 정밀도

`tokens`를 `float64`로 관리하기 때문에, 아주 작은 경과 시간에서 부동소수점 오차가 발생할 수 있다. 예: `tokens = 0.9999999999` → `Allow()`가 `tokens >= 1.0`에서 false를 반환. 실무에서는 문제되지 않을 정도로 미미하지만, 테스트에서 정확히 1.0을 기대하면 깨질 수 있다.

**교훈**: 토큰 테스트에서는 `time.Sleep`으로 충분한 시간을 준 뒤 확인하거나, 정확한 값 대신 범위를 검증한다.

## time.Now()의 비결정성

테스트에서 `time.Now()`에 의존하면 결과가 머신 속도에 따라 달라진다. 두 `Allow()` 호출 사이에 경과 시간이 거의 0이면, 리필 토큰이 0에 가깝다.

해결: 테스트에서는 Limiter를 burst=1로 만들고, 첫 `Allow()`는 true(초기 토큰 소비), 두 번째는 false(리필 안 됨)를 검증한다. 리필 테스트는 충분한 `time.Sleep` 후에.

## Cleanup에서 맵 삭제 중 순회

Go에서 `range` 중에 해당 맵에서 `delete`하는 건 안전하다. 스펙에 명시되어 있다. 하지만 다른 언어(Java의 ConcurrentModificationException 등)에서는 안 될 수 있으니 Go 특유의 동작이라는 걸 인식해야 한다.

## net.SplitHostPort 실패

`r.RemoteAddr`이 `192.168.1.1:12345` 형태일 때 `net.SplitHostPort`가 정상 작동한다. 하지만 IPv6 주소 `[::1]:12345`도 올바르게 파싱된다. 포트 없이 IP만 있는 경우(`192.168.1.1`)에는 `SplitHostPort`가 에러를 반환하므로 fallback으로 `r.RemoteAddr` 전체를 쓴다.

## X-Forwarded-For 스푸핑

클라이언트가 `X-Forwarded-For` 헤더를 임의로 설정할 수 있다. 신뢰할 수 있는 프록시에서만 이 헤더를 넣도록 서버 구성(nginx에서 `proxy_set_header X-Real-IP $remote_addr`)을 해야 한다. 이 프로젝트에서는 단순히 헤더를 읽지만, 실무에서는 신뢰 범위를 설정해야 한다.

## 429와 Retry-After

RFC 6585에 따르면 429 Too Many Requests에 `Retry-After` 헤더를 포함하는 것이 권장된다. 이 프로젝트에서는 `Retry-After: 1`(1초)로 고정했지만, 실제로는 토큰 리필까지 남은 시간을 계산해 동적으로 설정하면 더 정확하다.
