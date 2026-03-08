# Core Concepts

## 핵심 개념

- idempotency key는 네트워크 재시도와 중복 요청을 구분하지 않고 같은 결과로 수렴시키는 장치다.
- optimistic locking은 `version` 컬럼으로 충돌을 감지한다.
- Cockroach류 분산 SQL은 serialization failure를 애플리케이션 레벨에서 재시도하게 요구할 수 있다.
- handler/service/repository 분리는 transaction 정책과 HTTP 정책을 분리한다.

## Trade-offs

- idempotency는 구현 복잡도를 높이지만 결제/구매류 흐름에서는 사실상 필수다.
- retry를 과하게 넣으면 지연과 중복 부하가 늘어난다.

## 실패하기 쉬운 지점

- conflict와 retryable serialization failure를 같은 오류로 뭉개면 대응이 잘못된다.
- idempotency response 저장 시점이 트랜잭션 밖이면 dual-write 비슷한 문제가 생긴다.

