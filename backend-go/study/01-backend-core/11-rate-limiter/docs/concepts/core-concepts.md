# Core Concepts

## 핵심 개념

- token bucket은 burst를 허용하면서 평균 처리율을 제한한다.
- per-client limiter는 같은 서버 안에서 클라이언트 간 간섭을 줄인다.
- middleware에 붙이면 개별 handler가 rate limit 세부 사항을 몰라도 된다.
- stale client cleanup을 하지 않으면 장기적으로 메모리 누수가 된다.

## Trade-offs

- in-process limiter는 단일 인스턴스에서 단순하지만 다중 인스턴스에는 맞지 않는다.
- IP 기반 식별은 쉬우나 NAT나 프록시 환경에서는 거칠 수 있다.

## 실패하기 쉬운 지점

- `X-Forwarded-For`와 `RemoteAddr` 해석 순서를 잘못 두면 클라이언트 식별이 틀어진다.
- refill 계산을 부정확하게 하면 burst cap이 깨지거나 토큰이 과도하게 쌓인다.

