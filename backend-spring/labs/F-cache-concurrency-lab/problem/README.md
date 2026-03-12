# F-cache-concurrency-lab 문제 정의

캐시 무효화, 중복 요청, 재고 경합 문제를 inventory 시나리오 하나로 묶어 구체화하는 Spring 랩을 만든다.

## 성공 기준

- inventory 조회와 reservation 흐름에서 cacheable read path와 idempotency key 처리가 보인다.
- 같은 JVM 안에서의 동시성 제어가 재고 차감 문제와 연결된다.
- Redis나 분산 락을 왜 다음 단계로 남겼는지 설명할 수 있다.

## 이번 단계에서 다루지 않는 것

- Redis-backed cache assertion
- distributed lock implementation
- production-grade idempotency storage 분리

이 디렉터리는 canonical problem statement와 성공 기준을 남기는 곳이다.
