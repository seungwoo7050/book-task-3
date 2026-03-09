# 문제 정의 — 두 시스템 사이의 일관성

## 이중 쓰기 문제

게임 플랫폼에서 아이템을 구매하면 두 가지 일이 일어나야 한다:

1. **데이터베이스에 구매 기록** (잔액 차감, 인벤토리 추가)
2. **Kafka에 이벤트 발행** (분석, 알림, 리더보드 서비스가 반응)

문제는 이 둘이 별개의 시스템이라는 것이다. DB 쓰기 후 Kafka 발행이 실패하면? DB에는 구매가 완료됐지만 다운스트림 서비스는 모른다. Kafka 먼저 쓰고 DB가 실패하면? 이벤트는 발행됐지만 실제 구매는 없다.

## Outbox 패턴이라는 답

해결책: DB 트랜잭션 안에서 구매 로직과 함께 `outbox` 테이블에 이벤트를 INSERT한다. 별도의 relay 프로세스가 outbox를 폴링해서 Kafka에 발행하고, 발행 완료된 이벤트를 마킹한다.

```
[HTTP 구매] → DB 트랜잭션 {
    Balance 차감
    Inventory 추가
    Outbox INSERT  ← 같은 트랜잭션
} → COMMIT

[Relay 고루틴] → outbox 폴링 → Kafka 발행 → published_at 갱신

[Consumer] → Kafka 구독 → 이벤트 처리 → 중복 체크 → 오프셋 커밋
```

DB 트랜잭션이 원자성을 보장하므로, 구매와 이벤트 저장은 항상 함께 성공하거나 함께 실패한다. Relay가 "최소 한 번" 발행하므로 Consumer는 멱등 처리가 필요하다.

## 프로젝트 14와의 관계

프로젝트 14에서 CockroachDB + 멱등성 키 + 낙관적 잠금을 익혔다. 여기서는 같은 DB 위에 이벤트 파이프라인을 얹는다. outbox INSERT가 프로젝트 14의 purchase 트랜잭션에 한 줄 추가되는 것과 같다.

## 새로 등장하는 기술

- **segmentio/kafka-go**: Go용 Kafka 클라이언트. Writer(프로듀서)와 Reader(컨슈머) 제공
- **Redpanda**: Kafka 호환 스트리밍 플랫폼. Docker에서 JVM 없이 가볍게 실행
- **at-least-once 의미론**: 메시지가 최소 한 번은 전달되지만, 중복 전달될 수 있음
