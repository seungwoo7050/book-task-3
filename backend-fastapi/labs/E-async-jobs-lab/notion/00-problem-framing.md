# Outbox 패턴과 비동기 워커: 메시지를 잃지 않으려면

## 왜 이 문제를 만들었는가

웹 서버가 직접 이메일을 보내거나 외부 API를 호출하면, 요청-응답 사이클 안에서
네트워크 타임아웃, 외부 장애, 재시도 누락 같은 문제가 전부 HTTP 핸들러의 짐이 된다.
"일단 DB에 기록하고, 별도 워커가 꺼내서 처리한다"는 아이디어는 간단해 보이지만,
실제로 구현하려면 outbox table, idempotency key, retry 상태 전이, 워커 분리 같은
여러 조각이 맞물려야 한다.

E-async-jobs-lab은 이 조각들을 하나씩 만들어 보며
"메시지 유실 없는 비동기 처리"가 어떤 구조를 요구하는지 체험하는 랩이다.

## 어떤 상황을 기대하는가

- 클라이언트가 알림 발송을 요청하면, 서버는 즉시 job record를 만들고 응답한다.
- 같은 idempotency key로 재요청하면 새 job을 만들지 않고 기존 job을 돌려준다.
- outbox drain 엔드포인트를 호출하면, pending 이벤트를 꺼내 Celery 태스크로 위임한다.
- 태스크가 실패하면 상태가 `retrying`으로 전이되고, 재시도 시 최종 `sent`가 된다.
- `attempt_count`가 정확히 누적된다.

## 제약과 경계

| 항목 | 선택 |
|------|------|
| worker | Celery 5.4 |
| broker | Redis 7 (production), memory:// (test) |
| result backend | cache+memory:// (test), Redis (production) |
| DB | PostgreSQL 16 via SQLAlchemy 2.0 |
| 실제 알림? | 보내지 않는다—상태 전이가 핵심 |
| eager mode | 테스트에서 `task_always_eager=True`로 동기 실행 |

## 불확실한 것

- 실제 SMTP 연동까지 확장하면 retry 정책이 훨씬 복잡해지겠지만, 이 랩에서는
  상태 머신 자체를 학습 목표로 한정했다.
- outbox polling 대신 CDC(Change Data Capture)를 쓰는 방식은 여기서는 다루지 않는다.
- `task_always_eager=True` 환경과 실제 broker 환경의 동작 차이는 문서로만 남긴다.
