# 회고 — 캐시와 관측성을 붙여본 뒤

## 무엇을 만들었나

상품(Item) 조회/수정 API에 cache-aside 패턴을 적용하고, `/metrics` 엔드포인트와 X-Trace-ID 전파를 구현했다. Service 구조체 하나에 DB, 캐시, 메트릭, 로거를 모았다. 외부 의존성은 `modernc.org/sqlite` 하나.

## 잘된 점

**cache-aside 패턴이 일목요연하다.** GetItem의 흐름이 hit/miss → DB 조회 → 캐시 저장으로 읽기 쉽고, UpdateItem에서 `delete(s.cache, id)` 한 줄로 invalidation이 완결된다. 테스트에서 `cacheMisses`와 `cacheHits` 카운터로 동작을 검증할 수 있어 신뢰성이 높다.

**atomic 카운터 + /metrics가 관측성의 최소 단위를 보여준다.** Prometheus 클라이언트 라이브러리를 도입하지 않고도 동일한 텍스트 포맷을 출력한다. 관측성의 본질은 "무슨 일이 일어나고 있는지 외부에서 볼 수 있게 만드는 것"이고, 이 프로젝트가 그 최소 구현이다.

**withTrace 미들웨어**가 분산 트레이싱의 원리를 단순하게 보여준다. 클라이언트가 보낸 ID를 그대로 전파하고, 없으면 생성한다.

## 아쉬운 점

**캐시 TTL이 없다.** 현재 구현은 명시적 invalidation 없이는 캐시가 영원히 유지된다. 실무에서는 TTL(Time-To-Live)을 설정해 일정 시간 후 자동 만료되도록 한다.

**trace ID가 context에 전파되지 않는다.** 현재는 응답 헤더와 로그에만 남긴다. Repository나 DB 레벨까지 trace ID를 전달하려면 `context.WithValue`를 써야 한다. 07에서 인증 정보를 context에 넣은 것처럼.

**rand.Int63으로 trace ID를 생성하는 건 예측 가능하다.** `crypto/rand`를 쓰거나 UUID를 생성하는 게 더 안전하다.

## 프로젝트 흐름에서의 위치

| 프로젝트 | 캐시 | 메트릭 | 트레이싱 |
|---------|------|--------|---------|
| 08 | 없음 | 없음 | 없음 |
| **09** | **인메모리** | **/metrics** | **X-Trace-ID** |
| 이후 | Redis | OpenTelemetry | Jaeger |

09는 10(concurrency-patterns)으로 넘어가기 전, "백엔드 서버가 외부에 자신의 상태를 드러내는 방법"을 정립하는 역할이다.
