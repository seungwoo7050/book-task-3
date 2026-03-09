# 접근 기록 — Outbox에서 Consumer까지 3단계

## 패키지 구조

```
outbox/     → Event 모델 + DB 접근 (InsertTx, GetUnpublished, MarkPublished, Cleanup)
relay/      → outbox 폴링 → Kafka 발행 루프
consumer/   → Kafka 구독 → 멱등 처리 → 오프셋 커밋
cmd/relay/  → relay 진입점
cmd/consumer/ → consumer 진입점
```

outbox 패키지가 relay와 consumer 양쪽에서 사용되므로, 모델을 별도로 분리.

## outbox 패키지: 모델과 리포지토리

### Event 모델

```go
type Event struct {
    ID            string
    AggregateType string    // "player"
    AggregateID   string    // player UUID
    EventType     string    // "PurchaseCompleted"
    Payload       json.RawMessage
    CreatedAt     time.Time
    PublishedAt   *time.Time  // nil이면 미발행
}
```

`PublishedAt`이 nil이면 아직 Kafka에 발행되지 않은 이벤트. partial index `WHERE published_at IS NULL`로 미발행 이벤트만 빠르게 조회.

### InsertTx — 트랜잭션 내 삽입

패키지 수준 함수. `*sql.Tx`를 받아 outbox에 INSERT. 구매 트랜잭션과 같은 `tx`를 사용하므로 원자성 보장. 이 함수를 프로젝트 14의 PurchaseService에서 호출하면 outbox 패턴이 완성된다.

### 폴링 쿼리

```sql
SELECT ... FROM outbox WHERE published_at IS NULL ORDER BY created_at ASC LIMIT $1
```

`ORDER BY created_at`이 같은 aggregate에 대한 이벤트 순서를 보장. `LIMIT`로 배치 크기 제한.

### Cleanup

발행 완료된 이벤트를 주기적으로 삭제. `DELETE WHERE published_at IS NOT NULL AND published_at < now() - interval`. outbox가 무한히 커지는 것을 방지.

## relay 패키지: 폴링 + Kafka 발행

`Relay.Run(ctx)`은 ticker 루프:

1. `time.NewTicker(interval)` → 주기적 폴링
2. `repo.GetUnpublished(ctx, batchSize)` → 미발행 이벤트 조회
3. 이벤트별로 `kafka.Message` 생성:
   - **Key**: `AggregateID` → 같은 플레이어의 이벤트가 같은 파티션으로
   - **Value**: `event.Payload` (JSON)
   - **Headers**: `event_type`, `event_id`, `aggregate_type`
4. `writer.WriteMessages(ctx, msg)` → Kafka 발행
5. `repo.MarkPublished(ctx, eventID)` → 발행 완료 마킹

실패 시 배치 중단. 다음 폴링에서 재시도. MarkPublished 실패 시에도 다음 폴링에서 재발행 — at-least-once.

## consumer 패키지: 멱등 처리

Consumer는 2단계 중복 체크를 수행:

1. **인메모리 캐시** (`map[string]struct{}` + RWMutex): O(1) 조회, 재시작 시 사라짐
2. **DB 테이블** (`processed_events`): 영속적, `INSERT ON CONFLICT DO NOTHING`

처리 흐름:

```
FetchMessage → isProcessed(인메모리)? skip
             → isPersisted(DB)? markProcessed + skip
             → handler(ctx, eventType, payload)
             → markProcessed(인메모리) + persistProcessed(DB)
             → CommitMessages(ctx, msg)
```

핸들러가 실패하면 오프셋을 커밋하지 않는다. Kafka가 같은 메시지를 다시 전달한다.

`FetchMessage` + `CommitMessages`를 쌍으로 사용. `ReadMessage`(자동 커밋)와 달리, 처리 성공 후 명시적으로 커밋한다.
