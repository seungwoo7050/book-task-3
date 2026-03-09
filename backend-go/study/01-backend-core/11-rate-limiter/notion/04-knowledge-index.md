# 지식 색인 — Rate Limiter 핵심 개념

## Token Bucket 알고리즘

일정 속도로 토큰이 리필되는 버킷. 요청마다 토큰 1개를 소비한다. 버킷이 비면 거부.

- **rate**: 초당 리필 토큰 수 (평균 허용 속도)
- **burst**: 버킷 용량 (순간 최대 허용 수)
- rate=10, burst=20 → 평소 초당 10개, 순간 최대 20개

## 연속 리필 vs 이산 리필

**연속**: `Allow()` 호출 시 경과 시간으로 계산. goroutine 불필요.

```go
l.tokens += elapsed * l.rate
```

**이산**: 별도 goroutine이 주기적으로 토큰 추가. 타이머 오버헤드 발생.

연속 리필이 더 정확하고 효율적이다.

## Rate Limiting 알고리즘 비교

| 알고리즘 | 장점 | 단점 |
|---------|------|------|
| Token Bucket | 버스트 허용, 구현 단순 | 정확한 윈도우 집계 어려움 |
| Leaky Bucket | 출력 속도 일정 | 버스트 불허 |
| Fixed Window | 구현 매우 단순 | 윈도우 경계에서 2배 허용 |
| Sliding Window Log | 가장 정확 | 메모리 사용량 높음 |

## Per-Client Rate Limiting

클라이언트별(보통 IP) 독립된 제한. 한 클라이언트의 과다 요청이 다른 클라이언트에 영향을 주지 않는다. 구현: `map[string]*Limiter`.

## Stale Client Cleanup

비활성 클라이언트의 Limiter를 맵에서 제거. 메모리 누수 방지. background goroutine이 주기적으로(1분마다) 확인하고, TTL(3분) 초과 시 삭제.

## 429 Too Many Requests

RFC 6585에 정의된 HTTP 상태 코드. 클라이언트가 일정 시간 내 너무 많은 요청을 보냈음을 의미한다.

## Retry-After 헤더

429 또는 503 응답에 포함. 클라이언트에게 재시도까지 기다릴 시간을 초 단위로 알려준다.

```
HTTP/1.1 429 Too Many Requests
Retry-After: 1
```

## net.SplitHostPort

`"192.168.1.1:8080"` → `("192.168.1.1", "8080")`. IPv6도 지원: `"[::1]:8080"` → `("::1", "8080")`.

## X-Forwarded-For

HTTP 헤더. 리버스 프록시가 원래 클라이언트 IP를 서버에 전달한다. `client, proxy1, proxy2` 형태로 체인된다. 스푸핑 가능하므로 신뢰할 수 있는 프록시에서만 읽어야 한다.

## Back-pressure와 Rate Limiting의 차이

- **Back-pressure**: 생산자가 소비자의 속도에 맞춰 감속 (channel이 차면 블로킹)
- **Rate limiting**: 일정 속도 이상의 요청을 거부 (429 반환)

10의 Worker Pool은 back-pressure, 11의 Limiter는 rate limiting.

## time.Ticker

주기적 이벤트 발생기. `Stop()`을 호출하지 않으면 goroutine이 누수된다. `defer ticker.Stop()`은 필수.
