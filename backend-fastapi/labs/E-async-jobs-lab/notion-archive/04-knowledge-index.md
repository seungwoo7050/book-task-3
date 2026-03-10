# 지식 인덱스: 비동기 작업 패턴 정리

## Outbox Pattern

핵심 아이디어: 비즈니스 데이터와 이벤트를 같은 DB 트랜잭션에 기록한 뒤,
별도 프로세스가 이벤트를 읽어 외부 시스템으로 전달한다.

장점:
- 네트워크 장애로 이벤트가 유실되지 않는다 (DB에 있으므로)
- 비즈니스 로직과 전달 로직이 분리된다
- retry가 이벤트 단위로 가능하다

주의:
- outbox table이 무한히 커지지 않도록 done 이벤트를 정리해야 한다
- 동시 drain은 중복 전달을 유발할 수 있다 → SELECT FOR UPDATE 또는 advisory lock
- "exactly once"가 아니라 "at least once"를 목표로 한다

## Idempotency Key 패턴

클라이언트가 요청마다 고유 key를 보내고, 서버는 key로 기존 결과를 lookup한다.
같은 key가 있으면 새 작업을 만들지 않고 기존 결과를 반환한다.

구현의 핵심:
- key는 보통 UUID로, 클라이언트가 생성한다
- 서버 측 저장소는 key → result 매핑
- TTL을 두어 오래된 key를 정리할 수 있다

이 랩에서는 `NotificationJob.idempotency_key`를 unique 필드로 두고,
`SELECT ... WHERE idempotency_key = :key`로 lookup한다.

## Celery Architecture

```
Client → FastAPI → DB (job + outbox)
                        ↓ drain
                   Celery broker (Redis)
                        ↓
                   Worker process → deliver_notification task
```

핵심 설정:
- `broker_url`: 메시지 큐 주소 (Redis, RabbitMQ 등)
- `result_backend`: 태스크 결과 저장소
- `task_always_eager`: True면 같은 프로세스에서 동기 실행 (테스트용)

eager 모드 주의사항:
- broker에 연결하지 않아도 되지만, URL validation은 일어날 수 있다
- 동시성/직렬화 문제를 발견할 수 없다
- 프로덕션 동작과 완전히 같지 않다는 점을 인지해야 한다

## 상태 전이 머신

이 랩의 `NotificationJob` 상태:

| 현재 상태 | 조건 | 다음 상태 |
|-----------|------|-----------|
| pending | 정상 처리 | sent |
| pending | 일시적 실패 (retry@) | retrying |
| retrying | 재처리 성공 | sent |

`attempt_count`는 모든 전이에서 증가해야 한다.
"전이 전에 카운트 먼저" 규칙이 누락 방지에 효과적이다.

## 용어 정리

| 용어 | 의미 |
|------|------|
| outbox | 같은 트랜잭션에 기록되는 이벤트 테이블 |
| drain | outbox에서 pending 이벤트를 꺼내 처리하는 작업 |
| idempotency key | 중복 요청 방지를 위한 클라이언트 제공 식별자 |
| eager mode | Celery가 broker 없이 동기 실행하는 테스트 모드 |
| at-least-once | 최소 한 번 전달 보장 (중복 가능) |

## 참고 자료

| 제목 | 출처 | 확인 | 비고 |
|------|------|------|------|
| Transactional Outbox (Microservices Patterns) | Chris Richardson | 2025-01 | outbox 패턴의 정식 명명 |
| Celery Documentation - Testing | docs.celeryq.dev | 2025-01 | `task_always_eager` 설명 |
| Idempotency Patterns (Stripe Blog) | stripe.com/blog | 2025-01 | idempotency key 실전 사례 |
