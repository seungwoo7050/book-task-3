# Problem — Event Pipeline

## Background

You are extending the game platform from Task 06. When a player purchases
an item, the system must:

1. Record the purchase in the database (already done in Task 06).
2. **Publish a `PurchaseCompleted` event** to Kafka so that downstream
   services (analytics, notifications, leaderboards) can react.

The challenge: the database write and the Kafka publish are **two separate
systems**. If you do them sequentially, either can fail independently,
causing data inconsistency.

## Requirements

### Part 1: Outbox Table

Add an `outbox` table to the database:

```sql
CREATE TABLE outbox (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type TEXT NOT NULL,     -- e.g., "player"
    aggregate_id   UUID NOT NULL,     -- e.g., player_id
    event_type     TEXT NOT NULL,     -- e.g., "PurchaseCompleted"
    payload        JSONB NOT NULL,    -- event data
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    published_at   TIMESTAMPTZ        -- NULL until published
);

CREATE INDEX idx_outbox_unpublished ON outbox (created_at)
    WHERE published_at IS NULL;
```

### Part 2: Outbox Writer

When a purchase occurs, within the **same database transaction**:
1. Deduct balance, add inventory, etc. (from Task 06).
2. Insert a row into the `outbox` table with the event payload.

The event payload:
```json
{
  "player_id": "uuid",
  "item_name": "sword_of_fire",
  "price": 100,
  "new_balance": 900,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Part 3: Outbox Relay (Producer)

A background process that:
1. Polls the `outbox` table for unpublished events (WHERE published_at IS NULL).
2. Publishes each event to the Kafka topic `game.purchases`.
3. Marks the event as published (SET published_at = now()).
4. Respects ordering: events for the same `aggregate_id` must be published
   in order — use `aggregate_id` as the Kafka message key.

### Part 4: Consumer

A Kafka consumer that:
1. Joins consumer group `purchase-analytics`.
2. Reads from topic `game.purchases`.
3. Processes each event (simulated: log the event and update a counter).
4. Handles duplicates idempotently (track processed event IDs).
5. Commits offsets after successful processing.

### Part 5: Integration

Wire everything together:
- `POST /api/purchase` → DB transaction (purchase + outbox insert)
- Outbox relay goroutine → polls and publishes to Kafka
- Consumer process → reads and processes events

## Evaluation Criteria

| Criteria | Weight |
|----------|--------|
| Outbox pattern correctness (atomic DB+event) | 30% |
| Relay publishing with ordering guarantees | 20% |
| Consumer idempotency | 20% |
| Clean separation of concerns | 15% |
| Test coverage | 15% |
